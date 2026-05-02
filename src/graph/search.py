from collections import deque


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


def find_farthest_pair_bfs(graph):
    if not graph:
        return None

    # Get all users (both keys and values)
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
