from collections import deque
from operator import contains

from PIL.ImageOps import contain


def bfs(graph, start, target):
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        current_user = path[-1]

        if current_user == target:
            return {"path": path, "distance": len(path) - 1}

        if current_user not in visited:
            visited.add(current_user)

            for neighbor in graph.get(current_user, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited


def dfs_find_path_recursive(graph, start, target, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    if start == target:
        return path

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result_path = dfs_find_path_recursive(graph, neighbor, target, visited, list(path))
            if result_path:
                return result_path

    return None


def dfs_with_stack(graph, start):
    visited = set()
    stack = [start]

    while stack:
        current_router = stack.pop()

        if current_router in visited:
            continue

        visited.add(current_router)

        for neighbor in reversed(graph.get(current_router, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return visited


def is_network_connected(graph, central_router):
    all_routers = set(graph.keys())
    for neighbors in graph.values():
        all_routers.update(neighbors)

    if not all_routers:
        return False

    visited = dfs_with_stack(graph, central_router)
    return visited == all_routers


def find_farthest_pair_bfs(graph):
    if not graph:
        return None

    users = set(graph.keys())
    for follows in graph.values():
        users.update(follows)
    users = list(users)

    farthest_pair = None
    max_distance = 0

    for start_user in users:
        for end_user in users:
            if start_user == end_user:
                continue

            result = bfs(graph, start_user, end_user)
            if result and result["distance"] > max_distance:
                max_distance = result["distance"]
                farthest_pair = {
                    "user1": start_user,
                    "user2": end_user,
                    "path": result["path"],
                    "distance": result["distance"]
                }

    return farthest_pair

def dijkstra(graph, start, target):
    visited = set()
    dist = []
    previous = []

    for _ in graph:
        dist.append(float('inf'))
        previous.append(None)

    dist[start] = 0

    while not contains(visited, target):
        pass


def least_valued_unexplored_vertice(graph, start):
    visited = set()

    for neighbor in graph.get(start, []):
        pass

