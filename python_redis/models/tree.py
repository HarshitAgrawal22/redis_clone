import threading
from threading import RLock, Timer
from typing import Tuple, Optional
import time
from icecream import ic
from python_redis.db import *
import json


class Node_AVL:
    def __init__(self, key: int, value: dict) -> None:
        self.key: int = key
        self.value = value
        self.left: Optional[Node_AVL] = None
        self.right: Optional[Node_AVL] = None
        self.height: int = 1  # height of the node


class AVLTree:

    def insert(self, root: Optional[Node_AVL], key: int, value: dict) -> Node_AVL:
        """Insert a key into the AVL tree and return the new root."""

        # 1️⃣ Perform standard BST insertion
        if root is None:
            return Node_AVL(key, value)

        if key < root.key:
            root.left = self.insert(root.left, key, value)
            root.right = self.insert(root.right, key, value)
        else:
            # Equal keys are not allowed in BST
            return root

        # 2️⃣ Update height of this ancestor node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3️⃣ Get the balance factor
        balance = self.get_balance(root)

        # 4️⃣ If node is unbalanced, perform rotations

        # Case 1 - Left Left
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        # Return the (unchanged) node pointer
        return root

    # 🔹 Utility Functions

    def get_height(self, node: Optional[Node_AVL]) -> int:
        if not node:
            return 0
        return node.height

    def get_balance(self, node: Optional[Node_AVL]) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # 🔸 Right Rotation
    def rotate_right(self, y: Node_AVL) -> Node_AVL:
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        # Return new root
        return x

    # 🔸 Left Rotation
    def rotate_left(self, x: Node_AVL) -> Node_AVL:
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # Return new root
        return y

    def preorder(self, root: Optional[Node_AVL]) -> None:
        if root != None:

            ic(f"{root.key}")
            self.preorder(root.left)
            self.preorder(root.right)

    def inorder(self, root: Optional[Node_AVL]) -> None:
        if root:
            self.inorder(root.left)
            ic(f"{root.key}")
            self.inorder(root.right)


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
        self.meta_collection = self.db.new_collection("meta")
        self.collection: Collection
        if self.db.check_collection_exist("Tree"):

            self.collection: Collection = self.db.new_collection("Tree")
            self.dirty_items: set[tuple[int, str, str]] = set()
            self.load_from_hard_db()
        else:
            self.collection: Collection = self.db.new_collection("Tree")
            self.dirty_items: set[tuple[int, str, str]] = set()

        self.lock: RLock = threading.RLock()

        self.stop_event: threading.Event = threading.Event()
        t = threading.Thread(target=self.periodic_db_sync, args=(), daemon=True)
        t.start()

    def load_from_hard_db(self):
        print("loading data from db")
        obj = self.db.get_data_from_meta("Tree", self.meta_collection)
        if obj != None:
            self.key = obj["value"]
        else:
            self.key = None

        # meta_data = self.db.get_data_from_meta("Tree", self.db.new_collection("meta"))
        # TODO: Create a meta collection to store the meta data for the server
        # TODO: add a update Command(Function) to tree, where a node's fields can be updated
        # if meta_data is not None:
        bal_tree: AVLTree = AVLTree()
        root: Node_AVL = None

        for record in self.db.load_from_db(self.collection):
            print(record)
            root = bal_tree.insert(root, record["key"], json.loads(record["value"]))

        def pre_order_insertion(avl_root: Node_AVL):
            if avl_root != None:
                flat_list = []
                avl_root.value
                for k, v in avl_root.value.items():
                    flat_list.append(k)
                    flat_list.append(v)
                ic(flat_list)
                self.insert(flat_list)

                pre_order_insertion(avl_root.left)
                pre_order_insertion(avl_root.right)

        pre_order_insertion(root)
        ic(root)
        bal_tree.preorder(root)
        print("inorder")
        bal_tree.inorder(root)

        # root_key = db.bst_meta.find_one({"_id": "metadata"})["root_key"]
        # preorder_traversal(db, root_key)

        # TODO: figure out the way to load data from db to DS
        # self.ll.add_head(record["value"])

    def periodic_db_sync(self):
        while not self.stop_event.is_set():
            # TODO: here for now the work is getting done by checking each and every key-val pair,
            # TODO: create copy only of the dirty keys

            with self.lock:
                # dict_db_snapshot = dict(self.data)
                dirty_keys_snapshots = set(self.dirty_items)
            if len(dirty_keys_snapshots) != 0:
                synced_keys = set()
                for key_value, operation in dirty_keys_snapshots:
                    node_value = json.loads(key_value)
                    try:
                        # here is try catch because there can be a exception while having a transaction with db

                        if operation == "d":

                            ic(self.db.delete_key(key_value, self.collection))
                            synced_keys.add((key_value, operation))
                            print(operation)
                        else:
                            self.db.insert_and_update_key_val(
                                node_value[self.key], key_value, self.collection
                            )
                            # TODO update it to have key  not "key"
                            synced_keys.add((key_value, operation))
                    except Exception as e:
                        print(e)
                with self.lock:

                    # ic(f"dirty keys before => {self.dirty_keys}")

                    self.dirty_items -= synced_keys
                    # ic(f"dirty keys after { self.dirty_keys}")
            time.sleep(5)

    @staticmethod
    def new_tree(db: HardDatabase):
        return bstree(db)

    def check_key_None(self):
        return self.key != None

    def set_key(self, key):
        self.db.insert_and_update_key_val("Tree", key, self.meta_collection)
        self.key: str = key
        return key

    def get_key(self):
        return self.key

    def upsert_node_data(self, key: str, args: tuple[str]):
        def search(value, root: Node):

            if root == None:
                return root
            if root.value[self.key] == value:
                return root
            elif value > root.value[self.key]:
                return search(value, root.right)
            else:
                return search(value, root.left)

        if len(args) % 2 == 0:
            node: Node = search(key, self.root)
            if node == None:
                return "Invalid Key"
            for i in range(0, len(args), 2):
                if args[i] == self.key:
                    return "Invalid Key"
                node.value[args[i]] = args[i + 1]
            return "Ok"
        else:
            return "Invalid pairs"

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

        # TODO : check logic for duplication by updation for key-val in mongodb
        # TODO : duplicate entries are being made here check that
        with self.lock:
            temp_dict = dict()
            if (len(value)) % 2 == 0:

                for i in range(0, len(value), 2):
                    temp_dict[value[i]] = value[i + 1]
            print(f"{temp_dict} => temp_dict")
            self.dirty_items.add((json.dumps(temp_dict), "c"))
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
            # Shreyanshi's birhtday is just next day of janmashtmi

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


# python -m http.server 8080
