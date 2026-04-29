from collections import deque


def bfs(graph, start, target):
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        current_user = path[-1]

        if current_user == target:
            return path

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
