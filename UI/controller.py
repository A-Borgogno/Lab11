import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        years = self._model.getAllYears()
        for year in years:
            self._view._ddyear.options.append(ft.dropdown.Option(year))
        colors = self._model.getAllColors()
        for color in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))
        self._view.update_page()



    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        self._view._ddnode.options.clear()
        color = self._view._ddcolor.value
        year = self._view._ddyear.value
        if year == None:
            self._view.create_alert("Scegliere un anno")
            return
        if color == None:
            self._view.create_alert("Scegliere un colore")
            return
        self._view.btn_search.disabled = False
        self._view.txtOut.controls.append(ft.Text("Creazione grafo in corso", weight=ft.FontWeight.BOLD))
        self._view.update_page()

        grafo = self._model.buildGraph(color, year)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Grafo creato correttamente", weight=ft.FontWeight.BOLD))
        self._view.txtOut.controls.append(ft.Text(f"Numero vertici: {grafo.number_of_nodes()} Numero archi: {len(grafo.edges())}"))
        archiPesoMaggiore = []
        i = 0
        for edge in grafo.edges(data=True):
            while i < 3:
                archiPesoMaggiore.append(edge)
                i += 1
            else:
                listaAggiornata = self._aggiungiArco(archiPesoMaggiore, edge)
                archiPesoMaggiore = listaAggiornata
                i += 1
        # print(archiPesoMaggiore)
        for arco in archiPesoMaggiore:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {arco[0]} a {arco[1]}, peso={arco[2]['weight']}"))
        nodiRipetuti = self._cercaNodiRipetuti(archiPesoMaggiore)
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {nodiRipetuti}"))
        self._view.update_page()
        self.fillDDProduct()

    def fillDDProduct(self):
        nodi = self._model._graph.nodes()
        for nodo in nodi:
            self._view._ddnode.options.append(ft.dropdown.Option(nodo))
        self._view.update_page()


    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        nodo = self._view._ddnode.value
        path_lenght = self._model.searchPath(nodo)
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo : {path_lenght}"))
        self._view.update_page()


    def _aggiungiArco(self, listaArchiPesoMaggiore, edge):
        sorted(listaArchiPesoMaggiore, key=lambda w: edge[2]["weight"])
        for arco in listaArchiPesoMaggiore:
            if edge[2]["weight"] > arco[2]["weight"]:
                i = listaArchiPesoMaggiore.index(arco)
                listaArchiPesoMaggiore.insert(i, edge)
                return listaArchiPesoMaggiore[:3]
        return listaArchiPesoMaggiore[:3]


    def _cercaNodiRipetuti(self, listaArchiPesoMaggiore):
        nodi = {}
        for arco in listaArchiPesoMaggiore:
            if arco[0] in nodi.keys():
                nodi[arco[0]] += 1
            else:
                nodi[arco[0]] = 1
            if arco[1] in nodi.keys():
                nodi[arco[1]] += 1
            else:
                nodi[arco[1]] = 1
        nodiRipetuti = []
        for n in nodi:
            if nodi[n] > 1:
                nodiRipetuti.append(n.Product_number)
        return nodiRipetuti

