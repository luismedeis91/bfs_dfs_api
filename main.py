import sys
import os
from src.api.bluesky_api import login
from src.graph.graph_builder import build_graph
from src.graph.search import bfs, find_farthest_pair_bfs
from src.graph.visualize import visualize_graph

def main():
    logged_in = login()
    if not logged_in:
        print("Warning: Running without authentication. Results might be empty.")
    else:
        print("Logged in successfully.")

    start_user = "rubysecond.bsky.social"
    target_user = "bsky.app"

    print(f"Building graph starting from {start_user} to {target_user}:")
    graph = build_graph(start_user, depth=2, limit=5)

    print(f"Graph size: {len(graph)} users")
    
    result = bfs(graph, start_user, target_user)
    if result:
        print(f"Path found: {' -> '.join(result['path'])}")
        print(f"Distance: {result['distance']} connections")
    else:
        print(f"No path found between {start_user} and {target_user} within depth.")

    print("\nSearching two most distant users in the graph")
    farthest = find_farthest_pair_bfs(graph)
    if farthest:
        print(f"\nMost distant users:")
        print(f"From: {farthest['user1']}")
        print(f"To: {farthest['user2']}")
        print(f"Distance: {farthest['distance']} connections")
        print(f"Path: {' -> '.join(farthest['path'])}")
    else:
        print("\nNo connected pairs found in the graph.")

    # Visualize the graph
    print("\nGenerating graph visualization:")
    path_to_highlight = result['path'] if result else None
    visualize_graph(graph, path=path_to_highlight, title=f"Bluesky Network: {start_user}")

if __name__ == "__main__":
    main()
