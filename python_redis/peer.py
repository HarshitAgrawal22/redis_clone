import socket
from typing import Optional

from python_redis.db import HardDatabase
from python_redis.common import execute_command_hash_map, Message
import re
from icecream import ic
from python_redis.protocols.keyval_protocol import (
    Command,
    CreateNewQueue,
)
from python_redis.models import sets, stacks, liststruc, tree, queuestruc, graph, keyval

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_redis.db import HardDatabase
# from main import Server, Config
from queue import Queue


class Peer:

    def __str__(self):
        return (
            f"IP ->{self.Conn.getpeername()[0]}   port-> {self.Conn.getpeername()[1]}"
        )

    def __init__(self, conn: socket.socket, msg_chan: Queue, del_chan: list["Peer"]):
        self.Conn: socket.socket = conn

        self.DB_str: str = (
            f"{self.Conn.getpeername()[0]}P{self.Conn.getpeername()[1]}".replace(
                ".", "-"
            )
        )

        ic(self.DB_str)

        # self.db_conn_str = f"{self.Conn.raddr[0]}:{self.Conn.raddr[1]}"
        # ic(self.db_conn_str)
        # ic(self.Conn.raddr[0]  self.Conn.raddr[0])
        self.msg_chan: Queue = msg_chan
        self.del_chan: list[Peer] = del_chan
        self._db: HardDatabase = HardDatabase.new_db(self.DB_str)
        self._queue: queuestruc.DataQueue = queuestruc.DataQueue.new_queue()
        self._tree: tree.bstree = tree.bstree.new_tree()
        self._list: list = liststruc.List_Struc.new_list()
        self._stack: stacks.Stackstruc = stacks.Stackstruc.new_stack()
        self._sets: sets.Set = sets.Set.new_set(self._db)
        self._graph: graph.graph = graph.graph.new_graph()

        # self._db.new_collection("bh# The code snippet you provided defines a class `Peer` in Python.
        # The `a` variable is not explicitly defined or used within the
        # class. It seems like there might be a typo or a missing part of
        # the code where `a` should be referenced or utilized.
        # aang")
        self.kv: keyval.KV = keyval.KV.NewKV(self._db)

    @staticmethod
    def newPeer(conn: socket.socket, msg_chan: Queue, del_chan: list["Peer"]) -> "Peer":
        return Peer(conn, msg_chan, del_chan)

    def parse_command(self, raw: str) -> Optional[Command]:
        """Parses the raw RESP command bytes and returns a Command object if valid."""

        # Decode raw bytes to string without removing any characters
        # print(f"raw command => {raw} {type(raw)} ")
        arr_len = len(holder_arr := raw.split())
        raw = f"*{arr_len}\r\n"
        for i in holder_arr:
            temp_str = i
            raw += f"${len(i)}\r\n{temp_str}"
            raw += "\r\n"
        raw = raw.encode("utf-8")
        # print(raw)
        # ic(raw)
        raw = raw.decode("utf-8")
        # print("Decoded Command:", repr(raw))  # Debugging line

        # Regular expressions for RESP patterns
        array_pattern = r"\*([0-9]+)\r\n"
        bulk_string_pattern = r"\$([0-9]+)\r\n(.+?)\r\n"

        # Find the array count in the RESP string
        array_match = re.match(array_pattern, raw)
        if not array_match:
            raise ValueError("Invalid RESP format (Array not found)")

        expected_items = int(array_match.group(1))
        items = re.findall(bulk_string_pattern, raw)

        # Debugging output for items parsed
        # print(f"Found items: {items}")

        # Validate RESP format

        if len(items) != expected_items:
            raise ValueError(f"RESP array length mismatch command:{raw}")
        command_name: str
        # Extract command name and arguments
        command_name, *args = [item[1] for item in items]
        try:
            if command_name.lower().strip() == "kill":
                self.kv.kill()
                self.Conn.close()
            func = execute_command_hash_map.get(command_name.lower().strip())
            # print(func, "is the function we have got")
            if func != None:
                return func(args)
            # If no command matches, return None or raise an error
            else:
                raise ValueError(f"Unknown command: {command_name}")
        except Exception as e:
            print(e)

    def read_loop(self):
        # buf_size = 1024
        # try:
        #     while True:
        #         # Receive data from the connection
        #         data = self.Conn.recv(buf_size)
        #         if not data:
        #             # If data is empty, the connection has likely closed
        #             break
        #         # print(str(data.decode("utf-8")), len(str(data.decode("utf-8"))))
        #         # Decode and print the received data
        #         msg_buf = bytearray(data)
        #         self.msg_chan.put(main.Message(data=msg_buf, conn_peer=self))

        # except Exception as e:
        #     print(f"Read loop error: {e}")
        #     return e

        # raw = raw.decode("utf-8")

        """
        Continuously reads from the socket and processes RESP messages.
        """
        while True:
            try:
                # Read data from the socket
                raw_data: bytearray = self.Conn.recv(1024)
                if not raw_data:
                    # self.del_chan.append(self)
                    # print("Connection closed.")
                    break

                # Decode raw data to string for RESP parsing
                raw_str = raw_data.decode("utf-8")
                # print("Decoded Command:", repr(raw_str))
                raw_str = raw_str.strip()
                # Parse the command
                command = self.parse_command(raw_str)
                # print("got till here")
                # If a valid command is returned, add to message queue
                if command:
                    message = Message(cmd=command, conn_peer=self)
                    self.msg_chan.put(message)
                    # print(f"Message queued: {message}")

            except ConnectionResetError as e:
                print(f"Error in read_loop: {e}")
                HardDatabase.drop_peer_db(self.DB_str)
                # print("connection is broKen from the client")
                break
            except OSError as e:
                print(f"Error in read_loop: {e}")
                HardDatabase.drop_peer_db(self.DB_str)

                break
            except Exception as e:
                print(f"Error in read_loop: {e}")
                pass

                # Exit loop on error

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

        # check if the command is "hsetm" and requires more then 0 and even arguments
        # if command_name.lower().strip() == COMMAND_SET_MULTIPLE_KEY_VAL:
        #     if len(args) == 0:
        #         raise ValueError("No arguments given for SET MULTIPLE KEY VALUE PAIRS")
        #     if len(args) % 2 != 0:
        #         raise ValueError("Invalid Key Value pairs")
        #     return SetMultipleKeyValCommand(args)

        # check if the command is "getattr" and requires more than no arguments
        # if command_name.lower().strip() == COMMAND_MULTIPLE_ATTRIBUTE_GET:
        #     if len(args) == 0:
        #         raise ValueError("No argument for SET MULTIPLE ATTRIBUTE command")
        #     key: str = args[0]
        #     attrs: tuple = args[1:]

        #     return GetMultipleAttributeCommand(key=key, attrs=attrs)
        # check if the command is "setattr" and requires more than no arguments
        # if command_name.lower().strip() == COMMAND_MULTIPLE_ATTRIBUTE_SET:
        #     if len(args) == 0:
        #         raise ValueError("No argument for SET MULTIPLE ATTRIBUTE command")
        #     key: str = args[0]
        #     attrs: tuple = args[1:]

        #     return SetMultipleAttributeCommand(key=key, attrs=attrs)
        # check if the command is "total" and requires no argument
        # if command_name.lower().strip() == COMMAND_TOTAL:
        #     return TotalCommand("return total")

        # check if the command is "increment" and requires exactly 1 argument
        # if command_name.lower().strip() == COMMAND_INCREMENT:
        #     if len(args) == 0:
        #         raise ValueError("No key for INCREMENT command")
        #     return IncrementCommand(args[0])

        # check if the command is "hello" and requires exactly 1 argument
        # if command_name.lower().strip() == COMMAND_GET_MULTIPLE_VALUES:
        #     if len(args) == 0:
        #         raise ValueError("No key given to get value")
        #     return GetMultipleKeyValCommand(args)

        # check if the command is "delete" and requires exactly 1 argument
        # if command_name.lower().strip() == COMMAND_DELETE:
        #     if len(args) == 0:
        #         raise ValueError("No key given for DELETE command")
        #     print(args)
        #     return DeleteCommand(args[0])
        # check if the command is "client" and requires exactly 1 argument
        # if command_name.lower().strip() == COMMAND_CLIENT:
        #     if len(args) == 0:
        #         raise ValueError("No arguments for CLIENT command")
        #     return ClientCommand(args[0])

        # check if the command is "check" and requires exactly 1 argument
        # if command_name.lower().strip() == COMMAND_CHECK:
        #     if len(args) >= 1:
        #         return CheckCommand(args)
        #     raise ValueError("No arguments given for CHECK command")
        # check if the command is "quit" and requires no argument
        # if command_name.lower().strip() == COMMAND_QUIT:
        #     if len(args) != 0:
        #         print(f"{args} are args for quitting server")
        #         raise ValueError("Invalid number of arguments for GET command")

        #     return QuitCommand(want_to_quit=True)
        # check if the command is "get" and requires exactly 1 argument
        # if command_name.lower().strip() == COMMAND_GET:
        #     if len(args) != 1:
        #         print(f"{args} = args")
        #         raise ValueError("Invalid number of arguments for GET command")
        #     key = args[0]
        #     return GetCommand(key)
        # check if the command is "hello" and requires exactly 1 argument
        # if command_name.lower().strip() == COMMAND_HELLO:
        #     if len(args) != 1:
        #         raise ValueError("Invalid number of arguments for SET command")
        #     return HelloCommand(args[0])

        # Check if the command is "set" and requires exactly 2 arguments
        # if command_name.lower() == COMMAND_SET:
        #     if len(args) != 2:
        #         raise ValueError("Invalid number of arguments for SET command")
        #     key, value = args
        #     return SetCommand(key, value)


# socat TCP4-LISTEN:12345,reuseaddr,fork TCP4:172.22.99.160:5001  this is the socat tool for proper working


# socat TCP4-LISTEN:12345,reuseaddr,fork TCP:172.25.128.1:5001,sourceport=40000
