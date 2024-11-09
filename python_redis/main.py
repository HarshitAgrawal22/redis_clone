import socket
import threading
from typing import Dict
import protocol
import peer
import time
from icecream import ic
from queue import Queue
from client import client

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
        self.peers: Dict[peer.Peer, bool] = (
            {}
        )  # Dict to track connected peers with Peer as keys
        self.listener: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # Network listener
        self.add_peer_ch: list[peer.Peer] = []  # Channel to add peers to the server
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

    def handle_raw_message(self, rawMsg: bytearray):
        print(type(rawMsg))
        print(rawMsg)
        try:
            cmd = protocol.parse_command(rawMsg)
            # print(f"{cmd} is the cmd")
        except ValueError as e:
            return e
        if isinstance(cmd, protocol.SetCommand):
            print(
                f"Somebody wants to set a key into the hashtable \nkey=>{cmd.key}\nvalue =>{cmd.value}"
            )
        return None

    def loop(self) -> None:
        # This loop waits for a peer in add_peer_ch and adds to the peers dict
        while not self.quit_event.is_set():

            if not self.msg_queue.empty():
                print("analyzing command")
                raw_msg = self.msg_queue.get()

                if raw_msg.decode("utf-8") != "quit\r\n":
                    print(raw_msg.decode("utf-8"))
                    err = self.handle_raw_message(raw_msg)
                    if err:
                        print(f"Raw Message Error-> {err}")

                else:  # if we get quit message from any server then the server is stoppped
                    self.stop()
                    # this is for development phase only

            if self.add_peer_ch:
                peer = self.add_peer_ch.pop(0)
                self.peers[peer] = True
                print(
                    f"Added new peer: {peer.Conn.getpeername()}"
                )  # Added print statement
            else:
                threading.Event().wait(0.5)
                # slight delay tp prevent busy waiting
                # print("No new peer is received")

    def accept_loop(self) -> None:
        # Accepts incoming connections in a loop, handling each connection concurrently
        while not self.quit_event.is_set():
            try:
                conn, addr = self.listener.accept()
                print(f"Accepted a new connection from {addr}")  # Added print statement
                thread = threading.Thread(
                    target=self.handle_conn, args=(conn,), daemon=True
                )
                thread.start()
            except Exception as e:
                print(f"Accept error: {e}")

    def handle_conn(self, conn: socket.socket) -> None:
        # Handles each new connection by creating a Peer instance
        this_peer: peer.Peer = peer.Peer.newPeer(
            conn, self.msg_queue
        )  # here we are provinng the conn and msg_queue of server's to the Peer
        print(f"Handling connection for peer: {this_peer}")
        # this_peer.test_protocol()
        self.add_peer_ch.append(this_peer)
        # added new peer to the add_peer_ch of server
        ic(conn.getpeername())
        # starting the peer's readloop on a seperate thread to isolate each peer;s connection from every other peer
        thread = threading.Thread(target=this_peer.read_loop)
        thread.start()

    def stop(self) -> None:
        # stops the server gracefully
        self.quit_event.set()
        self.listener.close()
        print("Server stopped")


def main() -> None:
    server = Server.new_server(config=Config())
    try:
        server_thread = threading.Thread(target=server.start)
        server_thread.start()
        # ic(server.start())
        # Using IceCream to print the return value of start()
        time.sleep(1)

        client_server = client.Client("localhost:5001")
        if err := client_server.set(key="pakoda", value="aloo"):
            print(f"error= > {err}")
        time.sleep(1)
    except KeyboardInterrupt:
        print("server stopped")
        server.stop()


if __name__ == "__main__":
    main()
