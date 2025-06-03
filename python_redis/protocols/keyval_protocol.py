# this file contains all the protocols and Commands need for the server

import re
from typing import Union
from icecream import ic
from .command import Command

# from python_redis.common import Message

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_SET = "hset"
COMMAND_GET = "hget"
COMMAND_HELLO = "hello"
COMMAND_CLIENT = "client"
COMMAND_QUIT = "shaanti"
COMMAND_MULTIPLE_ATTRIBUTE_SET = "hsetattr"  # multiple attributes of a object where name of object will be key and attributes will be value
COMMAND_MULTIPLE_ATTRIBUTE_GET = "hgetattr"
COMMAND_SET_MULTIPLE_KEY_VAL = "hsetm"  # set multiple pairs in one command
COMMAND_GET_MULTIPLE_VALUES = "hgetm"  # multiple keys will given to server and server will return all keys' values in same order
COMMAND_CHECK = "hchec"  # check if a key exists
COMMAND_DELETE = "hdel"  # delete a pair
COMMAND_TOTAL = "hlen"  # total no. of keys and values on the database
COMMAND_INCREMENT = "hincryby"  # HINCRBY user:1000 age 1


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


def execute_set_command(args):
    if len(args) != 2:
        raise ValueError("Invalid number of arguments for SET command")
    key, value = args
    # print(f"setting {key} { value}")
    return SetCommand(key, value)


def execute_get_command(args):
    if len(args) != 1:
        print(f"{args} = args")
        raise ValueError("Invalid number of arguments for GET command")
    key = args[0]
    return GetCommand(key)


def execute_quit_command(args):
    if len(args) != 0:
        print(f"{args} are args for quitting server")
        raise ValueError("Invalid number of arguments for GET command")

    return QuitCommand(want_to_quit=True)


def execute_hello_command(args):
    if len(args) != 1:
        raise ValueError("Invalid number of arguments for SET command")
    return HelloCommand(args[0])


def execute_check_command(args):
    if len(args) >= 1:
        return CheckCommand(args)
    raise ValueError("No arguments given for CHECK command")


def execute_client_command(args):
    if len(args) == 0:
        raise ValueError("No arguments for CLIENT command")
    return ClientCommand(args[0])


def execute_delete_command(args):
    if len(args) == 0:
        raise ValueError("No key given for DELETE command")

    return DeleteCommand(args[0])


def execute_get_multiple_values_command(args):
    if len(args) == 0:
        raise ValueError("No key given to get value")
    return GetMultipleKeyValCommand(args)


def execute_incry_command(args):
    if len(args) == 0:
        raise ValueError("No key for INCREMENT command")
    return IncrementCommand(args[0])


def execute_total_command(args):
    return TotalCommand("return total")


def execute_multiple_attrs_set_command(args):
    if len(args) == 0:
        raise ValueError("No argument for SET MULTIPLE ATTRIBUTE command")
    key: str = args[0]
    attrs: tuple = args[1:]

    return SetMultipleAttributeCommand(key=key, attrs=attrs)


def execute_multiple_attrs_get_command(args):
    if len(args) == 0:
        raise ValueError("No argument for SET MULTIPLE ATTRIBUTE command")
    key: str = args[0]
    attrs: tuple = args[1:]

    return GetMultipleAttributeCommand(key=key, attrs=attrs)


def execute_set_multi_key_val_command(args):
    if len(args) == 0:
        raise ValueError("No arguments given for SET MULTIPLE KEY VALUE PAIRS")
    if len(args) % 2 != 0:
        raise ValueError("Invalid Key Value pairs")
    return SetMultipleKeyValCommand(args)


class HASHMAP_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_set_command(msg, server):
        # print(
        #     f"Somebody wants to set a key into the hash table \nkey=>{msg.cmd.key}\nvalue =>{msg.cmd.value}"
        # )
        # msg.conn_peer.send(
        #     f"key=>{msg.cmd.key}\nvalue =>{msg.cmd.value}".encode("utf-8")
        # )
        try:
            msg.conn_peer.send("OK".encode("utf-8"))

            return msg.conn_peer.kv.set(msg.cmd.key, msg.cmd.value)
        except Exception as e:
            print(f"got exception while sending SET message  {e}")

    @staticmethod
    def task_get_command(msg, server):

        try:
            (value, isOK) = msg.conn_peer.kv.get(msg.cmd.key)

            # if not OK:
            #     raise ValueError("response not OK ")
            try:
                msg.conn_peer.send(f"{value}".encode("utf-8"))
            except Exception as e:
                return e
        except ValueError as e:
            return e

    @staticmethod
    def task_total_command(msg, server):

        try:
            length: int = msg.conn_peer.kv.total()

            msg.conn_peer.send(f"{length}".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_get_multiple_attrs_command(msg, server):
        try:
            ic(msg.cmd.key)
            ic(msg.cmd.attrs)
            result = msg.conn_peer.kv.get_attributes(msg.cmd.key, msg.cmd.attrs)
            msg.conn_peer.send(f"{result}".encode("utf-8"))
        except Exception as e:
            print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")

    @staticmethod
    def task_set_multiple_attrs_command(msg, server):
        try:
            ic(msg.cmd.key)
            ic(msg.cmd.attrs)
            msg.conn_peer.kv.set_attributes(msg.cmd.key, msg.cmd.attrs)
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")

    @staticmethod
    def task_set_multi_key_val_command(msg, server):
        try:
            ic(msg.cmd.args)
            msg.conn_peer.kv.set_multiple_pairs(msg.cmd.args)

            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:

            print(f"got error in SET_MULTIPLE_KEY_VAL_COMMAND{e}")

    @staticmethod
    def task_get_multi_key_val_command(msg, server):
        try:
            ic(msg.cmd.keys)
            result: str = msg.conn_peer.kv.get_multiple_values(msg.cmd.keys)
            msg.conn_peer.send(f"{result}".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_quit_command(msg, server):
        server.stop()

    @staticmethod
    def task_increment_command(msg, server):
        try:
            msg.conn_peer.kv.increment(msg.cmd.key)
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_delete_command(msg, server):
        try:
            msg.conn_peer.kv.delete_pair(msg.cmd.key)
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_client_command(msg, server):

        try:
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_check_command(msg, server):
        try:

            result: list[bool] = msg.conn_peer.kv.check(msg.cmd.keys)
            data = "OK "
            for i in result:
                data += f"{i} "
            msg.conn_peer.send(data.encode("utf-8"))

        except Exception as e:
            print(f"got error while CHECK command: {e}")

    @staticmethod
    def task_hello_command(msg, server):
        spec = dict({"server": "redis"})
        try:
            msg.conn_peer.send(f"{spec}".encode("utf-8"))
        except:
            print("got error while sending specs")
