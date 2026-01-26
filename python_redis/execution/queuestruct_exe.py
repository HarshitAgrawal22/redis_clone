from python_redis.protocols.queue_protocols import *


def execute_enqueue_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return EnqueueCommand(args[0])


def execute_dequeue_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return DequeueCommand()


def execute_display_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return DisplayCommand()


def execute_peek_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return PeekCommand()
