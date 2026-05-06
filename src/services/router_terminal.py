from collections import deque
from random import choice, randint
from time import sleep


try:
    from rich import box
    from rich.align import Align
    from rich.columns import Columns
    from rich.console import Console, Group
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
    from rich.rule import Rule
    from rich.table import Table
    from rich.text import Text
except ModuleNotFoundError:
    Console = None


BG = "#07111f"
SURFACE = "#0f172a"
SURFACE_ALT = "#162033"
SURFACE_ALT_2 = "#1b2640"
ACCENT = "#4cc9f0"
ACCENT_SOFT = "#90e0ef"
SUCCESS = "#80ed99"
WARNING = "#ffd166"
DANGER = "#ff6b6b"
MUTED = "#94a3b8"
WHITE = "#f8fafc"
MATRIX = "#22c55e"
MATRIX_SOFT = "#86efac"
RICH_AVAILABLE = Console is not None


def _require_rich():
    if Console is None:
        raise ModuleNotFoundError(
            "A dependencia 'rich' nao esta instalada. Adicione-a com 'pip install rich'."
        )


def _build_levels(graph, central_router):
    levels = []
    seen = set()

    if central_router in graph or any(central_router in neighbors for neighbors in graph.values()):
        queue = deque([(central_router, 0)])
        seen.add(central_router)
        while queue:
            router, level = queue.popleft()
            while len(levels) <= level:
                levels.append([])
            levels[level].append(router)
            for neighbor in graph.get(router, []):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append((neighbor, level + 1))

    remaining = sorted(
        {
            router
            for router in set(graph.keys()).union(*[set(neighbors) for neighbors in graph.values()] or [set()])
            if router not in seen
        }
    )
    if remaining:
        levels.append(remaining)

    return levels


def _router_state(router, central_router, current_router, visited, stack, missing):
    if router == current_router:
        return "current"
    if router in stack:
        return "stack"
    if router in missing:
        return "missing"
    if router == central_router:
        return "central"
    if router in visited:
        return "visited"
    return "idle"


def _badge(router, state):
    styles = {
        "current": (WARNING, BG, "●"),
        "stack": (ACCENT, BG, "◆"),
        "visited": (SUCCESS, BG, "●"),
        "central": (ACCENT_SOFT, BG, "★"),
        "missing": (DANGER, BG, "●"),
        "idle": (MUTED, BG, "○"),
    }
    fg, bg, icon = styles[state]
    text = Text()
    text.append(f" {icon} ", style=f"bold {fg} on {bg}")
    text.append(f"{router} ", style=f"bold {fg} on {bg}")
    return text


def _build_header(name, analysis):
    status = "PASSOU" if analysis["passed"] else "FALHOU"
    status_color = SUCCESS if analysis["passed"] else DANGER
    title = Text()
    title.append("DFS COM PILHA", style=f"bold {ACCENT}")
    title.append("  ")
    title.append("Monitor de Roteadores", style=f"bold {WHITE}")

    subtitle = Text()
    subtitle.append(f"{analysis['scenario_label'] or name}", style=f"bold {MUTED}")
    subtitle.append("    ")
    subtitle.append(f"Resultado: {status}", style=f"bold {status_color}")

    return Panel(
        Group(Align.center(title), Align.center(subtitle)),
        border_style=ACCENT,
        box=box.DOUBLE,
        style=f"on {BG}",
        padding=(1, 2),
    )


def _build_metrics(analysis, current_router, stack):
    metrics = [
        ("Central", analysis["central_router"], ACCENT_SOFT),
        ("Atual", current_router or "-", WARNING),
        ("Visitados", f"{len(analysis['visited'])}/{analysis['total_routers']}", SUCCESS),
        ("Pilha", str(len(stack)), ACCENT),
        ("Pendentes", str(len(analysis["missing_routers"])), DANGER),
    ]

    cards = []
    for label, value, color in metrics:
        body = Group(
            Text(label.upper(), style=f"bold {MUTED}"),
            Text(value, style=f"bold {color}"),
        )
        cards.append(
            Panel(
                Align.center(body, vertical="middle"),
                border_style=color,
                box=box.ROUNDED,
                style=f"on {SURFACE}",
                padding=(1, 2),
            )
        )
    return cards


