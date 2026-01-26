from python_redis.protocols.sets_protocols import *


def execute_add_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for push command")
    return AddCommand(args[0])


def execute_check_command(args):
    if len(args) < 1:
        raise ValueError("invalid no. args for check command")
    return CheckCommand(args)


def execute_remove_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return RemoveCommand(args[0])


def execute_display_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for peek command")
    return DisplayCommand()
