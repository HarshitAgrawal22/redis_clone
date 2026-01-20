from typing import TYPE_CHECKING
from queue import PriorityQueue
from python_redis.models.graph_config.Vertex import Vertex
from python_redis.models.service_ds.LinkedList import LinkedList
from icecream import ic

ic.configureOutput(prefix="DEBUG: ", includeContext=True)
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

    def dijkistra_dicts(self, g, starting_vertex: Vertex, key: str) -> list[dict]:

        dist_dict: dict[str, int] = dict()

        prev_dict: dict[str, Vertex] = dict()

        queue: PriorityQueue[QueueObject] = PriorityQueue()

        queue.put(QueueObject(starting_vertex, 0))

        for v in g.get_vertices():

            if v != starting_vertex:
                dist_dict[v.get_data()[key]] = 2**63 - 1

            prev_dict[v.get_data()[key]] = Vertex("null")
        dist_dict[starting_vertex.get_data()[key]] = 0

        while not queue.empty():
            current: Vertex = queue.get().vertex

            for e in current.get_edges():

                alternative: int = (
                    dist_dict.get(current.get_data()[key]) + e.get_weight()
                )

                neighborValue: str = e.get_end().get_data()[key]

                if alternative < dist_dict.get(neighborValue):
                    dist_dict[neighborValue] = alternative
                    prev_dict[neighborValue] = current
                    queue.put(QueueObject(e.get_end(), dist_dict.get(neighborValue)))

        return [dist_dict, prev_dict]

    def dijkistra_distance_dict(self, d: list[dict]):

        result = "distances\n"
        for key, value in d[0].items():
            result += f"{key}: {value if value !=9223372036854775807 else '∞'}\n"
        return result

    def dijkistra_prev_dict(self, d: list[dict], key: str):
        result = "previous\n"
        for key, value in d[1].items():
            result += f"{key}: {value.get_data()}\n"
        return result

    def shortest_path_between(
        self, g, starting_vertex: Vertex, target_vertex: Vertex, key: str
    ):
        dijkistra_dictionaries: list[dict] = self.dijkistra_dicts(
            g, starting_vertex, key
        )
        dist_dict: dict = dijkistra_dictionaries[0]
        prev_dict: dict[str, Vertex] = dijkistra_dictionaries[1]
        distance = int(dist_dict.get(target_vertex.get_data().get(key)))
        # print(dist_dict)
        # print(prev_dict)

        path: LinkedList = LinkedList()
        v: Vertex = target_vertex

        while v.get_data() != "null":
            # ic(v.get_data())
            # ic(type(v.get_data()))
            path.add_head(v)

            v = prev_dict.get(v.get_data().get(key))

        print("Shortest path:")
        result = ""
        # result += (
        #     "Shortest Distance Between "
        #     + str(starting_vertex.get_data())
        #     + " and "
        #     + str(target_vertex.get_data())
        #     + "\n"
        # )
        result += str(distance) + "\n"

        while not path.is_empty():
            if path.head.next != None:
                result += str(path.remove_head().get_data().get(key)) + "-->"
            else:
                result += str(path.remove_head().get_data().get(key))

        return result
        # for pathVertex in path:
        #     result += str(pathVertex.get_data().get(key)) + "<--"
        # return reversed(result)
