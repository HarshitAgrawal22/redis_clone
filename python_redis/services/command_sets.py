import python_redis.protocols.sets_protocols as sets_protocols
import python_redis.commands.sets as cmds
import python_redis.execution.Dispatchers.dispatch_sets as sets_dispatchers
import python_redis.execution.sets_exe as sets_executer

execute_task_sets = {
    sets_protocols.DisplayCommand: sets_dispatchers.SETS_TASKS.task_display_command,
    sets_protocols.RemoveCommand: sets_dispatchers.SETS_TASKS.task_remove_command,
    sets_protocols.AddCommand: sets_dispatchers.SETS_TASKS.task_add_command,
    sets_protocols.CheckCommand: sets_dispatchers.SETS_TASKS.tesk_check_command,
}
execute_command_sets = {
    cmds.COMMAND_DISPLAY: sets_executer.execute_display_command,
    cmds.COMMAND_CHECK: sets_executer.execute_check_command,
    cmds.COMMAND_ADD: sets_executer.execute_add_command,
    cmds.COMMAND_REMOVE: sets_executer.execute_remove_command,
}
