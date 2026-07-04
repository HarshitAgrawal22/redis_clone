from python_redis.network.Message import Message
from icecream import ic


ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class TREE_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_set_key_command(msg: Message, server):
        value = msg.conn_peer._tree.set_key(msg.cmd.key)
        msg.conn_peer.socket_handler.send(f"OK","s")

    @staticmethod
    def task_get_key_command(msg: Message, server):
        value = msg.conn_peer._tree.get_key()

        msg.conn_peer.socket_handler.send(f"{value}", "b")

    @staticmethod
    def task_upsert_node_values(msg: Message, server):
        msg.conn_peer.socket_handler.send(
            f"{msg.conn_peer._tree.upsert_node_data(msg.cmd.items)}", "s"
        )

    @staticmethod
    def task_pre_order_traversal_command(msg: Message, server):
        result_arr:list[str] =msg.conn_peer._tree.pre_order_traversal().split("\n")
        result_arr= result_arr[:-1]
        msg.conn_peer.socket_handler.send(
            result_arr , "a"
        )

    @staticmethod
    def task_post_order_traversal_command(msg: Message, server):
        result_arr=msg.conn_peer._tree.post_order_traversal().split("\n")
        result_arr= result_arr[:-1]
        msg.conn_peer.socket_handler.send(
            result_arr , "a"
        )

    @staticmethod
    def task_in_order_traversal_command(msg: Message, server):
        result_arr=msg.conn_peer._tree.in_order_traversal().split("\n")
        result_arr= result_arr[:-1]
        msg.conn_peer.socket_handler.send(
            result_arr  , "a"
        )

    @staticmethod
    def task_search_node_command(msg: Message, server):

        msg.conn_peer.socket_handler.send(
            f"{ msg.conn_peer._tree.search_node(msg.cmd.key)}", "b"
        )

    @staticmethod
    def task_insert_command(msg: Message, server):

        print(result := msg.conn_peer._tree.insert(msg.cmd.item))
        msg.conn_peer.socket_handler.send(f"{result}", "s")

    @staticmethod
    def task_display_command(msg: Message, server):
        msg.conn_peer.socket_handler.send(f"{ msg.conn_peer._tree.display()}", "b")

    @staticmethod
    def task_delete_command(msg: Message, server):
        msg.conn_peer._tree.delete(msg.cmd.key)
        msg.conn_peer.socket_handler.send(f"OK", "s")
