#!/usr/bin/env python3
"""
render_mermaid.py  -  minimal, dependency-free Mermaid flowchart -> SVG renderer.

Standard library only (re, html, sys). Supports the subset used by this project:
  - `flowchart LR` / `flowchart TD`
  - node definitions `ID[Label]`
  - chained solid edges `A --> B --> C`
  - solid edges with a label `A -->|label| B`
  - one dashed side-branch `A -. label .-> B`
  - `style ID fill:#..,stroke:#..,stroke-width:..`
  - `%% caption: ...` (rendered as an italic caption under the figure)

It exists so the master's Mermaid blocks render as real vector figures in the
PDF build with no external tooling (no Node, no headless browser, no network).
The Mermaid text in the master is the single source of truth; this script is the
prerender step called by build_pdf.py.
"""
import re, html, sys

FS_NODE = 13.0      # node label font size
FS_EDGE = 9.0       # edge label font size
FS_CAP  = 9.5       # caption font size
CHARW   = 0.60      # avg glyph width as a fraction of font size (proportional serif)
PADX, PADY = 14, 8
MARGIN  = 12
FONT    = "Georgia, 'DejaVu Serif', serif"

_TOK = re.compile(r"""
    (?P<dash>-\.\s*(?P<dl>.*?)\s*\.-+>)
  | (?P<solidl>-{2,}>\s*\|\s*(?P<sl>[^|]*?)\s*\|)
  | (?P<solid>-{2,}>)
  | (?P<node>[A-Za-z_]\w*)(?:\[(?P<nl>[^\]]*)\])?
""", re.X)


def _wrap(label, maxc):
    words, lines, cur = label.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


def _parse(text):
    direction, caption, styles = "LR", None, {}
    statements = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("%%"):
            m = re.match(r"%%\s*caption:\s*(.*)", line, re.I)
            if m:
                caption = m.group(1).strip()
            continue
        low = line.lower()
        if low.startswith(("flowchart", "graph")):
            parts = line.split()
            if len(parts) >= 2 and parts[1].upper() in ("LR", "RL", "TD", "TB", "BT"):
                direction = "TD" if parts[1].upper() in ("TD", "TB", "BT") else "LR"
            continue
        if low.startswith("style "):
            m = re.match(r"style\s+(\w+)\s+(.*)", line)
            if m:
                d = {}
                for kv in m.group(2).split(","):
                    if ":" in kv:
                        k, v = kv.split(":", 1)
                        d[k.strip()] = v.strip()
                styles[m.group(1)] = d
            continue
        if low.split(" ")[0] in ("classdef", "class", "linkstyle", "subgraph", "end"):
            continue
        statements.append(line)

    nodes, order, edges = {}, [], []
    for st in statements:
        prev, pending = None, None
        for m in _TOK.finditer(st):
            if m.group("node"):
                nid, lbl = m.group("node"), m.group("nl")
                if nid not in nodes:
                    nodes[nid] = lbl if lbl is not None else nid
                    order.append(nid)
                elif lbl is not None and nodes[nid] == nid:
                    nodes[nid] = lbl
                if prev is not None and pending is not None:
                    edges.append((prev, nid, pending[0], pending[1]))
                    pending = None
                prev = nid
            elif m.group("dash") is not None:
                pending = ("dashed", (m.group("dl") or "").strip())
            elif m.group("solidl") is not None:
                pending = ("solid", (m.group("sl") or "").strip())
            elif m.group("solid") is not None:
                pending = ("solid", "")
    return direction, nodes, order, edges, styles, caption


def _box_size(lines):
    tw = max(len(l) for l in lines) * CHARW * FS_NODE
    return tw + 2 * PADX, len(lines) * (FS_NODE + 4) + 2 * PADY


def _rect(x, y, w, h, style):
    fill = style.get("fill", "#f0e8d6")
    stroke = style.get("stroke", "#0f5a4e")
    sw = style.get("stroke-width", "1.5")
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def _text_block(cx, cy, lines, fs, fill, weight="normal", style="normal", anchor="middle"):
    lh = fs + 4
    top = cy - (len(lines) * lh) / 2 + fs
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text x="{cx:.1f}" y="{top + i*lh:.1f}" text-anchor="{anchor}" '
                   f'font-size="{fs}" fill="{fill}" font-weight="{weight}" '
                   f'font-style="{style}">{html.escape(ln)}</text>')
    return "".join(out)


def _arrow(x1, y1, x2, y2, dashed=False):
    import math
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    p1 = (bx - 4 * math.sin(ang), by + 4 * math.cos(ang))
    p2 = (bx + 4 * math.sin(ang), by - 4 * math.cos(ang))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
            f'stroke="#b7873a" stroke-width="2"{dash}/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} '
            f'{p2[0]:.1f},{p2[1]:.1f}" fill="#b7873a"/>')


