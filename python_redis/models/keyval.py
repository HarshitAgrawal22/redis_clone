import threading
from typing import Dict, Tuple, Optional
from python_redis.db import Database
import asyncio


import asyncio


async def periodic_task():
    while True:
        print("Task executed")
        await asyncio.sleep(5)


async def main():
    # Run your main app logic alongside the periodic task
    task = asyncio.create_task(periodic_task())
    await your_main_server_loop()


# Example placeholder for your actual server logic
async def your_main_server_loop():
    while True:
        print("Main server running")
        await asyncio.sleep(1)


# Start event loop
asyncio.run(main())


class KV:
    def __init__(
        self, Db_str, db: Database
    ):  # Initialize an empty dictionary and an RLock for thread safety
        self.data: Dict[str, bytes] = {}
        self.lock = threading.RLock()
        self.db: Database = db
        self.db.new_collection("KV")

    def periodic_update_db(self):
        for i in enumerate(self.data):
            print(i)
        pass

    def LRU(self):
        with self.lock:
            pass

    def set(self, key: str, val: str):
        # Acquire the lock for writing to ensure thread safety
        with self.lock:
            try:
                self.data[key] = val.encode("utf-8")
            except MemoryError:
                print("System ran out of memory so deleting some key-val pair")
                self.LRU()

    def get(self, key: str) -> Tuple[Optional[bytes], bool]:
        # Acquire a read lock for safe concurrent access
        with self.lock:
            # Return the value for the key if it exists, otherwise None and False
            print(key)
            val = self.data.get(key).decode("utf-8")
            return (val, val is not None)

    def set_attributes(self, key: str, attr: list):
        with self.lock:
            try:
                for i in range(0, len(attr), 2):
                    self.data[f"{key}_{attr[i]}"] = attr[i + 1].encode("utf-8")
            except MemoryError:
                print("System ran out of memory so deleting some key-val pair")
                self.LRU()

    def get_attributes(self, key: str, attr: list):
        with self.lock:
            result = ""
            for i in range(0, len(attr)):
                value: bytes = self.data.get(f"{key}_{attr[i]}")
                result += f"{value.decode('utf-8') if value!=None else value } "
            return result

    def set_multiple_pairs(self, attrs: list):
        # this may trigger a error so needed to be solved later on if needed
        for i in range(0, len(attrs), 2):
            self.set(attrs[i], attrs[i + 1])

    def get_multiple_values(self, keys: list[str]) -> str:
        with self.lock:
            result: str = ""
            for i in keys:
                # print(f"value of {i} => {self.data.get(i)}")
                value: bytes = self.data.get(i)
                result += f"{value.decode('utf-8') if value!= None else value} "
            return result

    def check(self, keys: list[bool]):

        with self.lock:
            print(f"{keys} are the keys available")
            if len(keys) == 1:

                return [self.data.get(keys[0]) is not None]

            return [self.data.get(i) is not None for i in keys]

    def delete_pair(self, key: str):
        with self.lock:
            # Return the value for the key if it exists, otherwise None and False
            print(key)
            try:
                del self.data[key]
                return key
            except Exception as e:
                print(f"Exception in delete pair: {e}")
                return e

    def total(self):
        with self.lock:
            return len(self.data)

    def increment(self, key: str):
        with self.lock:
            # Return the value for the key if it exists, otherwise None and False
            try:
                print(key)
                self.data[key] = str(int(self.data.get(key)) + 1).encode("utf-8")
                print(self.data[key])
                return (self.data.get(key), self.data.get(key) is not None)
            except Exception as e:
                print(f"Exception in increment method: {e}")
                return e

    @staticmethod
    def NewKV(DB_str: str, db: Database):
        return KV(DB_str, db)


# In Redis, you can indeed implement queues, and while binary trees are not directly supported as a native data structure, you can achieve tree-like functionality using sorted sets and other structures. Here’s a closer loOK at how queues and tree structures can be achieved in Redis:

# 1. Queues in Redis
# Redis supports queues through its List data structure, which allows you to create both FIFO (First-In, First-Out) and LIFO (Last-In, First-Out) queues. The List commands provide efficient ways to add and remove items from both ends of a list, making it suitable for queue-like behavior.

# FIFO Queue:

# Use LPUSH to add an item to the start of the list and RPOP to remove an item from the end of the list, ensuring that the first item added is the first to be removed.
# Example:
# shell
# Copy code
# LPUSH myQueue item1  # Add item to the start of the queue
# RPOP myQueue         # Remove item from the end of the queue
# LIFO Queue (Stack):

# Use LPUSH to add an item and LPOP to remove from the start of the list.
# Example:
# shell
# Copy code
# LPUSH myStack item1  # Add item to the start of the stack
# LPOP myStack         # Remove item from the start of the stack
# Blocking Queues:

# Redis also provides blocking operations (BLPOP and BRPOP), which allow the queue to block and wait for new elements if the queue is empty, making it ideal for task queues or pub/sub patterns.
# 2. Binary Trees in Redis
# While Redis does not directly support binary trees as a native data structure, you can simulate a binary tree or other types of tree structures using:

# Sorted Sets (Zset):

# Redis Sorted Sets (ZSET) can be used to store elements in a sorted order with a score attached to each element, which you can leverage for tree-based logic. Each element in a ZSET is unique, and you can retrieve elements in sorted order based on their scores, somewhat simulating traversal in a binary tree structure.

# Sorted sets support operations like:

# Range queries (ZRANGE, ZREVRANGE): Fetch elements within a score range, useful for in-order traversal.
# Ranked elements (ZRANK, ZREVRANK): Get the rank (position) of an element, which helps in positioning within a tree-like structure.
# Example:

# shell
# Copy code
# ZADD myTree 1 "node1"  # Add node with score 1
# ZADD myTree 2 "node2"  # Add node with score 2
# ZADD myTree 3 "node3"  # Add node with score 3
# Parent-Child Relationships with Hashes:

# You can use Hashes or Lists to create relationships between nodes. For instance, each node could be a hash entry, and parent-child relationships can be stored as references within the hashes.
# Example structure:
# shell
# Copy code
# HSET node:1 value "root" left_child "node:2" right_child "node:3"
# HSET node:2 value "left_child" left_child "node:4" right_child "node:5"
# This setup emulates pointers in a binary tree, with each node containing references to its children.
# Tree-Like Data Access Patterns
# In Redis, using these methods, you can manage hierarchical data and access patterns common in binary trees. However, if your application demands highly complex tree operations, consider using a graph database like Neo4j or an embedded data structure specifically optimized for tree management, as Redis is optimized more for flat and linear data access.

# Summary
# Queues: Use Redis Lists for FIFO or LIFO queues.
# Binary Trees: Use Sorted Sets for sorted node access or Hashes to create parent-child relationships.
