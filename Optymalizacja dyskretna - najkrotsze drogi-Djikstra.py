import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def generuj_graf(l_wierzcholkow, l_krawedzi):
    # Sprawdzenie, czy liczba krawędzi jest wystarczająca
    if l_krawedzi < l_wierzcholkow:
        raise ValueError("Liczba krawędzi musi być większa lub równa liczbie wierzchołków.")

    G = nx.DiGraph()
    nodes = range(1, l_wierzcholkow + 1)
    G.add_nodes_from(nodes)

    # Dodawanie krawędzi między kolejnymi wierzchołkami
    for i in range(1, l_wierzcholkow):
        waga = random.randint(1, 20)
        G.add_edge(i, i + 1, weight=waga)
    waga = random.randint(1, 20)
    G.add_edge(l_wierzcholkow, 1, weight=waga)

    # Ustalenie maksymalnej liczby krawędzi i wygenerowanie losowych krawędzi
    maks_krawedzi = l_wierzcholkow * (l_wierzcholkow - 1)
    l_krawedzi = min(l_krawedzi, maks_krawedzi)

    while G.number_of_edges() < l_krawedzi:
        u = random.randint(1, l_wierzcholkow)
        v = random.randint(1, l_wierzcholkow)
        if u != v and not G.has_edge(u, v):
            waga = random.randint(1, 10)
            G.add_edge(u, v, weight=waga)
            # Jeśli krawędź w drugą stronę już istnieje, ustaw jej wagę na identyczną
            if G.has_edge(v, u):
                G[u][v]['weight'] = G[v][u]['weight']
    return G

def generuj_macierz_wag(graf):
    l_wierzcholkow = len(graf.nodes())
    macierz_wag = np.zeros((l_wierzcholkow, l_wierzcholkow))

    for u, v, weight in graf.edges(data='weight'):
        macierz_wag[u-1][v-1] = weight

    return macierz_wag

# Funkcja do rysowania grafu za pomocą NetworkX
def rysuj_graf(graf):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graf)
    edge_labels = nx.get_edge_attributes(graf, 'weight')  # Pobieramy wagi krawędzi
    nx.draw(graf, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, arrowsize=10)
    nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels)  # Dodajemy etykiety do krawędzi
    plt.title("Wygenerowany graf")
    plt.show()

# Funkcja do wypisywania macierzy incydencji
def wypisz_macierz_incydencji(graf):
    macierz_incydencji = nx.incidence_matrix(graf, oriented=True).toarray()
    print("Macierz incydencji:")
    print(macierz_incydencji)

def dijkstra(graf, wierzcholek_startowy):
    # Inicjalizacja odległości do wszystkich wierzchołków jako nieskończoność, a odległość do startowego jako 0
    odleglosci = {node: float('inf') for node in graf.nodes()}
    odleglosci[wierzcholek_startowy] = 0

    # Lista odwiedzonych wierzchołków
    odwiedzone = []

    # Pętla główna
    while odwiedzone != list(graf.nodes()):
        # Wybieramy wierzchołek z najmniejszą znaną odległością spośród nieodwiedzonych
        nieodwiedzone = set(odleglosci.keys()) - set(odwiedzone)
        nieodwiedzone_odleglosc = {node: odleglosci[node] for node in nieodwiedzone}
        if not nieodwiedzone_odleglosc:
            break
        aktualny_wierzcholek = min(nieodwiedzone_odleglosc, key=nieodwiedzone_odleglosc.get)

        # Dodajemy bieżący wierzchołek do listy odwiedzonych
        odwiedzone.append(aktualny_wierzcholek)

        # Sprawdzamy sąsiednich sąsiadów bieżącego wierzchołka
        for sasiad, waga in graf[aktualny_wierzcholek].items():
            # Obliczamy nową odległość od początkowego wierzchołka
            nowa_odleglosc = odleglosci[aktualny_wierzcholek] + waga['weight']

            # Aktualizujemy odległość, jeśli nowa odległość jest mniejsza
            if nowa_odleglosc < odleglosci[sasiad]:
                odleglosci[sasiad] = nowa_odleglosc

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

# Dodanie komentarza
wypisz_macierz_incydencji(graf)
# Generuj i wyświetl macierz wag
macierz_wag = generuj_macierz_wag(graf)
print("Macierz wag:")
print(macierz_wag)
rysuj_graf(graf)

# Test funkcji Dijkstry
wierzcholek_startowy = int(input("Podaj wierzchołek początkowy: "))
odleglosc = dijkstra(graf, wierzcholek_startowy)

print("Koszty dotarcia do każdego wierzchołka z wierzchołka źródłowego:")
for node, distance in odleglosc.items():
    print(f"Wierzchołek {node}: {distance}")

rysuj_graf(graf)
