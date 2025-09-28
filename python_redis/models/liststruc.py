import threading
from threading import RLock, Timer
from python_redis.db import *
from icecream import ic
import time


class List_Struc:
    def __init__(self, db: HardDatabase):
        ic.configureOutput(prefix="DEBUG: ", includeContext=True)
        self.storage: list = list()
        self.db: HardDatabase = db
        self.lock = threading.RLock()
        self.collection: Collection
        self.db_left_index = 0
        self.db_right_index = 0
        if self.db.check_collection_exist("List"):

            self.collection: Collection = self.db.new_collection("List")
            self.load_from_hard_db()
        else:
            self.collection: Collection = self.db.new_collection("List")

        self.lock: RLock = threading.RLock()
        self.dirty_items: set[tuple[int, str, str]] = set()
        # In it 1st=index, 2nd=value, 3rd=operation

        self.stop_event: threading.Event = threading.Event()
        t = threading.Thread(target=self.periodic_db_sync, args=(), daemon=True)
        t.start()

    def load_from_hard_db(self):
        print("loading data from db")
        for record in self.db.load_from_db(self.collection).sort("index", 1):

            self.storage.append(record["value"])

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

                            ic(self.db.delete_item(item, self.collection))
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

    def rpush(self, data):
        self.storage.append(data)
        self.db_right_index = self.db_right_index + 1
        self.dirty_items.add((self.db_right_index, data, "c"))

    def lpush(self, data):
        self.db_left_index = self.db_left_index - 1
        self.dirty_items.add((self.db_left_index, data, "c"))
        self.storage.insert(0, data)

    def lpull(self):
        if len(self.storage) > 0:
            data: str = self.storage.pop(0)
            self.db_left_index = self.db_left_index + 1
            self.dirty_items.add((self.db_left_index, data, "d"))
            return data

    def rpull(self):
        if len(self.storage) > 0:
            data: str = self.storage.pop()
            self.db_right_index = self.db_right_index - 1
            self.dirty_items.add((self.db_right_index, data, "d"))
            return data
        else:
            return "False"

    def lrange(self, start, end):
        if start < 0 or start > len(self.storage):
            return "not valid start point"
        if end < -1 or end > len(self.storage):
            return "not vaild end point "
        else:
            result: str = ""
            for i in range(start, end):
                result += f"{self.storage[i]} "
            return result.rstrip(" ")

    def rrange(self, start, end):
        if start < 0 or start > len(self.storage):
            return "not valid start point"
        if end < -1 or end > len(self.storage):
            return "not vaild end point "
        else:
            result = ""
            for i in range(end, start, -1):
                result += f"{self.storage[i]} "
            return result

    def search_index(self, index):
        if index < 0 or index > len(self.storage):
            return "not valid index"

        else:
            return self.storage[index]

    @staticmethod
    def new_list(db: HardDatabase):
        return List_Struc(db)
