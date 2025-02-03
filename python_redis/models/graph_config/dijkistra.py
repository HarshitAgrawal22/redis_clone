from typing import TYPE_CHECKING
from queue import PriorityQueue
from python_redis.models.graph_config.Vertex import Vertex

if TYPE_CHECKING:

    from python_redis.models.graph_config.Edge import Edge


class QueueObject:
    def __init__(self, vertex: Vertex, priority: int):
        self.vertex: Vertex = vertex
        self.priority: int = priority

    def __lt__(self, other: "QueueObject") -> bool:
        """Defines comparison for priority queue based on priority."""
        return self.priority < other.priority

    def __eq__(self, other: object) -> bool:
        """Defines equality based on priority."""
        if not isinstance(other, QueueObject):
            return NotImplemented
        return self.priority == other.priority


class dijkistra:

    def dijkistra_dicts(self, g, starting_vertex: Vertex) -> list[dict]:

        dist_dict: dict[str, int] = dict()

        prev_dict: dict[str, Vertex] = dict()

        queue: PriorityQueue[QueueObject] = PriorityQueue()

        queue.put(QueueObject(starting_vertex, 0))

        for v in g.get_vertices():

            if v != starting_vertex:
                dist_dict[v.get_data()] = 2**63 - 1

            prev_dict[v.get_data()] = Vertex("null")
        dist_dict[starting_vertex.get_data()] = 0

        while not queue.empty():
            current: Vertex = queue.get().vertex

            for e in current.get_edges():
                alternative: int = dist_dict.get(current.get_data()) + e.get_weight()
                neighborValue: str = e.get_end().get_data()

                if alternative < dist_dict.get(neighborValue):
                    dist_dict[neighborValue] = alternative
                    prev_dict[neighborValue] = current
                    queue.put(QueueObject(e.get_end(), dist_dict.get(neighborValue)))

        return [dist_dict, prev_dict]

    def dijkistra_result_printer(self, d: list[dict]):

        print("distances")

        for key, value in d[0].items():
            print(f"{key}: {value}")

        print("previous")
        for key, value in d[1].items():
            print(f"{key}: {value.get_data()}")

    def shortest_path_between(self, g, starting_vertex: Vertex, target_vertex: Vertex):
        dijkistra_dictionaries: list[dict] = self.dijkistra_dicts(
            g=g, starting_vertex=starting_vertex
        )
        dist_dict: dict = dijkistra_dictionaries[0]
        prev_dict: dict[str, Vertex] = dijkistra_dictionaries[1]
        distance = int(dist_dict.get(target_vertex.get_data()))
        print(
            "Shortest Distance Between "
            + str(starting_vertex.get_data() + " and " + str(target_vertex.get_data()))
        )
        print(distance)

        path: list = list()
        v: Vertex = target_vertex

        while v.get_data() != "null":
            path.append(v)
            v = prev_dict.get(v.get_data())

        print("Shortest path:")
        for pathVertex in path:
            print(pathVertex.get_data())
