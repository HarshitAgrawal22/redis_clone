import threading
from python_redis.models.service_ds.LinkedList import LinkedList, Node
from python_redis.models.graph_config import Vertex, Edge, dijkistra


class graph:
    def __init__(self, is_weighted: int, is_directed: int):
        self.vertices: list[Vertex.Vertex] = list()
        self.is_directed: bool = is_directed
        self.is_weighted: bool = is_weighted
        self.key_name: str = None

    @staticmethod
    def new_graph():  #
        return graph(True, True)

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
            print(f"{temp_dict} => temp_dict")

            if temp_dict.get(self.get_key_name()) != None:
                new_vertex: Vertex.Vertex = Vertex.Vertex(temp_dict)
                self.vertices.append(new_vertex)
                print("added to list")
                return new_vertex
            else:
                return None
        else:
            return None

    def remove_vertex(self, data: dict):
        targetVertex: Vertex
        for v in self.vertices:
            if v.get_data().get(self.get_key_name()) == data.get(self.get_key_name()):
                targetVertex = v
                self.remove_edge(v)
                self.vertices.remove(v)
            else:
                for e in v.get_edges():
                    if e.get_end() == targetVertex:
                        v.remove_edge(e)

    def breadth_first_search(
        self, start: str, visited_nodes: list[Vertex.Vertex]
    ) -> str:
        result = ""
        visited_queue: LinkedList = LinkedList()
        visited_queue.add_last(self.get_vertex_by_value(start))
        visited_queue.display()
        while not visited_queue.is_empty():
            current: Vertex.Vertex = visited_queue.remove_head()
            result += f"{current.get_data()}"

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

        def dfs(
            start: Vertex.Vertex, visitedNodes: list[Vertex.Vertex], result: str
        ) -> str:
            result += f"{start.get_data()}"
            for e in start.get_edges():
                neighbor: Vertex.Vertex = e.get_end()
                if neighbor not in visitedNodes:
                    visitedNodes.append(neighbor)
                    dfs(neighbor, visitedNodes)
            return result

        return dfs(start, visitedNodes, result)

    def add_edge(self, v1_name: Vertex.Vertex, v2_name: Vertex.Vertex, weight: int):  #
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

    def remove_edge(self, v1: Vertex.Vertex, v2: Vertex.Vertex):
        v1.remove_edge(v2)

    def is_directed_graph(self) -> bool:
        return self.is_directed

    def is_weighted_graph(self) -> bool:
        return self.is_weighted

    def get_vertices(self) -> list[Vertex.Vertex]:
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
