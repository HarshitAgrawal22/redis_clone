import threading
from threading import RLock, Timer


class String:
    def __init__(self):
        self.storage: dict = dict()

    @staticmethod
    def new_string():
        return String()
