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

def dijkstra(graph, start, target):
    num_nodes = len(graph)
    visited = set()
    dist = [] * num_nodes
    previous = [] * num_nodes

    for i, (_, _) in enumerate(graph.items()):
        dist[i] = float('inf')
        previous[i] = None

    dist[start] = 0

    while not contains(visited, target):
        pass

