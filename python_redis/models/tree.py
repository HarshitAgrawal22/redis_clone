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


# here we intent to store a object in the form of dictionary in the bst
class bstree:

    def __init__(self):
        self.root: Node = None
        self.lock = threading.RLock()
        self.key: str = None

    @staticmethod
    def new_tree():
        return bstree()

    def check_key_None(self):
        return self.key != None

    def set_key(self, key: list):
        self.key: str = key[0]
        return key

    def get_key(self):
        return self.key

    def pre_order_traversal(self):
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
            print(result)
            return result

    def post_order_traversal(self):
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
                print(result)
            return result

    def in_order_traversal(self):
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
            print(result)
            return result

    def search_node(self, value, root: Node):
        # we cant use recursion with lock as each function call will aquire a new lock and will increase the lock counter .
        def search(value, root: Node):
            if self.check_key_None(self):
                if root == None:
                    return False
                if root.value[self.key] == value:
                    return True
                elif value > root.value[self.key]:
                    return search(root.right)
                else:
                    return search(root.left)

        with self.lock:
            return search(value, root)

    def insert(self, value: list):
        temp_dict = dict()
        if (len(value)) % 2 == 0:

            for i in range(0, len(value), 2):
                temp_dict[value[i]] = value[i + 1]
        print(temp_dict)

        def insert_node(value: dict, root: Node):
            print(value)
            if root == None:
                root = Node(value=value)
            if root.value[self.key] == value[self.key]:
                return None
            elif value[self.key] > root.value[self.key]:
                root.right = insert_node(value, root.right)
            elif value[self.key] < root.value[self.key]:
                root.left = insert_node(value, root.left)
            return root

        with self.lock:
            if temp_dict.get(self.get_key()) != None:
                self.root = insert_node(temp_dict, self.root)
            else:
                return "key not set "
        # Timer(15 * 60, self.delete, args=(self, value[self.key])).start()

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
            print(x := display_tree(self.root, "", 0))
            return x

    def delete(self, key):
        def minValue(node: Node):
            minv = node.value
            while node.left != None:
                minv = node.left.value[self.key]
                node = node.left
            return minv

        def delete_node(key, root: Node):
            if root == None:
                return root
            if key < root.value[self.key]:
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
