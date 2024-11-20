# this file contains all the protocols and Commands need for the server

import re
from typing import Union
from icecream import ic
from io import BytesIO

ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_SET = "set"
COMMAND_GET = "get"
COMMAND_HELLO = "hello"
COMMAND_CLIENT = "client"
COMMAND_QUIT = "shaanti"
COMMAND_MULTIPLE_ATTRIBUTE_SET = "setattr"  # multiple attributes of a object where name of object will be key and attributes will be value
COMMAND_MULTIPLE_ATTRIBUTE_GET = "getattr"
COMMAND_SET_MULTIPLE_KEY_VAL = "setm"  # set multiple pairs in one command


COMMAND_GET_MULTIPLE_VALUES = "getm"  # multiple keys will given to server and server will return all keys' values in same order
COMMAND_CHECK = "chec"  # check if a key exists
COMMAND_DELETE = "del"  # delete a pair
COMMAND_TOTAL = "len"  # total no. of keys and values on the database
COMMAND_INCREMENT = "incryby"  # HINCRBY user:1000 age 1


class Command:
    pass


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


def resp_write_dict(m: dict[str, str]) -> bytes:

    buf = BytesIO()

    buf.write(b"%" + f"{len(m)}\r\n".encode("utf-8"))

    for k, v in m.items():

        buf.write(f"4{len(m)}\r\n".encode("utf-8"))

        buf.write(f":{v}\r\n".encode("utf-8"))

    return buf.getvalue()
