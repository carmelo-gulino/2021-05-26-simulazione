import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.soluzioni = None
        self.best_sol = None
        self.cities = DAO.get_all_cities()
        self.graph = None

    def build_graph(self, city, year):
        self.graph = nx.DiGraph()
        nodes = DAO.get_nodes(city, year)
        self.graph.add_nodes_from(nodes)
        for b1 in self.graph:
            for b2 in self.graph:
                peso = b1.media - b2.media
                if peso < 0:
                    self.graph.add_edge(b1, b2, weight=abs(peso))
                elif peso > 0:
                    self.graph.add_edge(b2, b1, weight=abs(peso))

    def get_best_locale(self):
        best_locale, best_bilancio = 0, 0
        for b in self.graph.nodes:
            bilancio = self.get_bilancio(b)
            if bilancio > best_bilancio:
                best_bilancio = bilancio
                best_locale = b
        return best_locale

    def get_bilancio(self, locale):
        u = 0
        e = 0
        for usc in self.graph.successors(locale):
            u += self.graph[locale][usc]["weight"]
        for entr in self.graph.predecessors(locale):
            e += self.graph[entr][locale]["weight"]
        return e - u

    def get_graph_details(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def get_percorso(self, partenza, arrivo, soglia):
        self.soluzioni = []
        if arrivo in self.graph.successors(partenza):
            self.best_sol = [partenza, arrivo]
            return self.best_sol
        for s in self.graph.successors(partenza):
            parziale = [partenza, s]
            self.ricorsione(parziale, arrivo, soglia)
            parziale.pop()
        self.soluzioni.sort(key=lambda x: len(x))
        if len(self.soluzioni) == 0:
            return None
        self.best_sol = self.soluzioni[0]
        return self.best_sol

    def ricorsione(self, parziale, arrivo, soglia):
        ultimo = parziale[-1]
        if parziale[-1] == arrivo:
            self.soluzioni.append(copy.deepcopy(parziale))
            print(parziale)
        for usc in self.graph.successors(ultimo):
            if usc not in parziale and self.graph[ultimo][usc]["weight"] >= soglia:
                parziale.append(usc)
                self.ricorsione(parziale, arrivo, soglia)
                parziale.pop()
