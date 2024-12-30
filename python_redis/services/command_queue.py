import python_redis.protocols.queue_protocols as queue_protocols

execute_task_queue = {
    queue_protocols.DisplayCommand: queue_protocols.QUEUE_TASKS.task_display_command,
    queue_protocols.DequeueCommand: queue_protocols.QUEUE_TASKS.task_dequeue_command,
    queue_protocols.PeekCommand: queue_protocols.QUEUE_TASKS.task_peek_command,
    queue_protocols.EnqueueCommand: queue_protocols.QUEUE_TASKS.task_enqueue_command,
}
execute_command_queue = {
    queue_protocols.COMMAND_ENQUEUE: queue_protocols.execute_enqueue_command,
    queue_protocols.COMMAND_DEQUEUE: queue_protocols.execute_dequeue_command,
    queue_protocols.COMMAND_PEEK: queue_protocols.execute_peek_command,
    queue_protocols.COMMAND_DISPLAY: queue_protocols.execute_display_command,
}
