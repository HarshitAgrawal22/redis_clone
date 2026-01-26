from python_redis.protocols.list_protocols import *


def execute_rpush_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return RPushCommand(args[0])


def execute_lpush_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return LPushCommand(args[0])


def execute_rpull_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return RPullCommand()


def execute_lpull_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return LPullCommand()


def execute_lrange_command(args):
    if len(args) != 2:
        raise ValueError("invalid no. args for peek command")
    args = tuple(map(str_to_int, args))
    return LRangeCommand(start=args[0], end=args[1])


def execute_rrange_command(args):
    if len(args) != 2:
        raise ValueError("invalid no. args for peek command")
    args = tuple(map(str_to_int, args))
    return RRangeCommand(start=args[0], end=args[1])


def execute_search_index_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for peek command")
    return SearchIndexCommand(args)
