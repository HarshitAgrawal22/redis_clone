from typing import Union
from icecream import ic
from .command import Command

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_ADD = "fadd"
COMMAND_REMOVE = "frem"

COMMAND_DISPLAY = "fmem"


class RemoveCommand(Command):
    def __init__(self, item):
        self.item = item


class AddCommand(Command):
    def __init__(self, item):
        self.item = item


class DisplayCommand(Command):
    def __init__(self):
        print("got the command to display items")


def execute_add_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return AddCommand(args[0])


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
    def task_display_command(msg, server):
        value = msg.conn_peer._sets.display()
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_add_command(msg, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._sets.add(msg.cmd.item)

    @staticmethod
    def task_remove_command(msg, server):
        msg.conn_peer.send(
            f"{ msg.conn_peer._sets.remove(msg.cmd.item)}".encode("utf-8")
        )
