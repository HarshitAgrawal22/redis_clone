import threading
from threading import RLock, Timer
from queue import Queue


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return f"{self.value} is the value stored at this node"


class DataQueue:
    def __init__(self):
        self.first: Node = None
        self.lock = threading.RLock()
        self.last: Node = None

    def display(self):
        with self.lock:
            ptr: Node = self.first
            result: str = ""
            while ptr != None:
                result += f"{ptr.value}"
                ptr = ptr.next
            return result

    def remove(self):
        with self.lock:
            if self.first == None:
                print("queue is empty ")
                return -1
            else:
                temp: Node = self.first
                self.first = self.first.next
                return temp.value

    def peek(self):
        with self.lock:
            return self.first.value

    def add(self, value):
        with self.lock:
            temp: Node = Node(value)
            if self.first == None:
                self.first = self.last = temp
                return
            self.last.next = temp
            self.last = temp
            return

    @staticmethod
    def new_queue():
        return DataQueue()
