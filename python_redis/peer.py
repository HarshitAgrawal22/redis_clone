import socket
from main import Server, Config
from queue import Queue


class Peer:
    def __str__(self):
        return (
            f"IP ->{self.Conn.getpeername()[0]}   port-> {self.Conn.getpeername()[1]}"
        )

    def __init__(self, conn: socket.socket, msg_chan: Queue):
        self.Conn: socket.socket = conn
        self.msg_chan: Queue = msg_chan

    @staticmethod
    def newPeer(conn: socket.socket, msg_chan: Queue) -> "Peer":
        return Peer(conn, msg_chan)

    def read_loop(self):
        buf_size = 1024
        try:
            while True:
                # Receive data from the connection
                data = self.Conn.recv(buf_size)
                if not data:
                    # If data is empty, the connection has likely closed
                    break
                print(
                    str(data.decode("utf-8")), len(str(data.decode("utf-8")))
                )  # Decode and print the received data
                msg_buf = bytearray(data)
                self.msg_chan.put(msg_buf)

        except Exception as e:
            print(f"Read loop error: {e}")
            return e
