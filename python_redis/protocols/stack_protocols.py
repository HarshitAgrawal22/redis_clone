from icecream import ic
from .command import Command

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


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
