from src.graph.search import bfs, dfs


def test_bfs_finds_shortest_path():
    graph = {
        "a.bsky.social": ["b.bsky.social", "c.bsky.social"],
        "b.bsky.social": ["d.bsky.social"],
        "c.bsky.social": ["d.bsky.social"],
        "d.bsky.social": []
    }

    result = bfs(graph, "a.bsky.social", "d.bsky.social")

    assert result == {"path": ["a.bsky.social", "b.bsky.social", "d.bsky.social"], "distance": 2}


def test_bfs_returns_none_when_path_does_not_exist():
    graph = {
        "a.bsky.social": ["b.bsky.social"],
        "b.bsky.social": [],
        "c.bsky.social": []
    }

    result = bfs(graph, "a.bsky.social", "c.bsky.social")

    assert result is None


def test_dfs_visits_all_reachable_users():
    graph = {
        "a.bsky.social": ["b.bsky.social", "c.bsky.social"],
        "b.bsky.social": ["d.bsky.social"],
        "c.bsky.social": [],
        "d.bsky.social": []
    }

    result = dfs(graph, "a.bsky.social")

    assert result == {
        "a.bsky.social",
        "b.bsky.social",
        "c.bsky.social",
        "d.bsky.social"
    }
