from src.graph.search import dfs_with_stack, is_network_connected


CONNECTED_NETWORK = {
    "R1": ["R2", "R3"],
    "R2": ["R1", "R4"],
    "R3": ["R1", "R5"],
    "R4": ["R2", "R5"],
    "R5": ["R3", "R4"]
}


DISCONNECTED_NETWORK = {
    "R1": ["R2"],
    "R2": ["R1", "R3"],
    "R3": ["R2"],
    "R4": ["R5"],
    "R5": ["R4"]
}


def analyze_network(network, central_router, name):
    visited = dfs_with_stack(network, central_router)
    connected = is_network_connected(network, central_router)

    print(name)
    print(f"Roteador central: {central_router}")
    print(f"Roteadores visitados: {sorted(visited)}")
    print(f"Todos os roteadores foram visitados? {visited == set(network.keys())}")
    print(f"Rede conectada? {connected}")
    print()

def main():
    analyze_network(CONNECTED_NETWORK, "R1", "Caso 1 - Rede conectada")
    analyze_network(DISCONNECTED_NETWORK, "R1", "Caso 2 - Rede desconectada")

if __name__ == "__main__":
    main()
