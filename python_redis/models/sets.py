import threading
from threading import RLock, Timer


class Set:
    def __init__(self):
        self.storage: set = set()
        self.lock = threading.RLock()

    def get(self, target_attr):
        with self.lock:
            for i in self.storage:
                if i.get(target_attr) != None:
                    return i
                return None

    @staticmethod
    def new_set():
        return Set()

    def set(self, item):
        with self.lock:
            self.storage.add(item)
