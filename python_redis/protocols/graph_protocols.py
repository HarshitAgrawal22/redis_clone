from icecream import ic
from .command import Command


class DijkistraShortestPathCommand(Command):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start}"


class DijkistraPrevDictionaryCommand(Command):
    def __init__(self, start):
        self.start = start

    def __str__(self):
        return f"{self.start}"


class DijkistraDistDictionaryCommand(Command):
    def __init__(self, start):
        self.start = start

    def __str__(self):
        return f"{self.start}"


class SetKeyCommand(Command):  #
    def __init__(self, key):
        self.key = key


class GetKeyCommand(Command):  #
    def __init__(self):
        print("Got command for getting key")


class BFSCommand(Command):  #
    def __init__(self, start):
        self.start = start

    def __str__(self):
        return "got command for bfs"


class DFSCommand(Command):  #
    def __init__(self, start):
        self.start = start

    def __str__(self):
        return "got command for dfs"


class AddVertexCommand(Command):  #
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)


class AddEdgeCommand(Command):  #
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight


class RemoveEdgeCommand(Command):  #
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2


class RemoveVertexCommand(Command):  #
    def __init__(self, data):
        self.data = data


class IsDirectedCommand(Command):  #
    def __init__(self):
        pass


class IsWeightedCommand(Command):  #
    def __init__(self):
        pass


class DisplayCommand(Command):  #
    def __init__(self):
        pass


class GetVertexCommand(Command):  #
    def __init__(self, data):
        self.data = data


class GetVerticesCommand(Command):  #
    def __init__(self):
        pass


class GetEdgesByVertexCommand(Command):  #
    def __init__(self, data):
        self.data = data