def _build_metric_rows(cards, compact):
    if compact:
        return Group(
            Columns(cards[:3], expand=True),
            Columns(cards[3:], expand=True),
        )
    return Columns(cards, expand=True)


def _build_network_table(graph, central_router):
    table = Table(box=None, expand=True, pad_edge=False)
    table.add_column("Roteador", style=f"bold {WHITE}")
    table.add_column("Links", style=MUTED)

    for router in sorted(graph):
        label = f"{router} (central)" if router == central_router else router
        links = "  ".join(graph[router]) if graph[router] else "sem conexoes"
        style = f"bold {ACCENT_SOFT}" if router == central_router else WHITE
        table.add_row(Text(label, style=style), links)

    return Panel(
        table,
        title=f"[bold {WHITE}]Topologia[/bold {WHITE}]",
        border_style=ACCENT,
        box=box.ROUNDED,
        style=f"on {SURFACE}",
        padding=(1, 2),
    )


def _build_ascii_map(graph, analysis, current_router, stack, visited):
    levels = _build_levels(graph, analysis["central_router"])
    missing = set(analysis["missing_routers"])
    lines = []

    for level_index, routers in enumerate(levels):
        prefix = "Nivel" if level_index < len(levels) - 1 or not missing else "Isolados"
        label = f"{prefix} {level_index}" if prefix == "Nivel" else prefix
        line = Text()
        line.append(f"{label:<10}", style=f"bold {MUTED}")
        for index, router in enumerate(routers):
            state = _router_state(
                router,
                analysis["central_router"],
                current_router,
                visited,
                stack,
                missing,
            )
            line.append_text(_badge(router, state))
            if index != len(routers) - 1:
                line.append("   ", style=MUTED)
        lines.append(line)

        if level_index < len(levels) - 1:
            connector = Text(" " * 10, style=MUTED)
            for _ in routers:
                connector.append("   │        ", style=ACCENT_SOFT)
            lines.append(connector)

    legend = Text()
    legend.append("Legenda: ", style=f"bold {WHITE}")
    legend.append("★ central  ", style=f"bold {ACCENT_SOFT}")
    legend.append("● visitado  ", style=f"bold {SUCCESS}")
    legend.append("◆ na pilha  ", style=f"bold {ACCENT}")
    legend.append("● atual  ", style=f"bold {WARNING}")
    legend.append("● isolado", style=f"bold {DANGER}")

    return Panel(
        Group(*lines, Text(""), legend),
        title=f"[bold {WHITE}]Mapa ASCII da Rede[/bold {WHITE}]",
        border_style=ACCENT_SOFT,
        box=box.ROUNDED,
        style=f"on {SURFACE_ALT}",
        padding=(1, 2),
    )


def _build_stack_panel(stack_before, stack_after, pushed_neighbors):
    stack_table = Table.grid(expand=True)
    stack_table.add_column()
    stack_table.add_row(Text("Topo", style=f"bold {WARNING}"))

    display_stack = list(reversed(stack_after))
    if not display_stack:
        stack_table.add_row(Text("vazia", style=MUTED))
    else:
        for router in display_stack:
            stack_table.add_row(
                Panel(
                    Align.center(Text(router, style=f"bold {ACCENT}")),
                    border_style=ACCENT,
                    box=box.SQUARE,
                    padding=(0, 2),
                    style=f"on {SURFACE_ALT_2}",
                )
            )

    notes = Group(
        Text(f"Antes do pop: {' -> '.join(reversed(stack_before)) if stack_before else 'vazia'}", style=MUTED),
        Text(f"Depois do push: {' -> '.join(reversed(stack_after)) if stack_after else 'vazia'}", style=MUTED),
        Text(
            f"Empilhados: {', '.join(pushed_neighbors) if pushed_neighbors else 'nenhum'}",
            style=f"bold {ACCENT_SOFT}",
        ),
    )

    return Panel(
        Group(stack_table, Text(""), notes),
        title=f"[bold {WHITE}]Pilha Vertical[/bold {WHITE}]",
        border_style=ACCENT,
        box=box.ROUNDED,
        style=f"on {SURFACE}",
        padding=(1, 2),
    )


