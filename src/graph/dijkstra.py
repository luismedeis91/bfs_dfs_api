import numpy as np
import random
import matplotlib.pyplot as plt
from operator import contains

def create_adj_matrix(vertices, edges, weights, undirected):
    matrix = np.zeros((vertices, vertices), dtype=int)
    for i in range(len(edges)):
        u, v = edges[i]
        weight = weights[i]
        if undirected:
            matrix[u][v] = weight
            matrix[v][u] = weight
        else:
            matrix[u][v] = weight
    return matrix

estados = [
    "AC", "AM", "RR", "PA", "AP", "MA", "TO", "PI", "CE", "RN",
    "PB", "PE", "AL", "SE", "BA", "MG", "ES", "RJ", "SP", "PR",
    "SC", "RS", "MS", "GO", "MT", "DF", "RO"
]

nodes = 27
edges = [(0,1),(0,26),(1,26),(1,24),(1,2),(1,3),(2,3),(3,4),(3,5),(3,6),(3,24),(5,6),(5,7),(7,6),(7,8),(7,11),(7,14),(8,9),(8,10),(8,11),(9,10),(10,11),(11,12),(11,14),(12,14),(12,13),(13,14),(6,14),(6,23),(6,24),(14,15),(14,16),(14,23),(15,25),(15,22),(15,18),(15,17),(15,16),(16,17),(17,18),(18,22),(18,19),(19,20),(19,22),(20,21),(22,23),(22,24),(23,25),(23,24),(23,15),(24,26),(25,15)]
weights = [
    2, 5, 3, 8, 4, 7, 1, 9, 6, 2, 5, 3, 8, 4, 7, 1, 9, 6, 2, 5,
    3, 8, 4, 7, 1, 9, 6, 2, 5, 3, 8, 4, 7, 1, 9, 6, 2, 5, 3, 8,
    4, 7, 1, 9, 6, 2, 5, 3, 8, 4, 7, 1
]
undirected = True
adj_matrix = create_adj_matrix(nodes, edges, weights, undirected)
degrees = adj_matrix.sum(axis=1)
min_degree = degrees.min()
max_degree = degrees.max()

test_graph = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'C': 6, 'D': 1, 'E': 3},
    'C': {'A': 5, 'B': 6, 'F': 8},
    'D': {'B': 1, 'E': 4},
    'E': {'B': 3, 'D': 4, 'G': 9},
    'F': {'C': 8, 'G': 7},
    'G': {'E': 9, 'F': 7}
}

def dijkstra(graph, start):
    num_nodes = len(graph)
    visited = set()
    dist = {}
    previous = {}

    for node in graph:
        dist[node] = float('inf')
        previous[node] = None

    dist[start] = 0

    while len(visited) != len(graph):
        current = None
        menor_distancia = float('inf')

        for node in graph:
            if node not in visited and dist[node] < menor_distancia:
                menor_distancia = dist[node]
                current = node

        if current is None:
            break

        visited.add(current)

        for neighbor, weight in graph[current].items():
            if neighbor not in visited:
                nova_distancia = dist[current] + weight

                if nova_distancia < dist[neighbor]:
                    dist[neighbor] = nova_distancia
                    previous[neighbor] = current

    return dist, previous


distancias, anteriores = dijkstra(test_graph, 'A')

print(distancias)
print(anteriores)

def dijkstra_mapa(graph, start, target):
    num_nodes = len(graph)
    visited = set()
    dist = {}
    previous = {}

    for node in graph:
        dist[node] = float('inf')
        previous[node] = None

    dist[start] = 0

    while not contains(visited, target):
        current = None
        menor_distancia = float('inf')

        for node in graph:
            if node not in visited and dist[node] < menor_distancia:
                menor_distancia = dist[node]
                current = node

        if current is None:
            break

        visited.add(current)

        for neighbor, weight in graph[current].items():
            if neighbor not in visited:
                nova_distancia = dist[current] + weight

                if nova_distancia < dist[neighbor]:
                    dist[neighbor] = nova_distancia
                    previous[neighbor] = current

    path = []
    current = previous.get(target)
    path.append(target)
    while current != start:
        path.append(current)
        current = previous.get(current)
    path.append(start)

    cost = dist.get(target)

    return dist, previous, path, cost

distancias, anteriores, path, cost = dijkstra_mapa(test_graph, 'A', 'D')
print(distancias)
print(anteriores)
print(path)
print(cost)
