import python_redis.protocols.stack_protocols as stack_protocols
import python_redis.commands.stacks as cmds
import python_redis.execution.Dispatchers.dispatch_stacks as stack_dispatchers
import python_redis.execution.stacks_exe as stack_executer

execute_task_stack = {
    stack_protocols.PushCommand: stack_dispatchers.STACK_TASKS.task_push_command,
    stack_protocols.PopCommand: stack_dispatchers.STACK_TASKS.task_pop_command,
    stack_protocols.PeekCommand: stack_dispatchers.STACK_TASKS.task_peek_command,
}
execute_command_stack = {
    cmds.COMMAND_PUSH: stack_executer.execute_push_command,
    cmds.COMMAND_POP: stack_executer.execute_pop_command,
    cmds.COMMAND_PEEK: stack_executer.execute_peek_command,
}
