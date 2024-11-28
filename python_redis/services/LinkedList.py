class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:

    def __init__(self):
        self.head: Node = None
        self.tail: Node = None

    def add_head(self, data):
        temp: Node = Node(data)
        if self.head == None:
            self.head = temp
            self.tail = temp
            return
        temp.next = self.head
        self.head = temp
        return

    def add_last(self, data):
        temp: Node = Node(data)
        if self.head == None:
            self.head = temp
            self.tail = temp
            return
        self.tail.next = temp
        self.tail = temp
        return

    def remove_head(self):
        if self.head == None:
            print("Cant delete head its empty ")
            return
        self.head = self.head.next
        return

    def remove_tail(self):
        if self.head == None:
            print("list is empty ")
            return

        ptr: Node = self.head
        while ptr.next.next != None:
            ptr = ptr.next
        ptr.next = None
        return

    def display(self):
        result = ""
        ptr: Node = self.head
        while ptr != None:
            result += f"{ptr.value} "
            ptr = ptr.next
        return result
