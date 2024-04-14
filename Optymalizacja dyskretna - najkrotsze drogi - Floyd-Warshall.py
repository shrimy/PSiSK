import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def generate_connected_directed_graph(num_nodes, num_edges):
    if num_edges < num_nodes:
        raise ValueError("Liczba krawędzi musi być większa lub równa liczbie wierzchołków.")

    G = nx.DiGraph()
    nodes = range(1, num_nodes + 1)
    G.add_nodes_from(nodes)

    for i in range(1, num_nodes):
        weight = random.randint(-5, 10)
        G.add_edge(i, i + 1, weight=weight)
    weight = random.randint(-5, 10)
    G.add_edge(num_nodes, 1, weight=weight)

    max_possible_edges = num_nodes * (num_nodes - 1)
    num_edges = min(num_edges, max_possible_edges)

    while G.number_of_edges() < num_edges:
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        if u != v and not G.has_edge(u, v):
            weight = random.randint(-5, 10)
            G.add_edge(u, v, weight=weight)
            # Jeśli krawędź w drugą stronę już istnieje, ustaw jej wagę na identyczną
            if G.has_edge(v, u):
                G[u][v]['weight'] = G[v][u]['weight']
    return G

def generate_weight_matrix(graph):
    num_nodes = len(graph.nodes())
    weight_matrix = np.zeros((num_nodes, num_nodes))

    for u, v, weight in graph.edges(data='weight'):
        weight_matrix[u-1][v-1] = weight

    return weight_matrix

# Funkcja do rysowania grafu za pomocą NetworkX
def draw_graph(graph):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, 'weight')  # Pobieramy wagi krawędzi
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=12, arrowsize=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)  # Dodajemy etykiety do krawędzi
    plt.title("Wygenerowany graf")
    plt.show()

# Funkcja do wypisywania macierzy incydencji
def print_incidence_matrix(graph):
    incidence_matrix = nx.incidence_matrix(graph, oriented=True).toarray()
    print("Macierz incydencji:")
    print(incidence_matrix)

# Przykładowe użycie funkcji
while True:
    try:
        num_nodes = int(input("Podaj liczbę wierzchołków: "))
        num_edges = int(input("Podaj liczbę krawędzi: "))
        graph = generate_connected_directed_graph(num_nodes, num_edges)
        break
    except ValueError as e:
        print(e)

print_incidence_matrix(graph)
# Generuj i wyświetl macierz wag
weight_matrix = generate_weight_matrix(graph)
print("Macierz wag:")
print(weight_matrix)
draw_graph(graph)

def floyd_warshall(graph):
    num_nodes = len(graph.nodes())
    dist = np.zeros((num_nodes, num_nodes))

    # Inicjalizacja macierzy odległości
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                dist[i][j] = 0
            elif graph.has_edge(i+1, j+1):
                dist[i][j] = graph[i+1][j+1]['weight']
            else:
                dist[i][j] = float('inf')

    # Algorytm Floyda-Warshalla
    for k in range(num_nodes):
        print("Macierz odległości po iteracji", k+1, ":")
        print(dist)
        print()  # Dodaj pusty wiersz dla czytelności
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

# Przykładowe użycie
distances = floyd_warshall(graph)
print("Macierz odległości końcowej:")
print(distances)
draw_graph(graph)