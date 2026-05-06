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


def build_neighborhood_monitor(all_routers, visited, router_profiles):
    grouped = {}

    for router in sorted(all_routers):
        profile = router_profiles.get(router, {})
        neighborhood = profile.get("neighborhood", "Nao mapeado")
        risk_score = profile.get("risk_score", 5)
        criticality = profile.get("criticality", "media")

        group = grouped.setdefault(
            neighborhood,
            {
                "neighborhood": neighborhood,
                "routers": [],
                "visited": 0,
                "missing": 0,
                "avg_risk": 0,
                "max_risk": 0,
                "critical_routers": 0,
                "status": "estavel",
            },
        )

        group["routers"].append(router)
        group["avg_risk"] += risk_score
        group["max_risk"] = max(group["max_risk"], risk_score)
        if criticality == "alta":
            group["critical_routers"] += 1
        if router in visited:
            group["visited"] += 1
        else:
            group["missing"] += 1

    monitored = []
    for neighborhood, group in grouped.items():
        total = len(group["routers"])
        group["avg_risk"] = round(group["avg_risk"] / total, 1) if total else 0
        coverage = round((group["visited"] / total) * 100, 1) if total else 0
        group["coverage_pct"] = coverage
        if group["missing"] > 0:
            group["status"] = "critico"
        elif group["avg_risk"] >= 7:
            group["status"] = "monitorar"
        else:
            group["status"] = "estavel"
        monitored.append(group)

    monitored.sort(
        key=lambda item: (-item["missing"], -item["avg_risk"], -item["critical_routers"], item["neighborhood"])
    )
    return monitored


def build_executive_summary(connected, missing_routers, incident, recovery):
    if incident.get("type") == "roubo_de_fibra" and not connected:
        missing = ", ".join(missing_routers) if missing_routers else "nenhum"
        return (
            "A DFS identificou perda de cobertura apos roubo de fibra e isolou "
            f"os roteadores afetados: {missing}."
        )

    if incident.get("type") == "roubo_de_fibra" and recovery.get("status") == "reparo_concluido":
        return "A DFS confirmou que o reparo restabeleceu a malha e que a redundancia voltou a operar."

    return "A DFS confirmou que todos os roteadores seguem alcancaveis a partir da central."


def analyze_router_network(
    graph,
    central_router,
    expected_connected=None,
    scenario_label=None,
    scenario_metadata=None,
):
    scenario_metadata = scenario_metadata or {}
    visited = dfs_with_stack(graph, central_router)
    visit_order = get_visit_order(graph, central_router)
    connected = is_network_connected(graph, central_router)
    all_routers = get_all_routers(graph)
    trace = build_visit_trace(graph, central_router)
    missing_routers = sorted(all_routers - visited)
    passed = expected_connected is None or connected == expected_connected
    router_profiles = scenario_metadata.get("router_profiles", {})
    incident = scenario_metadata.get("incident", {})
    recovery = scenario_metadata.get("recovery", {})
    context = scenario_metadata.get("context", {})
    monitoring_focus = scenario_metadata.get("monitoring_focus", [])
    neighborhood_monitor = build_neighborhood_monitor(all_routers, visited, router_profiles)
    risk_alerts = [item for item in neighborhood_monitor if item["status"] != "estavel"][:3]
    executive_summary = build_executive_summary(connected, missing_routers, incident, recovery)

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
        "objective": scenario_metadata.get("objective"),
        "context": context,
        "incident": incident,
        "recovery": recovery,
        "monitoring_focus": monitoring_focus,
        "neighborhood_monitor": neighborhood_monitor,
        "risk_alerts": risk_alerts,
        "executive_summary": executive_summary,
    }
