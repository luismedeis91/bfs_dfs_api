import json

from src.graph.search import dfs_with_stack, is_network_connected


def load_router_scenarios(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        scenarios = json.load(file)

    return scenarios


def get_visit_order(graph, central_router):
    visited = set()
    stack = [central_router]
    order = []

    while stack:
        current_router = stack.pop()

        if current_router in visited:
            continue

        visited.add(current_router)
        order.append(current_router)

        for neighbor in reversed(graph.get(current_router, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def build_visit_trace(graph, central_router):
    visited = set()
    stack = [central_router]
    trace = []

    while stack:
        snapshot_before_pop = list(stack)
        current_router = stack.pop()

        step = {
            "current_router": current_router,
            "stack_before_pop": snapshot_before_pop,
            "stack_after_pop": list(stack),
            "neighbors": list(graph.get(current_router, [])),
            "skipped": current_router in visited,
        }

        if step["skipped"]:
            step["visited_after_step"] = sorted(visited)
            step["stack_after_push"] = list(stack)
            step["pushed_neighbors"] = []
            trace.append(step)
            continue

        visited.add(current_router)
        pushed_neighbors = []

        for neighbor in reversed(graph.get(current_router, [])):
            if neighbor not in visited:
                stack.append(neighbor)
                pushed_neighbors.append(neighbor)

        step["visited_after_step"] = sorted(visited)
        step["stack_after_push"] = list(stack)
        step["pushed_neighbors"] = list(reversed(pushed_neighbors))
        trace.append(step)

    return trace


def get_all_routers(graph):
    all_routers = set(graph.keys())
    for neighbors in graph.values():
        all_routers.update(neighbors)
    return all_routers


def analyze_router_network(graph, central_router, expected_connected=None, scenario_label=None):
    visited = dfs_with_stack(graph, central_router)
    visit_order = get_visit_order(graph, central_router)
    connected = is_network_connected(graph, central_router)
    all_routers = get_all_routers(graph)
    trace = build_visit_trace(graph, central_router)
    missing_routers = sorted(all_routers - visited)
    passed = expected_connected is None or connected == expected_connected

    return {
        "scenario_label": scenario_label,
        "central_router": central_router,
        "visited": visited,
        "visit_order": visit_order,
        "total_routers": len(all_routers),
        "missing_routers": missing_routers,
        "trace": trace,
        "expected_connected": expected_connected,
        "passed": passed,
        "all_visited": visited == all_routers,
        "connected": connected,
    }
