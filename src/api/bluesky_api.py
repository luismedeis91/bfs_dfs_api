import os
from atproto import Client

_client = Client()


def login():
    global _client
    h = os.getenv("BSKY_HANDLE")
    p = os.getenv("BSKY_PASSWORD")

    if not h or not p:
        _client = Client(base_url="https://public.api.bsky.app/xrpc")
        return False

    _client.login(h, p)
    return True


def get_follows(handle, limit=10):
    try:
        response = _client.app.bsky.graph.get_follows({"actor": handle, "limit": limit})
        return [user.handle for user in response.follows]
    except Exception:
        return []


def setup_api():
    return login()
