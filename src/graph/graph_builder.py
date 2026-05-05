try:
    from src.api.bluesky_api import get_follows
except ModuleNotFoundError:
    get_follows = None


def build_graph(start_user, depth=2, limit=5):
    if get_follows is None:
        raise ModuleNotFoundError(
            "The optional dependency required to query Bluesky follows is not installed."
        )

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