def _build_activity_panel(step, phase_label):
    event = Text()
    event.append("Fase: ", style=f"bold {MUTED}")
    event.append(phase_label, style=f"bold {WARNING}")
    event.append("\n")
    event.append("Atual: ", style=f"bold {MUTED}")
    event.append(step["current_router"], style=f"bold {WHITE}")
    event.append("\n")
    event.append("Vizinhos: ", style=f"bold {MUTED}")
    event.append(", ".join(step["neighbors"]) if step["neighbors"] else "sem vizinhos", style=WHITE)
    event.append("\n")
    if step["skipped"]:
        event.append("Acao: passo ignorado para evitar repeticao", style=f"bold {DANGER}")
    else:
        event.append(
            f"Acao: expandindo e empilhando {', '.join(step['pushed_neighbors']) if step['pushed_neighbors'] else 'nenhum'}",
            style=f"bold {ACCENT_SOFT}",
        )

    return Panel(
        event,
        title=f"[bold {WHITE}]Evento da DFS[/bold {WHITE}]",
        border_style=WARNING,
        box=box.ROUNDED,
        style=f"on {SURFACE}",
        padding=(1, 2),
    )


def _build_visited_panel(visited_after_step, total_routers, missing):
    visited_text = Text()
    if visited_after_step:
        for index, router in enumerate(visited_after_step):
            if index:
                visited_text.append("  ")
            visited_text.append(router, style=f"bold {SUCCESS}")
    else:
        visited_text.append("nenhum", style=MUTED)

    missing_text = Text(", ".join(sorted(missing)) if missing else "nenhum", style=f"bold {DANGER}" if missing else MUTED)

    body = Group(
        Text(f"Cobertura: {len(visited_after_step)}/{total_routers}", style=f"bold {SUCCESS}"),
        Text(""),
        visited_text,
        Text(""),
        Text("Nao alcancados", style=f"bold {MUTED}"),
        missing_text,
    )

    return Panel(
        body,
        title=f"[bold {WHITE}]Cobertura da Busca[/bold {WHITE}]",
        border_style=SUCCESS,
        box=box.ROUNDED,
        style=f"on {SURFACE}",
        padding=(1, 2),
    )


def _build_timeline(trace, active_index):
    start = max(0, active_index - 5)
    items = []
    for index in range(start, active_index + 1):
        step = trace[index]
        icon = "↺" if step["skipped"] else "→"
        color = DANGER if step["skipped"] else ACCENT_SOFT
        entry = Text()
        entry.append(f"{index + 1:02d} ", style=MUTED)
        entry.append(icon, style=f"bold {color}")
        entry.append(f" pop {step['current_router']}", style=f"bold {WHITE}")
        if step["skipped"]:
            entry.append("  ignorado", style=f"bold {DANGER}")
        else:
            pushed = ", ".join(step["pushed_neighbors"]) if step["pushed_neighbors"] else "nenhum"
            entry.append(f"  push [{pushed}]", style=f"bold {ACCENT}")
        items.append(entry)

    return Panel(
        Group(*items) if items else Text("sem eventos", style=MUTED),
        title=f"[bold {WHITE}]Timeline[/bold {WHITE}]",
        border_style=ACCENT_SOFT,
        box=box.ROUNDED,
        style=f"on {SURFACE_ALT}",
        padding=(1, 2),
    )


