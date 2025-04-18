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
COMMAND_SET_KEY = "gsetk"
COMMAND_GET_KEY = "ggetk"
COMMAND_DIJKISTRA_DIST_DICT = "gdijdis"
COMMAND_DIJKISTRA_PREV_DICT = "gdijprev"
COMMAND_DIJKISTRA_SHORTEST_PATH = "gdijpa"


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


def execute_dij_shortest_path_command(args):
    if len(args) != 2:
        raise ValueError("wrong no. of args")
    return DijkistraShortestPathCommand(*args)


def execute_dij_dist_dict_command(args):
    if len(args) != 1:
        raise ValueError("wrong no. of args")
    return DijkistraDistDictionaryCommand(args[0])


def execute_dij_prev_dict_command(args):
    if len(args) != 1:
        raise ValueError("wrong no. of args")
    return DijkistraPrevDictionaryCommand(args[0])


def execute_set_key_command(args):
    if len(args) != 1:
        raise ValueError("not enough args")
    return SetKeyCommand(args[0])


def execute_get_key_command(args):
    if len(args) != 0:
        raise ValueError("not enough args")
    return GetKeyCommand()


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
    if len(args) != 3:
        raise ValueError("invalid no. args for add edge command")
    return AddEdgeCommand(*args)


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
    def task_set_key_command(msg, server):
        value = msg.conn_peer._graph.set_key_name(msg.cmd.key)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_get_key_command(msg, server):
        value = msg.conn_peer._graph.get_key_name()
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_bfs_command(msg, server):
        value = msg.conn_peer._graph.breadth_first_search(msg.cmd.start, list())
        ic(value)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_dfs_command(msg, server):
        value = msg.conn_peer._graph.depth_first_search(msg.cmd.start, list())
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_add_vertex_command(msg, server):

        vertex = msg.conn_peer._graph.add_vertex(msg.cmd.data)

        (
            msg.conn_peer.send("OK".encode("utf-8"))
            if vertex != None
            else msg.conn_peer.send("Task Not Done".encode("utf-8"))
        )

    @staticmethod
    def task_remove_vertex_command(msg, server):

        (
            msg.conn_peer.send("OK".encode("utf-8"))
            if msg.conn_peer._graph.remove_vertex(msg.cmd.data)
            else msg.conn_peer.send("Task Not Done".encode("utf-8"))
        )

    @staticmethod
    def task_add_edge_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.add_edge(msg.cmd.v1, msg.cmd.v2, msg.cmd.weight)}".encode(
                "utf-8"
            )
        )

    @staticmethod
    def task_remove_edge_command(msg, server):
        try:
            msg.conn_peer._graph.remove_edge(msg.cmd.v1, msg.cmd.v2)

            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(e)
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

        msg.conn_peer.send(
            f"{ msg.conn_peer._graph.is_directed_graph()}".encode("utf-8")
        )

    @staticmethod
    def task_is_weighted_command(msg, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._graph.is_weighted_graph()}".encode("utf-8")
        )

    @staticmethod
    def task_display_command(msg, server):

        msg.conn_peer.send(f"{msg.conn_peer._graph.print()}".encode("utf-8"))

    @staticmethod
    def task_get_vertices_command(msg, server):

        msg.conn_peer.send(f"{msg.conn_peer._graph.get_vertices_str()}".encode("utf-8"))

    @staticmethod
    def task_get_edges_by_vertex_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.get_vertex_by_value(msg.cmd.data).get_edges()}".encode(
                "utf-8"
            )
        )

    @staticmethod
    def task_dijkistra_prev_dict_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.dijkistra_prev(msg.cmd.start)}".encode("utf-8")
        )

    @staticmethod
    def task_dijkistra_dist_dict_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.dijkistra_distance(msg.cmd.start)}".encode("utf-8")
        )

    @staticmethod
    def task_dijkistra_shortest_path_command(msg, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.dijkistra_shortest_distance(msg.cmd.start,msg.cmd.end )}".encode(
                "utf-8"
            )
        )
