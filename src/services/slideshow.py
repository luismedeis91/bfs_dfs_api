from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich.box import ROUNDED
from rich.style import Style
from rich.live import Live
import os
import sys
import tty
import termios

console = Console()

ACCENT = "#4cc9f0"
SUCCESS = "#80ed99"
WARNING = "#ffd166"
DANGER = "#ff6b6b"
MUTED = "#94a3b8"
BG = "#07111f"

def create_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    return layout

def get_header(title):
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right", ratio=1)
    grid.add_row(
        Text(f" 🚀 PROJETO: ROTAS DE FORTALEZA", style=f"bold {ACCENT}"),
        Text(title, style=f"bold {WARNING}")
    )
    return Panel(grid, style=f"on {BG}", border_style=ACCENT)

def get_footer(current, total):
    progress = f"Slide {current}/{total} • ENTER para avançar • 'b' voltar • 'q' sair"
    return Panel(Align.center(Text(progress, style=MUTED)), border_style=MUTED)

def slide_intro():
    content = Text.from_markup(
        "\n\n[bold white]SISTEMA DE PLANEJAMENTO DE ROTAS[/]\n"
        f"[bold {ACCENT}]Algoritmos de Busca em Grafos[/]\n\n"
        "Explorando a conectividade da rede de internet em Fortaleza\n"
        "usando Busca em Profundidade (DFS) Recursiva e Iterativa.\n\n"
        "[italic muted]Uma solução focada em resiliência de malhas ópticas em áreas críticas.[/]"
    )
    return Panel(Align.center(content, vertical="middle"), title="[bold white]Apresentação[/]", border_style=ACCENT)

def get_image_render(img_name, width=60):
    try:
        from PIL import Image
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base_dir, "images", img_name)
        
        if not os.path.exists(img_path):
            return Text(f"[Imagem não encontrada: {img_name}]", style="bold yellow")
            
        img = Image.open(img_path).convert("RGB")
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio * 0.5) 
        img = img.resize((width, new_height * 2), resample=Image.Resampling.LANCZOS)
        
        pixels = img.load()
        text = Text()
        for y in range(0, img.height - 1, 2):
            for x in range(img.width):
                r1, g1, b1 = pixels[x, y]
                r2, g2, b2 = pixels[x, y + 1]
                text.append("▀", style=Style(color=f"rgb({r1},{g1},{b1})", bgcolor=f"rgb({r2},{g2},{b2})"))
            text.append("\n")
        return text
    except Exception as e:
        return Text(f"[Erro de renderização: {e}]", style="bold red")

def slide_noticia_1():
    img_render = get_image_render("otica.jpeg", width=80)
    content_group = [
        Text("CASO 1: EXTORSÃO E AMEAÇAS", style="bold red"),
        Text("09/12/2025 - G1 Ceará", style=MUTED),
        Text("\n'Facção cobra taxa de funcionamento a provedor de internet em Fortaleza e ameaça até clientes'", style="white"),
        Text(""),
        Align.center(img_render),
        Text.from_markup(f"\n[italic {DANGER}]Infraestrutura sob controle de grupos criminosos impede o livre acesso.[/]")
    ]
    return Panel(Group(*content_group), title="[bold white]Incidente de Segurança[/]", border_style=DANGER)

def slide_noticia_2():
    img_render = get_image_render("fibra_optica.jpeg", width=80)
    content_group = [
        Text("CASO 2: VANDALISMO NA SABIAGUABA", style="bold red"),
        Text("08/12/2025 - G1 Ceará", style=MUTED),
        Text("\n'Criminosos danificam equipamentos de provedora de internet e impedem reparos'", style="white"),
        Text(""),
        Align.center(img_render),
        Text.from_markup(f"\n[italic {DANGER}]Corte físico de cabos e destruição de caixas de emenda (CTOs).[/]")
    ]
    return Panel(Group(*content_group), title="[bold white]Vandalismo de Infraestrutura[/]", border_style=DANGER)

def slide_demo():
    content = Text.from_markup(
        "\n\n[bold white]INICIANDO DEMONSTRAÇÃO[/]\n\n"
        f"[bold {ACCENT}]Saindo do modo de slides para o Monitor de Rede...[/]\n\n"
        "Veremos o algoritmo DFS Iterativo (com Pilha) escaneando\n"
        "cada nó da rede e verificando a conectividade total.\n\n"
        "[bold warning]Pressione ENTER para carregar a Topologia...[/]"
    )
    return Panel(Align.center(content, vertical="middle"), title="[bold white]Execução do Algoritmo[/]", border_style=WARNING)

def slide_final():
    content = Text.from_markup(
        "\n\n\n[italic white]\"O homem livre é um lutador e a liberdade é algo que se conquista.\"[/]\n"
        f"[bold {MUTED}]- FRIEDRICH NIETZSCHE[/]\n\n\n"
        f"[bold {ACCENT}]Obrigado pela atenção![/]\n\n"
    )
    return Panel(
        Align.center(content, vertical="middle"), 
        title="[bold white]Conclusão[/]", 
        border_style=ACCENT,
        padding=(1, 2)
    )

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def run_presentation():
    slides = [
        ("Introdução", slide_intro),
        ("Notícia 1", slide_noticia_1),
        ("Notícia 2", slide_noticia_2),
        ("Demonstração", slide_demo),
    ]
    current_slide = 0
    total_slides = len(slides)
    layout = create_layout()
    
    with Live(layout, console=console, screen=True, auto_refresh=False) as live:
        while True:
            title, slide_func = slides[current_slide]
            layout["header"].visible = False
            layout["body"].update(slide_func())
            layout["footer"].update(get_footer(current_slide + 1, total_slides))
            live.refresh()
            
            ch = get_char().lower()
            if ch == 'q' or ch == '\x03':
                return False
            elif ch == 'b':
                if current_slide > 0: current_slide -= 1
            elif ch in ['\r', '\n', ' ']:
                if current_slide < total_slides - 1:
                    current_slide += 1
                else:
                    return True
