import socket
from python_redis.protocols.resp_protocols.resp_parser import RESP_Parser
from python_redis.persistence.db import HardDatabase

from python_redis.network.Message import Message

from icecream import ic

from python_redis.models import sets, stacks, liststruc, tree, queuestruc, graph, keyval

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_redis.persistence.db import HardDatabase
# from main import Server, Config
from queue import Queue


class Peer:

    def __str__(self):
        return (
            f"IP ->{self.Conn.getpeername()[0]}   port-> {self.Conn.getpeername()[1]}"
        )

    def __init__(
        self, conn: socket.socket, msg_chan: Queue, del_peer_chan: list["Peer"]
    ):
        self.Conn: socket.socket = conn

        self.DB_str: str = (
            f"{self.Conn.getpeername()[0]}P{self.Conn.getpeername()[1]}".replace(
                ".", "-"
            )
        )

        ic(self.DB_str)
        # TODO: here in it del_peer_chan can raise race condition so handle that and Chatgpt told that the we are refencing the original server's del_peer_chan
        self.msg_chan: Queue[Message] = msg_chan
        self.del_peer_chan: Queue[Peer] = del_peer_chan
        self._db: HardDatabase = HardDatabase.new_db(self.DB_str)
        self._queue: queuestruc.DataQueue = queuestruc.DataQueue.new_queue(self._db)
        self._tree: tree.bstree = tree.bstree.new_tree(self._db)
        self._list: liststruc.List_Struc = liststruc.List_Struc.new_list(self._db)
        self._stack: stacks.Stackstruc = stacks.Stackstruc.new_stack(self._db)
        self._sets: sets.Set = sets.Set.new_set(self._db)
        self._graph: graph.graph = graph.graph.new_graph(self._db)
        self.kv: keyval.KV = keyval.KV.NewKV(self._db)
        self.meta_collection = self._db.new_collection("meta")
        self.recv_buffer: str = str()
        self.resp_parser = RESP_Parser()

    @staticmethod
    def newPeer(
        conn: socket.socket, msg_chan: Queue, del_peer_chan: list["Peer"]
    ) -> "Peer":
        return Peer(conn, msg_chan, del_peer_chan)

    def read_loop(self):
        """
        Continuously reads from the socket and processes RESP messages.
        """
        while True:
            try:
                # Read data from the socket
                raw_data: bytearray = self.Conn.recv(1024)
                raw_str = raw_data.decode("utf-8")
                if not raw_data:
                    # self.del_chan.append(self)
                    # print("Connection closed.")
                    break
                # ! the parse command batch is now unconfigured

                else:
                    # print("this is the single command")
                    # command = self.parse_command(raw_str)
                    self.recv_buffer += raw_str
                    # TODO: solve the empty buffer exception problem 
                    while self.recv_buffer!= None and len(self.recv_buffer) >0 :

                        command_str, remaining = (
                            self.resp_parser.extract_one_resp_command(self.recv_buffer)
                        )
                        if command_str is None:
                            break
                        self.recv_buffer = remaining
                        command = self.resp_parser.parse_command(command_str)
                        # print("got till here")
                        # If a valid command is returned, add to message queue
                        if command != None:
                            message = Message(cmd=command, conn_peer=self)
                            self.msg_chan.put(message)

                    # print(f"Message queued: {message}")

            except ConnectionResetError as e:
                print(f"Connection reset Error in read_loop: {e}")
                # HardDatabase.drop_peer_db(self.DB_str)
                self.close_connection()
                # print("connection is broKen from the client")
                break
            except OSError as e:
                print(f"OS Error in read_loop: {e}")
                # HardDatabase.drop_peer_db(self.DB_str)
                # self.close_connection()

                break
            except Exception as e:
                print(f"Error in read_loop: {e}")
                self.send("-ERR invalid command format".encode("utf-8"))
                # self.close_connection()
                # when nothing is passed from client side then in that case that raises a error (because of that self.close_connection() is commented)
                break

                # Exit loop on error

    def send(self, msg: bytes):

        try:
            # Send the message and return the number of bytes sent
            bytes_sent = self.Conn.send(msg)
            return bytes_sent
        except socket.error as e:
            print(f"Send error: {e}")
            return None

    def close_connection(self):

        try:
            self.send("Bye! thanks for using redis".encode("utf-8"))
            # Step 1: Shutdown both send & receive
            self.Conn.shutdown(socket.SHUT_RDWR)
        except OSError as oe:
            # already closed or reset
            print(f"Encountered OS  error=> {oe}")
            pass
        finally:
            # Step 2: Close the socket

            self.Conn.close()
            self.del_peer_chan.put(self)

            # Step 3: Cleanup peer DB
            #  sudo service mongod start
            HardDatabase.drop_peer_db(self.DB_str)

            # print(f"Closed connection for {self}")

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


# socat TCP4-LISTEN:12345,reuseaddr,fork TCP4:172.22.99.160:5001
# this is the socat tool for proper working


# socat TCP4-LISTEN:12345,reuseaddr,fork TCP:172.25.128.1:5001,sourceport=40000
