from icecream import ic
from python_redis.network.Message import Message

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class QUEUE_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_enqueue_command(msg :Message, server):
        ic(msg.cmd.item)
        msg.conn_peer._queue.enqueue(msg.cmd.item)
        msg.conn_peer.socket_handler.send("OK","s")

    @staticmethod
    def task_peek_command(msg:Message, server):

        msg.conn_peer.socket_handler.send(f"{msg.conn_peer._queue.peek()}","b")

    @staticmethod
    def task_display_command(msg:Message, server):
        msg.conn_peer.socket_handler.send(f"{msg.conn_peer._queue.display()}","a")

    @staticmethod
    def task_dequeue_command(msg:Message, server):
        msg.conn_peer.socket_handler.send(f"{msg.conn_peer._queue.dequeue()}","b")
