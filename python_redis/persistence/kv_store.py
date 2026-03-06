from icecream import ic
from python_redis.persistence.db import *
from typing import Dict, Tuple, Optional
import threading
import time
class KV_store:
    def __init__(self, db:HardDatabase, data: Dict[str, bytes]):
        ic.configureOutput(prefix="DEBUG: ", includeContext=True)
        self.data: Dict[str, bytes] = data
        self.db:HardDatabase= db
        self.collection: Collection
        self.stop_event: threading.Event = threading.Event()
        self.dirty_keys: set[tuple[str, str]] = set()
        if self.db.check_collection_exist("KV"):
            self.collection: Collection = self.db.new_collection("KV")
            self.load_from_hard_db()
        else:
            self.collection: Collection = self.db.new_collection("KV")
    def load_from_hard_db(self):
        # print("loading data from db")
        for record in self.db.load_from_db(self.collection):
            # ic(record["key"], record["value"])
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
