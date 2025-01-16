from python_redis.models.graph_config.Edge import Edge


class Vertex:

    def __init__(self, data: str):
        self.data: str = data
        self.edges: list[Edge] = list()

    def add_edge(self, endVertex: "Vertex", weight: int):
        self.edges.append(Edge(self, endVertex, weight))

    def remove_edge(self, end_edge: Edge):  # testing is required

        self.edges = list(
            filter(lambda edge: not edge.get_end() == (end_edge), self.edges)
        )

    def get_data(self):
        return self.data

    def get_edges(self):
        return self.edges

    def print(self, show_weight: bool):
        message: str = ""
        if len(self.edges) == 0:
            print(str(self.data) + " --> ")
            return
        for i in range(len(self.edges)):
            if i == 0:
                message += str(self.edges[i].get_start().data) + " --> "
            message += str(self.edges[i].get_end().data)
            if show_weight:
                message += "(" + str(self.edges[i].get_weight()) + ")"
            if i != len(self.edges) - 1:
                message += ","
        print(message)
