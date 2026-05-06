from pathlib import Path

from src.services.router_networks import (
    analyze_router_network,
    build_visit_trace,
    load_router_scenarios,
)


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "router_networks.json"


def test_load_router_scenarios_reads_external_file():
    scenarios = load_router_scenarios(DATA_FILE)

    assert "connected_network" in scenarios
    assert "disconnected_network" in scenarios
    assert scenarios["connected_network"]["central_router"] == "R1"


def test_analyze_router_network_reports_connected_scenario():
    scenarios = load_router_scenarios(DATA_FILE)
    scenario = scenarios["connected_network"]

    analysis = analyze_router_network(scenario["network"], scenario["central_router"])

    assert analysis["all_visited"] is True
    assert analysis["connected"] is True
    assert analysis["passed"] is True
    assert analysis["visit_order"] == ["R1", "R2", "R4", "R5", "R6", "R3"]


def test_analyze_router_network_reports_disconnected_scenario():
    scenarios = load_router_scenarios(DATA_FILE)
    scenario = scenarios["disconnected_network"]

    analysis = analyze_router_network(scenario["network"], scenario["central_router"])

    assert analysis["all_visited"] is False
    assert analysis["connected"] is False
    assert analysis["passed"] is True
    assert analysis["visited"] == {"R1", "R2", "R3"}


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
