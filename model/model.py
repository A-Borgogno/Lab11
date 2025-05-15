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
        analizzati = []
        nodoSorgente = self._idMap[int(nodo)]
        self._numSuccessori = len(list(nx.descendants(self._graph, nodoSorgente)))
        print(self._numSuccessori)
        nodi_rimanenti = copy.deepcopy(self._nodes)
        nodi_rimanenti.remove(nodoSorgente)
        self._ricorsione(nodoSorgente, [nodoSorgente], analizzati, nodi_rimanenti)
        return len(self._best)

    def _ricorsione(self, source, precedenti, analizzati, nodi_rimanenti):
        if not nodi_rimanenti or self._viciniAnalizzati(nx.neighbors(self._graph, source), analizzati):
            if len(precedenti) > len(self._best):
                self._best = copy.deepcopy(precedenti)
            return

        for n in list(nx.neighbors(self._graph, source)):
            if n not in analizzati:
                analizzati.append(n)

            if n not in precedenti:
                peso = self._graph.get_edge_data(source, n)['weight']
                if len(precedenti) > 1:
                    peso_prev = self._graph.get_edge_data(precedenti[-2], source)['weight']
                if len(precedenti) > 1:
                    peso_prev = self._graph.get_edge_data(precedenti[-2], source)['weight']
                    if peso >= peso_prev:
                        nuovaLista = copy.deepcopy(nodi_rimanenti)
                        if n in nuovaLista:
                            nuovaLista.remove(n)
                        self._ricorsione(n, copy.deepcopy(precedenti + [n]), copy.deepcopy(analizzati), nuovaLista)
                else:
                    nuovaLista = copy.deepcopy(nodi_rimanenti)
                    if n in nuovaLista:
                        nuovaLista.remove(n)
                    self._ricorsione(n, copy.deepcopy(precedenti + [n]), copy.deepcopy(analizzati), nuovaLista)


    def _viciniAnalizzati(self, vicini, listaNodiAnalizzati):
        for vicino in list(vicini):
            if vicino not in listaNodiAnalizzati:
                return False
        return True

