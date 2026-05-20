from operator import contains

test_graph = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'C': 6, 'D': 1, 'E': 3},
    'C': {'A': 5, 'B': 6, 'F': 8},
    'D': {'B': 1, 'E': 4},
    'E': {'B': 3, 'D': 4, 'G': 9},
    'F': {'C': 8, 'G': 7},
    'G': {'E': 9, 'F': 7}
}

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

