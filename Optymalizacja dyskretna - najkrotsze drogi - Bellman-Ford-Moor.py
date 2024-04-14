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
        weight = random.randint(-5, 10)  # Zakres losowania może być zmieniony
        G.add_edge(i, i + 1, weight=weight)
    weight = random.randint(-5, 10)  # Zakres losowania może być zmieniony
    G.add_edge(num_nodes, 1, weight=weight)

    max_possible_edges = num_nodes * (num_nodes - 1)
    num_edges = min(num_edges, max_possible_edges)

    while G.number_of_edges() < num_edges:
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        if u != v and not G.has_edge(u, v):
            weight = random.randint(-5, 10)  # Zakres losowania może być zmieniony
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

# Algorytm Bellmana-Forda-Moora
def bellman_ford_moore(graph, source):
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())

    # Inicjalizacja odległości od źródła do wszystkich wierzchołków jako nieskończoność
    distance = [float('inf')] * num_nodes
    distance[source - 1] = 0

    # Relaksacja krawędzi
    for _ in range(num_nodes - 1):
        for u, v, weight in graph.edges(data='weight'):
            if distance[u - 1] != float('inf') and distance[u - 1] + weight < distance[v - 1]:
                distance[v - 1] = distance[u - 1] + weight

    # Sprawdzenie na obecność cykli o ujemnej sumie
    for u, v, weight in graph.edges(data='weight'):
        if distance[u - 1] != float('inf') and distance[u - 1] + weight < distance[v - 1]:
            print("Graf zawiera cykl o ujemnej sumie, algorytm Bellmana-Forda-Moora nie działa poprawnie.")
            return None

    return distance

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

# Użycie algorytmu Bellmana-Forda-Moora
while True:
    try:
        source_node = int(input("Podaj numer wierzchołka źródłowego: "))
        shortest_distances = bellman_ford_moore(graph, source_node)
        if shortest_distances:
            print("Najkrótsze odległości od wierzchołka źródłowego:")
            for i, distance in enumerate(shortest_distances):
                print(f"Wierzchołek {i+1}: {distance}")
        break
    except ValueError:
        print("Podano niepoprawny numer wierzchołka źródłowego.")

draw_graph(graph)