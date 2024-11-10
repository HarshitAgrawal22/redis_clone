import socket
from typing import Optional


class Client:
    def __init__(self, addr: str):
        self.addr: str = addr

    def set(self, key: str, value: str):
        try:

            conn = socket.create_connection(
                (self.addr.split(":")[0], int(self.addr.split(":")[1]))
            )

        except socket.error as e:
            return e
        # Format the RESP array for the SET command
        # RESP format for "*3\r\n$3\r\nSET\r\n$<key_length>\r\n<key>\r\n$<value_length>\r\n<value>\r\n"

        message = f"*3\r\n${len('SET')}\r\nSET\r\n${len(key)}\r\n{key}\r\n${len(value)}\r\n{value}\r\n"
        # message: str = f"set {key} {value}"
        encoded_message = message.encode("utf-8")

        try:
            # Send the message to the server
            conn.sendall(encoded_message)
        finally:
            # Close the connection
            conn.close()

        return None

    def get(self, key: str):
        try:

            conn = socket.create_connection(
                (self.addr.split(":")[0], int(self.addr.split(":")[1]))
            )

        except socket.error as e:
            return e
        # Format the RESP array for the SET command
        # RESP format for "*3\r\n$3\r\nSET\r\n$<key_length>\r\n<key>\r\n$<value_length>\r\n<value>\r\n"

        message = f"*2\r\n${len('GET')}\r\nGET\r\n${len(key)}\r\n{key}\r\n"
        # message: str = f"set {key} {value}"
        encoded_message = message.encode("utf-8")

        try:
            # Send the message to the server
            conn.sendall(encoded_message)
            response = conn.recv(1024)
            return response.decode("utf-8")
        finally:
            # Close the connection
            conn.close()

        return None


def new_client(addr: str):
    return Client(addr=addr)
