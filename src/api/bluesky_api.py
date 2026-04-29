import requests


BASE_URL = "https://public.api.bsky.app/xrpc"


def get_follows(handle, limit=10):
    url = f"{BASE_URL}/app.bsky.graph.getFollows"

    params = {
        "actor": handle,
        "limit": limit
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    follows = []

    for user in data.get("follows", []):
        follows.append(user["handle"])

    return follows
