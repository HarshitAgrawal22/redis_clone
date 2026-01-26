from icecream import ic
from python_redis.network.Message import Message

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class LISTS_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_rrange_command(msg: Message, server):
        value = msg.conn_peer._list.rrange(msg.cmd.start, msg.cmd.end)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_lrange_command(msg: Message, server):
        value = msg.conn_peer._list.lrange(msg.cmd.start, msg.cmd.end)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_rpush_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._list.rpush(msg.cmd.item)

    @staticmethod
    def task_lpush_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._list.lpush(msg.cmd.item)

    @staticmethod
    def task_lpull_command(msg: Message, server):

        msg.conn_peer.send(f"{ msg.conn_peer._list.lpull()}".encode("utf-8"))

    @staticmethod
    def task_rpull_command(msg: Message, server):

        msg.conn_peer.send(f"{ msg.conn_peer._list.rpull()}".encode("utf-8"))

    @staticmethod
    def task_search_index_command(msg: Message, server):

        msg.conn_peer.send(
            f"{ msg.conn_peer._list.search_index(int(msg.cmd.index[0]))}".encode(
                "utf-8"
            )
        )
