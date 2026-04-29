from src.graph.graph_builder import build_graph


def test_build_graph_creates_graph_using_fake_api(monkeypatch):
    fake_data = {
        "a.bsky.social": ["b.bsky.social", "c.bsky.social"],
        "b.bsky.social": ["d.bsky.social"],
        "c.bsky.social": [],
        "d.bsky.social": []
    }

    def fake_get_follows(user, limit=5):
        return fake_data.get(user, [])

    monkeypatch.setattr("src.graph.graph_builder.get_follows", fake_get_follows)

    graph = build_graph("a.bsky.social", depth=1, limit=5)

    assert graph == {
        "a.bsky.social": ["b.bsky.social", "c.bsky.social"],
        "b.bsky.social": ["d.bsky.social"],
        "c.bsky.social": []
    }
