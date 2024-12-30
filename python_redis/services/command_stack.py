import python_redis.protocols.stack_protocols as stack_protocols

execute_task_stack = {
    stack_protocols.PushCommand: stack_protocols.STACK_TASKS.task_push_command,
    stack_protocols.PopCommand: stack_protocols.STACK_TASKS.task_pop_command,
    stack_protocols.PeekCommand: stack_protocols.STACK_TASKS.task_peek_command,
}
execute_command_stack = {
    stack_protocols.COMMAND_PUSH: stack_protocols.execute_push_command,
    stack_protocols.COMMAND_POP: stack_protocols.execute_pop_command,
    stack_protocols.COMMAND_PEEK: stack_protocols.execute_peek_command,
}
