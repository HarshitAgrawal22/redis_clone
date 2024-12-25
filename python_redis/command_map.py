from services import command_bst, command_stack, command_dict

execute_task_hash_map = {
    **command_dict.execute_task_hash_map,
    **command_stack.execute_task_stack,
}
execute_command_hash_map = {
    **command_dict.execute_command_hash_map,
    **command_stack.execute_command_stack,
}
