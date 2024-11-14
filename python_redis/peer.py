import socket
from typing import Optional, Union
from main import Message
from protocol import (
    Command,
    SetCommand,
    GetCommand,
    QuitCommand,
    HelloCommand,
    CheckCommand,
    SetMultipleAttributeCommand,
    GetMultipleKeyValCommand,
    TotalCommand,
    ClientCommand,
    DeleteCommand,
    IncreamentCommand,
    SetMultipleKeyValCommand,
    COMMAND_SET,
    COMMAND_GET,
    COMMAND_QUIT,
    COMMAND_CHECK,
    COMMAND_DELETE,
    COMMAND_HELLO,
    COMMAND_CLIENT,
    COMMAND_GET_MULTIPLE_VALUES,
    COMMAND_INCREAMENT,
    COMMAND_MULTIPLE_ATTRIBUTE_SET,
    COMMAND_SET_MULTIPLE_KEY_VAL,
)
import re
from icecream import ic

# from main import Server, Config
from queue import Queue

# from protocol import RESPReader
import io


class Peer:
    def __str__(self):
        return (
            f"IP ->{self.Conn.getpeername()[0]}   port-> {self.Conn.getpeername()[1]}"
        )

    def __init__(self, conn: socket.socket, msg_chan: Queue, del_chan: list["Peer"]):
        self.Conn: socket.socket = conn
        self.msg_chan: Queue = msg_chan
        self.del_chan: list[Peer] = del_chan

    @staticmethod
    def newPeer(conn: socket.socket, msg_chan: Queue, del_chan: list["Peer"]) -> "Peer":
        return Peer(conn, msg_chan, del_chan)

    def parse_command(self, raw: str) -> Optional[Command]:
        """Parses the raw RESP command bytes and returns a Command object if valid."""

        # Decode raw bytes to string without removing any characters
        print(f"raw commadn => {raw} {type(raw)} ")
        arr_len = len(holder_arr := raw.split())
        raw = f"*{arr_len}\r\n"
        for i in holder_arr:
            temp_str = i
            raw += f"${len(i)}\r\n{temp_str}"
            raw += "\r\n"
        raw = raw.encode("utf-8")
        print(raw)
        ic(raw)
        raw = raw.decode("utf-8")
        print("Decoded Command:", repr(raw))  # Debugging line

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
        print(f"Found items: {items}")

        # Validate RESP format
        if len(items) != expected_items:
            raise ValueError(f"RESP array length mismatch command:{raw}")
        command_name: str
        # Extract command name and arguments
        command_name, *args = [item[1] for item in items]

        # Check if the command is "set" and requires exactly 2 arguments
        if command_name.lower().strip() == COMMAND_QUIT:
            if len(args) != 0:
                print(f"{args} are args for quitting server")
                raise ValueError("Invalid number of arguments for GET command")

            return QuitCommand(want_to_quit=True)

        if command_name.lower() == COMMAND_GET:
            if len(args) != 1:
                print(f"{args} = args")
                raise ValueError("Invalid number of arguments for GET command")
            key = args[0]
            return GetCommand(key)
        if command_name.lower() == COMMAND_HELLO:
            if len(args) != 1:
                raise ValueError("Invalid number of arguments for SET command")
            return HelloCommand(args[0])
        # If no command matches, return None or raise an error

        if command_name.lower() == COMMAND_SET:
            if len(args) != 2:
                raise ValueError("Invalid number of arguments for SET command")
            key, value = args
            return SetCommand(key, value)

        # If no command matches, return None or raise an error
        raise ValueError(f"Unknown command: {command_name}")

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
                    print("Connection closed.")
                    break

                # Decode raw data to string for RESP parsing
                raw_str = raw_data.decode("utf-8")
                print("Decoded Command:", repr(raw_str))  # Debugging line
                raw_str = raw_str.strip()
                # Parse the command
                command = self.parse_command(raw_str)
                # print("got till here")
                # If a valid command is returned, add to message queue
                if command:
                    message = Message(cmd=command, conn_peer=self)
                    self.msg_chan.put(message)
                    print(f"Message queued: {message}")

            except Exception as e:
                print(f"Error in read_loop: {e}")
                pass  # Exit loop on error

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
