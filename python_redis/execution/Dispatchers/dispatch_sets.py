from icecream import ic
from python_redis.network.Message import Message

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class SETS_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def tesk_check_command(msg: Message, server):
        value = msg.conn_peer._sets.check(msg.cmd.item)
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_display_command(msg: Message, server):
        value = msg.conn_peer._sets.display()
        msg.conn_peer.send(f"{value}".encode("utf-8"))

    @staticmethod
    def task_add_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._sets.add(msg.cmd.item)

    @staticmethod
    def task_remove_command(msg: Message, server):
        msg.conn_peer.send(
            f"{ msg.conn_peer._sets.remove(msg.cmd.item)}".encode("utf-8")
        )
