import numpy as np
import random
import matplotlib.pyplot as plt
from operator import contains

adj_matrix = np.array([
    [0, 2, -1, 8, -1],
    [-1, 0, 3, -1, -1],
    [-1, -1, 0, -1, 1],
    [-1, -1, 4, 0, -1],
    [-1, -1, -1, 5, 0]
], dtype=float)

# transforma -1 em inf
for l, c in np.ndindex(adj_matrix.shape):
    if adj_matrix[l, c] == -1:
        adj_matrix[l, c] = float('inf')

def floyd_warshall(graph, start, target):
    inf = float('inf')
    n = len(graph)
    dist = graph.copy()
    next = [[-1 if graph[i][j] == inf else j for j in range(n)] for i in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != inf and dist[k][j] != inf:
                    caminho_com_intermediario = dist[i][k] + dist[k][j]

                    if caminho_com_intermediario < dist[i][j]:
                        next[i][j] = next[i][k]

                    dist[i][j] = min(dist[i][j], caminho_com_intermediario)

    custo = dist[start][target]

    if custo == inf:
        print(f"Não existe caminho ligando o vértice {start} ao vértice {target}.")
    else:
        print(f"Custo total do caminho ligando o vértice {start} ao vértice {target} igual à: {custo}.")

    print("Matriz de distancias")
    print(dist)
    print("Matriz de anteriores")
    print(np.array(next))

floyd_warshall(adj_matrix, 0, 4)
