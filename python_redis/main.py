import socket
import threading
from typing import Dict


import python_redis.protocols.keyval_protocol as keyval_protocol

from python_redis.common import execute_task_hash_map, Message
from python_redis import peer
from queue import Queue
import queue
from python_redis.client import client
import python_redis.models.keyval as keyval

from icecream import ic

default_listen_address: str = ":5001"
ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class Config:
    def __init__(self, listen_address: str = default_listen_address):
        # It holds data like "ListenAddress," specifying where the server listens for connections
        self.listen_address: str = listen_address


class Server:
    def __init__(self, config: Config):
        # Server holds settings, a list of peers, a listener, and a channel for new peers.
        self.config: Config = config
        self.peers_lock: threading.RLock = threading.RLock()  # ✅ ADD THIS

        self.peers: Dict[peer.Peer, bool] = dict()
        # Dict to track connected peers with Peer as keys
        self.listener: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # Network listener
        self.del_peer_ch: Queue[peer.Peer] = (
            # list()
            Queue()  # TODO: Lists are not thread safe, so replace the lists with queue
        )
        # Channel to delete connection of a peer from the server
        self.add_peer_ch: Queue[peer.Peer] = (
            Queue()
        )  # Channel to add peers to the server
        self.quit_event = threading.Event()
        self.msg_queue = Queue()  # Queue to manage message for broadcasting

    @staticmethod
    def new_server(config: Config) -> "Server":
        # Initializes the server instance with config settings
        if len(config.listen_address) == 0:
            config.listen_address = default_listen_address
        return Server(config)

    def start(self) -> None:
        # Starts the server by binding to the configured address and entering the accept loop
        try:
            self.listener.bind(
                (
                    self.config.listen_address.split(":")[0],
                    int(self.config.listen_address.split(":")[1]),
                )
            )
            self.listener.listen()
            print(
                f"Server started, listening on {self.config.listen_address}"
            )  # Added print statement

            threading.Thread(target=self.loop, daemon=True).start()
            self.accept_loop()
        except Exception as e:
            print(f"Error starting server: {e}")

    def handle_message(self, msg: Message):

        # if isinstance(msg.cmd, keyval_protocol.CreateNewQueue):
        #     msg.conn_peer.storage_queue = Queue()
        #     msg.conn_peer.send("OK".encode("utf-8"))

        func = execute_task_hash_map.get(type(msg.cmd))
        if func != None:
            data = func(msg, self)
            # ic(f"{data} is the data we got in return ")
        else:
            print("Invalid Command")

        return str("killed a Peer")

    def loop(self) -> None:
        # print("loop started")
        # This loop waits for a peer in add_peer_ch and adds to the peers dict
        while not self.quit_event.is_set():
            # TODO: Check for peers which remain in self.peers
            # TODO: Add pub/sub module

            # ic(self.peers)
            # print("a iteration in loop ")
            # print("", end="")

            # print("", end="")
            try:
                msg = self.msg_queue.get(timeout=0.05)
                err = self.handle_message(
                    msg
                )  # TODO: check and add error in this function's response
                if err:
                    print(f"Raw Message Error-> {err}")

                # print(f"got exception while fetching msg->  {e}")

                # if not self.msg_queue.empty():
                # print("analyzing command")
                # msg: Message = self.msg_queue.get(timeout=0.001)

                # if msg.cmd.decode("utf-8") != "quit\r\n":
                # print(raw_msg.decode("utf-8"))

                # else:  # if we get quit message from any server then the server is stopped
                # self.stop()
                # this is for development phase only

                # if self.add_peer_ch:
                # peer = self.add_peer_ch.pop(0)

                peer = self.add_peer_ch.get_nowait()
                with self.peers_lock:
                    self.peers[peer] = True
                print(f"Added new peer: {peer.Conn.getpeername()}")

                # Added print statement
                # if self.del_peer_ch:
                # this_peer = self.del_peer_ch.pop(0)

                this_peer = self.del_peer_ch.get_nowait()
                # ic(self.peers)
                # print(f"Deleted peer: {this_peer.Conn.getpeername()}")
                with self.peers_lock:
                    # TODO: get how to configure peers lock

                    del self.peers[this_peer]
            except queue.Empty:
                pass
            # else:
            # threading.Event().wait(0.1)
            # pass
            # slight delay tp prevent busy waiting
            # print("No new peer is received")
        print("Thanks For Using Redis")

    #     Why this works

    # msg_queue.get(timeout=0.05) blocks

    # If no message arrives:

    # Thread sleeps up to 50ms

    # CPU usage drops to near-zero

    # Peer queues are checked opportunistically

    # 🧠 Important design rule

    # At least one blocking operation must exist in every server loop.

    # Otherwise, the loop will busy-spin.

    # Redis achieves this via:

    # epoll / event loop

    # blocking socket reads

    # In your threaded design:

    # Queue.get(timeout=...) is the correct equivalent
    def accept_loop(self) -> None:
        # Accepts incoming connections in a loop, handling each connection concurrently
        while not self.quit_event.is_set():
            try:
                conn, addr = self.listener.accept()
                # print(f"Accepted a new connection from {addr}")  # Added print statement
                thread = threading.Thread(
                    target=self.handle_conn, args=(conn,), daemon=True
                )
                thread.start()
            except Exception as e:
                print(f"Accept error: {e}")

    def handle_conn(self, conn: socket.socket) -> None:
        # Handles each new connection by creating a Peer instance
        this_peer: peer.Peer = peer.Peer.newPeer(
            conn, self.msg_queue, self.del_peer_ch
        )  # here we are provinng the conn and msg_queue of server's to the Peer

        # print(f"Handling connection for peer: {this_peer}")

        # this_peer.test_protocol()
        # self.add_peer_ch.append(this_peer)
        self.add_peer_ch.put(this_peer)
        # added new peer to the add_peer_ch of server
        # ic(conn.getpeername())
        # starting the peer's readloop on a seperate thread to isolate each peer;s connection from every other peer
        thread = threading.Thread(target=this_peer.read_loop)
        thread.start()

    def stop(self) -> None:
        from python_redis.db import HardDatabase

        # stops the server gracefully
        # TODO: figureout the server stopping problem

        map(lambda peer: peer.close_connection(), self.peers.keys())
        self.quit_event.set()
        self.listener.close()
        for peer in self.peers.keys():
            HardDatabase.drop_peer_db(peer.DB_str)
            print("Server stopped")


