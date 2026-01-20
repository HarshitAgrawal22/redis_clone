import python_redis.protocols.list_protocols as list_protocols

execute_task_list = {
    list_protocols.LPullCommand: list_protocols.LISTS_TASKS.task_lpull_command,
    list_protocols.LPushCommand: list_protocols.LISTS_TASKS.task_lpush_command,
    list_protocols.RPullCommand: list_protocols.LISTS_TASKS.task_rpull_command,
    list_protocols.RPushCommand: list_protocols.LISTS_TASKS.task_rpush_command,
    list_protocols.SearchIndexCommand: list_protocols.LISTS_TASKS.task_search_index_command,
    list_protocols.LRangeCommand: list_protocols.LISTS_TASKS.task_lrange_command,
    list_protocols.RRangeCommand: list_protocols.LISTS_TASKS.task_rrange_command,
}
execute_command_list = {
    list_protocols.COMMAND_LPULL: list_protocols.execute_lpull_command,
    list_protocols.COMMAND_LPUSH: list_protocols.execute_lpush_command,
    list_protocols.COMMAND_LRANGE: list_protocols.execute_lrange_command,
    list_protocols.COMMAND_RRANGE: list_protocols.execute_rrange_command,
    list_protocols.COMMAND_RPULL: list_protocols.execute_rpull_command,
    list_protocols.COMMAND_RPUSH: list_protocols.execute_rpush_command,
    list_protocols.COMMAND_SEARCH_INDEX: list_protocols.execute_search_index_command,
}
