"""Render Tarang's responsive GitHub profile SVGs with no dependencies."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

DARK = {
    "bg": "#080b12", "panel": "#0e1422", "panel2": "#121b2c",
    "line": "#24324a", "text": "#dce7f7", "muted": "#8191aa",
    "cyan": "#59e1ff", "violet": "#c38cff", "green": "#a9f0c1",
    "pink": "#ff7b9c", "amber": "#ffd27a",
}

LIGHT = {
    "bg": "#f5f8fc", "panel": "#ffffff", "panel2": "#edf3fa",
    "line": "#c7d3e2", "text": "#182235", "muted": "#60708a",
    "cyan": "#007c99", "violet": "#7042a8", "green": "#187a4d",
    "pink": "#b72f57", "amber": "#9c6500",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(x: int, y: int, value: str, fill: str, size: int = 14,
         weight: int = 400, anchor: str = "start", cls: str = "") -> str:
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" class="{cls}">{esc(value)}</text>')


def line(x1: int, y1: int, x2: int, y2: int, stroke: str, width: int = 1) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"/>'


def base_svg(width: int, height: int, body: str, palette: dict[str, str], title: str,
             animate: bool = False) -> str:
    motion = """
      .cursor { animation: blink 1.05s steps(1,end) infinite; }
      .scan { animation: scan 8s linear infinite; }
      @keyframes blink { 0%,48% { opacity:1 } 49%,100% { opacity:0 } }
      @keyframes scan { from { transform:translateY(-24px) } to { transform:translateY(460px) } }
      @media (prefers-reduced-motion: reduce) { .cursor,.scan { animation:none } }
    """ if animate else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(title)}</desc>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    {motion}
  </style>
  <rect width="{width}" height="{height}" rx="12" fill="{palette['bg']}"/>
  {body}
</svg>'''


def chrome(width: int, palette: dict[str, str], label: str, right: str = "") -> str:
    p = palette
    return "".join([
        f'<rect x="1" y="1" width="{width-2}" height="34" rx="11" fill="{p["panel2"]}"/>',
        f'<circle cx="18" cy="17" r="5" fill="{p["pink"]}"/>',
        f'<circle cx="35" cy="17" r="5" fill="{p["amber"]}"/>',
        f'<circle cx="52" cy="17" r="5" fill="{p["green"]}"/>',
        text(70, 22, label, p["muted"], 12, 600),
        text(width-16, 22, right, p["muted"], 11, 400, "end") if right else "",
        line(0, 35, width, 35, p["line"]),
    ])


def metric(x: int, y: int, value: str, label: str, palette: dict[str, str], color: str) -> str:
    p = palette
    return "".join([
        text(x, y, value, color, 23, 700),
        text(x, y + 22, label, p["muted"], 11, 500),
    ])


def hero_desktop(palette: dict[str, str], animate: bool) -> str:
    p = palette
    w, h = 846, 430
    b = [chrome(w, p, "LOCUS//OS · builder console", "session: tarang@atlas")]
    b += [
        f'<rect x="16" y="51" width="500" height="324" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="530" y="51" width="300" height="324" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        text(34, 78, "0: whoami", p["muted"], 11, 600),
        text(34, 111, "$ whoami", p["cyan"], 14, 600),
        text(34, 156, "TARANG GOYAL", p["text"], 32, 800),
        text(34, 184, "AI product engineer · agent builder · ships end-to-end", p["muted"], 13),
        line(34, 203, 498, 203, p["line"]),
        metric(34, 239, "8×", "wins", p, p["violet"]),
        metric(132, 239, "35", "public repos", p, p["cyan"]),
        metric(260, 239, "1", "paper", p, p["green"]),
        metric(350, 239, "600+", "Locus tests", p, p["amber"]),
        text(34, 304, "now", p["muted"], 12, 600),
        text(86, 304, "building context infrastructure for coding agents", p["text"], 12),
        text(34, 331, "stack", p["muted"], 12, 600),
        text(86, 331, "typescript · python · react · fastapi · postgres · mcp", p["text"], 12),
        text(548, 78, "1: locus.router", p["muted"], 11, 600),
        text(548, 111, "$ locus benchmark --summary", p["cyan"], 13, 600),
        text(548, 150, "required files", p["muted"], 11),
        text(812, 150, "100%", p["green"], 16, 700, "end"),
        f'<rect x="548" y="161" width="264" height="8" rx="4" fill="{p["panel2"]}"/>',
        f'<rect x="548" y="161" width="264" height="8" rx="4" fill="{p["green"]}"/>',
        text(548, 202, "context reduced", p["muted"], 11),
        text(812, 202, "53%", p["violet"], 16, 700, "end"),
        f'<rect x="548" y="213" width="264" height="8" rx="4" fill="{p["panel2"]}"/>',
        f'<rect x="548" y="213" width="140" height="8" rx="4" fill="{p["violet"]}"/>',
        text(548, 254, "active processes", p["muted"], 11, 600),
        text(548, 281, "● locus.index", p["green"], 12),
        text(682, 281, "code graph", p["muted"], 11),
        text(548, 305, "● locus.mcp", p["cyan"], 12),
        text(682, 305, "agent tools", p["muted"], 11),
        text(548, 329, "● product.ship", p["violet"], 12),
        text(682, 329, "end-to-end", p["muted"], 11),
        f'<rect x="0" y="390" width="846" height="40" rx="0" fill="{p["panel2"]}"/>',
        text(18, 415, "tarang@atlas:~$", p["green"], 13, 700),
        text(157, 415, "build the whole thing", p["text"], 13),
        f'<rect x="320" y="403" width="8" height="16" fill="{p["cyan"]}" class="cursor"/>',
        text(828, 415, "8 wins · 1 paper · shipping", p["muted"], 11, 500, "end"),
    ]
    if animate:
        b.append(f'<rect x="1" y="37" width="844" height="2" fill="{p["cyan"]}" opacity="0.12" class="scan"/>')
    return base_svg(w, h, "".join(b), p, "Tarang Goyal's Locus builder console", animate)


def hero_phone(palette: dict[str, str]) -> str:
    p = palette
    w, h = 360, 590
    b = [chrome(w, p, "LOCUS//OS", "tarang@atlas")]
    b += [
        text(18, 72, "$ whoami", p["cyan"], 13, 600),
        text(18, 112, "TARANG", p["text"], 31, 800),
        text(18, 146, "GOYAL", p["text"], 31, 800),
        text(18, 178, "AI product engineer · agent builder", p["muted"], 12),
        line(18, 199, 342, 199, p["line"]),
        metric(18, 235, "8×", "wins", p, p["violet"]),
        metric(104, 235, "35", "repos", p, p["cyan"]),
        metric(188, 235, "1", "paper", p, p["green"]),
        metric(260, 235, "600+", "tests", p, p["amber"]),
        text(18, 298, "$ locus benchmark", p["cyan"], 13, 600),
        text(18, 332, "required files", p["muted"], 11),
        text(342, 332, "100%", p["green"], 15, 700, "end"),
        f'<rect x="18" y="343" width="324" height="8" rx="4" fill="{p["panel2"]}"/>',
        f'<rect x="18" y="343" width="324" height="8" rx="4" fill="{p["green"]}"/>',
        text(18, 384, "context reduced", p["muted"], 11),
        text(342, 384, "53%", p["violet"], 15, 700, "end"),
        f'<rect x="18" y="395" width="324" height="8" rx="4" fill="{p["panel2"]}"/>',
        f'<rect x="18" y="395" width="172" height="8" rx="4" fill="{p["violet"]}"/>',
        text(18, 447, "now", p["muted"], 11, 600),
        text(18, 470, "context infrastructure for coding agents", p["text"], 11),
        text(18, 507, "stack", p["muted"], 11, 600),
        text(18, 530, "typescript · python · react · mcp", p["text"], 11),
        f'<rect x="0" y="552" width="360" height="38" fill="{p["panel2"]}"/>',
        text(16, 576, "tarang@atlas:~$", p["green"], 12, 700),
        f'<rect x="151" y="564" width="8" height="15" fill="{p["cyan"]}" class="cursor"/>',
    ]
    return base_svg(w, h, "".join(b), p, "Tarang Goyal's mobile Locus builder console", True)


PROJECTS = [
    ("LOCUS", "context engine for coding agents", "100% required-file recall · 53% less context", "PRIVATE CORE · PUBLIC SUPPORT", "violet"),
    ("CORTEX", "company knowledge -> agent-ready skills", "citations · review · Slack · REST/MCP", "SHIPPED", "cyan"),
    ("PROJECT EVOLVE", "inspectable GTM experimentation", "observed A/B data · Bayesian decisions", "SHIPPED", "green"),
    ("CHRONOS-2 LAB", "interactive forecasting research", "equities · Treasury rates · 25 years", "PUBLISHED", "amber"),
]


def card(x: int, y: int, w: int, h: int, item: tuple[str, str, str, str, str], p: dict[str, str]) -> str:
    name, blurb, detail, status, color = item
    accent = p[color]
    return "".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{accent}"/>',
        text(x + 22, y + 31, name, accent, 15, 800),
        text(x + w - 18, y + 30, status, p["muted"], 9, 600, "end"),
        text(x + 22, y + 62, blurb, p["text"], 12, 600),
        text(x + 22, y + 88, detail, p["muted"], 11),
        text(x + 22, y + 116, "$ open --project", accent, 10, 600),
    ])


def projects_desktop(palette: dict[str, str]) -> str:
    p, w, h = palette, 846, 340
    b = [chrome(w, p, "1: /srv/ships", "four systems · one builder")]
    for i, item in enumerate(PROJECTS):
        x = 16 + (i % 2) * 415
        y = 52 + (i // 2) * 140
        b.append(card(x, y, 399, 124, item, p))
    b += [text(18, 329, "tarang@atlas:/srv/ships$", p["green"], 11, 700),
          text(212, 329, "ls --shipped", p["text"], 11)]
    return base_svg(w, h, "".join(b), p, "Systems shipped by Tarang Goyal")


def projects_phone(palette: dict[str, str]) -> str:
    p, w, h = palette, 360, 592
    b = [chrome(w, p, "1: /srv/ships", "4 systems")]
    for i, item in enumerate(PROJECTS):
        b.append(card(12, 48 + i * 132, 336, 118, item, p))
    b += [text(14, 582, "tarang@atlas:/srv/ships$", p["green"], 10, 700)]
    return base_svg(w, h, "".join(b), p, "Systems shipped by Tarang Goyal")


WINS = [
    ("01", "Stanford AI Hackathon", "winner"),
    ("02", "AWS × INRIX", "winner"),
    ("03", "YC-backed Stack Auth", "winner"),
    ("04", "A10 Networks", "winner"),
    ("05", "AgentForge", "winner"),
    ("06", "Beta Fund × GMI Cloud", "winner"),
    ("07", "SCU Analytical Showdown", "winner"),
    ("08", "Syndicate by Maximor", "track 2"),
]


def proof_desktop(palette: dict[str, str]) -> str:
    p, w, h = palette, 846, 300
    b = [chrome(w, p, "2: /var/log/proof", "8 wins · 1 paper")]
    b += [text(20, 66, "$ ./verify --external", p["cyan"], 12, 700)]
    for i, (num, name, result) in enumerate(WINS):
        col, row = i % 2, i // 2
        x, y = 20 + col * 410, 100 + row * 34
        b += [text(x, y, num, p["muted"], 10, 700),
              text(x + 34, y, name, p["text"], 11, 600),
              text(x + 380, y, result.upper(), p["green"], 9, 700, "end")]
    b += [line(20, 248, 826, 248, p["line"]),
          text(20, 273, "PAPER", p["violet"], 10, 800),
          text(84, 273, "Multivariate Forecasting with Foundation Models", p["text"], 11, 600),
          text(826, 273, "arXiv:2605.21504", p["muted"], 10, 500, "end")]
    return base_svg(w, h, "".join(b), p, "Eight wins and one research paper")


def proof_phone(palette: dict[str, str]) -> str:
    p, w, h = palette, 360, 430
    b = [chrome(w, p, "2: /var/log/proof", "8 + 1")]
    b += [text(14, 64, "$ ./verify --external", p["cyan"], 11, 700)]
    for i, (num, name, result) in enumerate(WINS):
        y = 96 + i * 34
        b += [text(14, y, num, p["muted"], 9, 700),
              text(42, y, name, p["text"], 10, 600),
              text(346, y, result.upper(), p["green"], 8, 700, "end")]
    b += [line(14, 375, 346, 375, p["line"]),
          text(14, 401, "PAPER", p["violet"], 9, 800),
          text(64, 401, "Chronos-2 forecasting", p["text"], 10, 600),
          text(346, 418, "arXiv:2605.21504", p["muted"], 9, 500, "end")]
    return base_svg(w, h, "".join(b), p, "Eight wins and one research paper")


def write(name: str, content: str) -> None:
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
    else:
        print(f"unchanged {path.relative_to(ROOT)}")


def main() -> None:
    write("hero.svg", hero_desktop(DARK, True))
    write("hero-light.svg", hero_desktop(LIGHT, False))
    write("hero-phone.svg", hero_phone(DARK))
    write("projects.svg", projects_desktop(DARK))
    write("projects-light.svg", projects_desktop(LIGHT))
    write("projects-phone.svg", projects_phone(DARK))
    write("proof.svg", proof_desktop(DARK))
    write("proof-light.svg", proof_desktop(LIGHT))
    write("proof-phone.svg", proof_phone(DARK))


if __name__ == "__main__":
    main()

