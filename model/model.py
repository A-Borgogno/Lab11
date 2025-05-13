import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}


    def getAllYears(self):
        return DAO.getAllYears()
    def getAllColors(self):
        return DAO.getAllColors()


    def buildGraph(self, color, year):
        self._graph.clear()
        nodes = DAO.getNodesColor(color)
        for node in nodes:
            self._idMap[node.Product_number] = node
        self._graph.add_nodes_from(nodes)
        print(self._graph.nodes)
        print(self._graph.number_of_nodes())
        self.addEdges(year)

    def addEdges(self, year):
        for node in self._graph.nodes:
            for s in self._graph.neighbors(node):
                if DAO.verificaNodi(year, node.Product_number, s.Product_number):
                    self._graph.add_edge(node, s, weight="")

