import threading
from typing import Dict, Tuple, Optional


class KV:
    def __init__(self):  # Initialize an empty dictionary and an RLock for thread safety
        self.data: Dict[str, bytes] = {}
        self.lock = threading.RLock()

    def set(self, key: str, val: str):
        # Acquire the lock for writing to ensure thread safety
        with self.lock:
            self.data[key] = val.encode("utf-8")

    def get(self, key: str) -> Tuple[Optional[bytes], bool]:
        # Acquire a read lock for safe concurrent access
        with self.lock:
            # Return the value for the key if it exists, otherwise None and False
            print(key)
            val = self.data.get(key)
            return (val, val is not None)

    @staticmethod
    def NewKV():
        return KV()
