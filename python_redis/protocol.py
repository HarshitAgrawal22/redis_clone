import socket
import threading
from typing import Dict

from icecream import ic
from queue import Queue
import io


class RESPReader:
    CommandSET, CommandGET, CommandHELLO, CommandClient = (
        "SET",
        "GET",
        "HELLO",
        "CLIENT",
    )

    # this class gets the raw string and after analyzing the raw string it performs task like setting keys in ram or read them

    def __init__(self, buffer: io.StringIO):
        self.buffer = buffer

    def read_value(self):
        # Read a line from the buffer and parse according to RESP protocol
        line = self.buffer.readline().strip()
        if not line:
            raise EOFError("End of buffer reached")
        if line.startswith("*"):  # Array type
            length = int(line[1:])
            array_values = []
            for _ in range(length):
                element_type, element_value = (
                    self.read_value()
                )  # Unpack the type and value of each element
                array_values.append((element_type, element_value))  # Append as a tuple
            return "Array", array_values
        elif line.startswith("$"):  # Bulk string type
            length = int(line[1:])
            value = self.buffer.read(length)
            self.buffer.readline()  # Consume newline after value
            return "BulkString", value
        else:
            raise ValueError("Unknown RESP type")


class SetCommand:
    def __init__(self, key: str, value: str):
        self.key: str = key
        self.value: str = value


def parse_command(raw: str):
    buffer = io.StringIO(raw)
    reader = RESPReader(buffer)

    try:
        while True:
            v_type, v_value = reader.read_value()
            if v_type == "Array":
                ic(v_value)
                print(type(v_value))
                for i, element in enumerate(v_value):

                    e_type, e_value = element

                    print(f" #{i} {e_type}, value: '{e_value}'")
                    if (
                        e_type == "BulkString"
                        and i == 0
                        and e_value == RESPReader.CommandSET
                    ):
                        if len(v_value) == 3:
                            cmd = SetCommand(key=v_value[1][1], value=v_value[2][1])
                            return cmd
                        else:
                            raise ValueError("Invalid SET command format")
    except EOFError:
        pass
