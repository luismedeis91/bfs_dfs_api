import argparse
import os
from pathlib import Path
import sys

from src.services.router_networks import analyze_router_network, load_router_scenarios
from src.services.router_terminal import (
    RICH_AVAILABLE,
    print_plain_analysis,
    render_compact_results,
    render_final_conclusion,
    render_hacker_intro,
    render_router_analysis,
)


DEFAULT_DATA_FILE = Path(__file__).resolve().parent / "data" / "router_networks.json"
DEFAULT_VENV_PYTHON = Path(__file__).resolve().parent / ".venv" / "bin" / "python"
REEXEC_ENV_VAR = "BFS_DFS_API_REEXEC"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Analisa a conectividade de uma rede de roteadores com DFS usando pilha."
    )
    parser.add_argument(
        "--data-file",
        default=str(DEFAULT_DATA_FILE),
        help="Caminho para o arquivo JSON com os cenarios de rede.",
    )
    parser.add_argument(
        "--scenario",
        default=None,
        help="Nome de um cenario especifico para executar. Sem isso, executa todos.",
    )
    parser.add_argument(
        "--central-router",
        default=None,
        help="Sobrescreve o roteador central definido no arquivo.",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="Desativa a interface animada e imprime uma saida simples.",
    )
    parser.add_argument(
        "--step-delay",
        type=float,
        default=0.18,
        help="Atraso entre os passos da animacao em segundos.",
    )
    parser.add_argument(
        "--no-intro",
        action="store_true",
        help="Desativa a intro hacker antes da animacao principal.",
    )
    parser.add_argument(
        "--apresentacao",
        action="store_true",
        help="Inicia o modo de apresentacao em slides antes da analise.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.plain and not RICH_AVAILABLE:
        already_reexecuted = os.environ.get(REEXEC_ENV_VAR) == "1"
        if DEFAULT_VENV_PYTHON.exists() and not already_reexecuted:
            reexec_env = os.environ.copy()
            reexec_env[REEXEC_ENV_VAR] = "1"
            os.execve(
                str(DEFAULT_VENV_PYTHON),
                [str(DEFAULT_VENV_PYTHON), __file__, *sys.argv[1:]],
                reexec_env,
            )

    if args.apresentacao and RICH_AVAILABLE:
        from src.services.slideshow import run_presentation
        should_continue = run_presentation()
        if not should_continue:
            return

    scenarios = load_router_scenarios(args.data_file)

    selected = scenarios
    if args.scenario:
        if args.scenario not in scenarios:
            available = ", ".join(sorted(scenarios))
            raise SystemExit(
                f"Cenario '{args.scenario}' nao encontrado. Cenarios disponiveis: {available}"
            )
        selected = {args.scenario: scenarios[args.scenario]}

    analyses = []
    items = list(selected.items())

    for name, scenario in items:
        central_router = args.central_router or scenario["central_router"]
        analysis = analyze_router_network(
            scenario["network"],
            central_router,
            expected_connected=scenario.get("expected_connected"),
            scenario_label=scenario.get("label", name),
            scenario_metadata=scenario,
        )
        analyses.append((scenario, analysis))

    if args.plain:
        for name, (_, analysis) in zip(selected.keys(), analyses):
            print_plain_analysis(name, analysis)
        return

    if len(analyses) > 1:
        if not args.no_intro:
            render_hacker_intro(title=f"DFS ROUTER STACK :: {len(analyses)} CENARIOS")

        for scenario, analysis in analyses:
            label = analysis["scenario_label"] or "Teste"
            render_router_analysis(
                label,
                scenario["network"],
                analysis,
                step_delay=args.step_delay,
                show_intro=False,
            )

        render_compact_results([analysis for _, analysis in analyses])
        
        if not args.plain and RICH_AVAILABLE:
            render_final_conclusion()
        return

    for scenario, analysis in analyses:
        label = analysis["scenario_label"] or "Teste"
        render_router_analysis(
            label,
            scenario["network"],
            analysis,
            step_delay=args.step_delay,
            show_intro=not args.no_intro,
        )

    if not args.plain and RICH_AVAILABLE:
        render_final_conclusion()


if __name__ == "__main__":
    main()
