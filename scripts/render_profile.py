"""Render the interactive TARANG//OS GitHub profile assets without dependencies."""

from __future__ import annotations

import html
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

DARK = {
    "bg": "#0d1117", "panel": "#151b23", "panel2": "#21262d",
    "line": "#3d444d", "text": "#f0f6fc", "muted": "#9198a1",
    "cyan": "#58d6ff", "violet": "#c04bff", "green": "#7ee787",
    "pink": "#ff7b9c", "amber": "#ffb000",
}

LIGHT = {
    "bg": "#ffffff", "panel": "#f6f8fa", "panel2": "#e6eaef",
    "line": "#d1d9e0", "text": "#1f2328", "muted": "#59636e",
    "cyan": "#0969da", "violet": "#7b2cbf", "green": "#1a7f37",
    "pink": "#b72f57", "amber": "#bc4c00",
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
    """.strip() if animated else ""
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(title)}</desc>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    {motion}
  </style>
  <rect width="{width}" height="{height}" rx="12" fill="{p['bg']}"/>
  {body}
</svg>'''
    return "\n".join(line.rstrip() for line in content.splitlines()) + "\n"


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
        ("boot-1", "[ OK ] product engine", p["green"]),
        ("boot-2", "[ OK ] agent systems", p["green"]),
        ("boot-3", "[ OK ] full-stack runtime", p["green"]),
        ("boot-4", "[ OK ] customer feedback", p["green"]),
        ("boot-5", "[ OK ] research archive", p["green"]),
        ("boot-6", "ATTACHING TARANG@ATLAS...", p["cyan"]),
    ]
    out = [f'<g class="boot">', f'<rect x="1" y="36" width="{w-2}" height="{h-37}" fill="{p["bg"]}"/>',
           txt(left, 68, "TARANG//OS  release 8.0", p["violet"], size, 800)]
    for i, (cls, label, color) in enumerate(lines):
        out.append(txt(left, y0 + i * 31, label, color, line_size, 600, cls=cls))
    bar_y = h - 54
    out += [f'<rect x="{left}" y="{bar_y}" width="{w-left*2}" height="7" rx="3" fill="{p["panel2"]}"/>',
            f'<rect x="{left}" y="{bar_y}" width="{w-left*2}" height="7" rx="3" fill="{p["cyan"]}" class="progress"/>',
            txt(left, h - 25, "loading builder workspace", p["muted"], line_size), "</g>"]
    return "".join(out)


def flow_graph(x: int, y: int, p: dict[str, str], compact: bool = False) -> str:
    nodes = [("problem", p["cyan"]), ("build", p["violet"]), ("ship", p["amber"]), ("learn", p["green"])]
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
    s = [f'<g class="session">', chrome(w, p, "TARANG//OS · builder workspace", "attached: tarang@atlas")]
    s += [
        f'<rect x="16" y="51" width="502" height="360" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="532" y="51" width="298" height="360" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        txt(34, 78, "0: operator", p["muted"], 11, 700), txt(34, 111, "$ whoami --verbose", p["cyan"], 14, 700),
        txt(34, 154, "TARANG GOYAL", p["text"], 32, 800),
        txt(34, 182, "AI product engineer · full-stack · agents · FDE", p["muted"], 13), rule(34, 202, 500, 202, p["line"]),
        metric(34, 239, "8×", "wins", p, p["violet"]), metric(132, 239, "48", "repositories", p, p["cyan"]),
        metric(260, 239, "1", "paper", p, p["green"]), metric(350, 239, "0→1", "product scope", p, p["amber"]),
        txt(34, 302, "CURRENT MISSION", p["muted"], 10, 800),
        txt(34, 329, "Take ambiguous customer problems from zero to production.", p["text"], 12, 600),
        txt(34, 358, "product · agents · frontend · backend · evaluation · deployment", p["muted"], 11),
        txt(550, 78, "1: product.loop", p["muted"], 11, 700), txt(550, 109, "$ build --from problem --to users", p["cyan"], 12, 700),
        flow_graph(572, 158, p), txt(550, 207, "BUILDER JOURNAL", p["muted"], 10, 800),
        txt(550, 237, "● 0→1 products", p["green"], 11, 600), txt(812, 237, "SHIPPED", p["green"], 12, 800, "end"),
        txt(550, 263, "● agent systems", p["muted"], 11), txt(812, 263, "GUARDED", p["cyan"], 12, 800, "end"),
        txt(550, 289, "● customer work", p["muted"], 11), txt(812, 289, "PRODUCTION", p["violet"], 12, 800, "end"),
        txt(550, 315, "● ownership", p["muted"], 11), txt(812, 315, "END-TO-END", p["amber"], 12, 800, "end"),
        txt(550, 354, "STATUS", p["muted"], 10, 800),
        f'<circle cx="600" cy="351" r="4" fill="{p["green"]}" class="pulse"/>', txt(612, 355, "shipping", p["green"], 11, 700),
        f'<rect x="0" y="427" width="846" height="43" fill="{p["panel2"]}"/>', txt(18, 454, "tarang@atlas:~$", p["green"], 13, 800),
        txt(158, 454, "open a route below", p["text"], 13), f'<rect x="315" y="441" width="8" height="16" fill="{p["cyan"]}" class="cursor"/>',
        txt(828, 454, "ready · 4 artifacts mounted", p["muted"], 11, 500, "end"), "</g>",
    ]
    if animated:
        s.append(boot_screen(w, h, p))
        s.append(f'<rect x="1" y="37" width="844" height="2" fill="{p["cyan"]}" opacity=".12" class="scan"/>')
    return base_svg(w, h, "".join(s), p, "Tarang OS booting into Tarang Goyal's builder workspace", animated)


def hero_phone(p: dict[str, str]) -> str:
    w, h = 360, 610
    s = [f'<g class="session">', chrome(w, p, "TARANG//OS", "tarang@atlas"), txt(18, 72, "$ whoami --verbose", p["cyan"], 12, 700),
         txt(18, 110, "TARANG GOYAL", p["text"], 27, 800), txt(18, 139, "AI product engineer · full-stack · agents", p["muted"], 11),
         rule(18, 160, 342, 160, p["line"]), metric(18, 198, "8×", "wins", p, p["violet"]), metric(102, 198, "48", "repos", p, p["cyan"]),
         metric(184, 198, "1", "paper", p, p["green"]), metric(258, 198, "0→1", "scope", p, p["amber"]),
         txt(18, 257, "$ build --problem-to-users", p["cyan"], 11, 700), flow_graph(44, 302, p, True),
         txt(18, 357, "BUILDER JOURNAL", p["muted"], 10, 800), txt(18, 388, "● AI products", p["muted"], 11),
         txt(342, 388, "SHIPPED", p["green"], 11, 800, "end"), txt(18, 416, "● agent systems", p["muted"], 11),
         txt(342, 416, "PRODUCTION", p["cyan"], 11, 800, "end"), txt(18, 444, "● ownership", p["muted"], 11),
         txt(342, 444, "END-TO-END", p["amber"], 11, 800, "end"), rule(18, 470, 342, 470, p["line"]),
         txt(18, 500, "MISSION", p["muted"], 10, 800), txt(18, 527, "Turn rough ideas into useful", p["text"], 11, 600),
         txt(18, 548, "AI products people can use.", p["text"], 11, 600), f'<rect x="0" y="572" width="360" height="38" fill="{p["panel2"]}"/>',
         txt(16, 596, "tarang@atlas:~$", p["green"], 12, 800), f'<rect x="151" y="584" width="8" height="15" fill="{p["cyan"]}" class="cursor"/>',
         "</g>", boot_screen(w, h, p, True)]
    return base_svg(w, h, "".join(s), p, "Tarang OS mobile boot sequence for Tarang Goyal", True)


def signal_asset(p: dict[str, str], phone: bool = False) -> str:
    signals = [
        ("STANFORD UNIVERSITY", "AI HACKATHON WINNER", "violet"),
        ("AWS × INRIX", "HACKATHON WINNER", "cyan"),
        ("YC S24", "STACK AUTH WINNER", "green"),
        ("arXiv:2605.21504", "PUBLISHED RESEARCH", "amber"),
    ]
    if phone:
        w, h = 360, 202
        body = [
            f'<rect x="1" y="1" width="358" height="200" rx="11" fill="{p["panel"]}" stroke="{p["line"]}"/>',
            txt(18, 28, "VERIFIED SIGNAL", p["cyan"], 10, 800),
            txt(342, 28, "8× WINS · 1 PAPER", p["violet"], 9, 800, "end"),
            rule(18, 42, 342, 42, p["line"]),
        ]
        for i, (name, detail, color) in enumerate(signals):
            col, row = i % 2, i // 2
            x, y = 18 + col * 168, 78 + row * 72
            body += [
                txt(x, y, name, p[color], 10, 800),
                txt(x, y + 20, detail, p["muted"], 8, 700),
            ]
        body += [rule(178, 53, 178, 184, p["line"]), rule(18, 113, 342, 113, p["line"])]
        return base_svg(w, h, "".join(body), p, "Verified external signals: Stanford, AWS, YC, and published research")

    w, h = 846, 118
    body = [
        f'<rect x="1" y="1" width="844" height="116" rx="11" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        txt(20, 27, "VERIFIED SIGNAL", p["cyan"], 10, 800),
        txt(826, 27, "8× WINS · 1 PAPER", p["violet"], 10, 800, "end"),
        rule(20, 40, 826, 40, p["line"]),
    ]
    cell_w = 201
    for i, (name, detail, color) in enumerate(signals):
        x = 20 + i * cell_w
        body += [
            txt(x, 75, name, p[color], 13, 800),
            txt(x, 97, detail, p["muted"], 9, 700),
        ]
        if i:
            body.append(rule(x - 16, 54, x - 16, 101, p["line"]))
    return base_svg(w, h, "".join(body), p, "Verified external signals: Stanford, AWS, YC, and published research")


KEYS = [
    ("F1", "portfolio", "", "cyan"),
    ("F2", "github", "", "violet"),
    ("F3", "paper", "", "green"),
    ("F4", "linkedin", "", "amber"),
    ("F5", "email", "", "pink"),
    ("F6", "projects", "", "cyan"),
    ("F7", "locus", "", "violet"),
]


def key_asset(item: tuple[str, str, str, str], p: dict[str, str]) -> str:
    code, label, hint, color = item
    accent = p[color]
    body = "".join([
        f'<rect x="1" y="1" width="116" height="30" rx="6" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="7" y="7" width="25" height="18" rx="3" fill="{accent}"/>',
        txt(19.5, 20, code, p["bg"], 9, 800, "middle"),
        txt(40, 21, label, p["text"], 9, 600),
    ])
    return base_svg(118, 32, body, p, f"{code} {label}")


PROJECTS = [
    {"slug": "tickmark", "name": "TICKMARK", "type": "AUTONOMOUS OFFICE OF THE CFO", "color": "violet", "blurb": "A month-end close agent that compiles corrections into deterministic rules.", "proof": "39% auto-cleared · 100% precision · controller time 63→47 min", "stack": "Next.js · TypeScript · Postgres · local model eval", "status": "MEASURED"},
    {"slug": "locus", "name": "LOCUS", "type": "CONTROL LAYER FOR CODING AGENTS", "color": "cyan", "blurb": "Finds the right code and evidence before a coding agent starts.", "proof": "15-case replay · 100% fix-file recall · 53% median reduction", "stack": "web · REST · CLI · MCP · Guard · Sandbox", "status": "LIVE"},
    {"slug": "versionless", "name": "VERSIONLESS", "type": "PROOF LAYER FOR AGENT-WRITTEN CODE", "color": "green", "blurb": "Locks tests and contracts, then makes an agent prove the rules stayed intact.", "proof": "exact-commit proof · immutable hashes · fresh-clone verification", "stack": "GitHub Actions · TypeScript · Codex runtime", "status": "VERIFIED"},
    {"slug": "agent-access", "name": "AGENT ACCESS", "type": "IDENTITY FOR AI-AGENT CUSTOMERS", "color": "amber", "blurb": "Turns OpenAPI contracts into scoped capabilities and signed receipts.", "proof": "delegated credentials · idempotent replay · isolated smoke path", "stack": "Next.js · Neon · OpenAPI · signed receipts", "status": "SANDBOX"},
]


def project_asset(item: dict[str, str], p: dict[str, str], phone: bool = False) -> str:
    accent = p[item["color"]]
    if phone:
        blurb_lines = textwrap.wrap(item["blurb"], width=46)
        proof_lines = textwrap.wrap(item["proof"], width=50)
        body = [
            f'<rect x="1" y="1" width="358" height="238" rx="11" fill="{p["panel"]}" stroke="{p["line"]}"/>',
            f'<rect x="1" y="1" width="6" height="238" rx="3" fill="{accent}"/>',
            txt(18, 27, item["type"], p["muted"], 8, 800),
            txt(18, 61, item["name"], accent, 22, 800),
            txt(342, 61, item["status"], accent, 8, 800, "end"),
        ]
        for i, line in enumerate(blurb_lines[:2]):
            body.append(txt(18, 91 + i * 20, line, p["text"], 10, 600))
        body.append(rule(18, 124, 342, 124, p["line"]))
        for i, line in enumerate(proof_lines[:2]):
            body.append(txt(18, 151 + i * 20, line, p["text"], 9, 600))
        body += [
            rule(18, 194, 342, 194, p["line"]),
            txt(18, 220, item["stack"], p["muted"], 8, 500),
        ]
        return base_svg(360, 240, "".join(body), p, f"Open {item['name']}: {item['blurb']}")

    blurb = textwrap.wrap(item["blurb"], width=48)
    proof = textwrap.wrap(item["proof"], width=52)
    body = [
        f'<rect x="1" y="1" width="412" height="174" rx="7" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        txt(14, 20, "tarang@atlas:~/ships", p["muted"], 8, 600),
        txt(400, 20, item["status"], accent, 8, 800, "end"),
        rule(10, 28, 404, 28, p["line"]),
        txt(14, 51, item["type"], p["muted"], 8, 700),
        txt(14, 80, item["name"], accent, 20, 800),
    ]
    for i, line in enumerate(blurb[:2]):
        body.append(txt(14, 103 + i * 16, line, p["text"], 9, 600))
    body.append(rule(14, 132, 398, 132, p["line"]))
    for i, line in enumerate(proof[:2]):
        body.append(txt(14, 150 + i * 14, line, p["muted"], 8, 600))
    return base_svg(414, 176, "".join(body), p, f"Open {item['name']}: {item['blurb']}")


def project_action_asset(item: dict[str, str], p: dict[str, str], action: str) -> str:
    accent = p[item["color"]]
    if action == "live":
        label, hint, mark = "LIVE PRODUCT", "open deployed experience", "●"
    else:
        label, hint, mark = "SOURCE CODE", "inspect architecture + tests", "</>"
    body = "".join([
        f'<rect x="1" y="1" width="408" height="48" rx="9" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<rect x="1" y="1" width="5" height="48" rx="2" fill="{accent}"/>',
        txt(20, 30, mark, accent, 10, 800),
        txt(52, 22, label, p["text"], 10, 800),
        txt(52, 37, hint, p["muted"], 8, 600),
        txt(392, 30, "↗", accent, 15, 800, "end"),
    ])
    return base_svg(410, 50, body, p, f"{label}: {item['name']}")


WINS = [
    ("01", "Stanford University AI Hackathon", "WINNER"),
    ("02", "AWS × INRIX", "WINNER"),
    ("03", "A10 Networks", "WINNER"),
    ("04", "AgentForge", "WINNER"),
    ("05", "Beta Fund × GMI Cloud", "WINNER"),
    ("06", "SCU Analytical Showdown", "WINNER"),
    ("07", "Syndicate by Maximor · Track 2", "WINNER"),
]


def proof_asset(p: dict[str, str]) -> str:
    b = [chrome(846, p, "2: /var/log/proof", "8 wins · 1 paper"), txt(20, 67, "$ verify --source external", p["cyan"], 12, 800)]
    for i, (num, name, result) in enumerate(WINS):
        col, row = i % 2, i // 2
        x, y = 20 + col * 410, 103 + row * 35
        b += [txt(x, y, num, p["muted"], 10, 700), txt(x + 34, y, name, p["text"], 11, 600), txt(x + 382, y, result, p["green"], 9, 800, "end")]
    b += [rule(20, 255, 826, 255, p["line"]), txt(20, 282, "PAPER", p["violet"], 10, 800),
          txt(84, 282, "Multivariate Forecasting with Foundation Models", p["text"], 11, 600), txt(826, 282, "arXiv:2605.21504", p["muted"], 10, 600, "end")]
    return base_svg(846, 306, "".join(b), p, "Eight competition wins and a published research paper")


def section_asset(index: str, path: str, detail: str, p: dict[str, str]) -> str:
    body = "".join([
        f'<rect x="1" y="1" width="844" height="26" rx="5" fill="{p["panel2"]}" stroke="{p["line"]}"/>',
        txt(14, 19, f"{index}:{path}", p["text"], 10, 800),
        txt(832, 19, detail, p["muted"], 9, 600, "end"),
    ])
    return base_svg(846, 28, body, p, f"tmux window {index}: {path}")


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
    write("hero-light.svg", hero_desktop(LIGHT, True))
    write("hero-phone.svg", hero_phone(DARK))
    for item in KEYS:
        slug = item[1].lower()
        write(f"keys/{slug}.svg", key_asset(item, DARK))
        write(f"keys/{slug}-light.svg", key_asset(item, LIGHT))
    for item in PROJECTS:
        write(f"ships/{item['slug']}.svg", project_asset(item, DARK))
        write(f"ships/{item['slug']}-light.svg", project_asset(item, LIGHT))
        write(f"ships/{item['slug']}-phone.svg", project_asset(item, DARK, True))
        write(f"ships/{item['slug']}-phone-light.svg", project_asset(item, LIGHT, True))
    write("proof.svg", proof_asset(DARK))
    write("proof-light.svg", proof_asset(LIGHT))
    sections = [
        ("1", "ships", "sort -r /var/log/builds | head -4", "ships"),
        ("2", "proof", "verify --source external", "proof"),
        ("3", "etc", "cat /etc/tarang; crontab -l", "operator"),
    ]
    for index, path, detail, slug in sections:
        write(f"sections/{slug}.svg", section_asset(index, path, detail, DARK))
        write(f"sections/{slug}-light.svg", section_asset(index, path, detail, LIGHT))


if __name__ == "__main__":
    main()
