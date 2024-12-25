import threading
from threading import RLock, Timer


class Set:
    def __init__(self):
        self.storage: set = set()
        self.lock = threading.RLock()

    def remove(self, target_attr):
        with self.lock:
            try:
                self.storage.remove(target_attr)
                return "OK"
            except:
                return "NOT FOUND"

    @staticmethod
    def new_set():
        return Set()

    def display(self):
        with self.lock:
            result = ""
            for i in self.storage:
                result += f"-{i}"
            return result

    def add(self, item):
        with self.lock:
            self.storage.add(item)
