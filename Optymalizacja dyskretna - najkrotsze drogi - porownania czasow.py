import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import time

def generuj_graf(l_wierzcholkow, l_krawedzi):
    # Funkcja generująca losowy graf skierowany z wagami na krawędziach
    if l_krawedzi < l_wierzcholkow:
        raise ValueError("Liczba krawędzi musi być większa lub równa liczbie wierzchołków.")

    G = nx.DiGraph()
    nodes = range(1, l_wierzcholkow + 1)
    G.add_nodes_from(nodes)

    # Dodanie losowych krawędzi między kolejnymi wierzchołkami
    for i in range(1, l_wierzcholkow):
        waga = random.randint(1, 20)  # Zakres losowania wag krawędzi
        G.add_edge(i, i + 1, weight=waga)
    waga = random.randint(1, 20)  # Zakres losowania wag krawędzi
    G.add_edge(l_wierzcholkow, 1, weight=waga)

    # Ustalenie maksymalnej liczby krawędzi i wygenerowanie losowych krawędzi
    maks_krawedzi = l_wierzcholkow * (l_wierzcholkow - 1)
    l_krawedzi = min(l_krawedzi, maks_krawedzi)

    while G.number_of_edges() < l_krawedzi:
        u = random.randint(1, l_wierzcholkow)
        v = random.randint(1, l_wierzcholkow)
        if u != v and not G.has_edge(u, v):
            waga = random.randint(1, 20)  # Zakres losowania wag krawędzi
            G.add_edge(u, v, weight=waga)
            # Jeśli krawędź w drugą stronę już istnieje, ustaw jej wagę na identyczną
            if G.has_edge(v, u):
                G[u][v]['weight'] = G[v][u]['weight']
    return G

def generate_weight_matrix(graf):
    # Generowanie macierzy wag na podstawie danego grafu
    l_wierzcholkow = len(graf.nodes())
    macierz_wag = np.zeros((l_wierzcholkow, l_wierzcholkow))

    for u, v, weight in graf.edges(data='weight'):
        macierz_wag[u-1][v-1] = weight

    return macierz_wag

# Funkcja do rysowania grafu za pomocą NetworkX
def rysuj_graf(graf):
    # Rysowanie grafu wraz z wagami krawędzi
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graf)
    edge_labels = nx.get_edge_attributes(graf, 'weight')  # Pobranie wag krawędzi
    nx.draw(graf, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, arrowsize=10)
    nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels)  # Dodanie etykiet do krawędzi
    plt.title("Wygenerowany graf")
    plt.show()

# Funkcja do wypisywania macierzy incydencji
def wypisz_macierz_incydencji(graf):
    # Wypisanie macierzy incydencji dla danego grafu
    macierz_incydencji = nx.incidence_matrix(graf, oriented=True).toarray()
    print("Macierz incydencji:")
    print(macierz_incydencji)

# Algorytm Dijkstry
def dijkstra(graf, wierzcholek_startowy):
    # Algorytm Dijkstry dla wyznaczania najkrótszych ścieżek z danego wierzchołka startowego do pozostałych wierzchołków
    odleglosci = {node: float('inf') for node in graf.nodes()}
    odleglosci[wierzcholek_startowy] = 0
    odwiedzone = set()

    while len(odwiedzone) < len(graf.nodes()):
        aktualny_wierzcholek = min((node for node in graf.nodes() if node not in odwiedzone), key=lambda node: odleglosci[node])
        odwiedzone.add(aktualny_wierzcholek)

        for sasiad, waga in graf[aktualny_wierzcholek].items():
            odleglosci[sasiad] = min(odleglosci[sasiad], odleglosci[aktualny_wierzcholek] + waga['weight'])

    return odleglosci

# Algorytm Forda-Bellmana-Moora
def bellman_ford_moore(graf, wierzcholek_startowy):
    # Algorytm Forda-Bellmana-Moora dla wyznaczania najkrótszych ścieżek z danego wierzchołka startowego do pozostałych wierzchołków
    odleglosci = {node: float('inf') for node in graf.nodes()}
    odleglosci[wierzcholek_startowy] = 0

    for _ in range(len(graf.nodes()) - 1):
        for u, v, waga in graf.edges(data='weight'):
            if odleglosci[u] != float('inf') and odleglosci[u] + waga < odleglosci[v]:
                odleglosci[v] = odleglosci[u] + waga

    return odleglosci

# Algorytm Floyda-Warshalla
def floyd_warshall(graf):
    # Algorytm Floyda-Warshalla dla wyznaczania najkrótszych ścieżek między wszystkimi parami wierzchołków
    l_wierzcholkow = len(graf.nodes())
    odleglosci = np.full((l_wierzcholkow, l_wierzcholkow), float('inf'))

    for wierzcholek in graf.nodes():
        odleglosci[wierzcholek-1][wierzcholek-1] = 0

    for u, v, waga in graf.edges(data='weight'):
        odleglosci[u-1][v-1] = waga

    for k in range(l_wierzcholkow):
        for i in range(l_wierzcholkow):
            for j in range(l_wierzcholkow):
                odleglosci[i][j] = min(odleglosci[i][j], odleglosci[i][k] + odleglosci[k][j])

    return odleglosci

# Przykładowe użycie funkcji
while True:
    try:
        l_wierzcholkow = int(input("Podaj liczbę wierzchołków: "))
        l_krawedzi = int(input("Podaj liczbę krawędzi: "))
        graf = generuj_graf(l_wierzcholkow, l_krawedzi)
        break
    except ValueError as e:
        print(e)

wypisz_macierz_incydencji(graf)

# Generuj i wyświetl macierz wag
macierz_wag = generate_weight_matrix(graf)
print("Macierz wag:")
print(macierz_wag)
rysuj_graf(graf)

# Pomiar czasu wykonania dla każdego z algorytmów
czas_start = time.time()
dijkstra_odleglosci = dijkstra(graf, 1)
dijkstra_czas = time.time() - czas_start

czas_start = time.time()
bellman_ford_odleglosci = bellman_ford_moore(graf, 1)
bellman_ford_czas = time.time() - czas_start

czas_start = time.time()
floyd_warshall_odleglosci = floyd_warshall(graf)
floyd_warshall_czas = time.time() - czas_start

# Wyświetlenie wyników
print("Algorytm Dijkstry:")
print(dijkstra_odleglosci)
print("Czas wykonania: %.6f sekund" % dijkstra_czas)
print()

print("Algorytm Forda-Bellmana-Moora:")
print(bellman_ford_odleglosci)
print("Czas wykonania: %.6f sekund" % bellman_ford_czas)
print()

print("Algorytm Floyda-Warshalla:")
print(floyd_warshall_odleglosci)
print("Czas wykonania: %.6f sekund" % floyd_warshall_czas)
