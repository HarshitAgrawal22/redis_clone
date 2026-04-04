import threading
from threading import RLock
from typing import Dict, Tuple, Optional
from python_redis.persistence.db import *
from python_redis.persistence.kv_store import KV_store

import time
from icecream import ic


# socat TCP4-LISTEN:12345,reuseaddr,fork TCP:172.25.128.1:5001,sourceport=40000


class KV:
    def __init__(self, db: HardDatabase):
        # TODO:  Here we wil need to add a backup storage which will have the incoming updates when the dictiony is geting synced with the hard db
        ic.configureOutput(prefix="DEBUG: ", includeContext=True)
        # Initialize an empty dictionary and an RLock for thread safety

        self.data: Dict[str, bytes] = dict()
        # self.store:KV_store = KV_store(db, self.data)
        self.lock: RLock = threading.RLock()

        self.db: HardDatabase = db
        self.collection: Collection
        # has_collections: bool = db.list_collections(limit=1).alive
        if self.db.check_collection_exist("KV"):

            self.collection: Collection = self.db.new_collection("KV")
            ic(self.collection)
            self.load_from_hard_db()
        else:
            self.collection: Collection = self.db.new_collection("KV")

        self.stop_event: threading.Event = threading.Event()
        self.dirty_keys: set[tuple[str, str]] = set()
        
        t = threading.Thread(target=self.periodic_db_sync, args=(), daemon=True)
        t.start()
        # Track dirty keys for periodic updates

    def load_from_hard_db(self):
        # print("loading data from db")
        for record in self.db.load_from_db(self.collection):
            self.data[record["key"]] = record["value"]

    def periodic_db_sync(self):
        while not self.stop_event.is_set():
            # TODO: here for now the work is getting done by checking each and every key-val pair,
            # TODO: create copy only of the dirty keys

            with self.lock:
                dict_db_snapshot = dict(self.data)
                dirty_keys_snapshots = set(self.dirty_keys)
            if len(dirty_keys_snapshots) != 0:
                synced_keys = set()
                for key, operation in dirty_keys_snapshots:
                    try:
                        # ! here is try catch because there can be a exception while having a transaction with db

                        if dict_db_snapshot.get(key) == None:

                            ic(self.db.delete_key(key, self.collection))
                            synced_keys.add((key, operation))
                            print(operation)
                        else:
                            self.db.insert_and_update_key_val(
                                key, dict_db_snapshot.get(key), self.collection
                            )
                            synced_keys.add((key, operation))
                    except Exception:
                        print(Exception)
                with self.lock:

                    ic(f"dirty keys before => {self.dirty_keys}")

                    self.dirty_keys -= synced_keys
                    ic(f"dirty keys after { self.dirty_keys}")
            time.sleep(5)

    def LRU(self):
        with self.lock:
            pass

    def set(self, key: str, val: str):
        # Acquire the lock for writing to ensure thread safety
        with self.lock:
            try:

                (
                    self.dirty_keys.add((key, "c"))
                    if self.data.get(key) == None
                    else self.dirty_keys.add((key, "u"))
                )

                self.data[key] = val.encode("utf-8")

            except MemoryError:
                print("System ran out of memory so deleting some key-val pair")
                self.LRU()

    def get(self, key: str) -> Tuple[Optional[bytes], bool]:
        # Acquire a read lock for safe concurrent access
        with self.lock:
            # Return the value for the key if it exists, otherwise None and False
            print(key)

            val = (
                self.data.get(key).decode("utf-8")
                if self.data.get(key) != None
                else None
            )

            return (val, val is not None)

    def set_attributes(self, key: str, attr: list):
        with self.lock:
            try:

                for i in range(0, len(attr), 2):

                    self.set(f"{key}_{attr[i]}", attr[i + 1])

            except MemoryError:
                print("System ran out of memory so deleting some key-val pair")
                self.LRU()

    def get_attributes(self, key: str, attr: list):
        with self.lock:
            result = ""
            for i in range(0, len(attr)):

                value: bytes = self.data.get(f"{key}_{attr[i]}")
                result += f"{value.decode('utf-8') if value!=None else value } "
            return result.strip()

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
            return result.strip()

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
                self.dirty_keys.add((key, "d"))

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
                self.dirty_keys.add(key)
                # print(self.data[key])

                return (self.data.get(key), self.data.get(key) is not None)
            except Exception as e:
                print(f"Exception in increment method: {e}")
                return e

    @staticmethod
    def NewKV(db: HardDatabase):
        return KV(db)

