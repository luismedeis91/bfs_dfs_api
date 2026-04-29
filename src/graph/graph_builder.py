from src.api.bluesky_api import get_follows


def build_graph(start_user, depth=2, limit=5):
    graph = {}
    visited = set()

    def explore(user, current_depth):
        if current_depth > depth:
            return

        if user in visited:
            return

        visited.add(user)

        try:
            follows = get_follows(user, limit)
            graph[user] = follows

            for next_user in follows:
                explore(next_user, current_depth + 1)

        except Exception:
            graph[user] = []

    explore(start_user, 0)

    return graph
