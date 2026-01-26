from icecream import ic
from python_redis.network.Message import Message

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class QUEUE_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_enqueue_command(msg, server):
        ic(msg.cmd.item)
        msg.conn_peer.send("OK".encode("utf-8"))
        return msg.conn_peer._queue.enqueue(msg.cmd.item)

    @staticmethod
    def task_peek_command(msg, server):

        msg.conn_peer.send(f"{msg.conn_peer._queue.peek()}".encode("utf-8"))

    @staticmethod
    def task_display_command(msg, server):
        msg.conn_peer.send(f"{msg.conn_peer._queue.display()}".encode("utf-8"))

    @staticmethod
    def task_dequeue_command(msg, server):
        msg.conn_peer.send(f"{msg.conn_peer._queue.dequeue()}".encode("utf-8"))
