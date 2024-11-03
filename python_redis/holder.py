import socket
import threading
from typing import Dict, Optional, List

default_listen_address: str = ":5001"


class Config:
    def __init__(self, listen_address: str = default_listen_address):
        # It holds data like "ListenAddress," specifying where the server listens for connections
        self.listen_address: str = listen_address


class Peer:
    def __init__(self, conn: socket.socket):
        self.conn: socket.socket = conn

    @staticmethod
    def new_peer(conn: socket.socket) -> "Peer":
        return Peer(conn)

    def read_loop(self) -> None:
        # Placeholder for a method that would handle continuous reading from the connection
        pass


class Server:
    def __init__(self, config: Config):
        # Server holds settings, a list of peers, a listener, and a channel for new peers.
        self.config: Config = config
        self.peers: Dict[Peer, bool] = (
            {}
        )  # Dict to track connected peers with Peer as keys
        self.listener: Optional[socket.socket] = None  # Network listener
        self.add_peer_ch: List[Peer] = []  # Channel to add peers to the server

    @staticmethod
    def new_server(config: Config) -> "Server":
        # Initializes the server instance with config settings
        if len(config.listen_address) == 0:
            config.listen_address = default_listen_address
        return Server(config)

    def start(self) -> None:
        # Starts the server by binding to the configured address and entering the accept loop
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.bind(
                (
                    self.config.listen_address.split(":")[0],
                    int(self.config.listen_address.split(":")[1]),
                )
            )
            self.listener.listen()
            self.accept_loop()
        except Exception as e:
            print(f"Error starting server: {e}")

    def loop(self) -> None:
        # This loop waits for a peer in add_peer_ch and adds to the peers dict
        while True:
            if self.add_peer_ch:
                peer = self.add_peer_ch.pop(0)
                self.peers[peer] = True
            else:
                print("No new peer is received")

    def accept_loop(self) -> None:
        # Accepts incoming connections in a loop, handling each connection concurrently
        while True:
            try:
                conn, _ = self.listener.accept()
                thread = threading.Thread(target=self.handle_conn, args=(conn,))
                thread.start()
            except Exception as e:
                print(f"Accept error: {e}")

    def handle_conn(self, conn: socket.socket) -> None:
        # Handles each new connection by creating a Peer instance and starting its read loop
        peer = Peer.new_peer(conn)
        self.add_peer_ch.append(peer)
        thread = threading.Thread(target=peer.read_loop)
        thread.start()


def main() -> None:
    # Setting up configuration and server instance
    config = Config()
    server = Server.new_server(config)
    server.start()


if __name__ == "__main__":
    main()


import socket
from typing import Optional


class Peer:
    def __init__(self, conn: socket.socket):
        self.conn: socket.socket = conn

    @staticmethod
    def new_peer(conn: socket.socket) -> "Peer":
        # Creates a new instance of Peer with the provided connection
        return Peer(conn)

    def read_loop(self) -> None:
        # Placeholder for the continuous reading loop, similar to Go's `readLoop` method.
        # Add any connection handling logic here.
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                print("Received:", data.decode())
        except Exception as e:
            print(f"Error in read loop: {e}")
        finally:
            self.conn.close()
