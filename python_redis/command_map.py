from services import (
    command_bst,
    command_stack,
    command_dict,
    command_queue,
    command_sets,
)

execute_task_hash_map = {
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
}
