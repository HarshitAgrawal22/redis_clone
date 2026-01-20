class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return str(self.value)


class LinkedList:

    def __init__(self):
        self.head: Node = None
        self.tail: Node = None

    def show_head(self):
        if self.head is None:
            return "Empty"
        else:
            return self.head.value

    def show_tail(self):
        if self.head is None:
            return "Empty"
        else:
            return self.tail.value

    def add_head(self, data):
        temp: Node = Node(data)
        if self.head is None:
            self.head = temp
            self.tail = temp
            return
        temp.next = self.head
        self.head = temp
        return

    def add_last(self, data):
        temp: Node = Node(data)
        if self.head is None:
            self.head = temp
            self.tail = temp
            return
        self.tail.next = temp
        self.tail = temp
        return

    def is_empty(self):
        return self.head is None

    def remove_head(self) -> int:
        if self.head is None:
            print("Cant delete head its empty ")
            return -1
        temp = self.head.value
        self.head = self.head.next
        return temp

    def remove_tail(self):
        if self.head is None:
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
            result += f"<-{ptr.value}"
            ptr = ptr.next
        return result