def _build_summary_panel(name, analysis):
    status_color = SUCCESS if analysis["passed"] else DANGER
    status_text = "PASSOU" if analysis["passed"] else "FALHOU"
    actual = "CONECTADA" if analysis["connected"] else "DESCONECTADA"
    expected = None
    if analysis["expected_connected"] is not None:
        expected = "CONECTADA" if analysis["expected_connected"] else "DESCONECTADA"

    summary = Table.grid(padding=(0, 2))
    summary.add_column(style=f"bold {MUTED}")
    summary.add_column(style=WHITE)
    summary.add_row("Teste", analysis["scenario_label"] or name)
    summary.add_row("Central", analysis["central_router"])
    if analysis.get("objective"):
        summary.add_row("Objetivo", analysis["objective"])
    if analysis.get("context", {}).get("city"):
        summary.add_row("Cidade", analysis["context"]["city"])
    if expected is not None:
        summary.add_row("Esperado", expected)
    summary.add_row("Resultado", actual)
    summary.add_row("Status", status_text)
    if analysis.get("incident", {}).get("date"):
        summary.add_row("Incidente", analysis["incident"]["date"])
    if analysis.get("incident", {}).get("status"):
        summary.add_row("Estado do incidente", analysis["incident"]["status"])
    summary.add_row("Ordem final", " -> ".join(analysis["visit_order"]))
    summary.add_row("Visitados", ", ".join(sorted(analysis["visited"])))
    summary.add_row(
        "Faltando",
        ", ".join(analysis["missing_routers"]) if analysis["missing_routers"] else "nenhum",
    )
    summary.add_row("Todos visitados", str(analysis["all_visited"]))

    title = Text()
    title.append("Resultado Final ", style=f"bold {WHITE}")
    title.append(status_text, style=f"bold {status_color}")

    return Panel(
        summary,
        title=title,
        border_style=status_color,
        box=box.DOUBLE_EDGE,
        style=f"on {SURFACE}",
        padding=(1, 2),
    )


def _build_risk_monitor_panel(analysis):
    monitor = analysis.get("neighborhood_monitor", [])
    table = Table(box=None, expand=True, pad_edge=False)
    table.add_column("Bairro", style=f"bold {WHITE}")
    table.add_column("Cobertura", style=WHITE)
    table.add_column("Risco medio", style=WHITE)
    table.add_column("Status", style=WHITE)

    for item in monitor[:6]:
        if item["status"] == "critico":
            color = DANGER
            status = "critico"
        elif item["status"] == "monitorar":
            color = WARNING
            status = "monitorar"
        else:
            color = SUCCESS
            status = "estavel"
        table.add_row(
            item["neighborhood"],
            f"{item['visited']}/{len(item['routers'])} ({item['coverage_pct']}%)",
            str(item["avg_risk"]),
            Text(status, style=f"bold {color}"),
        )

    focus = ", ".join(analysis.get("monitoring_focus", [])) or "nenhum"
    summary = Group(
        Text(analysis.get("executive_summary", ""), style=f"bold {WHITE}"),
        Text(""),
        table,
        Text(""),
        Text(f"Foco recomendado: {focus}", style=f"bold {ACCENT_SOFT}"),
    )

    return Panel(
        summary,
        title=f"[bold {WHITE}]Monitor de Bairros Vulneraveis[/bold {WHITE}]",
        border_style=WARNING,
        box=box.ROUNDED,
        style=f"on {SURFACE}",
        padding=(1, 2),
    )


def _build_compact_result_panel(analysis):
    status_color = SUCCESS if analysis["passed"] else DANGER
    status_text = "PASSOU" if analysis["passed"] else "FALHOU"
    expected = "CONECTADA" if analysis["expected_connected"] else "DESCONECTADA"
    actual = "CONECTADA" if analysis["connected"] else "DESCONECTADA"

    body = Table.grid(padding=(0, 2))
    body.add_column(style=f"bold {MUTED}")
    body.add_column(style=WHITE)
    body.add_row("Esperado", expected)
    body.add_row("Resultado", actual)
    body.add_row("Status", status_text)
    body.add_row("Visitados", f"{len(analysis['visited'])}/{analysis['total_routers']}")
    if analysis.get("risk_alerts"):
        body.add_row(
            "Alertas",
            ", ".join(item["neighborhood"] for item in analysis["risk_alerts"]),
        )

    return Panel(
        body,
        title=f"[bold {WHITE}]{analysis['scenario_label']}[/bold {WHITE}]",
        border_style=status_color,
        box=box.ROUNDED,
        style=f"on {SURFACE}",
        padding=(1, 2),
    )


def render_compact_results(analyses):
    _require_rich()
    console = Console()
    console.print(Rule(style=ACCENT))
    console.print(Align.center(Text(f"Resumo dos {len(analyses)} Cenarios", style=f"bold {WHITE}")))
    console.print("")

    for analysis in analyses:
        console.print(_build_compact_result_panel(analysis))

    passed = sum(1 for analysis in analyses if analysis["passed"])
    total = len(analyses)
    overall_color = SUCCESS if passed == total else DANGER
    overall = Table.grid(padding=(0, 3))
    overall.add_column(style=f"bold {MUTED}")
    overall.add_column(style=WHITE)
    overall.add_row("Total", str(total))
    overall.add_row("Passaram", str(passed))
    overall.add_row("Falharam", str(total - passed))

    console.print(
        Panel(
            overall,
            title=f"[bold {WHITE}]Resumo Geral: {passed}/{total}[/bold {WHITE}]",
            border_style=overall_color,
            box=box.DOUBLE_EDGE,
            style=f"on {SURFACE}",
            padding=(1, 2),
        )
    )
    console.print("")


