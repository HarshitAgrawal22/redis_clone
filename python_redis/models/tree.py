import threading
from threading import RLock, Timer
from typing import Tuple, Optional


class Node:
    def __init__(self, value):
        self.value: dict = value
        self.right: Node = None
        self.left: Node = None

    def __str__(self):
        return f"value stored on this node is:{self.value}"


class bstree:

    def __init__(
        self,
    ):
        self.ll
        self.lock = threading.RLock()

    @staticmethod
    def new_tree():
        return bstree()

    def pre_order_traversal(self, root: Node):
        with self.lock:
            stack: list = [self.root]
            result: str = ""
            while stack:
                node: Node = stack.pop()
                if node:
                    result += str(node.value)
                    result += "\n"
                    stack.append(node.right)
                    stack.append(node.left)
            return result

    def post_order_traversal(self, root: Node):
        with self.lock:
            result: str = ""
            stack: list = [self.root]
            while stack:
                node: Node = stack.pop()
                if node:
                    stack.append(node.right)
                    stack.append(node.left)
                    result += str(node.value)
                    result += "\n"
            return result

    def in_order_traversal(self, root: Node):
        with self.lock:
            result: str = ""
            stack: list = [self.root]
            while stack:
                node: Node = stack.pop()
                if node:
                    stack.append(node.right)
                    result += str(node.value)
                    result += "\n"
                    stack.append(node.left)
            return result

    def search_node(self, value, key, root: Node):
        # we cant use recursion with lock as each function call will aquire a new lock and will increase the lock counter .
        def search(value, root: Node):

            if root == None:
                return False
            if root.value == value:
                return True
            elif value > root.value:
                return search(root.right)
            else:
                return search(root.left)

        with self.lock:
            return search(value, root)

    def insert(self, value):
        def insert_node(value, root: Node):
            if root == None:
                root = Node(value=value)

            elif value > root.value:
                root.right = insert_node(root.right)
            elif value < root.value:
                root.left = insert_node(root.left)
            return root

        with self.lock:
            self.root = insert_node(value, self.root)
        Timer(15 * 60, self.delete_root).start()

    def display(self):
        def display_tree(root: Node, map: str, level: int):
            if root == None:
                return ""
            else:
                level += 1
                map = display_tree(root.left, map, level)
                map += "  " * level
                map += str(root.value) + "\n"
                map += display_tree(root.right, map, level)
            return map

        with self.lock:
            display_tree(self.root)

    def delete(self, key):
        def minValue(node: Node):
            minv = node.value
            while node.left != None:
                minv = node.left.value
                node = node.left
            return minv

        def delete_node(key, root: Node):
            if root == None:
                return root
            if key < root.value:
                root.left = delete_node(key, root.left)

            elif root > root.right:
                root.right = delete_node(key, root.right)
            else:
                if root.left == None:
                    return root.right
                elif root.right == None:
                    return root.right

                root.value = minValue(root.right)
                root.right = delete_node(key, root.right)
            return root

        with self.lock:
            self.root = delete_node(key, self.root)


# Redis supports a variety of data structures that allow for efficient storage and retrieval of data. Here are the primary data structures in Redis:

# 1. Strings
# Description: The simplest data structure in Redis, storing text or binary data.
# Use Cases:
# Caching strings, JSON, or serialized objects.
# Storing counters or numeric values (e.g., view counts).
# Example:
# bash
# Copy code
# SET key "value"
# GET key
# 2. Lists
# Description: Linked lists of strings, where items are ordered by insertion.
# Use Cases:
# Task queues.
# Streaming or timeline-like data.
# Commands:
# bash
# Copy code

# LPUSH list "item1"
# RPUSH list "item2"
# LRANGE list 0 -1
# 3. Sets
# Description: Unordered collections of unique strings.
# Use Cases:
# Tracking unique items (e.g., IPs or user IDs).
# Performing set operations like intersections, unions, and differences.
# Commands:
# bash
# Copy code
# SADD set "item1" "item2"
# SMEMBERS set
# SINTER set1 set2
# 4. Sorted Sets (ZSets)
# Description: Similar to sets but with an associated score for each item, allowing sorting.
# Use Cases:
# Leaderboards.
# Ranking systems.
# Time-series data with scores as timestamps.
# Commands:
# bash
# Copy code
# ZADD zset 1 "item1"
# ZADD zset 2 "item2"
# ZRANGE zset 0 -1 WITHSCORES
# 5. Hashes
# Description: Key-value pairs within a single key, similar to a dictionary.
# Use Cases:
# Storing user profiles or small objects.
# Representing database rows or JSON-like structures.
# Commands:
# bash
# Copy code
# HSET hash key1 "value1"
# HGET hash key1
# HGETALL hash
# 6. Bitmaps
# Description: A string of bits, where each bit can be set or cleared.
# Use Cases:
# Storing true/false values.
# Tracking user activity (e.g., daily login status).
# Commands:
# bash
# Copy code
# SETBIT key 0 1
# GETBIT key 0
# 7. HyperLogLogs
# Description: A probabilistic data structure for approximate cardinality estimation.
# Use Cases:
# Estimating unique items in large datasets (e.g., unique visitors).
# Commands:
# bash
# Copy code
# PFADD hyperloglog "item1"
# PFCOUNT hyperloglog
# 8. Streams
# Description: Log-like data structure for handling event streams.
# Use Cases:
# Event sourcing.
# Real-time messaging systems.
# Commands:
# bash
# Copy code
# XADD stream * key "value"
# XRANGE stream - +
# 9. Geospatial Indexes
# Description: A specialized data type for storing and querying geographic locations.
# Use Cases:
# Location-based applications (e.g., "find the nearest restaurant").
# Commands:
# bash
# Copy code
# GEOADD geo 13.361389 38.115556 "Palermo"
# GEORADIUS geo 15 37 100 km
# Summary of Use Cases by Data Structure


# Data Structure	Common Use Cases
# Strings	Caching, counters, serialized data.
# Lists	Queues, logs, timelines.
# Sets	Unique items, set operations.
# Sorted Sets	Leaderboards, rankings, time-series data.
# Hashes	User profiles, JSON-like data.
# Bitmaps	Tracking true/false states.
# HyperLogLogs	Cardinality estimation.
# Streams	Event sourcing, real-time analytics.
# Geospatial	Location-based queries.
# Redis's flexible data structures make it suitable for a wide range of applications, from caching and messaging to advanced analytics and real-time data processing.


# Eviction Policies

# Redis uses algorithms for managing memory and deciding which keys to evict (e.g., LRU or LFU).
