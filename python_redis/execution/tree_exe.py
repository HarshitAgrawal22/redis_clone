from python_redis.protocols.bst_protocols import *


def execute_insert_command(args):
    if len(args) <= 0:
        raise ValueError("not enough args")
    return InsertCommand(args)


def execute_upsert_key_val_command(args):
    if len(args) < 3:
        raise ValueError("Not Enough Argument to perform upsert node operation")
    return UpsertCommand(args[0], args[1:])


def execute_search_command(args):
    if len(args) <= 0:
        raise ValueError("not enough Arguments to process")
    return SearchCommand(args[0])


def execute_pre_order_traversal_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pre order traversal command")
    return PreOrderTraversalCommand()


def execute_post_order_traversal_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for post order traversal command")
    return PostOrderTraversalCommand()


def execute_in_order_traversal_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for in order traversal command")
    return InOrderTraversalCommand()


def execute_display_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for push command")
    return DisplayCommand()


def execute_delete_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return DeleteCommand(args[0])


def execute_set_command(args):
    if len(args) != 1:
        raise ValueError("invalid no. args for pop command")
    return SetKeyCommand(args[0])


def execute_get_command(args):
    if len(args) != 0:
        raise ValueError("invalid no. args for pop command")
    return GetKeyCommand()
