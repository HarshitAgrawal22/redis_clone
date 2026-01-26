import python_redis.protocols.list_protocols as list_protocols
import python_redis.commands.liststruct as cmds
import python_redis.execution.Dispatchers.dispatch_liststruct as list_dispatchers
import python_redis.execution.liststruct_exe as list_executer

execute_task_list = {
    list_protocols.LPullCommand: list_dispatchers.LISTS_TASKS.task_lpull_command,
    list_protocols.LPushCommand: list_dispatchers.LISTS_TASKS.task_lpush_command,
    list_protocols.RPullCommand: list_dispatchers.LISTS_TASKS.task_rpull_command,
    list_protocols.RPushCommand: list_dispatchers.LISTS_TASKS.task_rpush_command,
    list_protocols.SearchIndexCommand: list_dispatchers.LISTS_TASKS.task_search_index_command,
    list_protocols.LRangeCommand: list_dispatchers.LISTS_TASKS.task_lrange_command,
    list_protocols.RRangeCommand: list_dispatchers.LISTS_TASKS.task_rrange_command,
}
execute_command_list = {
    cmds.COMMAND_LPULL: list_executer.execute_lpull_command,
    cmds.COMMAND_LPUSH: list_executer.execute_lpush_command,
    cmds.COMMAND_LRANGE: list_executer.execute_lrange_command,
    cmds.COMMAND_RRANGE: list_executer.execute_rrange_command,
    cmds.COMMAND_RPULL: list_executer.execute_rpull_command,
    cmds.COMMAND_RPUSH: list_executer.execute_rpush_command,
    cmds.COMMAND_SEARCH_INDEX: list_executer.execute_search_index_command,
}
