import copy
from copy import deepcopy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._best = []
        self._numSuccessori = 0
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
            self._nodes.append(node)
        self._graph.add_nodes_from(nodes)
        # print(self._graph.nodes)
        # print(self._graph.number_of_nodes())
        self.addEdges(year)
        return self._graph

    def addEdges(self, year):
        for node in self._graph.nodes:
            for s in self._graph.nodes:
                if node.Product_number < s.Product_number:
                    res = DAO.verificaNodi(year, node.Product_number, s.Product_number)
                    if res:
                        self._graph.add_edge(node, s, weight=res[0])


    def searchPath(self, nodo):
        analizzati = 0
        nodoSorgente = self._idMap[int(nodo)]
        self._numSuccessori = len(list(nx.descendants(self._graph, nodoSorgente)))
        print(self._numSuccessori)
        self._ricorsione(nodoSorgente, [nodoSorgente], analizzati, self._nodes)
        return len(self._best)


    def _ricorsione(self, source, precedenti, analizzati, nodi_rimanenti):
        if len(nodi_rimanenti)==0:       # condizione terminale
            print(analizzati)
            if len(precedenti)>len(self._best):
                self._best = copy.deepcopy(precedenti)
                return
        else:
            for n in list(nx.neighbors(self._graph, source))[1:]:
                analizzati += 1
                if n not in precedenti:
                    peso = self._graph.get_edge_data(source, n)['weight']
                    if len(precedenti) > 1:
                        if peso >= self._graph.get_edge_data(precedenti[-2], source)['weight']:
                            precedenti.append(n)
                            self._ricorsione(n, precedenti, analizzati, nodi_rimanenti.remove(n))
                            precedenti.pop()
                    else:
                        precedenti.append(n)
                        self._ricorsione(n, precedenti, analizzati, nodi_rimanenti.remove(n))
                        precedenti.pop()
