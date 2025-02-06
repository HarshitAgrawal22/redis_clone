from python_redis.models.graph_config.Edge import Edge


class Vertex:

    def __init__(self, data: dict):
        self.data: dict = data
        self.edges: list[Edge] = list()

    def add_edge(self, endVertex: "Vertex", weight: int):
        self.edges.append(Edge(self, endVertex, weight))

    def remove_edge(self, end_vertex: Edge):  # testing is required

        self.edges = list(
            filter(lambda edge: not edge.get_end() == (end_vertex), self.edges)
        )

    def get_data(self) -> dict:
        return self.data

    def get_edges(self) -> list:
        return self.edges

    def get_edges_str(self) -> list:
        return f'{self.data}-> {", ".join(map(str, self.edges))}'

    def print(self, show_weight: bool) -> str:
        message: str = ""
        if len(self.edges) == 0:
            message += str(self.data) + " --> \n"
            return message
        for i in range(len(self.edges)):
            if i == 0:
                message += str(self.edges[i].get_start().data) + " --> "
            message += str(self.edges[i].get_end().data)
            if show_weight:
                message += "(" + str(self.edges[i].get_weight()) + ")"
            if i != len(self.edges) - 1:
                message += ",\n"
        return message

    def __str__(self):
        return f"{self.data}"
