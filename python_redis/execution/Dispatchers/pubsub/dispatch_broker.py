from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING :
    from python_redis.network import Server, Message
class PUBSUB_TASKS:
    pass

    @staticmethod
    def task_subscribe(msg:Message, server:Server):
        pass
    @staticmethod
    def task_unsubscribe(msg: Message, server: Server):
        pass
    @staticmethod
    def task_publish(msg: Message, server: Server):
        pass