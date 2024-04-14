import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import time

def generate_connected_directed_graph(num_nodes, num_edges):
    if num_edges < num_nodes:
        raise ValueError("Liczba krawędzi musi być większa lub równa liczbie wierzchołków.")

    G = nx.DiGraph()
    nodes = range(1, num_nodes + 1)
    G.add_nodes_from(nodes)

    for i in range(1, num_nodes):
        weight = random.randint(1, 20)  # Zakres losowania może być zmieniony
        G.add_edge(i, i + 1, weight=weight)
    weight = random.randint(1, 20)  # Zakres losowania może być zmieniony
    G.add_edge(num_nodes, 1, weight=weight)

    max_possible_edges = num_nodes * (num_nodes - 1)
    num_edges = min(num_edges, max_possible_edges)

    while G.number_of_edges() < num_edges:
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        if u != v and not G.has_edge(u, v):
            weight = random.randint(1, 20)  # Zakres losowania może być zmieniony
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


# Algorytm Dijkstry
def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[source] = 0
    visited = set()

    while len(visited) < len(graph.nodes()):
        current_node = min((node for node in graph.nodes() if node not in visited), key=lambda node: distances[node])
        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distances[neighbor] = min(distances[neighbor], distances[current_node] + weight['weight'])

    return distances

# Algorytm Forda-Bellmana-Moora
def bellman_ford_moore(graph, source):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[source] = 0

    for _ in range(len(graph.nodes()) - 1):
        for u, v, weight in graph.edges(data='weight'):
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    return distances

# Algorytm Floyda-Warshalla
def floyd_warshall(graph):
    num_nodes = len(graph.nodes())
    distances = np.full((num_nodes, num_nodes), float('inf'))

    for node in graph.nodes():
        distances[node-1][node-1] = 0

    for u, v, weight in graph.edges(data='weight'):
        distances[u-1][v-1] = weight

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

    return distances

# Pomiar czasu wykonania dla każdego z algorytmów
start_time = time.time()
dijkstra_distances = dijkstra(graph, 1)
dijkstra_time = time.time() - start_time

start_time = time.time()
bellman_ford_distances = bellman_ford_moore(graph, 1)
bellman_ford_time = time.time() - start_time

start_time = time.time()
floyd_warshall_distances = floyd_warshall(graph)
floyd_warshall_time = time.time() - start_time

# Wyświetlenie wyników
print("Algorytm Dijkstry:")
print(dijkstra_distances)
print("Czas wykonania: %.6f sekund" % dijkstra_time)
print()

print("Algorytm Forda-Bellmana-Moora:")
print(bellman_ford_distances)
print("Czas wykonania: %.6f sekund" % bellman_ford_time)
print()

print("Algorytm Floyda-Warshalla:")
print(floyd_warshall_distances)
print("Czas wykonania: %.6f sekund" % floyd_warshall_time)

