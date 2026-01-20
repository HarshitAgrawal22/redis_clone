import threading
from threading import RLock, Timer
from python_redis.persistence.db import *
from python_redis.models.service_ds.LinkedList import LinkedList, Node
from icecream import ic
import time
from datetime import datetime


class DataQueue:
    def __init__(self, db: HardDatabase):
        self.ll: LinkedList = LinkedList()
        self.lock = threading.RLock()
        ic.configureOutput(prefix="DEBUG: ", includeContext=True)
        self.db: HardDatabase = db
        self.collection: Collection
        if self.db.check_collection_exist("Queue"):

            self.collection: Collection = self.db.new_collection("Queue")
            self.load_from_hard_db()
        else:
            self.collection: Collection = self.db.new_collection("Queue")

        self.lock: RLock = threading.RLock()
        self.dirty_items: set[tuple[int, str, str]] = set()

        self.stop_event: threading.Event = threading.Event()
        t = threading.Thread(target=self.periodic_db_sync, args=(), daemon=True)
        t.start()

    def load_from_hard_db(self):
        print("loading data from db")
        for record in self.db.load_from_db(self.collection).sort("index", 1):

            self.ll.add_head(record["value"])

    def periodic_db_sync(self):

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

    def display(self):
        with self.lock:

            return self.ll.display()

    def dequeue(self):
        with self.lock:
            self.dirty_items.add((time.time(), "", "d"))
            return self.ll.remove_head()

    def peek(self):
        with self.lock:
            return self.ll.show_head()

    def enqueue(self, value):
        with self.lock:
            self.dirty_items.add((time.time(), value, "e"))
            return self.ll.add_last(value)

    @staticmethod
    def new_queue(db: HardDatabase):
        return DataQueue(db)


# hset name harshit
# hset billo rani
# gsek name
# gaddv name harshit age 20
# gaddv name shivam age 20
# gadde harshit shivam 15
