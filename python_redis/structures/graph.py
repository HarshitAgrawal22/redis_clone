import threading
from services.LinkedList import LinkedList, Node


# class Node:
#     def __init__(self, vertex):
#         self.vertex = vertex
#         self.next = None

#     def __str__(self):
#         return f"{self.next} is the next node , {self.vertex}"


class GraphMatrix:
    def __init__(self, nodes):
        self.lock = threading.RLock()
        self.E = 0
        self.v = nodes
        self.adj_matrix = [[0 for j in range(nodes)] for i in range(nodes)]

    def addEdgeMatrix(self, u: int, v: int):
        with self.lock:
            self.adj_matrix[u][v] = 1
            self.adj_matrix[v][u] = 1
            self.E += 1

    def removeEdgeMatrix(self, u: int, v: int):
        with self.lock:
            self.adj_matrix[v][u] = 0
            self.adj_matrix[u][v] = 0
            self.E -= 1

    def __str__(self):
        with self.lock:
            result = ""

            for i in self.adj_matrix:
                for j in i:
                    result += f"{self.adj_matrix[i][j]} "
                result += "\n"

            return result

    def dfs(self, root):
        pass

    @staticmethod
    def new_graph():

        return GraphMatrix()


class GraphList:
    def __init__(self, nodes):
        self.adj_list: list[LinkedList] = list()
        for i in range(nodes):
            self.adj_list[i] = LinkedList()

    def addEdgeList(self, u: int, v: int):
        self.adj_list[u].add_tail(v)
        self.adj_list[v].add_tail(u)

    def __str__(self):
        result: str = ""
        for i in range(len(self.adj_list)):
            ptr: Node = self.adj_list[i].head
            result += f"{i} -> "
            while ptr != None:
                result += ptr.value
                ptr = ptr.next
            result += "\n"
        return result


"""this file have the code to store in graph format in cache"""
