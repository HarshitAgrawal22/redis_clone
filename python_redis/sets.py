import threading
from threading import RLock, Timer


class Set:
    def __init__(self):
        self.storage = set()
        self.lock = threading.RLock()

    @staticmethod
    def new_set():
        return Set()
