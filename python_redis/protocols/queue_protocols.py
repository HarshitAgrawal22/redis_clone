from icecream import ic
from .command import Command

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


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
