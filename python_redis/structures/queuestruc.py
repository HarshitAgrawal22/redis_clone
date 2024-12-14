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

        self.last: Node = None

    def display(self):
        ptr: Node = self.first
        result: str = ""
        while ptr != None:
            result += f"{ptr.value}"
            ptr = ptr.next
        return result

    def remove(self):
        if self.first == None:
            print("queue is empty ")
            return -1
        else:
            temp: Node = self.first
            self.first = self.first.next
            return temp.value

    def peek(self):
        return self.first.value

    def add(self, value):
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
