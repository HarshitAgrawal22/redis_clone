from __future__ import annotations
from .command import Command
from icecream import ic
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from python_redis.common import Message

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


def str_to_int(string):
    return int(string)


class RPushCommand(Command):
    def __init__(self, item):
        self.item = item


class LPushCommand(Command):
    def __init__(self, item):
        self.item = item


class RPullCommand(Command):
    def __init__(self):
        print("got command to rpull")


class LPullCommand(Command):
    def __init__(self):
        print("got command to rpull")


class LRangeCommand(Command):
    def __init__(self, start: int, end: int):
        self.start: int = start
        self.end: int = end


class RRangeCommand(Command):
    def __init__(self, start: int, end: int):
        self.start: int = start
        self.end: int = end


class SearchIndexCommand(Command):
    def __init__(self, index):
        self.index: int = index


def execute_rpush_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return RPushCommand(args[0])


def execute_lpush_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return LPushCommand(args[0])


def execute_rpull_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return RPullCommand()


def execute_lpull_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return LPullCommand()


def execute_lrange_command(args):
    if len(args) != 2:
        raise ValueError("invalid no. args for peek command")
    args = tuple(map(str_to_int, args))
    return LRangeCommand(start=args[0], end=args[1])


def execute_rrange_command(args):
    if len(args) != 2:
        raise ValueError("invalid no. args for peek command")
    args = tuple(map(str_to_int, args))
    return RRangeCommand(start=args[0], end=args[1])


def execute_search_index_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for peek command")
    return SearchIndexCommand(args)


class LISTS_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_rrange_command(msg: Message, server):
        value = msg.conn_peer._list.rrange(msg.cmd.start, msg.cmd.end)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_lrange_command(msg: Message, server):
        value = msg.conn_peer._list.lrange(msg.cmd.start, msg.cmd.end)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_rpush_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._list.rpush(msg.cmd.item)

    @staticmethod
    def task_lpush_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._list.lpush(msg.cmd.item)

    @staticmethod
    def task_lpull_command(msg: Message, server):

        msg.conn_peer.send(f"{ msg.conn_peer._list.lpull()}".encode("utf-8"))

    @staticmethod
    def task_rpull_command(msg: Message, server):

        msg.conn_peer.send(f"{ msg.conn_peer._list.rpull()}".encode("utf-8"))

    @staticmethod
    def task_search_index_command(msg: Message, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._list.search_index(int(msg.cmd.index[0]))}".encode(
                "utf-8"
            )
        )
