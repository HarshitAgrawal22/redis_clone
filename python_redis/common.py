from __future__ import annotations
from python_redis.protocols.command import Command
from python_redis.services import (
    command_bst,
    command_graph,
    command_stack,
    command_dict,
    command_queue,
    command_sets,
    command_lists,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_redis.peer import Peer


class Message:
    def __init__(self, cmd: bytearray, conn_peer: Peer):
        # this is the peer from/to this message is sent/received
        self.conn_peer: Peer = conn_peer
        self.cmd: Command = cmd

    def __str__(self):
        return f"conn_peer:{self.conn_peer}     cmd:{self.cmd}"


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
