from python_redis.protocols.stack_protocols import *


def execute_push_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return PushCommand(args[0])


def execute_pop_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return PopCommand()


def execute_peek_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return PeekCommand()
