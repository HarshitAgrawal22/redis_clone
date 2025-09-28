import threading
from threading import RLock, Timer
from typing import Tuple, Optional
import time
from icecream import ic
from python_redis.db import *


class Node:
    def __init__(self, value):
        self.value: dict = value

        self.right: Node = None
        self.left: Node = None

    def __str__(self):
        return f"value stored on this node is:{self.value}"


# here we intent to store a object in the form of dictionary in the bst
class bstree:

    def __init__(self, db: HardDatabase):
        self.root: Node = None
        self.lock = threading.RLock()
        self.key: str = None
        ic.configureOutput(prefix="DEBUG: ", includeContext=True)
        self.db: HardDatabase = db
        self.collection: Collection
        if self.db.check_collection_exist("Tree"):

            self.collection: Collection = self.db.new_collection("Tree")
            self.load_from_hard_db()
        else:
            self.collection: Collection = self.db.new_collection("Tree")

        self.lock: RLock = threading.RLock()
        self.dirty_items: set[tuple[int, str, str]] = set()

        self.stop_event: threading.Event = threading.Event()
        t = threading.Thread(target=self.periodic_db_sync, args=(), daemon=True)
        t.start()

    def load_from_hard_db(self):
        print("loading data from db")
        for record in self.db.load_from_db(self.collection).sort("index", 1):
            pass
        # TODO: figure out the way to load data from db to DS
        # self.ll.add_head(record["value"])

    def periodic_db_sync(self):
        # TODO change variable names
        while not self.stop_event.is_set():
            with self.lock:
                dirty_items_snapshots = set(self.dirty_items)

            if len(dirty_items_snapshots) != 0:
                synced_items = set()
                for index, item, operation in dirty_items_snapshots:

                    try:
                        # here is try catch because there can be a exception while having a transaction with db

                        if operation == "d":

                            ic(self.db.delete_dequeue_item(item, self.collection))
                            synced_items.add((index, item, operation))
                            print(operation)
                        else:
                            self.db.insert_and_update_ordered_items(
                                item, index, self.collection
                            )
                            synced_items.add((index, item, operation))
                    except Exception:
                        print(Exception)
                with self.lock:
                    ic(self.dirty_items)
                    ic(synced_items)
                    self.dirty_items -= synced_items

            time.sleep(5)

    @staticmethod
    def new_tree(db: HardDatabase):
        return bstree(db)

    def check_key_None(self):
        return self.key != None

    def set_key(self, key: list):
        self.key: str = key[0]
        return key

    def get_key(self):
        return self.key

    def pre_order_traversal(self):

        def traversal(node: Node):

            if node == None:
                return ""
            else:
                map = f"{node.value}\n"
                map += traversal(node.left)
                map += traversal(node.right)
                return map

        print("pre order traversal ")
        with self.lock:
            return traversal(self.root)

    def post_order_traversal(self):
        print("post order traversal ")

        def traversal(node: Node):

            if node == None:
                return ""
            else:
                map = traversal(node.left)
                map += traversal(node.right)
                map += f"{node.value}\n"
                return map

        with self.lock:

            return traversal(self.root)

    def in_order_traversal(self):
        print("in order traversal ")

        def traversal(node: Node):

            if node == None:
                return ""
            else:
                map = traversal(node.left)
                map += f"{node.value}\n"
                map += traversal(node.right)
                return map

        with self.lock:

            return traversal(self.root)

    def search_node(self, value: str):
        # we cant use recursion with lock as each function call will aquire a new lock and will increase the lock counter .

        def search(value, root: Node):

            if root == None:
                return "NOT FOUND"
            if root.value[self.key] == value:
                return root.value
            elif value > root.value[self.key]:
                return search(value, root.right)
            else:
                return search(value, root.left)

        with self.lock:
            if self.check_key_None():
                return search(value, self.root)

    def insert(self, value: list):

        def insert_node(value: dict, root: Node):
            print(value)
            if root == None:
                root = Node(value=value)
            # if root.value[self.key] == value[self.key]:
            #     print("here we are ")
            #     return None
            elif value[self.key] > root.value[self.key]:
                root.right = insert_node(value, root.right)
            elif value[self.key] < root.value[self.key]:
                root.left = insert_node(value, root.left)
            return root

        with self.lock:
            temp_dict = dict()
            if (len(value)) % 2 == 0:

                for i in range(0, len(value), 2):
                    temp_dict[value[i]] = value[i + 1]
            print(f"{temp_dict} => temp_dict")
            if temp_dict.get(self.get_key()) != None:
                self.root = insert_node(temp_dict, self.root)
                # self.display()
                return "OK"
            else:

                return "key not in set "

        # Timer(15 * 60, self.delete, args=(self, value[self.key])).start()

    def display(self):
        def display_tree(root: Node, map: str, level: int):
            if root == None:
                return ""
            else:
                level += 1
                map = display_tree(root.left, map, level)
                map += "        " * level
                map += str(root.value) + "\n"
                map += display_tree(root.right, map, level)
            return map

        with self.lock:
            if self.root == None:
                print("empty tree")
            print(x := display_tree(self.root, "", 0))
            return x

    def delete(self, key):
        # def minValue(node: Node):
        #     minv = node.value
        #     while node.left != None:
        #         minv = node.left.value
        #         node = node.left
        #     return minv
        def minValueNode(node: Node) -> Node:
            current = node
            # Keep moving left until we reach the smallest value
            while current.left is not None:
                current = current.left
            return current

        def delete_node(key, root: Node):
            if root == None:
                return root
            if key < root.value[self.key]:
                root.left = delete_node(key, root.left)

            elif key > root.value[self.key]:
                root.right = delete_node(key, root.right)
            else:
                if root.left == None:
                    return root.right
                elif root.right == None:
                    return root.left
                succesor = minValueNode(root.right)
                # root.value = minValue(root.right)
                root.value = succesor.value
                root.right = delete_node(succesor.value[self.key], root.right)
            return root

        with self.lock:
            self.root = delete_node(key, self.root)
            self.display()


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
