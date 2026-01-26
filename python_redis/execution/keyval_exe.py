from python_redis.protocols.keyval_protocol import *


def execute_set_command(args):
    if len(args) != 2:
        raise ValueError("Invalid number of arguments for SET command")
    key, value = args
    # print(f"setting {key} { value}")
    return SetCommand(key, value)


def execute_unknown_command(args):
    return UnknownCommand(args)


def execute_get_command(args):
    if len(args) != 1:
        print(f"{args} = args")
        raise ValueError("Invalid number of arguments for GET command")
    key = args[0]
    return GetCommand(key)


def execute_kill_command(args):
    if len(args) != 0:
        raise ValueError("Invalid number of arguments for kill command")
    return KillCommand()


def execute_quit_command(args):
    if len(args) != 0:
        print(f"{args} are args for quitting server")
        raise ValueError("Invalid number of arguments for GET command")

    return QuitCommand(want_to_quit=True)


def execute_hello_command(args):
    if len(args) != 1:
        raise ValueError("Invalid number of arguments for SET command")
    return HelloCommand(args[0])


def execute_check_command(args):
    if len(args) >= 1:
        return CheckCommand(args)
    raise ValueError("No arguments given for CHECK command")


def execute_client_command(args):
    if len(args) == 0:
        raise ValueError("No arguments for CLIENT command")
    return ClientCommand(args[0])


def execute_delete_command(args):
    if len(args) == 0:
        raise ValueError("No key given for DELETE command")

    return DeleteCommand(args[0])


def execute_get_multiple_values_command(args):
    if len(args) == 0:
        raise ValueError("No key given to get value")
    return GetMultipleKeyValCommand(args)


def execute_incry_command(args):
    if len(args) == 0:
        raise ValueError("No key for INCREMENT command")
    return IncrementCommand(args[0])


def execute_total_command(args):
    return TotalCommand("return total")


def execute_multiple_attrs_set_command(args):
    if len(args) == 0:
        raise ValueError("No argument for SET MULTIPLE ATTRIBUTE command")
    key: str = args[0]
    attrs: tuple = args[1:]

    return SetMultipleAttributeCommand(key=key, attrs=attrs)


def execute_multiple_attrs_get_command(args):
    if len(args) == 0:
        raise ValueError("No argument for SET MULTIPLE ATTRIBUTE command")
    key: str = args[0]
    attrs: tuple = args[1:]

    return GetMultipleAttributeCommand(key=key, attrs=attrs)


def execute_set_multi_key_val_command(args):
    if len(args) == 0:
        raise ValueError("No arguments given for SET MULTIPLE KEY VALUE PAIRS")
    if len(args) % 2 != 0:
        raise ValueError("Invalid Key Value pairs")
    return SetMultipleKeyValCommand(args)
