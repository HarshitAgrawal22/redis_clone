import threading
from threading import RLock, Timer


class List_Struc:
    def __init__(self):
        self.storage: list = list()
        self.lock = threading.RLock()

    def rpush(self, data):
        self.storage.append(data)

    def lpush(self, data):

        self.storage.insert(0, data)

    def lpull(self):

        return self.storage.pop(0)

    def rpull(self):

        return self.storage.pop()

    def lrange(self, start, end):
        if start < 0 or start > len(self.storage):
            return "not valid start point"
        if end < -1 or end > len(self.storage):
            return "not vaild end point "
        else:
            result = ""
            for i in range(start, end):
                result += f"{self.storage[i]} "
            return result

    def rrange(self, start, end):
        if start < 0 or start > len(self.storage):
            return "not valid start point"
        if end < -1 or end > len(self.storage):
            return "not vaild end point "
        else:
            result = ""
            for i in range(end, start, -1):
                result += f"{self.storage[i]} "
            return result

    def search_index(self, index):
        if index < 0 or index > len(self.storage):
            return "not valid index"

        else:
            return self.storage[index]

    @staticmethod
    def new_list():
        return List_Struc()
