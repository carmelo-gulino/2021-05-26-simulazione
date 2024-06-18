import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.best_locale = None
        self.chosen_locale = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dds(self):
        for y in range(2005, 2014):
            self.view.dd_year.options.append(ft.dropdown.Option(f"{y}"))
        for c in self.model.cities:
            self.view.dd_city.options.append(ft.dropdown.Option(f"{c}"))

    def handle_crea_grafo(self, e):
        if self.view.dd_city.value is None or self.view.dd_year.value is None:
            self.view.create_alert("Selezionare una città e un anno")
            return
        city = self.view.dd_city.value
        year = int(self.view.dd_year.value)
        self.model.build_graph(city, year)
        self.fill_dd_locale()
        self.view.txt_result.controls.clear()
        nodi, archi = self.model.get_graph_details()
        self.view.txt_result.controls.append(ft.Text(f"Grafo con {nodi} nodi e {archi} archi creato"))
        self.view.update_page()

    def handle_locale_migliore(self, e):
        if self.model.graph is None:
            self.view.create_alert("Creare prima un grafo")
            return
        self.best_locale = self.model.get_best_locale()
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(
            ft.Text(f"Il migliore locale in cui passare la serata è {self.best_locale}"))
        self.view.update_page()
        
    def fill_dd_locale(self):
        for b in self.model.graph.nodes:
            self.view.dd_locale.options.append(ft.dropdown.Option(data=b, text=b, on_click=self.choose_locale))
            
    def choose_locale(self, e):
        if e.control.data is None:
            self.chosen_locale = None
        self.chosen_locale = e.control.data

    def handle_percorso(self, e):
        if self.model.graph is None:
            self.view.create_alert("Creare prima un grafo")
            return
        if self.chosen_locale is None:
            self.view.create_alert("Selezionare un locale")
            return
        try:
            soglia = float(self.view.txt_soglia.value)
        except ValueError:
            self.view.create_alert("Inserire un numero decimale tra 0 e 1")
            return
        path = self.model.get_percorso(self.chosen_locale, self.best_locale, soglia)
        self.view.txt_result.controls.clear()
        if path is None:
            self.view.txt_result.controls.append(ft.Text(f"Non esiste un percorso minimo"))
        else:
            self.view.txt_result.controls.append(ft.Text(f"Il percorso minimo con i migliori locali è: "))
            for p in path:
                self.view.txt_result.controls.append(ft.Text(f"{p}"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
