import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def generuj_graf(l_wierzcholkow, l_krawedzi):
    # Funkcja generująca losowy graf skierowany z wagami na krawędziach
    if l_krawedzi < l_wierzcholkow:
        raise ValueError("Liczba krawędzi musi być większa lub równa liczbie wierzchołków.")

    G = nx.DiGraph()
    nodes = range(1, l_wierzcholkow + 1)
    G.add_nodes_from(nodes)

    # Dodanie losowych krawędzi między kolejnymi wierzchołkami
    for i in range(1, l_wierzcholkow):
        waga = random.randint(-5, 10)  # Zakres losowania wag krawędzi
        G.add_edge(i, i + 1, weight=waga)
    waga = random.randint(-5, 10)  # Zakres losowania wag krawędzi
    G.add_edge(l_wierzcholkow, 1, weight=waga)

    # Ustalenie maksymalnej liczby krawędzi i wygenerowanie losowych krawędzi
    maks_krawedzi = l_wierzcholkow * (l_wierzcholkow - 1)
    l_krawedzi = min(l_krawedzi, maks_krawedzi)

    while G.number_of_edges() < l_krawedzi:
        u = random.randint(1, l_wierzcholkow)
        v = random.randint(1, l_wierzcholkow)
        if u != v and not G.has_edge(u, v):
            waga = random.randint(-5, 10)  # Zakres losowania wag krawędzi
            G.add_edge(u, v, weight=waga)
            # Jeśli krawędź w drugą stronę już istnieje, ustaw jej wagę na identyczną
            if G.has_edge(v, u):
                G[u][v]['weight'] = G[v][u]['weight']
    return G

def generuj_macierz_wag(graf):
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

def floyd_warshall(graf):
    # Algorytm Floyd-Warshall dla wyznaczania najkrótszych ścieżek między wszystkimi parami wierzchołków
    l_wierzcholkow = len(graf.nodes())
    odleglosc = np.zeros((l_wierzcholkow, l_wierzcholkow))

    # Inicjalizacja macierzy odległości
    for i in range(l_wierzcholkow):
        for j in range(l_wierzcholkow):
            if i == j:
                odleglosc[i][j] = 0
            elif graf.has_edge(i + 1, j + 1):
                odleglosc[i][j] = graf[i + 1][j + 1]['weight']
            else:
                odleglosc[i][j] = float('inf')

    # Algorytm Floyda-Warshalla
    for k in range(l_wierzcholkow):
        print("Macierz odległości po iteracji", k+1, ":")
        print(odleglosc)
        print()  # Dodaj pusty wiersz dla czytelności
        for i in range(l_wierzcholkow):
            for j in range(l_wierzcholkow):
                if odleglosc[i][k] + odleglosc[k][j] < odleglosc[i][j]:
                    odleglosc[i][j] = odleglosc[i][k] + odleglosc[k][j]

    return odleglosc

# Przykładowe użycie funkcji
while True:
    try:
        l_wierzcholkow = int(input("Podaj liczbę wierzchołków: "))
        l_krawedzi = int(input("Podaj liczbę krawędzi: "))
        graf = generuj_graf(l_wierzcholkow, l_krawedzi)
        break
    except ValueError as e:
        print(e)

# Wypisanie macierzy incydencji dla wygenerowanego grafu
wypisz_macierz_incydencji(graf)

# Generuj i wyświetl macierz wag
macierz_wag = generuj_macierz_wag(graf)
print("Macierz wag:")
print(macierz_wag)

# Rysowanie wygenerowanego grafu
rysuj_graf(graf)

# Wykonanie algorytmu Floyd-Warshalla i wyświetlenie macierzy odległości
odleglosc = floyd_warshall(graf)
print("Macierz odległości końcowej:")
print(odleglosc)

# Ponowne rysowanie wygenerowanego grafu
rysuj_graf(graf)
