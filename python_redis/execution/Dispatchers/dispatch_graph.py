from python_redis.network.Message import Message
from icecream import ic


ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class GRAPH_TASKS:

    @staticmethod
    def task_set_key_command(msg: Message, server):
        value = msg.conn_peer._graph.set_key_name(msg.cmd.key)
        msg.conn_peer.socket_handler.send(f"{value}", "s")

    @staticmethod
    def task_get_key_command(msg: Message, server):
        value = msg.conn_peer._graph.get_key_name()
        msg.conn_peer.socket_handler.send(f"{value}", "s")

    @staticmethod
    def task_bfs_command(msg: Message, server):
        value = msg.conn_peer._graph.breadth_first_search(msg.cmd.start, list())
        ic(value)
        msg.conn_peer.socket_handler.send(f"{value}", 's')

    @staticmethod
    def task_dfs_command(msg: Message, server):
        value = msg.conn_peer._graph.depth_first_search(msg.cmd.start, list())
        msg.conn_peer.socket_handler.send(f"{value}", "b")

    @staticmethod
    def task_add_vertex_command(msg: Message, server):

        vertex = msg.conn_peer._graph.add_vertex(msg.cmd.data)

        (
            msg.conn_peer.socket_handler.send("OK", "s")
            if vertex != None
            else msg.conn_peer.socket_handler.send("Task Not Done", "s")
        )

    @staticmethod
    def task_remove_vertex_command(msg: Message, server):

        (
            msg.conn_peer.socket_handler.send("OK","s")
            if msg.conn_peer._graph.remove_vertex(msg.cmd.data)
            else msg.conn_peer.socket_handler.send("Task Not Done","s")
        )

    @staticmethod
    def task_add_edge_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{msg.conn_peer._graph.add_edge(msg.cmd.v1, msg.cmd.v2, msg.cmd.weight)}","s"
        )

    @staticmethod
    def task_remove_edge_command(msg: Message, server):
        try:
            msg.conn_peer._graph.remove_edge(msg.cmd.v1, msg.cmd.v2)

            msg.conn_peer.socket_handler.send("OK", "s")
        except Exception as e:
            print(e)
            msg.conn_peer.socket_handler.send("invalid Vertex data", "e")

    @staticmethod
    def task_get_vertex_by_value_command(msg: Message, server):
        vertex = msg.conn_peer._graph.get_vertex_by_value(msg.cmd.data)
        
        if vertex != None:
            msg.conn_peer.socket_handler.send(f"{vertex.data}", "b")
        else:
            msg.conn_peer.socket_handler.send(f"vertex not found", "e")

    @staticmethod
    def task_is_directed_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{ msg.conn_peer._graph.is_directed_graph()}", "s"
        )

    @staticmethod
    def task_is_weighted_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{ msg.conn_peer._graph.is_weighted_graph()}", "s"
        )

    @staticmethod
    def task_display_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(f"{msg.conn_peer._graph.print()}", "b") 
    @staticmethod
    def task_get_vertices_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(f"{msg.conn_peer._graph.get_vertices_str()}", "b")

    @staticmethod
    def task_get_edges_by_vertex_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{msg.conn_peer._graph.get_vertex_by_value(msg.cmd.data).get_edges()}", "b"
        )

    @staticmethod
    def task_dijkistra_prev_dict_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{msg.conn_peer._graph.dijkistra_prev(msg.cmd.start)}", "b"
        )

    @staticmethod
    def task_dijkistra_dist_dict_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{msg.conn_peer._graph.dijkistra_distance(msg.cmd.start)}"
        ,"b" )

    @staticmethod
    def task_dijkistra_shortest_path_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{msg.conn_peer._graph.dijkistra_shortest_distance(msg.cmd.start,msg.cmd.end )}","b"
        )
