import sys
import os
from src.api.bluesky_api import login
from src.graph.graph_builder import build_graph
from src.graph.search import bfs

def main():
    logged_in = login()
    if not logged_in:
        print("Warning: Running without authentication. Results might be empty.")
    else:
        print("Logged in successfully.")

    start_user = "rubysecond.bsky.social"
    target_user = "bsky.app"

    print(f"Building graph starting from {start_user}...")
    graph = build_graph(start_user, depth=2, limit=5)
    
    print(f"Graph size: {len(graph)} users")
    
    path = bfs(graph, start_user, target_user)
    if path:
        print(f"Path found: {' -> '.join(path)}")
    else:
        print(f"No path found between {start_user} and {target_user} within depth.")

if __name__ == "__main__":
    main()