def main() -> None:
    server = Server.new_server(config=Config())
    try:
        server_thread = threading.Thread(target=server.start)
        server_thread.start()
        # client.Client("127.0.0.1:5001").test_tree()
        # cl = client.Client("127.0.0.1:5001")
        # thr = threading.Thread(target=cl.set, args=("name", "Harshit"))
        # # cl.set("name", "HArshit")
        # thr.start()

        # threading.Thread(target=cl.get, args=("name",)).start()
        # thread.start()
        # cl.get("name")

        # ic(clint.get("name"))
        # (clint.insert_vertex_to_graph())
        # clint.add_edges_to_graph()
        # ic(clint.bfs())
        # clint.dij_dis()
        # clint.show_graph()
        # clint.remove_edge()
        # clint.show_graph()
        # clint.dij_shortest_path()
        # ic(clint.show_graph())
        # threading.Event().wait(1)

        # ic(server.start())
        # Using IceCream to print the return value of start()
        # time.sleep(1)

        # for i in range(10):
        #     client_server = client.Client("127.0.0.1:5001")
        #     if err := client_server.set(key=f"pakoda_{i}", value=f"aloo_{i}"):
        #         print(f"error= > {err}")
        #     try:
        #         value = client_server.get(key=f"pakoda_{i}")

        #         print(f"received value => { value}")
        #     except Exception as e:
        #         print(e)
        # time.sleep(1)
        # print(server.kv.data)
    except KeyboardInterrupt:
        print("server stopped")
        server.stop()


# python -m python_redis.main

if __name__ == "__main__":
    main()


# 🔧 1. Data Consistency
# Problem: There may be data changes between sync intervals, leading to inconsistent or outdated snapshots in MongoDB.

# Impact: A crash before a scheduled sync causes data loss.

# Mitigation: Consider implementing a write-ahead log (WAL) or event queue to replay missed changes.

# 🔃 2. Performance Overhead
# Problem: Serializing and writing large data volumes to disk every 5 minutes may cause CPU or I/O bottlenecks.

# Impact: Latency spikes or reduced responsiveness of your Redis clone.

# Mitigation: Perform writes in a background thread/process and compress or diff the data before saving.

# 📂 3. Data Modeling in MongoDB
# Problem: Redis uses varied data structures (sets, lists, graphs, trees, etc.) that may not directly map to MongoDB documents.

# Impact: Incorrect schema choices can lead to inefficient queries and storage.

# Mitigation: Design schema per data type:

# Store lists as arrays,

# Sets as arrays with uniqueness enforced,

# Graphs using reference documents,

# Trees via nested documents or adjacency lists.

# 🧵 4. Concurrency Issues
# Problem: Reads/writes may happen during a sync operation.

# Impact: May result in race conditions or corrupted snapshots.

# Mitigation: Use locking mechanisms or snapshot copies to serialize state safely.

# 🕒 5. Clock/Sync Timing
# Problem: Scheduling syncs precisely every 5 minutes can be tricky across threads or async handlers.

# Impact: Delays or overlapping writes.

# Mitigation: Use a scheduler like APScheduler, threading.Timer, or asyncio.

# 📈 6. Storage Growth and Cleanup
# Problem: Without pruning, MongoDB may grow rapidly with old data or snapshots.

# Impact: Increased disk usage and degraded performance.

# Mitigation: Use TTL indexes or regularly purge obsolete data.

# 🔁 7. Recovery Logic
# Problem: On restart, recovering from MongoDB may involve rebuilding complex structures (e.g., trees, graphs).

# Impact: Startup time becomes slow or error-prone.

# Mitigation: Store metadata or version markers for each data structure to aid reconstruction.

# ✅ Summary
# Challenge	Risk	Recommendation
# Data Loss	Mid-sync crash	Use WAL/event queue
# CPU/I/O Overhead	Performance dips	Background writing & compression
# Schema Mismatch	Inefficient data use	Tailored schema for each structure
# Concurrency	Data race/corruption	Locking or consistent snapshot strategy
# Timing Drift	Missed or overlapping writes	Reliable async scheduler
# Storage Bloat	Disk overflow	TTL, cleanup jobs
# Complex Recovery	Error-prone restarts	Store metadata with structure dumps
