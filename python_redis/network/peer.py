import socket
from typing import Optional

from python_redis.persistence.db import HardDatabase
from python_redis.common import execute_command_hash_map
from python_redis.network.Message import Message
import re
from icecream import ic
from python_redis.protocols.keyval_protocol import (
    Command,
    CreateNewQueue,
)
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

    @staticmethod
    def newPeer(
        conn: socket.socket, msg_chan: Queue, del_peer_chan: list["Peer"]
    ) -> "Peer":
        return Peer(conn, msg_chan, del_peer_chan)

    def parse_command(self, raw: str) -> Optional[Command]:
        """Parses the raw RESP command bytes and returns a Command object if valid."""
        # TODO DONE learn what is RESP protocol
        # Decode raw bytes to string without removing any characters
        # print(f"raw command => {raw} {type(raw)} ")

        # ? this is the code which does all the RESP task
        # arr_len = len(holder_arr := raw.split())
        # raw: str = f"*{arr_len}\r\n"
        # for i in holder_arr:
        #     temp_str = i
        #     raw += f"${len(i)}\r\n{temp_str}"
        #     raw += "\r\n"
        # raw = raw.encode("utf-8")
        # # print(raw)
        ic(raw)
        # raw = raw.decode("utf-8")

        # print("Decoded Command:", repr(raw))  # Debugging line

        # Regular expressions for RESP patterns
        # TODO: Move this resp parsinng code to resp_parser.py(need to create that )
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

            func = (
                resultfunc
                if (
                    resultfunc := execute_command_hash_map.get(
                        command_name.lower().strip()
                    )
                )
                != None
                else execute_command_hash_map.get("ukc")
            )
            # print(func, "is the function we have got")

            if func != None:
                return func(args)
            # If no command matches, return None or raise an error
            else:

                raise ValueError(f"Unknown command: {command_name}")

        except Exception as e:
            print(e)

    def extract_one_resp_command(self, buffer: str) -> tuple[str | None, str]:
        """
        Extracts exactly ONE complete RESP command from a buffer.

        Parameters:
            buffer: A string that may contain:
                    - an incomplete RESP command
                    - exactly one RESP command
                    - multiple RESP commands concatenated

        Returns:
            (command, remaining_buffer)
                command            → the full RESP command as a string
                remaining_buffer   → leftover data after extracting one command

            (None, buffer) if the buffer does NOT yet contain a full command
        """

        # RESP commands must start with '*' (array type)
        # If buffer does not start with '*', protocol is invalid
        if not buffer.startswith("*"):
            raise ValueError("Invalid RESP start")

        try:
            # -----------------------------------------
            # STEP 1: Read the RESP array length
            # Example:
            #   *2\r\n
            #    ↑
            #    number of elements (argc = 2)
            # -----------------------------------------

            # Find the end of the first line (*<count>\r\n)
            line_end = buffer.find("\r\n")

            # If we haven't received "\r\n" yet,
            # the command is incomplete → wait for more data
            if line_end == -1:
                return None, buffer

            # Extract number after '*'
            # buffer[1:line_end] → "2"
            argc = int(buffer[1:line_end])

            # Move index to the first bulk string
            # Skip "*<argc>\r\n"
            idx = line_end + 2

            # -----------------------------------------
            # STEP 2: Parse each bulk string
            # -----------------------------------------
            for _ in range(argc):

                # Each bulk string must start with '$'
                if buffer[idx] != "$":
                    raise ValueError("Invalid bulk string")

                # Find end of "$<length>\r\n"
                len_end = buffer.find("\r\n", idx)

                # If length line is incomplete → wait
                if len_end == -1:
                    return None, buffer

                # Extract the bulk string length
                # Example: $4\r\n → strlen = 4
                strlen = int(buffer[idx + 1 : len_end])

                # Move index to the actual data
                idx = len_end + 2

                # Check if the buffer already contains:
                # <data> + "\r\n"
                if len(buffer) < idx + strlen + 2:
                    # Not enough data yet → wait
                    return None, buffer

                # Skip over:
                #   <data> + "\r\n"
                idx += strlen + 2

            # -----------------------------------------
            # STEP 3: Full RESP command extracted
            # -----------------------------------------

            # buffer[:idx]     → one complete RESP command
            # buffer[idx:]     → remaining data (next commands)
            return buffer[:idx], buffer[idx:]

        except Exception:
            # Any parsing error:
            # treat buffer as incomplete / invalid
            return None, buffer

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
                    while True:

                        command_str, remaining = self.extract_one_resp_command(raw_str)
                        if command_str is None:
                            break
                        command = self.parse_command(command_str)
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

    # def parse_command_batch(self, buffer: str):

    #     while "\n" in buffer:
    #         line, buffer = buffer.split("\n", 1)
    #         ic(line)
    #         # Parse the command
    #         # command = self.parse_command(raw_str)
    #         command = self.parse_command(line)
    #         # print("got till here")
    #         # If a valid command is returned, add to message queue
    #         if command != None:
    #             message = Message(cmd=command, conn_peer=self)
    #             self.msg_chan.put(message)
    #     # the last command wasn't getting processed in the while loop so that was handled here

    #     if buffer.strip():
    #         buffer = buffer.rstrip("\r")
    #         ic(buffer)
    #         command = self.parse_command(buffer)
    #         if command != None:
    #             message = Message(cmd=command, conn_peer=self)
    #             self.msg_chan.put(message)

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