def mermaid_to_svg(text):
    direction, nodes, order, edges, styles, caption = _parse(text)
    solid_ids = set()
    for s, d, st, _ in edges:
        if st == "solid":
            solid_ids.add(s); solid_ids.add(d)
    main = [n for n in order if n in solid_ids] or order[:]
    branches = [n for n in order if n not in main]

    wrapped = {n: _wrap(nodes[n], 30) for n in order}
    sizes = {n: _box_size(wrapped[n]) for n in order}
    mainW = max(sizes[n][0] for n in main)
    mainH = max(sizes[n][1] for n in main)

    els, pos = [], {}

    if direction == "LR":
        top = MARGIN + 16                      # headroom for edge labels
        x = MARGIN
        gaps = []
        for i, n in enumerate(main):
            pos[n] = (x, top, mainW, mainH)
            if i < len(main) - 1:
                lbl = next((e[3] for e in edges if e[0] == n and e[1] == main[i+1]), "")
                gap = max(28, len(lbl) * CHARW * FS_EDGE + 12)
                gaps.append(gap)
                x += mainW + gap
        rightmost = x + mainW
        for i, n in enumerate(main):
            bx, by, w, h = pos[n]
            els.append(_rect(bx, by, w, h, styles.get(n, {})))
            els.append(_text_block(bx + w/2, by + h/2, wrapped[n], FS_NODE, "#211d18"))
            if i < len(main) - 1:
                nb = pos[main[i+1]]
                els.append(_arrow(bx + w, by + h/2, nb[0], by + h/2))
                lbl = next((e[3] for e in edges if e[0] == n and e[1] == main[i+1]), "")
                if lbl:
                    els.append(f'<text x="{(bx+w+nb[0])/2:.1f}" y="{by-6:.1f}" '
                               f'text-anchor="middle" font-size="{FS_EDGE}" fill="#7e221d">'
                               f'{html.escape(lbl)}</text>')
        bottom = top + mainH
        for bn in branches:
            src = next((e[0] for e in edges if e[1] == bn), main[0])
            style_edge = next((e[2] for e in edges if e[1] == bn), "dashed")
            lbl = next((e[3] for e in edges if e[1] == bn), "")
            sx, sy, sw, sh = pos[src]
            bw, bh = sizes[bn]
            cx = sx + sw/2
            byy = sy + sh + 34
            els.append(_rect(cx - bw/2, byy, bw, bh, styles.get(bn, {"fill": "#f7ecec", "stroke": "#7e221d"})))
            els.append(_text_block(cx, byy + bh/2, wrapped[bn], FS_NODE - 1, "#5a1714"))
            els.append(_arrow(cx, sy + sh, cx, byy, dashed=(style_edge == "dashed")))
            if lbl:
                els.append(f'<text x="{cx+7:.1f}" y="{sy+sh+22:.1f}" text-anchor="start" '
                           f'font-size="{FS_EDGE}" fill="#7e221d">{html.escape(lbl)}</text>')
            rightmost = max(rightmost, cx + bw/2 + MARGIN)
            bottom = max(bottom, byy + bh)
        W = rightmost + MARGIN
        H = bottom + MARGIN + (20 if caption else 0)
    else:  # TD
        cx = MARGIN + mainW/2
        y = MARGIN
        for n in main:
            pos[n] = (cx - mainW/2, y, mainW, mainH)
            y += mainH + 24
        bottom = y - 24 + mainH
        for i, n in enumerate(main):
            bx, by, w, h = pos[n]
            els.append(_rect(bx, by, w, h, styles.get(n, {})))
            els.append(_text_block(cx, by + h/2, wrapped[n], FS_NODE, "#211d18"))
            if i < len(main) - 1:
                nb = pos[main[i+1]]
                els.append(_arrow(cx, by + h, cx, nb[1]))
        W = mainW + 2 * MARGIN
        capw = (len(caption) * CHARW * FS_CAP + 2 * MARGIN) if caption else 0
        W = max(W, capw)
        H = bottom + MARGIN + (20 if caption else 0)

    if caption:
        els.append(f'<text x="{W/2:.1f}" y="{H-8:.1f}" text-anchor="middle" '
                   f'font-size="{FS_CAP}" font-style="italic" fill="#6b6353">'
                   f'{html.escape(caption)}</text>')

    return (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="{FONT}">' + "".join(els) + "</svg>")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        src = open(sys.argv[1], encoding="utf-8").read()
        open(sys.argv[2], "w", encoding="utf-8").write(mermaid_to_svg(src))
        print("wrote", sys.argv[2])
    else:
        data = sys.stdin.read()
        sys.stdout.write(mermaid_to_svg(data))
