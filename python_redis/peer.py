import socket
from main import Server, Config


class Peer:
    def __init__(self, conn):
        self.Conn: socket.socket = conn

    @staticmethod
    def newPeer(conn: socket.socket) -> "Peer":
        return Peer(conn)

    def readLoop(self):
        # starts a new server within the peer , which mimics the behaviour
        server = Server(config=Config(listen_address=":5001"))
