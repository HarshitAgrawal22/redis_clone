from __future__ import annotations
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from python_redis.common import Message
from typing import Union
from icecream import ic
from .command import Command

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_PUSH = "spush"  # push a element to the stack
COMMAND_POP = "spop"  # pop a element from the stack
COMMAND_PEEK = "speek"  # will show the element which will be poped next


class PushCommand(Command):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return f"{self.item} is pushed to the stack"


class PopCommand(Command):
    def __init__(self):
        print("commanded to pop a item from stack ")


class PeekCommand(Command):
    def __init__(self):
        print("got the command to peek ")


def execute_push_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return PushCommand(args[0])


def execute_pop_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return PopCommand()


def execute_peek_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return PeekCommand()


class STACK_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_push_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._stack.push(msg.cmd.item)

    @staticmethod
    def task_pop_command(msg: Message, server):
        value = msg.conn_peer._stack.pop()
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_peek_command(msg: Message, server):
        msg.conn_peer.send(f"{msg.conn_peer._stack.peek()}".encode("utf-8"))
