from typing import Union
from icecream import ic
from .command import Command

# from python_redis.common import Message

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class UnknownCommand(Command):
    def __init__(self, command: tuple[str]):
        self.response = f"command:({ ', '.join(command) }) is unknown"

    def __str__(self):
        return self.response


class CreateNewQueue(Command):
    def __init__(self, key: str, peer):
        self.key = key
        self.peer = peer

    def __str__(self):
        return f"command to create a new Queue for {self.peer} "


class SetCommand(Command):  #
    def __init__(self, key: bytearray, value: bytearray):
        self.key: bytearray = key
        self.value: bytearray = value

    def __str__(self):
        return f"key:{self.key}  value:{self.value}"


class GetCommand(Command):  #
    def __init__(self, key: bytearray):
        self.key: bytearray = key
        # self.value: bytearray

    def __str__(self):
        return f"key:{self.key}"


class KillCommand(Command):

    def __init__(self):
        pass

    # here we are doing nothing


class QuitCommand(Command):  #
    def __init__(self, want_to_quit: bool):
        self.want_to_quit: bool = want_to_quit

    def __str__(self):
        return "Got Order to Quit Server"


class ClientCommand(Command):  #
    def __init__(self, value: str):
        self.string: str = value


class HelloCommand(Command):  #
    def __init__(self, value: str):
        self.value: str = value

    def __str__(self):
        return "hello from peer"


class SetMultipleAttributeCommand(Command):
    def __init__(self, key: str, attrs: dict):
        self.attrs: list = attrs
        self.key: str = key

    def __str__(self):
        return f"{self.key}:{self.attrs}"


class GetMultipleAttributeCommand(Command):
    def __init__(self, key: str, attrs: list):
        self.attrs: list = attrs
        self.key: str = key

    def __str__(self):
        return f"{self.key}:{self.attrs}"


class SetMultipleKeyValCommand(Command):  #
    def __init__(self, pairs: list):
        self.args = pairs


class GetMultipleKeyValCommand(Command):  #
    def __init__(self, keys: list[str]):
        self.keys: list[str] = keys


class CheckCommand(Command):  #
    def __init__(self, keys: list[str]):
        self.keys: list[str] = keys


class DeleteCommand(Command):  #
    def __init__(self, key: str):
        self.key: str = key


class TotalCommand(Command):  #
    def __init__(self, cmd):
        self.cmd: str = cmd


class IncrementCommand(Command):  #
    def __init__(self, key):
        self.key: str = key
