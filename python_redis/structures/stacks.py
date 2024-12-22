from services.LinkedList import LinkedList
import threading


class Stackstruc:
    def __init__(self):
        self.lock = threading.RLock()
        self.ll: LinkedList = LinkedList()

    def push(self, item):
        self.ll.add_head(item)

    def pop(self):
        return self.ll.remove_head()

    def peek(self):
        return self.ll.show_head()