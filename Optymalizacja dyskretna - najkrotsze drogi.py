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
        weight = random.randint(1, 20)
        G.add_edge(i, i + 1, weight=weight)
    weight = random.randint(1, 20)
    G.add_edge(num_nodes, 1, weight=weight)

    max_possible_edges = num_nodes * (num_nodes - 1)
    num_edges = min(num_edges, max_possible_edges)

    while G.number_of_edges() < num_edges:
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        if u != v and not G.has_edge(u, v):
            weight = random.randint(1, 10)
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

def dijkstra(graph, start_node, end_node):
    # Inicjalizacja odległości do wszystkich wierzchołków jako nieskończoność, a odległość do startowego jako 0
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0

    # Inicjalizacja poprzedników na None
    predecessors = {node: None for node in graph.nodes()}

    # Lista odwiedzonych wierzchołków
    visited = []

    # Pętla główna
    while visited != list(graph.nodes()):
        # Wybieramy wierzchołek z najmniejszą znaną odległością
        current_node = min((set(distances.keys()) - set(visited)), key=distances.get)

        # Dodajemy bieżący wierzchołek do listy odwiedzonych
        visited.append(current_node)

        # Sprawdzamy sąsiednich sąsiadów bieżącego wierzchołka
        for neighbor, weight in graph[current_node].items():
            # Obliczamy nową odległość od początkowego wierzchołka
            new_distance = distances[current_node] + weight['weight']

            # Aktualizujemy odległość i poprzednika, jeśli nowa odległość jest mniejsza
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node

    # Rekonstrukcja najkrótszej ścieżki
    shortest_path = []
    current_node = end_node
    while current_node is not None:
        shortest_path.insert(0, current_node)
        current_node = predecessors[current_node]

    return shortest_path, distances[end_node]

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

# Test funkcji Dijkstry
start_node = int(input("Podaj wierzchołek początkowy: "))
end_node = int(input("Podaj wierzchołek końcowy: "))
shortest_path, distance = dijkstra(graph, start_node, end_node)
print("Najkrótsza ścieżka:", shortest_path)
print("Długość najkrótszej ścieżki:", distance)
