from python_redis.services import (
    command_stack,
    command_bst,
    command_graph,
    command_dict,
    command_queue,
    command_sets,
    command_lists,
)

SyncTime: int = 600


execute_task_hash_map = {
    **command_graph.execute_task_graph,
    **command_bst.execute_task_bst,
    **command_lists.execute_task_list,
    **command_dict.execute_task_hash_map,
    **command_stack.execute_task_stack,
    **command_queue.execute_task_queue,
    **command_sets.execute_task_sets,
}
execute_command_hash_map = {
    **command_graph.execute_command_graph,
    **command_bst.execute_command_bst,
    **command_dict.execute_command_hash_map,
    **command_stack.execute_command_stack,
    **command_queue.execute_command_queue,
    **command_sets.execute_command_sets,
    **command_lists.execute_command_list,
}


"""🚀 How to Optimize Performance?
Here are some areas where you can improve the efficiency of your Redis clone:

1️⃣ Reduce Lock Contention (Threading & Concurrency)
If you're using Python's threading, GIL (Global Interpreter Lock) might slow performance.
Consider using multiprocessing or async I/O (like asyncio or FastAPI) for better parallelism.
2️⃣ Optimize Network Handling
Use epoll (Linux) or IOCP (Windows) for efficient socket handling.
Implement connection pooling to reuse client connections instead of creating new ones.
3️⃣ Improve Data Storage Efficiency
If using dictionaries for storage, try a hash table with a better resizing strategy.
Use faster serialization formats (like MsgPack instead of JSON) for efficient memory usage.
4️⃣ Batch Processing & Pipelining
Instead of processing requests one by one, batch similar operations to reduce overhead.
Example: Redis allows pipelining, which sends multiple commands in a single network round trip.
5️⃣ Optimize Memory & Caching Strategy
Use memory-efficient data structures (like struct for fixed-size storage).
Implement lazy deletion or eviction policies to prevent memory bloat."""


# TODO implement these response patterns
# | Prefix | Type          | Example                              |
# | ------ | ------------- | ------------------------------------ |
# | `+`    | Simple String | `+OK\r\n`                            |
# | `-`    | Error         | `-ERR wrong number of arguments\r\n` |
# | `:`    | Integer       | `:10\r\n`                            |
# | `$`    | Bulk String   | `$5\r\nvalue\r\n`                    |
# | `*`    | Array         | `*2\r\n$3\r\none\r\n$3\r\ntwo\r\n`   |
