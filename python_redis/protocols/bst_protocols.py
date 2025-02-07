from typing import Union
from icecream import ic
from .command import Command


ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_INSERT = "tins"
COMMAND_SET = "tset"
COMMAND_GET = "tget"
COMMAND_SEARCH = "tlook"
COMMAND_DELETE = "tdel"
COMMAND_PRE_ORDER = "tpre"
COMMAND_POST_ORDER = "tpost"
COMMAND_IN_ORDER = "tin"
COMMAND_SHOW = "tshow"


class InsertCommand(Command):
    def __init__(self, data):
        self.item: tuple = data

    def __str__(self):
        return f"data for insertion is {self.item}"


class DisplayCommand(Command):
    def __init__(self):
        print("got command to display tree")


class SearchCommand(Command):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"data to search {self.key}"


class DeleteCommand(Command):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"data to delete is {self.key}"


class SetKeyCommand(Command):
    def __init__(self, key):
        self.key = key


class GetKeyCommand(Command):
    def __init__(self):
        print("got command to get key ")


class PreOrderTraversalCommand(Command):
    def __init__(self):
        print("got command for pre order ")

    def __str__(self):
        return f"got order to print preorder traversal"


class PostOrderTraversalCommand(Command):
    def __init__(self):
        print("got command for post order ")

    def __str__(self):
        return f"got order to print postorder traversal"


class InOrderTraversalCommand(Command):
    def __init__(self):
        print("got command for in order ")

    def __str__(self):
        return f"got order to print inorder traversal"


def execute_insert_command(args):
    if len(args) <= 0:
        raise ValueError("not enough args")
    return InsertCommand(args)


def execute_search_command(args):
    if len(args) <= 0:
        raise ValueError("not enough ")
    return SearchCommand(args[0])


def execute_pre_order_traversal_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pre order traversal command")
    return PreOrderTraversalCommand()


def execute_post_order_traversal_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for post order traversal command")
    return PostOrderTraversalCommand()


def execute_in_order_traversal_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for in order traversal command")
    return InOrderTraversalCommand()


def execute_display_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for push command")
    return DisplayCommand()


def execute_delete_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return DeleteCommand(args[0])


def execute_set_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return SetKeyCommand(args)


def execute_get_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return GetKeyCommand()


class TREE_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_set_key_command(msg, server):
        value = msg.conn_peer._tree.set_key(msg.cmd.key)
        msg.conn_peer.send(f"OK".encode("utf-8"))

    @staticmethod
    def task_get_key_command(msg, server):
        value = msg.conn_peer._tree.get_key()

        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_pre_order_traversal_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._tree.pre_order_traversal()}".encode("utf-8")
        )

    @staticmethod
    def task_post_order_traversal_command(msg, server):
        msg.conn_peer.send(
            f"{msg.conn_peer._tree.post_order_traversal()}".encode("utf-8")
        )

    @staticmethod
    def task_in_order_traversal_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._tree.in_order_traversal()}".encode("utf-8")
        )

    @staticmethod
    def task_search_node_command(msg, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._tree.search_node(msg.cmd.key)}".encode("utf-8")
        )

    @staticmethod
    def task_insert_command(msg, server):

        print(result := msg.conn_peer._tree.insert(msg.cmd.item))
        msg.conn_peer.send(f"{result}".encode("utf-8"))

    @staticmethod
    def task_display_command(msg, server):
        msg.conn_peer.send(f"{ msg.conn_peer._tree.display()}".encode("utf-8"))

    @staticmethod
    def task_delete_command(msg, server):
        msg.conn_peer._tree.delete(msg.cmd.key)
        msg.conn_peer.send(f"OK".encode("utf-8"))
