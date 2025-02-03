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
    if len(args) != 1:
        raise ValueError("invalid no. args for pre order traversal command")
    return DFSCommand(args[0])


def execute_breadth_first_search_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for post order traversal command")
    return BFSCommand(args[0])


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
    if len(args) != 2:
        raise ValueError("invalid no. args for pop command")
    return AddEdgeCommand(args)


def execute_remove_edge_command(args):
    if len(args) != 2:
        raise ValueError("invalid no. args for pop command")
    return RemoveEdgeCommand(args[0], args[1])


def execute_get_edges_by_vertex_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return GetEdgesByVertexCommand(args[0])


def execute_is_weighted_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return IsWeightedCommand()


def execute_is_directed_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return IsDirectedCommand()


class GRAPH_TASKS:

    def __init__(self):
        print(self)

    @staticmethod
    def task_bfs_command(msg, server):
        value = msg.conn_peer._graph.breadth_first_search(msg.cmd.start, list())
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_dfs_command(msg, server):
        value = msg.conn_peer._graph.depth_first_search(msg.cmd.start, list())
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_add_vertex_command(msg, server):
        ic(msg.cmd.item)
        vertex = msg.conn_peer._graph.add_vertex(msg.cmd.data)

        (
            msg.conn_peer.send("OK".encode("utf-8"))
            if vertex != None
            else msg.conn_peer.send("Task Not Done".encode("utf-8"))
        )

    @staticmethod
    def task_remove_vertex_command(msg, server):
        ic(msg.cmd.item)
        msg.conn_peer._graph.remove_vertex(msg.cmd.data)
        msg.conn_peer.send("OK".encode("utf-8"))

    @staticmethod
    def task_add_edge_command(msg, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._graph.add_edge(msg.cmd.v1,msg.cmd.v2,msg.cmd.weight )}".encode(
                "utf-8"
            )
        )

    @staticmethod
    def task_remove_edge_command(msg, server):
        try:
            vertex = msg.conn_peer._graph.get_vertex_by_value(msg.cmd.v1)
            vertex.remove_edge(msg.cmd.v2)
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:

            msg.conn_peer.send("invalid Vertex data".encode("utf-8"))

    @staticmethod
    def task_get_vertex_by_value_command(msg, server):
        vertex = msg.conn_peer._graph.get_vertex_by_value(msg.cmd.data)
        if vertex != None:

            msg.conn_peer.send(f"{vertex.data}".encode("utf-8"))
        else:
            msg.conn_peer.send(f"vertex not found".encode("utf-8"))

    @staticmethod
    def task_is_directed_command(msg, server):

        msg.conn_peer.send(f"{ msg.conn_peer._graph.is_directed()}".encode("utf-8"))

    @staticmethod
    def task_is_weighted_command(msg, server):

        msg.conn_peer.send(f"{ msg.conn_peer._graph.is_weighted()}".encode("utf-8"))

    @staticmethod
    def task_display_command(msg, server):

        msg.conn_peer.send(f"{msg.conn_peer._graph.print()}".encode("utf-8"))

    @staticmethod
    def task_get_vertices_command(msg, server):

        msg.conn_peer.send(f"{msg.conn_peer._graph.get_vertices()}".encode("utf-8"))

    @staticmethod
    def task_get_edges_by_vertex_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.get_vertex_by_value(msg.cmd.data).get_edges}".encode(
                "utf-8"
            )
        )
