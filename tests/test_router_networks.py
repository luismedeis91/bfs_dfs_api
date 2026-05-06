from pathlib import Path

from src.services.router_networks import (
    analyze_router_network,
    build_visit_trace,
    load_router_scenarios,
)


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "router_networks.json"


def test_load_router_scenarios_reads_external_file():
    scenarios = load_router_scenarios(DATA_FILE)

    assert "preventive_monitoring_success" in scenarios
    assert "fiber_theft_outage" in scenarios
    assert scenarios["preventive_monitoring_success"]["central_router"] == "NOC-CENTRO"


def test_analyze_router_network_reports_connected_scenario():
    scenarios = load_router_scenarios(DATA_FILE)
    scenario = scenarios["preventive_monitoring_success"]

    analysis = analyze_router_network(
        scenario["network"],
        scenario["central_router"],
        scenario_metadata=scenario,
    )

    assert analysis["all_visited"] is True
    assert analysis["connected"] is True
    assert analysis["passed"] is True
    assert analysis["visit_order"] == [
        "NOC-CENTRO",
        "EDGE-ALDEOTA",
        "EDGE-MEIRELES",
        "EDGE-MUCURIPE",
        "EDGE-PAPICU",
        "EDGE-PIRAMBU",
        "EDGE-COCO",
    ]
    assert analysis["executive_summary"].startswith("A DFS confirmou")
    assert analysis["risk_alerts"][0]["neighborhood"] == "Pirambu"


def test_analyze_router_network_reports_disconnected_scenario():
    scenarios = load_router_scenarios(DATA_FILE)
    scenario = scenarios["fiber_theft_outage"]

    analysis = analyze_router_network(
        scenario["network"],
        scenario["central_router"],
        scenario_metadata=scenario,
    )

    assert analysis["all_visited"] is False
    assert analysis["connected"] is False
    assert analysis["passed"] is True
    assert analysis["visited"] == {"NOC-CENTRO", "EDGE-ALDEOTA", "EDGE-PAPICU", "EDGE-PIRAMBU"}
    assert analysis["risk_alerts"][0]["neighborhood"] == "Jangurussu"
    assert analysis["executive_summary"].startswith("A DFS identificou perda de cobertura")


def test_build_visit_trace_tracks_stack_and_skips_repeated_nodes():
    graph = {
        "R1": ["R2", "R3"],
        "R2": ["R1", "R4"],
        "R3": ["R1", "R4"],
        "R4": ["R2", "R3"],
    }

    trace = build_visit_trace(graph, "R1")

    assert trace[0]["current_router"] == "R1"
    assert trace[0]["stack_before_pop"] == ["R1"]
    assert trace[0]["stack_after_push"] == ["R3", "R2"]
    assert trace[-1]["current_router"] == "R3"
    assert trace[-1]["skipped"] is True
    assert trace[-1]["visited_after_step"] == ["R1", "R2", "R3", "R4"]
