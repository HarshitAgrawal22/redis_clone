from typing import Union
from icecream import ic
from .command import Command


ic.configureOutput(prefix="DEBUG: ", includeContext=True)

COMMAND_INSERT = "tins"
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


class GetCommand(Command):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"data to get is {self.key}"


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


class PreOrderTraversalCommand(Command):
    def __init__(self, data):
        print(f"data got is {data}")

    def __str__(self):
        return f"got order to print preorder traversal"


class PostOrderTraversalCommand(Command):
    def __init__(self, data):
        print(f"data got is {data}")

    def __str__(self):
        return f"got order to print postorder traversal"


class InOrderTraversalCommand(Command):
    def __init__(self, data):
        print(f"data got is {data}")

    def __str__(self):
        return f"got order to print inorder traversal"


class PostOrderTraversalCommand(Command):
    def __init__(self, data):
        print(f"data got is {data}")

    def __str__(self):
        return f"got order to print whole tree"


def execute_insert_command(args):
    if len(args) <= 0:
        raise ValueError("not enough ")
    return InsertCommand(args)


def execute_get_command(args):
    pass
