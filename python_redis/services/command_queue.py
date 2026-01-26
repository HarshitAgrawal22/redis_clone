import python_redis.protocols.queue_protocols as queue_protocols
import python_redis.commands.queuestruct as cmds
import python_redis.execution.Dispatchers.dispatch_tree as bst_dispatchers
import python_redis.execution.tree_exe as bst_executer
import python_redis.execution.Dispatchers.dispatch_queuestruct as queue_dispatchers
import python_redis.execution.queuestruct_exe as queue_executer

execute_task_queue = {
    queue_protocols.DisplayCommand: queue_dispatchers.QUEUE_TASKS.task_display_command,
    queue_protocols.DequeueCommand: queue_dispatchers.QUEUE_TASKS.task_dequeue_command,
    queue_protocols.PeekCommand: queue_dispatchers.QUEUE_TASKS.task_peek_command,
    queue_protocols.EnqueueCommand: queue_dispatchers.QUEUE_TASKS.task_enqueue_command,
}
execute_command_queue = {
    cmds.COMMAND_ENQUEUE: queue_executer.execute_enqueue_command,
    cmds.COMMAND_DEQUEUE: queue_executer.execute_dequeue_command,
    cmds.COMMAND_PEEK: queue_executer.execute_peek_command,
    cmds.COMMAND_DISPLAY: queue_executer.execute_display_command,
}
