import socket
from typing import Optional
import threading

from icecream import ic

default_listen_address: str = ":5001"
ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class Client:
    def __init__(self, addr: str):
        self.addr: str = addr
        self.conn = socket.create_connection(
            (self.addr.split(":")[0], int(self.addr.split(":")[1]))
        )

    def __str__(self):
        return f"addr:{self.addr}   conn:{self.conn}"

    def set(self, key: str, value: str):
        # try:

        # conn = socket.create_connection(
        #     (self.addr.split(":")[0], int(self.addr.split(":")[1]))
        # )

        # except socket.error as e:
        #     return e
        # Format the RESP array for the SET command
        # RESP format for "*3\r\n$3\r\nSET\r\n$<key_length>\r\n<key>\r\n$<value_length>\r\n<value>\r\n"

        # message = f"*3\r\n${len('SET')}\r\nSET\r\n${len(key)}\r\n{key}\r\n${len(value)}\r\n{value}\r\n"
        lists = ["harshit", "hrishika", "tiwari", "samosa", "mayank", "billa", "uday"]

        for i in lists:
            message = f"hset name {i}"

            encoded_message = message.encode("utf-8")
            self.conn.send(encoded_message)

            threading.Event().wait(0.1)
            response = self.conn.recv(1024)
            ic(response.decode("utf-8"))
            threading.Event().wait(0.1)

        return None

    def get(self, key: str):

        message: str = f"hget {key}"
        encoded_message = message.encode("utf-8")

        try:
            # Send the message to the server
            self.conn.send(encoded_message)
            response = self.conn.recv(1024)
            return response.decode("utf-8")
        except Exception as e:
            print(e)
            # Close the connection
            # self.conn.close()

    def insert_vertex_to_graph(self):
        try:
            data_arr = [
                "name harshit sec k",
                "name tiwari sec j",
                "name  samosa sec l",
                "name mayank sec i",
                "name billa sec a",
                "name uday sec z",
                "name hrishika sec op",
            ]
            self.conn.send("gsetk name".encode("utf-8"))
            for i in data_arr:
                threading.Event().wait(0.1)
                enc_mess = f"gaddv {i}".encode("utf-8")
                self.conn.send(enc_mess)
                threading.Event().wait(0.1)
                response = self.conn.recv(1024)
                ic(response.decode("utf-8"))

            # return response
        except Exception as e:
            print(e)

    def bfs(self):
        threading.Event().wait(0.1)
        try:

            self.conn.send("gdfs harshit".encode("utf-8"))
            threading.Event().wait(0.5)
            response = self.conn.recv(1024)
            print(response.decode("utf-8"))
        except Exception as e:
            print(e)

    def show_graph(self):
        threading.Event().wait(0.1)
        try:

            self.conn.send("gshow".encode("utf-8"))
            threading.Event().wait(1)
            response = self.conn.recv(1024)
            print(response.decode("utf-8"))
        except Exception as e:
            print(e)

    def add_edges_to_graph(self):
        threading.Event().wait(0.1)

        try:
            lists = [
                "harshit",
                "hrishika",
                "tiwari",
                "samosa",
                "mayank",
                "billa",
                "uday",
            ]
            for i in range(5):
                threading.Event().wait(1)
                self.conn.send(
                    f"gadde {lists[i]} {lists[len( lists)-i-1]} 12".encode("utf-8")
                )
                threading.Event().wait(1)
                response = self.conn.recv(1024)
                print(response.decode("utf-8"))
            self.conn.send(f"gadde hrishika harshit 12".encode("utf-8"))
            threading.Event().wait(1)
            self.conn.send(f"gadde tiwari uday 12".encode("utf-8"))
            threading.Event().wait(1)
            self.conn.send(f"gadde uday mayank 12".encode("utf-8"))
            threading.Event().wait(1)
            self.conn.send(f"gadde hrishika tiwari 12".encode("utf-8"))
        except Exception as e:
            print(e)

    def remove_vertex(self):
        threading.Event().wait(0.1)

        self.conn.send("gremv sher".encode("utf-8"))
        threading.Event().wait(1)
        response = self.conn.recv(1024)
        print(response.decode("utf-8"))
        threading.Event().wait(0.1)
        self.conn.send("gremv mayank".encode("utf-8"))

    def remove_edge(self):
        threading.Event().wait(0.1)

        self.conn.send("greme harshit uday".encode("utf-8"))
        threading.Event().wait(1)
        response = self.conn.recv(1024)
        print(response.decode("utf-8"))
        threading.Event().wait(0.1)
        self.conn.send("greme mayank tiwari".encode("utf-8"))

    def dij(self):
        threading.Event().wait(0.1)
        self.conn.send("gdij harshit".encode("utf-8"))
        threading.Event().wait(1)
        response = self.conn.recv(1024)
        print(response.decode("utf-8"))
        threading.Event().wait(0.1)
        self.conn.send("greme mayank tiwari".encode("utf-8"))


def new_client(addr: str):
    return Client(addr=addr)
