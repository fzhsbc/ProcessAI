import networkx as nx


class KnowledgeGraphManager:
    def __init__(self):
        self.graph = nx.MultiDiGraph()


    def add_entity(self, node_id: str, **attrs):
        self.graph.add_node(node_id, **attrs)


    def add_relation(self, src: str, dst: str, relation: str):
        self.graph.add_edge(src, dst, relation=relation)


    def query_neighbors(self, node_id: str):
        return list(self.graph.neighbors(node_id))