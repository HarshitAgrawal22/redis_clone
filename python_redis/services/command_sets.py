import python_redis.protocols.sets_protocols as sets_protocols

execute_task_sets = {
    sets_protocols.DisplayCommand: sets_protocols.SETS_TASKS.task_display_command,
    sets_protocols.RemoveCommand: sets_protocols.SETS_TASKS.task_remove_command,
    sets_protocols.AddCommand: sets_protocols.SETS_TASKS.task_add_command,
    sets_protocols.CheckCommand: sets_protocols.SETS_TASKS.tesk_check_command,
}
execute_command_sets = {
    sets_protocols.COMMAND_DISPLAY: sets_protocols.execute_display_command,
    sets_protocols.COMMAND_CHECK: sets_protocols.execute_check_command,
    sets_protocols.COMMAND_ADD: sets_protocols.execute_add_command,
    sets_protocols.COMMAND_REMOVE: sets_protocols.execute_remove_command,
}
