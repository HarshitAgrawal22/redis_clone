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
        self.storage.pop(0)

    def rpull(self):
        self.storage.pop(-1)

    def lrange(self, start, end):
        if start < 0 or start > len(self.storage):
            raise ValueError("not valid start point")
        if end < -1 or end > len(self.storage):
            raise ValueError("not vaild end point ")
        else:
            result = ""
            for i in range(start, end):
                result += self.storage[i]
            return result

    def rrange(self, start, end):
        if start < 0 or start > len(self.storage):
            raise ValueError("not valid start point")
        if end < -1 or end > len(self.storage):
            raise ValueError("not vaild end point ")
        else:
            result = ""
            for i in range(end, start, -1):
                result += self.storage[i]
            return result

    def search_index(self, index):
        if index < 0 or index > len(self.storage):
            raise ValueError("not valid index")

        else:
            return self.storage[index]

    @staticmethod
    def new_list():
        return List_Struc()
