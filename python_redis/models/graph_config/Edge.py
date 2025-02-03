from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_redis.models.graph_config.Vertex import Vertex


class Edge:
    # it is just an entity to store the edge with its details we need
    def __init__(self, startV, endV, inputWeight):
        self.start: Vertex = startV  # the node from where the edge is starting
        self.end: Vertex = endV  # to where the edge will be ending
        self.weight: int = inputWeight  # weight of the edge

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_weight(self) -> int:
        return self.weight
