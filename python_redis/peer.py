import socket
from typing import Optional
import main

# from main import Server, Config
from queue import Queue

# from protocol import RESPReader
import io


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
                # print(str(data.decode("utf-8")), len(str(data.decode("utf-8"))))
                # Decode and print the received data
                msg_buf = bytearray(data)
                self.msg_chan.put(main.Message(data=msg_buf, conn_peer=self))

        except Exception as e:
            print(f"Read loop error: {e}")
            return e

    def send(self, msg: bytes) -> Optional[int]:
        """
        Sends a message to the peer's connection.

        :param msg: The message to send, as bytes.
        :return: The number of bytes sent, or None if an error occurred.
        """
        try:
            # Send the message and return the number of bytes sent
            bytes_sent = self.Conn.send(msg)
            return bytes_sent
        except socket.error as e:
            print(f"Send error: {e}")
            return None

    # def test_protocol(self):
    #     raw = "*3\r\n$3\r\nSET\r\n$5\r\nmyKey\r\n$3\r\nbar\r\n"

    #     buffer = io.StringIO(raw)
    #     rd = RESPReader(buffer)

    #     try:
    #         while True:
    #             v_type, v_value = rd.read_value()
    #             print(f"Read {v_type}")
    #             if v_type == "Array":
    #                 for i, element in enumerate(v_value):
    #                     e_type, e_value = element
    #                     print(f" #{i} {e_type}, value: '{e_value}'")
    #     except EOFError:
    #         pass
    #     except Exception as e:
    #         print(f"Error: {e}")
