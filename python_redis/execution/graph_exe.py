# TODO: rename all files as they perform
from python_redis.protocols.graph_protocols import *


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
