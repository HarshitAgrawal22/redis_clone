import threading
from threading import RLock, Timer
from queue import Queue
from services.LinkedList import LinkedList, Node


class DataQueue:
    def __init__(self):
        self.ll: LinkedList = LinkedList()
        self.lock = threading.RLock()

    def display(self):
        with self.lock:
            return self.ll.display()

    def dequeue(self):
        with self.lock:
            return self.ll.remove_head()

    def peek(self):
        with self.lock:
            return self.ll.show_head()

    def enqueue(self, value):
        with self.lock:
            return self.ll.add_last()

    @staticmethod
    def new_queue():
        return DataQueue()
