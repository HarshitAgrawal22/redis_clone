from python_redis.services import (
    # command_bst,
    # command_graph,
    command_stack,
    command_dict,
    command_queue,
    command_sets,
    command_lists,
)
from python_redis.protocols.command import Command


class Message:
    def __init__(self, cmd: bytearray, conn_peer):
        # this is the peer from/to this message is sent/received
        self.conn_peer = conn_peer
        self.cmd: Command = cmd

    def __str__(self):
        return f"conn_peer:{self.conn_peer}     cmd:{self.cmd}"


execute_task_hash_map = {
    **command_lists.execute_task_list,
    **command_dict.execute_task_hash_map,
    **command_stack.execute_task_stack,
    **command_queue.execute_task_queue,
    **command_sets.execute_task_sets,
}
execute_command_hash_map = {
    **command_dict.execute_command_hash_map,
    **command_stack.execute_command_stack,
    **command_queue.execute_command_queue,
    **command_sets.execute_command_sets,
    **command_lists.execute_command_list,
}
