import re
from typing import Union
from icecream import ic

ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_SET = "set"
COMMAND_GET = "get"
COMMAND_HELLO = "hello"
COMMAND_CLIENT = "client"


class Command:
    pass


class SetCommand(Command):
    def __init__(self, key: str, value: str):
        self.key: str = key
        self.value: str = value

    def __str__(self):
        return f"key:{self.key}  value:{self.value}"


def parse_command(raw: bytes) -> Union[Command, None]:
    """Parses the raw RESP command bytes and returns a Command object if valid."""

    # Decode raw bytes to string without removing any characters
    arr_len = len(holder_arr := raw.split())
    raw = "*3\r\n"
    for i in holder_arr:
        temp_str = i.decode("utf-8")
        raw += f"${len(i)}\r\n{temp_str}"
        raw += "\r\n"
    raw = raw.encode("utf-8")
    # print(raw)
    # ic(raw)
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

    # Extract command name and arguments
    command_name, *args = [item[1] for item in items]

    # Check if the command is "set" and requires exactly 2 arguments
    if command_name.lower() == COMMAND_SET:
        if len(args) != 2:
            raise ValueError("Invalid number of arguments for SET command")
        key, value = args
        return SetCommand(key, value)

    # If no command matches, return None or raise an error
    raise ValueError(f"Unknown command: {command_name}")


# Example usage
# Testing with a correctly formatted RESP command
# raw_resp = "*3\r\n$3\r\nSET\r\n$5\r\nhello\r\n$5\r\nworld\r\n".encode("utf-8")
# resp = "set harshit bro"
# command = parse_command(resp)

# if isinstance(command, SetCommand):
#     print(f"SET Command: key={command.key}, value={command.value}")
