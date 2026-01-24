from __future__ import annotations
from typing import Union, TYPE_CHECKING
from icecream import ic
from .command import Command


if TYPE_CHECKING:
    from python_redis.common import Message

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class RemoveCommand(Command):
    def __init__(self, item):
        self.item = item


class AddCommand(Command):
    def __init__(self, item):
        self.item = item


class DisplayCommand(Command):
    def __init__(self):
        print("got the command to display items")


class CheckCommand(Command):
    def __init__(self, item):
        self.item = item


def execute_add_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return AddCommand(args[0])


def execute_check_command(args):
    if len(args) < 1:
        raise ValueError("invalid no. args for check command")
    return CheckCommand(args)


def execute_remove_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return RemoveCommand(args[0])


def execute_display_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return DisplayCommand()


class SETS_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def tesk_check_command(msg: Message, server):
        value = msg.conn_peer._sets.check(msg.cmd.item)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_display_command(msg: Message, server):
        value = msg.conn_peer._sets.display()
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_add_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._sets.add(msg.cmd.item)

    @staticmethod
    def task_remove_command(msg: Message, server):
        msg.conn_peer.send(
            f"{ msg.conn_peer._sets.remove(msg.cmd.item)}".encode("utf-8")
        )
