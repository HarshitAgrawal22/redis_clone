import threading
from python_redis.models.service_ds.LinkedList import LinkedList, Node
from python_redis.models.graph_config import Vertex, Edge

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
        self.stack: LinkedList = LinkedList()
        self.queue: LinkedList = LinkedList()
        self.adj_matrix = [[0 for j in range(nodes)] for i in range(nodes)]
        self.map: dict = (
            dict()
        )  # it will map the name of the nodes to the integer index of arrays

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

    @staticmethod
    def NewGraph():
        return GraphList()


"""this file have the code to store in graph format in cache"""


class graph:
    def __init__(self, is_weighted: int, is_directed: int):
        self.vertices: list[Vertex.Vertex] = list()
        self.is_directed: bool = is_directed
        self.is_weighted: bool = is_weighted

    def add_vertex(self, data: str) -> Vertex:
        new_vertex: Vertex.Vertex = Vertex.Vertex(data)
        self.vertices.append(new_vertex)
        return new_vertex

    def add_edge(self, v1: Vertex.Vertex, v2: Vertex.Vertex, weight: int):
        if not self.is_weighted:
            weight = 0
        v1.add_edge(v2, weight)
        if not self.is_directed:
            v2.add_edge(v1, weight)

    def remove_edge(self, vertex: Vertex.Vertex):
        self.vertices.remove(vertex)

    def is_directed(self) -> bool:
        return self.is_directed

    def is_weighted(self) -> bool:
        return self.is_weighted

    def get_vertices(self) -> list[Vertex.Vertex]:
        return self.vertices

    def get_vertex_by_value(self, value: str):
        for v in self.vertices:
            if v.get_data() == value:
                return v
        return None

    def print(self):
        for v in self.vertices:
            v.print(self.is_weighted)


bus_network = graph(True, False)
mathura: Vertex.Vertex = bus_network.add_vertex("Mathura")
Agra: Vertex.Vertex = bus_network.add_vertex("Agra")
bus_network.add_edge(mathura, Agra, 65)
bus_network.print()
