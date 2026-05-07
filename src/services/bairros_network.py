import json
from src.graph.search import dfs_find_path_recursive

def load_bairros_network(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("bairros_network", {})

def find_route_between_bairros(graph, start_node, target_node):
    return dfs_find_path_recursive(graph, start_node, target_node)

def analyze_bairros_network(graph, origin, destination):
    path = find_route_between_bairros(graph, origin, destination)
    all_cities = sorted(list(graph.keys()))
    
    return {
        "origin": origin,
        "destination": destination,
        "path_found": path,
        "total_cities": len(all_cities),
        "available_cities": all_cities,
        "success": path is not None
    }

def format_route_output(analysis_result):
    """Formata o resultado."""
    if analysis_result["success"]:
        route_str = " -> ".join(analysis_result["path_found"])
        return f"Caminho encontrado de {analysis_result['origin']} até {analysis_result['destination']}:\n{route_str}"
    else:
        return f"Não foi possível encontrar um caminho de {analysis_result['origin']} até {analysis_result['destination']}."
