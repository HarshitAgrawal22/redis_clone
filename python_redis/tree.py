import threading
from threading import RLock, Timer
from typing import dict, Tuple, Optional


# Use Cases
# Redis is widely used for:

# Caching: Reducing database load by storing frequently accessed data.

# Session Management: Storing user session data for web applications.

# Real-Time Analytics: Handling high-speed data for dashboards and monitoring.

# Message Queues: Implementing lightweight and fast message brokers.

# Leaderboard and Ranking: Using sorted sets for scoring and ranking systems.

# Geo-based Applications: Storing and querying location data.


# atures of Redis Database

# In-Memory Data Store

# Redis stores data entirely in memory, ensuring low-latency and high-speed operations.
# Data Persistence

# Although an in-memory database, Redis offers persistent storage through:
# RDB (Redis Database Backup): Periodic snapshots of data.
# AOF (Append-Only File): Logs all write operations for durability.
# Data Structures

# Redis supports a variety of data structures beyond simple key-value pairs, including:
# Strings
# Lists (linked lists)
# Sets (collections of unique values)
# Sorted Sets (sets with a score for ordering)
# Hashes (key-value pairs, like dictionaries)
# Streams
# Bitmaps and HyperLogLogs (used for approximate data structures)
# Pub/Sub Messaging

# Redis provides a publish/subscribe mechanism for building real-time messaging systems.
# Lua Scripting

# Redis supports server-side Lua scripts, enabling complex operations to be performed atomically.
# Transactions

# Redis supports transactions with the commands MULTI, EXEC, WATCH, and DISCARD, ensuring atomicity.
# Replication

# Redis supports master-slave replication for high availability and horizontal scaling.
# Clustering

# Redis Cluster allows sharding and scaling data across multiple Redis nodes for distributed use cases.
# High Availability

# Using Redis Sentinel, you can monitor Redis instances, perform failover, and ensure the system is resilient to outages.
# Lightweight and Fast

# Redis is extremely lightweight and efficient, capable of handling millions of requests per second.
# Geospatial Support
# Redis includes geospatial data types and commands for storing and querying location-based data.
# Streams for Data Logging
# Redis Streams allow storage and processing of a log of data points, useful for event sourcing and real-time analytics.
# Atomic Operations
# All Redis operations are atomic, ensuring data consistency during concurrent operations.
# Redis Modules

# Redis can be extended with modules such as RedisJSON (JSON handling), RedisGraph (graph database), and RedisAI (AI/ML model serving).
# Rich Set of Clients

# Redis has client libraries available for almost all programming languages, including Python, Go, Java, Node.js, and more.


class Node:
    def __init__(self, value):
        self.value = value
        self.right: Node = None
        self.left: Node = None

    def __str__(self):
        return f"value stored on this node is:{self.value}"


class bstree:

    def __init__(self, value):
        self.root: Node = Node(value)
        self.lock = threading.RLock()

    @staticmethod
    def new_tree(value_type):  # 0 for string and 1 for integer
        return bstree(value_type)

    def pre_order_traversal(self, root: Node):
        with self.lock:
            stack: list = [self.root]
            result: str = ""
            while stack:
                node: Node = stack.pop()
                if node:
                    result += str(node.value)
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
                    stack.append(node.left)
            return result

    def search_node(self, value, root: Node):
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
