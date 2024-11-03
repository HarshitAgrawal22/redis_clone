import socket
import threading
from typing import Dict
import peer
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
        self.peers: Dict[peer.Peer, bool] = (
            {}
        )  # Dict to track connected peers with Peer as keys
        self.listener: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # Network listener
        self.add_peer_ch: list[peer.Peer] = []  # Channel to add peers to the server

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
            self.accept_loop()
        except Exception as e:
            print(f"Error starting server: {e}")

    def loop(self) -> None:
        # This loop waits for a peer in add_peer_ch and adds to the peers dict
        while True:
            if self.add_peer_ch:
                peer = self.add_peer_ch.pop(0)
                self.peers[peer] = True
                print(f"Added new peer: {peer}")  # Added print statement
            else:
                print("No new peer is received")

    def accept_loop(self) -> None:
        # Accepts incoming connections in a loop, handling each connection concurrently
        while True:
            try:
                conn, _ = self.listener.accept()
                print("Accepted a new connection")  # Added print statement
                thread = threading.Thread(target=self.handle_conn, args=(conn,))
                thread.start()
            except Exception as e:
                print(f"Accept error: {e}")

    def handle_conn(self, conn: socket.socket) -> None:
        # Handles each new connection by creating a Peer instance
        this_peer: peer.Peer = peer.Peer.new_peer(conn)
        print(f"Handling connection for peer: {this_peer}")  # Added print statement
        self.add_peer_ch.append(this_peer)
        thread = threading.Thread(target=this_peer.readLoop)
        thread.start()


def main() -> None:
    server = Server.new_server(config=Config())
    ic(server.start())  # Using IceCream to print the return value of start()


if __name__ == "__main__":
    main()
