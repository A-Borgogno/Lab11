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
        self._view.txtOut.controls.append(ft.Text("Crezione grafo in corso", weight=ft.FontWeight.BOLD))
        self._view.update_page()
        color = self._view._ddcolor.value
        year = self._view._ddyear.value
        grafo = self._model.buildGraph(color, year)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Grafo creato correttamente", weight=ft.FontWeight.BOLD))
        self._view.txtOut.controls.append(ft.Text(f"Numero vertici: {grafo.number_of_nodes()} Numero archi: {grafo.number_of_edges()}"))
        self._view.update_page()



    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
