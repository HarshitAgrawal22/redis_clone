from icecream import ic
from .command import Command
from ..common import Message

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_RPUSH = "rpush"
COMMAND_LPUSH = "lpush"
COMMAND_LPULL = "lpull"
COMMAND_RPULL = "rpull"
COMMAND_LRANGE = "lrang"
COMMAND_SEARCH_INDEX = "si"
COMMAND_RRANGE = "rrang"


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
    return RPushCommand(args[0])


def execute_rpull_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return RPullCommand(args[0])


def execute_lpull_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return LPullCommand(args[0])


def execute_lrange_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return LRangeCommand(args)


def execute_rrange_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return RRangeCommand(args)


def execute_search_index_command(args):
    if len(args) != 0:
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
    def task_rpush_command(msg, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._list.rpush(msg.cmd.item)

    @staticmethod
    def task_remove_command(msg, server):
        msg.conn_peer.send(
            f"{ msg.conn_peer._sets.remove(msg.cmd.item)}".encode("utf-8")
        )
