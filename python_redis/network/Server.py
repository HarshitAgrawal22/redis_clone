import socket
import threading
from typing import Dict

# TODO: write middleware python application which will convert the normal logical commands to the RESP which this redis needs and then also return the result in Human readable form which will be generated from RESP result

# TODO: add module for server's config
import python_redis.protocols.keyval_protocol as keyval_protocol

from python_redis.common import execute_task_hash_map, Message
from python_redis.network import peer
from queue import Queue, Empty as EmptyQueue

# import queue
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
        self.del_peer_ch: Queue[peer.Peer] = Queue()

        # Channel to delete connection of a peer from the server
        self.add_peer_ch: Queue[peer.Peer] = Queue()

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
            return None
            # ic(f"{data} is the data we got in return ")
        else:
            return str("killed a Peer")

    def loop(self) -> None:
        # print("loop started")
        # This loop waits for a peer in add_peer_ch and adds to the peers dict
        while not self.quit_event.is_set():
            # TODO: Check for peers which remain in self.peers
            # TODO: Add pub/sub module
            # ! this can create problem here
            # ? solve the problem here
            # // @param harhsit is wrong here
            # * this is high lighted

            # ic(self.peers)

            try:
                msg = self.msg_queue.get(timeout=0.05)
                err = self.handle_message(
                    msg
                )  # TODO: check and add error in this function's response
                if err != None:
                    print(f"Raw Message Error-> {err}")
            except EmptyQueue:
                pass

                # if self.add_peer_ch:
                # peer = self.add_peer_ch.pop(0)
            try:
                peer = self.add_peer_ch.get_nowait()
                with self.peers_lock:
                    self.peers[peer] = True
                    ic(self.peers)
                print(f"Added new peer: {peer.Conn.getpeername()}")
            except EmptyQueue:
                pass
                # Added print statement
                # if self.del_peer_ch:
                # this_peer = self.del_peer_ch.pop(0)
            try:
                this_peer = self.del_peer_ch.get_nowait()
                with self.peers_lock:

                    # TODO: get how to configure peers lock

                    del self.peers[this_peer]
                    # TODO: solve the race condition in del_peer_chan
                    ic(self.peers)

                    ic(this_peer)

            except EmptyQueue:
                pass
                # ic(self.peers)

        print("Thanks For Using Redis")

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
            

            except OSError:
                break
            except Exception as e:
                print(f"Accept error: {e}")
        print("Stopped accept loop")

    def handle_conn(self, conn: socket.socket) -> None:
        # TCP keep alive
        # conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # Windows-specific tuning
        # conn.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 30_000, 10_000))
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
        

        # stops the server gracefully

        for peer in list(self.peers):
            peer.close_connection()
        self.quit_event.set()
        self.listener.close()
        # raise Exception("Good Bye")
        
        # ! the server is not stopping gracefully 
