"""Render the interactive LOCUS//OS GitHub profile assets without dependencies."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

DARK = {
    "bg": "#070a11", "panel": "#0d1421", "panel2": "#111c2e",
    "line": "#263650", "text": "#e0ebfa", "muted": "#8293ad",
    "cyan": "#59e1ff", "violet": "#c38cff", "green": "#a9f0c1",
    "pink": "#ff7b9c", "amber": "#ffd27a",
}

LIGHT = {
    "bg": "#f5f8fc", "panel": "#ffffff", "panel2": "#eaf1f9",
    "line": "#c7d4e4", "text": "#172235", "muted": "#60718b",
    "cyan": "#007e9c", "violet": "#7042a8", "green": "#187a4d",
    "pink": "#b72f57", "amber": "#9c6500",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def txt(x: int, y: int, value: str, fill: str, size: int = 14,
        weight: int = 400, anchor: str = "start", cls: str = "") -> str:
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" class="{cls}">{esc(value)}</text>')


def rule(x1: int, y1: int, x2: int, y2: int, stroke: str, width: int = 1,
         cls: str = "") -> str:
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{width}" class="{cls}"/>')


def base_svg(width: int, height: int, body: str, p: dict[str, str], title: str,
             animated: bool = False) -> str:
    motion = """
      .boot { animation: boot-out .28s ease 3.05s forwards; }
      .session { opacity:0; animation: session-in .35s ease 3.08s forwards; }
      .boot-1 { opacity:0; animation: reveal .01s .20s forwards; }
      .boot-2 { opacity:0; animation: reveal .01s .58s forwards; }
      .boot-3 { opacity:0; animation: reveal .01s .98s forwards; }
      .boot-4 { opacity:0; animation: reveal .01s 1.38s forwards; }
      .boot-5 { opacity:0; animation: reveal .01s 1.84s forwards; }
      .boot-6 { opacity:0; animation: reveal .01s 2.35s forwards; }
      .progress { transform-origin:left; transform:scaleX(0); animation: load 2.35s ease .25s forwards; }
      .cursor { animation: blink 1.05s steps(1,end) infinite; }
      .scan { animation: scan 8s linear infinite; }
      .flow-a { animation: flow 2.8s linear infinite; }
      .flow-b { animation: flow 2.8s linear .9s infinite; }
      .flow-c { animation: flow 2.8s linear 1.8s infinite; }
      .pulse { animation: pulse 1.8s ease-in-out infinite; }
      @keyframes reveal { to { opacity:1; } }
      @keyframes load { to { transform:scaleX(1); } }
      @keyframes boot-out { to { opacity:0; visibility:hidden; } }
      @keyframes session-in { to { opacity:1; } }
      @keyframes blink { 0%,48% { opacity:1 } 49%,100% { opacity:0 } }
      @keyframes scan { from { transform:translateY(-30px) } to { transform:translateY(490px) } }
      @keyframes pulse { 0%,100% { opacity:.3 } 50% { opacity:1 } }
      @keyframes flow { from { transform:translateX(0) } to { transform:translateX(184px) } }
      @media (prefers-reduced-motion: reduce) {
        .boot { display:none; }
        .session { opacity:1; animation:none; }
        .cursor,.scan,.flow-a,.flow-b,.flow-c,.pulse,.progress { animation:none; }
      }
    """ if animated else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(title)}</desc>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    {motion}
  </style>
  <rect width="{width}" height="{height}" rx="12" fill="{p['bg']}"/>
  {body}
</svg>'''


def chrome(width: int, p: dict[str, str], label: str, right: str = "") -> str:
    return "".join([
        f'<rect x="1" y="1" width="{width-2}" height="34" rx="11" fill="{p["panel2"]}"/>',
        f'<circle cx="18" cy="17" r="5" fill="{p["pink"]}"/>',
        f'<circle cx="35" cy="17" r="5" fill="{p["amber"]}"/>',
        f'<circle cx="52" cy="17" r="5" fill="{p["green"]}"/>',
        txt(70, 22, label, p["muted"], 12, 600),
        txt(width - 16, 22, right, p["muted"], 11, 400, "end") if right else "",
        rule(0, 35, width, 35, p["line"]),
    ])


def metric(x: int, y: int, value: str, label: str, p: dict[str, str], color: str) -> str:
    return txt(x, y, value, color, 23, 800) + txt(x, y + 22, label, p["muted"], 11, 500)


def boot_screen(w: int, h: int, p: dict[str, str], phone: bool = False) -> str:
    left = 24 if phone else 40
    size = 25 if phone else 34
    line_size = 10 if phone else 12
    y0 = 84 if phone else 92
    lines = [
        ("boot-1", "[ OK ] memory map", p["green"]),
        ("boot-2", "[ OK ] code graph", p["green"]),
        ("boot-3", "[ OK ] semantic index", p["green"]),
        ("boot-4", "[ OK ] MCP transport", p["green"]),
        ("boot-5", "[ OK ] product journal", p["green"]),
        ("boot-6", "ATTACHING TARANG@ATLAS...", p["cyan"]),
    ]
    out = [f'<g class="boot">', f'<rect x="1" y="36" width="{w-2}" height="{h-37}" fill="{p["bg"]}"/>',
           txt(left, 68, "LOCUS//BIOS  v8.1", p["violet"], size, 800)]
    for i, (cls, label, color) in enumerate(lines):
        out.append(txt(left, y0 + i * 31, label, color, line_size, 600, cls=cls))
    bar_y = h - 54
    out += [f'<rect x="{left}" y="{bar_y}" width="{w-left*2}" height="7" rx="3" fill="{p["panel2"]}"/>',
            f'<rect x="{left}" y="{bar_y}" width="{w-left*2}" height="7" rx="3" fill="{p["cyan"]}" class="progress"/>',
            txt(left, h - 25, "loading operator workspace", p["muted"], line_size), "</g>"]
    return "".join(out)


def flow_graph(x: int, y: int, p: dict[str, str], compact: bool = False) -> str:
    nodes = [("repo", p["cyan"]), ("index", p["violet"]), ("rank", p["amber"]), ("agent", p["green"])]
    step = 68 if compact else 74
    radius = 18 if compact else 21
    out = [rule(x + radius, y, x + step * 3, y, p["line"], 2)]
    for i, (label, color) in enumerate(nodes):
        cx = x + i * step
        out += [f'<circle cx="{cx}" cy="{y}" r="{radius}" fill="{p["panel2"]}" stroke="{color}"/>',
                txt(cx, y + 4, label, color, 8 if compact else 9, 700, "middle")]
    if not compact:
        for cls, yy, color in [("flow-a", y - 5, p["cyan"]), ("flow-b", y, p["violet"]), ("flow-c", y + 5, p["green"])]:
            out.append(f'<circle cx="{x + radius + 5}" cy="{yy}" r="2.5" fill="{color}" class="{cls}"/>')
    return "".join(out)


def hero_desktop(p: dict[str, str], animated: bool) -> str:
    w, h = 846, 470
    s = [f'<g class="session">', chrome(w, p, "LOCUS//OS · operator workspace", "attached: tarang@atlas")]
    s += [
        f'<rect x="16" y="51" width="502" height="360" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="532" y="51" width="298" height="360" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        txt(34, 78, "0: operator", p["muted"], 11, 700), txt(34, 111, "$ whoami --verbose", p["cyan"], 14, 700),
        txt(34, 154, "TARANG GOYAL", p["text"], 32, 800),
        txt(34, 182, "AI product engineer · builds the whole product", p["muted"], 13), rule(34, 202, 500, 202, p["line"]),
        metric(34, 239, "8×", "wins", p, p["violet"]), metric(132, 239, "36", "public repos", p, p["cyan"]),
        metric(260, 239, "1", "paper", p, p["green"]), metric(350, 239, "600+", "Locus tests", p, p["amber"]),
        txt(34, 302, "CURRENT MISSION", p["muted"], 10, 800),
        txt(34, 329, "Give coding agents the right context before they act.", p["text"], 12, 600),
        txt(34, 358, "typescript · python · react · fastapi · postgres · mcp", p["muted"], 11),
        txt(550, 78, "1: locus.route", p["muted"], 11, 700), txt(550, 109, "$ locus route ./repo", p["cyan"], 12, 700),
        flow_graph(572, 158, p), txt(550, 207, "LIVE JOURNAL", p["muted"], 10, 800),
        txt(550, 237, "● graph indexed", p["green"], 11, 600), txt(550, 263, "● required files", p["muted"], 11),
        txt(812, 263, "100%", p["green"], 12, 800, "end"), txt(550, 289, "● context removed", p["muted"], 11),
        txt(812, 289, "53%", p["violet"], 12, 800, "end"), txt(550, 315, "● tool surface", p["muted"], 11),
        txt(812, 315, "CLI + MCP", p["cyan"], 12, 800, "end"), txt(550, 354, "STATUS", p["muted"], 10, 800),
        f'<circle cx="600" cy="351" r="4" fill="{p["green"]}" class="pulse"/>', txt(612, 355, "shipping", p["green"], 11, 700),
        f'<rect x="0" y="427" width="846" height="43" fill="{p["panel2"]}"/>', txt(18, 454, "tarang@atlas:~$", p["green"], 13, 800),
        txt(158, 454, "open a route below", p["text"], 13), f'<rect x="315" y="441" width="8" height="16" fill="{p["cyan"]}" class="cursor"/>',
        txt(828, 454, "ready · 4 artifacts mounted", p["muted"], 11, 500, "end"), "</g>",
    ]
    if animated:
        s.append(boot_screen(w, h, p))
        s.append(f'<rect x="1" y="37" width="844" height="2" fill="{p["cyan"]}" opacity=".12" class="scan"/>')
    return base_svg(w, h, "".join(s), p, "LOCUS OS booting into Tarang Goyal's operator workspace", animated)


def hero_phone(p: dict[str, str]) -> str:
    w, h = 360, 610
    s = [f'<g class="session">', chrome(w, p, "LOCUS//OS", "tarang@atlas"), txt(18, 72, "$ whoami --verbose", p["cyan"], 12, 700),
         txt(18, 110, "TARANG GOYAL", p["text"], 27, 800), txt(18, 139, "AI product engineer · agent builder", p["muted"], 11),
         rule(18, 160, 342, 160, p["line"]), metric(18, 198, "8×", "wins", p, p["violet"]), metric(102, 198, "36", "repos", p, p["cyan"]),
         metric(184, 198, "1", "paper", p, p["green"]), metric(258, 198, "600+", "tests", p, p["amber"]),
         txt(18, 257, "$ locus route ./repo", p["cyan"], 12, 700), flow_graph(44, 302, p, True),
         txt(18, 357, "LIVE JOURNAL", p["muted"], 10, 800), txt(18, 388, "● required files", p["muted"], 11),
         txt(342, 388, "100%", p["green"], 12, 800, "end"), txt(18, 416, "● context removed", p["muted"], 11),
         txt(342, 416, "53%", p["violet"], 12, 800, "end"), txt(18, 444, "● tool surface", p["muted"], 11),
         txt(342, 444, "CLI + MCP", p["cyan"], 12, 800, "end"), rule(18, 470, 342, 470, p["line"]),
         txt(18, 500, "MISSION", p["muted"], 10, 800), txt(18, 527, "Give agents the right context", p["text"], 11, 600),
         txt(18, 548, "before they act.", p["text"], 11, 600), f'<rect x="0" y="572" width="360" height="38" fill="{p["panel2"]}"/>',
         txt(16, 596, "tarang@atlas:~$", p["green"], 12, 800), f'<rect x="151" y="584" width="8" height="15" fill="{p["cyan"]}" class="cursor"/>',
         "</g>", boot_screen(w, h, p, True)]
    return base_svg(w, h, "".join(s), p, "LOCUS OS mobile boot sequence for Tarang Goyal", True)


KEYS = [
    ("F1", "PORTFOLIO", "open full site", "cyan"), ("F2", "LOCUS", "open support repo", "violet"),
    ("F3", "SHIPS", "browse products", "green"), ("F4", "PAPER", "read on arXiv", "amber"),
    ("F5", "LINKEDIN", "open profile", "cyan"), ("F6", "EMAIL", "start a conversation", "pink"),
]


def key_asset(item: tuple[str, str, str, str], p: dict[str, str]) -> str:
    code, label, hint, color = item
    accent = p[color]
    body = "".join([
        f'<rect x="1" y="1" width="256" height="58" rx="9" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="1" y="1" width="5" height="58" rx="2" fill="{accent}"/>',
        f'<rect x="16" y="13" width="38" height="34" rx="6" fill="{p["panel2"]}" stroke="{accent}"/>',
        txt(35, 35, code, accent, 11, 800, "middle"), txt(68, 26, label, p["text"], 12, 800),
        txt(68, 44, hint, p["muted"], 9, 500), txt(241, 36, "↗", accent, 17, 700, "end"),
    ])
    return base_svg(258, 60, body, p, f"{code} {label}: {hint}")


PROJECTS = [
    {"slug": "locus", "name": "LOCUS", "type": "AI DEVELOPER TOOL", "color": "violet", "blurb": "Routes coding agents to the files and dependencies that matter.", "proof": "100% required-file recall · 53% less context · 600+ tests", "stack": "agent · API · web · CLI · MCP · auth · deployment", "status": "PRIVATE CORE · PUBLIC SUPPORT"},
    {"slug": "cortex", "name": "CORTEX", "type": "KNOWLEDGE INFRASTRUCTURE", "color": "cyan", "blurb": "Turns company knowledge into reviewed, agent-ready skills.", "proof": "citations · human review · Slack · REST/MCP", "stack": "ingest · retrieve · draft · verify · publish", "status": "SHIPPED"},
    {"slug": "evolve", "name": "PROJECT EVOLVE", "type": "GTM EXPERIMENTATION", "color": "green", "blurb": "Makes product experiments inspectable from evidence to decision.", "proof": "observed A/B data · Bayesian decisions · audit trail", "stack": "React · TypeScript · analytics · experiment engine", "status": "SHIPPED"},
    {"slug": "chronos", "name": "CHRONOS-2 LAB", "type": "PUBLISHED RESEARCH", "color": "amber", "blurb": "Tests when related time series help foundation-model forecasts.", "proof": "7 major tech stocks · U.S. Treasury rates · 2000–2025", "stack": "Python · Chronos-2 · forecasting · interactive lab", "status": "arXiv:2605.21504"},
]


def project_asset(item: dict[str, str], p: dict[str, str]) -> str:
    accent = p[item["color"]]
    body = "".join([
        f'<rect x="1" y="1" width="844" height="152" rx="11" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="1" y="1" width="7" height="152" rx="3" fill="{accent}"/>', txt(26, 34, item["type"], p["muted"], 9, 800),
        txt(26, 66, item["name"], accent, 22, 800), txt(276, 65, item["blurb"], p["text"], 12, 600), rule(26, 88, 820, 88, p["line"]),
        txt(26, 116, item["proof"], p["text"], 11, 600), txt(26, 138, item["stack"], p["muted"], 10),
        txt(820, 34, item["status"], accent, 9, 800, "end"), f'<rect x="718" y="106" width="102" height="29" rx="6" fill="{p["panel2"]}" stroke="{accent}"/>',
        txt(769, 125, "OPEN  ↗", accent, 10, 800, "middle"),
    ])
    return base_svg(846, 154, body, p, f"Open {item['name']}: {item['blurb']}")


WINS = [
    ("01", "Stanford AI Hackathon", "WINNER"), ("02", "AWS × INRIX", "WINNER"),
    ("03", "YC-backed Stack Auth", "WINNER"), ("04", "A10 Networks", "WINNER"),
    ("05", "AgentForge", "WINNER"), ("06", "Beta Fund × GMI Cloud", "WINNER"),
    ("07", "SCU Analytical Showdown", "WINNER"), ("08", "Syndicate by Maximor", "TRACK 2"),
]


def proof_asset(p: dict[str, str]) -> str:
    b = [chrome(846, p, "3: /var/log/external-proof", "8 wins · 1 paper"), txt(20, 67, "$ verify --source external", p["cyan"], 12, 800)]
    for i, (num, name, result) in enumerate(WINS):
        col, row = i % 2, i // 2
        x, y = 20 + col * 410, 103 + row * 35
        b += [txt(x, y, num, p["muted"], 10, 700), txt(x + 34, y, name, p["text"], 11, 600), txt(x + 382, y, result, p["green"], 9, 800, "end")]
    b += [rule(20, 255, 826, 255, p["line"]), txt(20, 282, "PAPER", p["violet"], 10, 800),
          txt(84, 282, "Multivariate Forecasting with Foundation Models", p["text"], 11, 600), txt(826, 282, "arXiv:2605.21504", p["muted"], 10, 600, "end")]
    return base_svg(846, 306, "".join(b), p, "Eight competition wins and a published research paper")


def section_asset(index: str, path: str, detail: str, p: dict[str, str]) -> str:
    body = "".join([f'<rect x="1" y="1" width="844" height="44" rx="8" fill="{p["panel2"]}" stroke="{p["line"]}"/>',
                    txt(18, 29, index, p["violet"], 11, 800), txt(58, 29, path, p["text"], 12, 800), txt(828, 29, detail, p["muted"], 10, 600, "end")])
    return base_svg(846, 46, body, p, f"Section {path}: {detail}")


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
    for item in KEYS:
        slug = item[1].lower()
        write(f"keys/{slug}.svg", key_asset(item, DARK))
        write(f"keys/{slug}-light.svg", key_asset(item, LIGHT))
    for item in PROJECTS:
        write(f"ships/{item['slug']}.svg", project_asset(item, DARK))
        write(f"ships/{item['slug']}-light.svg", project_asset(item, LIGHT))
    write("proof.svg", proof_asset(DARK))
    write("proof-light.svg", proof_asset(LIGHT))
    sections = [
        ("01", "/operator/routes", "every control opens a real destination", "routes"),
        ("02", "/srv/ships", "four complete products · click any card", "ships"),
        ("03", "/var/log/external-proof", "results verified outside the repo", "proof"),
        ("04", "/etc/operator", "how I work", "operator"),
    ]
    for index, path, detail, slug in sections:
        write(f"sections/{slug}.svg", section_asset(index, path, detail, DARK))
        write(f"sections/{slug}-light.svg", section_asset(index, path, detail, LIGHT))


if __name__ == "__main__":
    main()
