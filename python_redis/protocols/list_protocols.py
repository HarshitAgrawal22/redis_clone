from .command import Command
from icecream import ic

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
