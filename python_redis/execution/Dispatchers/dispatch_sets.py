from icecream import ic
from python_redis.network.Message import Message

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class SETS_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def tesk_check_command(msg: Message, server):
        value = msg.conn_peer._sets.check(msg.cmd.item)
        msg.conn_peer.socket_handler.send(f"{value}","b")

    @staticmethod
    def task_display_command(msg: Message, server):
        value = msg.conn_peer._sets.display()
        msg.conn_peer.socket_handler.send(value.split("-"), "a")

    @staticmethod
    def task_add_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer._sets.add(msg.cmd.item)
        msg.conn_peer.socket_handler.send("OK","s")

    @staticmethod
    def task_remove_command(msg: Message, server):
        msg.conn_peer.socket_handler.send(
            f"{ msg.conn_peer._sets.remove(msg.cmd.item)}", "s"
        )