def _build_dashboard(name, graph, analysis, step, phase_label, active_index, progress, width):
    current_router = step["current_router"]
    stack = step["stack_after_push"] if phase_label != "POP" else step["stack_after_pop"]
    visited = set(step["visited_after_step"])
    missing = set(analysis["missing_routers"]) - visited
    compact = width < 140
    metric_cards = _build_metrics(analysis, current_router, stack)

    layout = Layout()
    layout.split_column(
        Layout(_build_header(name, analysis), size=5),
        Layout(name="body", ratio=1),
        Layout(progress, size=3),
    )
    layout["body"].split_column(
        Layout(_build_metric_rows(metric_cards, compact), size=11 if compact else 7),
        Layout(name="middle", ratio=1),
        Layout(name="bottom", size=29 if compact else 12),
    )
    if compact:
        layout["body"]["middle"].split_column(
            Layout(_build_ascii_map(graph, analysis, current_router, stack, visited), ratio=3),
            Layout(_build_network_table(graph, analysis["central_router"]), ratio=2),
        )
        layout["body"]["bottom"].split_column(
            Layout(_build_stack_panel(step["stack_before_pop"], step["stack_after_push"], step["pushed_neighbors"]), size=12),
            Layout(_build_activity_panel(step, phase_label), size=9),
            Layout(_build_visited_panel(step["visited_after_step"], analysis["total_routers"], missing), size=10),
            Layout(_build_timeline(analysis["trace"], active_index), ratio=1),
        )
    else:
        layout["body"]["middle"].split_row(
            Layout(_build_network_table(graph, analysis["central_router"]), ratio=5),
            Layout(_build_ascii_map(graph, analysis, current_router, stack, visited), ratio=7),
        )
        layout["body"]["bottom"].split_row(
            Layout(_build_stack_panel(step["stack_before_pop"], step["stack_after_push"], step["pushed_neighbors"]), ratio=4),
            Layout(
                Group(
                    _build_activity_panel(step, phase_label),
                    _build_visited_panel(step["visited_after_step"], analysis["total_routers"], missing),
                    _build_timeline(analysis["trace"], active_index),
                ),
                ratio=6,
            ),
        )
    return layout


def _phase_sleep(step_delay, weight):
    sleep(max(0.03, step_delay * weight))


