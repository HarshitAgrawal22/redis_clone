from icecream import ic
from python_redis.network.Message import Message

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class STACK_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_push_command(msg: Message, server):
        ic(msg.cmd.item)
        msg.conn_peer._stack.push(msg.cmd.item)
        msg.conn_peer.socket_handler.send("OK","s")

    @staticmethod
    def task_pop_command(msg: Message, server):
        value = msg.conn_peer._stack.pop()
        msg.conn_peer.socket_handler.send(f"{value}", "s")

    @staticmethod
    def task_peek_command(msg: Message, server):
        msg.conn_peer.socket_handler.send(f"{msg.conn_peer._stack.peek()}", "b")
