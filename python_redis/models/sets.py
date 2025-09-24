import threading
from threading import RLock, Timer
from icecream import ic
import time
from python_redis.db import *


class Set:
    def __init__(self, db: HardDatabase):
        ic.configureOutput(prefix="DEBUG: ", includeContext=True)
        self.db: HardDatabase = db
        self.storage: set[str] = set()
        self.collection: Collection
        if self.db.check_collection_exist("Set"):

            self.collection: Collection = self.db.new_collection("Set")
            self.load_from_hard_db()
        else:
            self.collection: Collection = self.db.new_collection("Set")

        self.lock: RLock = threading.RLock()
        self.dirty_items: set[tuple[str, str]] = set()

        self.stop_event: threading.Event = threading.Event()
        t = threading.Thread(target=self.periodic_db_sync, args=(), daemon=True)
        t.start()

    def remove(self, target_attr):
        with self.lock:
            try:
                self.storage.remove(target_attr)
                self.dirty_items.add((target_attr, "d"))
                return "OK"
            except Exception as e:
                ic(e)
                return "NOT FOUND"

    def load_from_hard_db(self):
        print("loading data from db")
        for record in self.db.load_from_db(self.collection):
            # ic(record["key"], record["value"])
            # self.data[record["key"]] = record["value"]
            self.storage.add(record["value"])

    def kill(self):
        # this is to stope the periodic update thread
        # self.db.log(self.collection)
        self.dirty_items.clear()
        self.stop_event.set()

    def periodic_db_sync(self):
        # TODO change variable names
        while not self.stop_event.is_set():
            with self.lock:
                dirty_items_snapshots = set(self.dirty_items)

            if len(dirty_items_snapshots) != 0:
                synced_items = set()
                for item, operation in dirty_items_snapshots:
                    try:
                        # here is try catch because there can be a exception while having a transaction with db

                        if operation == "d":

                            ic(self.db.delete_item(item, self.collection))
                            synced_items.add((item, operation))
                            print(operation)
                        else:
                            self.db.insert_and_update_item(item, self.collection)
                            synced_items.add((item, operation))
                    except Exception:
                        print(Exception)
                with self.lock:
                    ic(self.dirty_items)
                    ic(synced_items)
                    self.dirty_items -= synced_items

            time.sleep(5)

    @staticmethod
    def new_set(db: HardDatabase):
        return Set(db)

    def display(self):
        with self.lock:
            result: str = ""

            for i in self.storage:

                result += f"-{i}"

            return result.lstrip("-")

    def check(self, items: str):
        with self.lock:
            result: str = ""
            for item in items:
                if item in self.storage:
                    result += f"{True} "
                else:
                    result += f"{False} "
                    ic(result)
            return result

    def add(self, item):
        with self.lock:

            self.dirty_items.add((item, "c"))
            self.storage.add(item)
