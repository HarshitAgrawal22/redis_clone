from python_redis.network.Message import Message
from icecream import ic


ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class GRAPH_TASKS:

    def __init__(self):
        print(self)

    @staticmethod
    def task_set_key_command(msg: Message, server):
        value = msg.conn_peer._graph.set_key_name(msg.cmd.key)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_get_key_command(msg: Message, server):
        value = msg.conn_peer._graph.get_key_name()
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_bfs_command(msg: Message, server):
        value = msg.conn_peer._graph.breadth_first_search(msg.cmd.start, list())
        ic(value)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_dfs_command(msg: Message, server):
        value = msg.conn_peer._graph.depth_first_search(msg.cmd.start, list())
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_add_vertex_command(msg: Message, server):

        vertex = msg.conn_peer._graph.add_vertex(msg.cmd.data)

        (
            msg.conn_peer.send("OK".encode("utf-8"))
            if vertex != None
            else msg.conn_peer.send("Task Not Done".encode("utf-8"))
        )

    @staticmethod
    def task_remove_vertex_command(msg: Message, server):

        (
            msg.conn_peer.send("OK".encode("utf-8"))
            if msg.conn_peer._graph.remove_vertex(msg.cmd.data)
            else msg.conn_peer.send("Task Not Done".encode("utf-8"))
        )

    @staticmethod
    def task_add_edge_command(msg: Message, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.add_edge(msg.cmd.v1, msg.cmd.v2, msg.cmd.weight)}".encode(
                "utf-8"
            )
        )

    @staticmethod
    def task_remove_edge_command(msg: Message, server):
        try:
            msg.conn_peer._graph.remove_edge(msg.cmd.v1, msg.cmd.v2)

            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(e)
            msg.conn_peer.send("invalid Vertex data".encode("utf-8"))

    @staticmethod
    def task_get_vertex_by_value_command(msg: Message, server):
        vertex = msg.conn_peer._graph.get_vertex_by_value(msg.cmd.data)
        if vertex != None:

            msg.conn_peer.send(f"{vertex.data}".encode("utf-8"))
        else:
            msg.conn_peer.send(f"vertex not found".encode("utf-8"))

    @staticmethod
    def task_is_directed_command(msg: Message, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._graph.is_directed_graph()}".encode("utf-8")
        )

    @staticmethod
    def task_is_weighted_command(msg: Message, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._graph.is_weighted_graph()}".encode("utf-8")
        )

    @staticmethod
    def task_display_command(msg: Message, server):

        msg.conn_peer.send(f"{msg.conn_peer._graph.print()}".encode("utf-8"))

    @staticmethod
    def task_get_vertices_command(msg: Message, server):

        msg.conn_peer.send(f"{msg.conn_peer._graph.get_vertices_str()}".encode("utf-8"))

    @staticmethod
    def task_get_edges_by_vertex_command(msg: Message, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.get_vertex_by_value(msg.cmd.data).get_edges()}".encode(
                "utf-8"
            )
        )

    @staticmethod
    def task_dijkistra_prev_dict_command(msg: Message, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.dijkistra_prev(msg.cmd.start)}".encode("utf-8")
        )

    @staticmethod
    def task_dijkistra_dist_dict_command(msg: Message, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.dijkistra_distance(msg.cmd.start)}".encode("utf-8")
        )

    @staticmethod
    def task_dijkistra_shortest_path_command(msg: Message, server):

        msg.conn_peer.send(
            f"{msg.conn_peer._graph.dijkistra_shortest_distance(msg.cmd.start,msg.cmd.end )}".encode(
                "utf-8"
            )
        )
