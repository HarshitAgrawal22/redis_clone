from icecream import ic
from .command import Command


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
