from src.graph.search import bfs, dfs, dfs_with_stack, is_network_connected


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


def test_dfs_with_stack_visits_all_reachable_routers():
    network = {
        "R1": ["R2", "R3"],
        "R2": ["R1", "R4"],
        "R3": ["R1"],
        "R4": ["R2"]
    }

    result = dfs_with_stack(network, "R1")

    assert result == {"R1", "R2", "R3", "R4"}


def test_is_network_connected_returns_true_for_connected_network():
    network = {
        "R1": ["R2", "R3"],
        "R2": ["R1", "R4"],
        "R3": ["R1", "R5"],
        "R4": ["R2"],
        "R5": ["R3"]
    }

    result = is_network_connected(network, "R1")

    assert result is True


def test_is_network_connected_returns_false_for_disconnected_network():
    network = {
        "R1": ["R2"],
        "R2": ["R1", "R3"],
        "R3": ["R2"],
        "R4": ["R5"],
        "R5": ["R4"]
    }

    result = is_network_connected(network, "R1")

    assert result is False
