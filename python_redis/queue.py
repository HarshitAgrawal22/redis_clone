import threading
from threading import RLock, Timer
from queue import Queue


class DataQueue:
    def __init__(self):
        self.queue: Queue = Queue()

    @staticmethod
    def new_queue():
        return DataQueue()
