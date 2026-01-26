# from typing import Union
from .command import Command
from icecream import ic


ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class InsertCommand(Command):
    def __init__(self, data):
        self.item: tuple = data

    def __str__(self):
        return f"data for insertion is {self.item}"


class UpsertCommand(Command):
    def __init__(self, key, itemspairs):
        self.key = key
        self.items = itemspairs

    def __str__(self):
        return f"Got Data for Upsertion"


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
