import threading
from python_redis.models.service_ds.LinkedList import LinkedList, Node
from python_redis.models.graph_config import Vertex, Edge, dijkistra
from python_redis.persistence.db import *
from icecream import ic
import time
from datetime import datetime

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class graph:
    def __init__(self, is_weighted: bool, is_directed: bool, db: HardDatabase):
        self.vertices: list[Vertex.Vertex] = list()
        self.is_directed: bool = is_directed
        self.is_weighted: bool = is_weighted
        self.key_name: str = None
        self.dij: dijkistra.dijkistra = dijkistra.dijkistra()
        self.db: HardDatabase = db

    @staticmethod
    def new_graph(db: HardDatabase):  #
        return graph(True, True, db)

    def check_key_name_none(self):  #
        return self.key_name != None

    def get_key_name(self):  #
        return self.key_name

    def set_key_name(self, key):  #
        self.key_name = key
        return self.key_name

    def add_vertex(self, data: list) -> Vertex:  #
        if self.check_key_name_none():

            temp_dict = dict()
            if (len(data)) % 2 == 0:

                for i in range(0, len(data), 2):
                    temp_dict[data[i]] = data[i + 1]
            # print(f"{temp_dict} => temp_dict")

            if temp_dict.get(self.get_key_name()) != None:
                new_vertex: Vertex.Vertex = Vertex.Vertex(temp_dict)
                self.vertices.append(new_vertex)
                # print("added to list")
                return new_vertex
            else:
                return None
        else:
            return None

    def remove_vertex(self, data: dict):
        targetVertex: Vertex = self.get_vertex_by_value(data)
        if targetVertex == None:
            return False
        for v in self.vertices:

            if v.get_data().get(self.get_key_name()) == data:

                # self.remove_edge(v)
                self.vertices.remove(v)

            else:
                for e in v.get_edges():
                    if e.get_end().get_data().get(
                        self.get_key_name()
                    ) == targetVertex.get_data().get(self.get_key_name()):

                        v.remove_edge(e, self.get_key_name())

        return True

    def breadth_first_search(
        self, start: str, visited_nodes: list[Vertex.Vertex]
    ) -> str:
        result = ""
        visited_queue: LinkedList = LinkedList()
        visited_queue.add_last(self.get_vertex_by_value(start))
        visited_queue.display()
        while not visited_queue.is_empty():
            current: Vertex.Vertex = visited_queue.remove_head()

            result += f"{current.get_data()}" + "\n"

            for e in current.get_edges():
                neighbor: Vertex.Vertex = e.get_end()
                if neighbor not in visited_nodes:
                    visited_nodes.append(neighbor)
                    visited_queue.add_last(neighbor)
        return result

    def depth_first_search(
        self, start: Vertex.Vertex, visitedNodes: list[Vertex.Vertex]
    ):
        result = ""
        start = self.get_vertex_by_value(start)

        def dfs(
            start: Vertex.Vertex, visitedNodes: list[Vertex.Vertex], result: str
        ) -> str:
            result += f"{start.get_data()}\n"
            for e in start.get_edges():
                neighbor: Vertex.Vertex = e.get_end()
                if neighbor not in visitedNodes:
                    visitedNodes.append(neighbor)
                    result = dfs(neighbor, visitedNodes, result)
            return result

        return dfs(start, visitedNodes, result)

    def add_edge(self, v1_name: Vertex.Vertex, v2_name: Vertex.Vertex, weight: int):  #
        weight = int(weight)
        v1, v2 = self.get_vertex_by_value(v1_name), self.get_vertex_by_value(v2_name)
        if v1 == None:
            return f"{v1_name} Node not found"

        if v2 == None:
            return f"{v2_name} Node not found"

        if not self.is_weighted:
            weight = 0
        v1.add_edge(v2, weight)
        if not self.is_directed:
            v2.add_edge(v1, weight)
        return "OK"

    def remove_edge(self, v1_data: Vertex.Vertex, v2_data: Vertex.Vertex):
        v1 = self.get_vertex_by_value(v1_data)
        v2 = self.get_vertex_by_value(v2_data)
        if v1 != None and v2 != None:
            v1.remove_edge_by_vertex(v2, self.get_key_name())

    def is_directed_graph(self) -> bool:
        return self.is_directed

    def is_weighted_graph(self) -> bool:
        return self.is_weighted

    def get_vertices(self) -> list[Vertex.Vertex]:
        return self.vertices

    def get_vertices_str(self) -> str:
        return "\n".join(map(str, self.vertices))

    def get_vertex_by_value(self, value: str):  #
        if self.check_key_name_none:

            for v in self.vertices:
                if v.get_data().get(self.get_key_name()) == value:
                    return v
            return None
        return None

    def print(self):  #
        result = ""
        for v in self.vertices:
            result += v.print(self.is_weighted) + "\n"
        return result

    def dijkistra_distance(self, starting_vertex: Vertex):
        starting_vertex = self.get_vertex_by_value(starting_vertex)
        if starting_vertex == None:
            return -1
        return self.dij.dijkistra_distance_dict(
            self.dij.dijkistra_dicts(self, starting_vertex, self.get_key_name())
        )

    def dijkistra_prev(self, starting_vertex: Vertex):
        starting_vertex = self.get_vertex_by_value(starting_vertex)
        if starting_vertex == None:
            return -1
        return self.dij.dijkistra_prev_dict(
            self.dij.dijkistra_dicts(self, starting_vertex, self.get_key_name()),
            self.get_key_name(),
        )

    def dijkistra_shortest_distance(self, v1_key: str, v2_key: str):
        v1 = self.get_vertex_by_value(v1_key)
        v2 = self.get_vertex_by_value(v2_key)
        if v1 != None and v2 != None:

            return self.dij.shortest_path_between(self, v1, v2, self.get_key_name())
        else:
            return -1


# bus_network = graph(True, False)
# mathura: Vertex.Vertex = bus_network.add_vertex("Mathura")
# Agra: Vertex.Vertex = bus_network.add_vertex("Agra")
# bus_network.add_edge(mathura, Agra, 65)
# bus_network.print()
# print("bfs")
# bus_network.breath_first_search(mathura, list())
# print("dfs")
# bus_network.depth_first_search(Agra, list())

# testGraph: graph = graph(True, True)

# a = testGraph.add_vertex("a")
# b = testGraph.add_vertex("b")
# c = testGraph.add_vertex("c")

# d = testGraph.add_vertex("d")

# e = testGraph.add_vertex("e")
# f = testGraph.add_vertex("f")
# g = testGraph.add_vertex("g")
# testGraph.add_edge(a, b, 3)
# testGraph.add_edge(a, c, 100)
# testGraph.add_edge(a, d, 4)
# testGraph.add_edge(d, c, 3)
# testGraph.add_edge(d, e, 8)
# testGraph.add_edge(e, b, 2)
# testGraph.add_edge(a, f, 10)
# testGraph.add_edge(b, g, 10)
# testGraph.add_edge(e, g, 50)

# dij: dijkistra.dijkistra = dijkistra.dijkistra()
# dij.dijkistra_result_printer(dij.dijkistra_dicts(testGraph, a))
# dij.shortest_path_between(testGraph, a, f)
# # python -m python_redis.models.graph
