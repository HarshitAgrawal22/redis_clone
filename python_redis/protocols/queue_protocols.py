import re
from typing import Union
from icecream import ic
from .command import Command

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


COMMAND_DISPLAY = "qdisp"

COMMAND_DEQUEUE = "qdeq"

COMMAND_PEEK = "qpeek"
COMMAND_ENQUEUE = "qenq"


class DisplayCommand(Command):
    def __init__(self):
        print("got the command to display")


class DequeueCommand(Command):
    def __init__(self):
        print("got command to dequeue")


class PeekCommand(Command):
    def __init__(self):
        print("got command to dequeue")

    def __str__(self) -> str:
        return self.id


class EnqueueCommand(Command):
    def __init__(self, item):
        self.item = item

    def __str__(self) -> str:
        return self.id


def execute_enqueue_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return EnqueueCommand(args[0])


def execute_dequeue_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return DequeueCommand()


def execute_display_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return DisplayCommand()


def execute_peek_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return PeekCommand()


class QUEUE_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_enqueue_command(msg, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._queue.enqueue(msg.cmd.item)

    @staticmethod
    def task_peek_command(msg, server):

        msg.conn_peer.send(f"{msg.conn_peer._queue.peek()}".encode("utf-8"))

    @staticmethod
    def task_display_command(msg, server):
        msg.conn_peer.send(f"{msg.conn_peer._queue.display()}".encode("utf-8"))

    @staticmethod
    def task_dequeue_command(msg, server):
        msg.conn_peer.send(f"{msg.conn_peer._queue.dequeue()}".encode("utf-8"))
