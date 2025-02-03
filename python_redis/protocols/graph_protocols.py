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
COMMAND_GET_VERTEX_EDGE = "ggetved"


class BFSCommand(Command):  #
    def __init__(self):
        print("got command to bfs")

    def __str__(self):
        return "got command for bfs"


class DFSCommand(Command):  #
    def __init__(self):
        print("got command to dfs")

    def __str__(self):
        return "got command for dfs"


class AddVertexCommand(Command):  #
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


class RemoveVertexCommand(Command):  #
    def __init__(self, data):
        self.data = data


class IsDirectedCommand(Command):
    def __init__(self):
        pass


class IsWeightedCommand(Command):
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


class GetEdgesByVertexCommand(Command):
    def __init__(self, data):
        self.data = data


def execute_add_vertex_command(args):
    if len(args) <= 0:
        raise ValueError("not enough args")
    return AddVertexCommand(args)


def execute_get_vertex_by_value_command(args):
    if len(args) != 1:
        raise ValueError("not enough arguments")
    return GetVertexCommand(args[0])


def execute_depth_first_search_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pre order traversal command")
    return DFSCommand()


def execute_breadth_first_search_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for post order traversal command")
    return BFSCommand()


def execute_get_vertices_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for in order traversal command")
    return GetVerticesCommand()


def execute_display_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for push command")
    return DisplayCommand()


def execute_remove_vertex_by_value_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return RemoveVertexCommand(args[0])


def execute_add_edge_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return SetKeyCommand(args)


def execute_get_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return GetKeyCommand()


class GRAPH_TASKS:

    def __init__(self):
        print(self)

    @staticmethod
    def task_bfs_command(msg, server):
        value = msg.conn_peer._list.rrange(msg.cmd.start, msg.cmd.end)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_dfs_command(msg, server):
        value = msg.conn_peer._list.lrange(msg.cmd.start, msg.cmd.end)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_add_vertex_command(msg, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._list.rpush(msg.cmd.item)

    @staticmethod
    def task_remove_vertex_command(msg, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._list.lpush(msg.cmd.item)

    @staticmethod
    def task_add_edge_command(msg, server):

        msg.conn_peer.send(f"{ msg.conn_peer._list.lpull()}".encode("utf-8"))

    @staticmethod
    def task_remove_edge_command(msg, server):

        msg.conn_peer.send(f"{ msg.conn_peer._list.rpull()}".encode("utf-8"))

    @staticmethod
    def task_search_vertex_by_value_command(msg, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._list.search_index(int(msg.cmd.index[0]))}".encode(
                "utf-8"
            )
        )