def _build_intro_frame(width, height, columns, title):
    glyphs = "01ABCDEF#@$%&*"
    rows = []
    top_padding = max(1, height // 6)

    for _ in range(top_padding):
        rows.append(Text(" " * width))

    for row in range(max(8, height - top_padding - 6)):
        line = Text()
        for column in range(width):
            matching = None
            for column_data in columns:
                if column_data["x"] == column:
                    matching = column_data
                    break

            if matching is None:
                line.append(" ")
                continue

            distance = matching["y"] - row
            if distance == 0:
                line.append(choice(glyphs), style=f"bold {WHITE}")
            elif 0 < distance <= matching["tail"]:
                shade = MATRIX_SOFT if distance <= 2 else MATRIX
                line.append(choice(glyphs), style=shade)
            else:
                line.append(" ")
        rows.append(line)

    rows.append(Text(""))
    rows.append(Align.center(Text(title, style=f"bold {MATRIX_SOFT}")))
    rows.append(Align.center(Text("Inicializando monitor de roteadores...", style=f"bold {MATRIX}")))
    return Group(*rows)


def play_hacker_intro(console, title="DFS STACK ROUTER SCAN", duration=2.4):
    width = max(40, console.width - 2)
    height = max(18, console.height - 4)
    column_count = max(10, width // 3)
    columns = []

    for _ in range(column_count):
        columns.append(
            {
                "x": randint(0, width - 1),
                "y": randint(-height, 0),
                "speed": randint(1, 3),
                "tail": randint(4, 10),
            }
        )

    frames = max(12, int(duration / 0.08))
    console.clear()

    with Live(console=console, refresh_per_second=18, transient=True, screen=True) as live:
        for _ in range(frames):
            live.update(_build_intro_frame(width, height, columns, title))
            for column in columns:
                column["y"] += column["speed"]
                if column["y"] - column["tail"] > height:
                    column["y"] = randint(-height // 2, 0)
                    column["x"] = randint(0, width - 1)
                    column["speed"] = randint(1, 3)
                    column["tail"] = randint(4, 10)
            sleep(0.08)

    console.clear()


def render_hacker_intro(title="DFS STACK ROUTER SCAN", duration=2.4):
    _require_rich()
    console = Console()
    play_hacker_intro(console, title=title, duration=duration)


def render_router_analysis(name, graph, analysis, step_delay=0.18, show_intro=True):
    _require_rich()
    console = Console()
    width = console.width
    if show_intro:
        play_hacker_intro(console, title=f"DFS ROUTER STACK :: {name.upper()}")
    console.print(Rule(style=ACCENT))

    progress = Progress(
        SpinnerColumn(style=ACCENT),
        TextColumn("[bold white]{task.description}[/bold white]"),
        BarColumn(bar_width=None, complete_style=SUCCESS, finished_style=SUCCESS),
        TextColumn("[bold white]{task.completed}/{task.total}[/bold white]"),
        console=console,
        expand=True,
    )
    trace = analysis["trace"]
    task_id = progress.add_task("Executando DFS", total=len(trace))

    with Live(console=console, refresh_per_second=18, transient=False, screen=False) as live:
        for index, step in enumerate(trace):
            live.update(_build_dashboard(name, graph, analysis, step, "POP", index, progress, width))
            _phase_sleep(step_delay, 0.4)

            phase = "SKIP" if step["skipped"] else "EXPAND"
            live.update(_build_dashboard(name, graph, analysis, step, phase, index, progress, width))
            _phase_sleep(step_delay, 0.6)

            live.update(_build_dashboard(name, graph, analysis, step, "PUSH", index, progress, width))
            progress.update(task_id, advance=1)
            _phase_sleep(step_delay, 0.5)

        final_group = Group(
            _build_dashboard(name, graph, analysis, trace[-1], "FINAL", len(trace) - 1, progress, width),
            _build_summary_panel(name, analysis),
            _build_risk_monitor_panel(analysis),
        )
        live.update(final_group)


def print_plain_analysis(name, analysis):
    print(f"Teste: {analysis['scenario_label'] or name}")
    print(f"Roteador central: {analysis['central_router']}")
    if analysis.get("context", {}).get("city"):
        print(f"Cidade: {analysis['context']['city']}")
    if analysis.get("objective"):
        print(f"Objetivo: {analysis['objective']}")
    if analysis["expected_connected"] is not None:
        expected = "True" if analysis["expected_connected"] else "False"
        print(f"Esperado conectado?: {expected}")
    print(f"Resultado conectado?: {analysis['connected']}")
    print(f"Status do teste: {'PASSOU' if analysis['passed'] else 'FALHOU'}")
    if analysis.get("incident", {}).get("date"):
        print(f"Data do incidente: {analysis['incident']['date']}")
    if analysis.get("incident", {}).get("details"):
        print(f"Incidente: {analysis['incident']['details']}")
    if analysis.get("recovery", {}).get("planned_action"):
        print(f"Plano de resposta: {analysis['recovery']['planned_action']}")
    print(f"Resumo executivo: {analysis.get('executive_summary', '-')}")
    print(f"Ordem de visita: {' -> '.join(analysis['visit_order'])}")
    print(f"Roteadores visitados: {sorted(analysis['visited'])}")
    print(f"Todos os roteadores foram visitados? {analysis['all_visited']}")
    if analysis.get("neighborhood_monitor"):
        print("Monitor de bairros vulneraveis:")
        for item in analysis["neighborhood_monitor"][:5]:
            print(
                f"  - {item['neighborhood']}: cobertura {item['visited']}/{len(item['routers'])} "
                f"| risco {item['avg_risk']} | status {item['status']}"
            )
    print()
