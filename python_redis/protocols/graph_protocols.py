import re
from typing import Union
from icecream import ic
from .command import Command

# from main import Message, Server

ic.configureOutput(prefix="DEBUG: ", includeContext=True)
COMMAND_BFS = "gbfs"
COMMAND_DFS = "gdfs"
COMMAND_ADD_VERTEX = "gaddv"
COMMAND_ADD_EDGE = "gadde"
COMMAND_REMOVE_EDGE = "greme"
COMMAND_REMOVE_VERTEX = "gremv"
COMMAND_IS_DIRECTED = "gisdir"
COMMAND_IS_WEIGHTED = "gisweig"
COMMAND_SHOW = "gshow"
COMMAND_GET_VERTEX_BY_VALUE = "ggetvv"
COMMAND_GET_VERTICES = "ggetv"


class BFSCommand(Command):
    def __init__(self):
        print("got command to bfs")

    def __str__(self):
        return "got command for bfs"


class DFSCommand(Command):
    def __init__(self):
        print("got command to dfs")

    def __str__(self):
        return "got command for dfs"


class AddVertexCommand(Command):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)


class AddEdgeCommand(Command):
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight


class RemoveEdgeCommand(Command):
    def __init__(self, v1, v2):

        self.v1 = v1

        self.v2 = v2


class RemoveVertexCommand(Command):
    def __init__(self, data):
        self.data = data


class IsDirectedCommand(Command):
    def __init__(self):
        pass


class IsWeightedCommand(Command):
    def __init__(self):
        pass


class ShowCommand(Command):
    def __init__(self):
        pass


class GetVertexCommand(Command):
    def __init__(self, data):
        self.data = data


class GetVerticesCommand(Command):
    def __init__(self):
        pass
