#!/usr/bin/env python3
import os, re, markdown, pathlib
HERE = os.path.dirname(os.path.abspath(__file__))
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

SRC   = os.path.join(HERE, "..", "Vaal_Reconstruction.md")
OUT   = os.path.join(HERE, "The_Vaal_Tongue.pdf")
FONTS = os.path.join(HERE, "fonts")

raw = pathlib.Path(SRC).read_text(encoding="utf-8")

# --- prerender mermaid blocks to inline SVG (dependency-free, see render_mermaid.py) ---
import sys as _sys
_sys.path.insert(0, HERE)
import render_mermaid
def _inline_mermaid(m):
    return "\n\n<div class=\"figure\">" + render_mermaid.mermaid_to_svg(m.group(1)) + "</div>\n\n"
raw = re.sub(r"```mermaid[ \t]*\n(.*?)\n```", _inline_mermaid, raw, flags=re.DOTALL)

# --- split title / tagline / body ---
lines = raw.splitlines()
title_line = lines[0].lstrip("# ").strip()              # The Vaal Tongue: A Reconstruction
main_title, sub_title = [s.strip() for s in title_line.split(":", 1)]
tagline = ""
for ln in lines[1:8]:
    if ln.strip().startswith("*") and ln.strip().endswith("*"):
        tagline = ln.strip().strip("*").strip()
        break
body_start = next(i for i, ln in enumerate(lines) if ln.startswith("## 1."))
cit_h = next(i for i, ln in enumerate(lines) if ln.startswith("## 18. Citations"))

def _is_cite_cat(ln):
    s = ln.strip()
    return bool(re.match(r"^#{3,4}\s+\S", s) or re.match(r"^\*\*[^*].*\*\*\s*$", s))

def _is_cite_num(ln):
    return bool(re.match(r"^\d+\.\s", ln))

stream_start = next(
    i for i in range(cit_h + 1, len(lines))
    if _is_cite_cat(lines[i]) or _is_cite_num(lines[i])
)
body_md = "\n".join(lines[body_start:stream_start])

# parse citations and category subtitles; keep literal source numbers
blocks, cur_n, cur = [], None, []

def _flush_cite():
    global cur_n, cur
    if cur_n is not None:
        blocks.append(("cite", cur_n, " ".join(cur).strip()))
        cur_n, cur = None, []

for ln in lines[stream_start:]:
    if _is_cite_cat(ln):
        _flush_cite()
        title = re.sub(r"^#{3,4}\s+", "", ln.strip())
        title = title.strip("*").strip()
        blocks.append(("cat", title))
    else:
        m = re.match(r"^(\d+)\.\s+(.*)", ln)
        if m:
            _flush_cite()
            cur_n, cur = m.group(1), [m.group(2)]
        elif ln.strip():
            if cur_n is not None:
                cur.append(ln.strip())
_flush_cite()

# --- markdown -> html, capture section ids for the TOC ---
md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"],
                       extension_configs={"toc": {"permalink": False}})
body_html = md.convert(body_md)
def _flatten_toc(tokens):
    out = []
    for t in tokens:
        out.append((t["id"], t["name"], t["level"]))
        out += _flatten_toc(t.get("children", []))
    return out
toc_items = [(i, n, lv) for i, n, lv in _flatten_toc(md.toc_tokens) if lv <= 3]  # sections + subsections

mdi = markdown.Markdown(extensions=[])
def inline_md(t):
    mdi.reset()
    return re.sub(r"^<p>|</p>$", "", mdi.convert(t))
cit_parts = []
for b in blocks:
    if b[0] == "cat":
        cit_parts.append(f'<h3 class="cite-cat">{inline_md(b[1])}</h3>')
    else:
        n, t = b[1], b[2]
        cit_parts.append(
            f'<div class="cite"><span class="cn">{n}.</span>'
            f'<span class="ct">{inline_md(t)}</span></div>'
        )
body_html += '<div class="citations">' + "".join(cit_parts) + '</div>'

toc_html = "\n".join(
    f'<div class="toc-row toc-l{lv}"><a href="#{i}"><span class="toc-name">{n}</span><span class="toc-page" data-target="{i}">?</span></a></div>'
    for i, n, lv in toc_items
)

# --- original Mesoamerican-style cover emblem (all geometry is original) ---
EMBLEM = '''
<svg class="emblem" width="300" height="300" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="disc" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#13443b"/>
      <stop offset="100%" stop-color="#0a2c26"/>
    </radialGradient>
  </defs>
  <circle cx="200" cy="200" r="190" fill="url(#disc)" stroke="#b7873a" stroke-width="2.5"/>
  <circle cx="200" cy="200" r="178" fill="none" stroke="#7e221d" stroke-width="6"/>
  <circle cx="200" cy="200" r="170" fill="none" stroke="#d8b25a" stroke-width="1.4"/>
  <!-- radiating sun rays -->
  <g stroke="#c69a3a" stroke-width="3">
    ''' + "".join(
        f'<line x1="200" y1="200" x2="{200+150*__import__("math").cos(a)}" '
        f'y2="{200+150*__import__("math").sin(a)}" opacity="0.32"/>'
        for a in [i*3.14159/12 for i in range(24)]
    ) + '''
  </g>
  <circle cx="200" cy="200" r="120" fill="#0a2c26" stroke="#b7873a" stroke-width="1.2"/>
  <!-- stepped temple (3 tiers) -->
  <g fill="#b7873a">
    <rect x="150" y="232" width="100" height="14"/>
    <rect x="161" y="218" width="78"  height="14"/>
    <rect x="172" y="204" width="56"  height="14"/>
    <rect x="190" y="186" width="20"  height="18"/>
  </g>
  <!-- doorway -->
  <rect x="194" y="232" width="12" height="14" fill="#7e221d"/>
  <!-- sun disc above temple -->
  <circle cx="200" cy="150" r="22" fill="none" stroke="#d8b25a" stroke-width="3"/>
  <circle cx="200" cy="150" r="9"  fill="#7e221d"/>
  <!-- offering drop -->
  <path d="M200 168 q9 13 0 22 q-9 -9 0 -22 z" fill="#7e221d"/>
  <!-- flanking glyph blocks -->
  <g fill="none" stroke="#c69a3a" stroke-width="2.4">
    <rect x="120" y="138" width="20" height="20"/>
    <rect x="260" y="138" width="20" height="20"/>
  </g>
  <g fill="#7e221d">
    <rect x="126" y="144" width="8" height="8"/>
    <rect x="266" y="144" width="8" height="8"/>
  </g>
</svg>
'''

# greca (stepped-fret) divider used under the main title on the cover and as an hr
GRECA = ('data:image/svg+xml;utf8,'
  "<svg xmlns='http://www.w3.org/2000/svg' width='120' height='16' viewBox='0 0 120 16'>"
  "<g fill='none' stroke='%23b7873a' stroke-width='2'>"
  "<path d='M2 14 H22 V4 H14 V10 H8'/>"
  "<path d='M42 14 H62 V4 H54 V10 H48'/>"
  "<path d='M82 14 H102 V4 H94 V10 H88'/>"
  "</g></svg>")

# small glyph-block bullet shown before each section heading
GLYPH = ('data:image/svg+xml;utf8,'
  "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 22 22'>"
  "<rect x='1' y='1' width='20' height='20' rx='2' fill='none' stroke='%230f5a4e' stroke-width='1.6'/>"
  "<rect x='5' y='5' width='12' height='12' fill='none' stroke='%23b7873a' stroke-width='1.4'/>"
  "<rect x='9' y='9' width='4' height='4' fill='%237e221d'/></svg>")

CSS_TEXT = '''
@font-face { font-family:"Cardo"; src:url("file://%(F)s/Cardo-Regular.ttf"); font-weight:normal; font-style:normal; }
@font-face { font-family:"Cardo"; src:url("file://%(F)s/Cardo-Bold.ttf");    font-weight:bold;   font-style:normal; }
@font-face { font-family:"Cardo"; src:url("file://%(F)s/Cardo-Italic.ttf");  font-weight:normal; font-style:italic; }
@font-face { font-family:"Cinzel"; src:url("file://%(F)s/Cinzel-Regular.ttf"); font-weight:normal; }
@font-face { font-family:"Cinzel"; src:url("file://%(F)s/Cinzel-Bold.ttf");    font-weight:bold; }

@page {
  size: Letter;
  margin: 23mm 19mm 20mm 19mm;
  background: #f7f1e4;
  @top-center {
    content: "The Vaal Tongue";
    font-family:"Cinzel"; font-size:7.5pt; letter-spacing:2px;
    color:#9c7b3f; padding-bottom:3pt;
  }
  @bottom-center {
    content: counter(page);
    font-family:"Cinzel"; font-size:8.5pt; color:#7e221d;
  }
}
@page cover { margin:0; background:#0c352d; @top-center{content:none} @bottom-center{content:none} }
@page frontmatter { @top-center{content:none} }

html { -weasy-hyphens:auto; }
body { margin:0; font-family:"Cardo","DejaVu Serif",serif; font-size:10.4pt; line-height:1.5;
       color:#211d18; text-align:justify; }

/* ---------- COVER ---------- */
.cover { page:cover; width:215.9mm; height:279mm; box-sizing:border-box;
         position:relative; color:#f3e9d2; background:#0c352d; }
.cover .frame { position:absolute; top:14mm; left:14mm; right:14mm; bottom:14mm;
                border:1.5px solid #b7873a; }
.cover .frame2 { position:absolute; top:16mm; left:16mm; right:16mm; bottom:16mm;
                 border:0.8px solid #7e221d; }
.cover .inner { position:absolute; top:0; left:0; right:0; bottom:0;
                display:flex; flex-direction:column; align-items:center;
                justify-content:flex-start; padding:26mm 24mm 22mm 24mm; }
.emblem { width:60mm; height:60mm; display:block; margin-bottom:7mm; }
.cover h1 { font-family:"Cinzel"; font-weight:bold; color:#e7c771;
            font-size:33pt; letter-spacing:5px; margin:0; text-align:center; line-height:1.08; }
.cover .greca { width:42mm; height:8mm; margin:6mm 0 5mm 0;
                background:url("%(GRECA)s") no-repeat center; background-size:contain; }
.cover h2 { font-family:"Cinzel"; font-weight:normal; color:#f3e9d2;
            font-size:14pt; letter-spacing:7px; margin:0; text-align:center;
            background:none; border-bottom:none; padding:0; break-before:avoid; }
.cover .tag { font-family:"Cardo"; font-style:italic; font-size:11pt; color:#cdbd97;
              text-align:center; max-width:118mm; margin:13mm auto 0 auto; line-height:1.5; }
.cover .strip { position:absolute; left:24mm; right:24mm; bottom:24mm; text-align:center;
                font-family:"Cinzel"; font-size:8pt; letter-spacing:3px; color:#b7873a; }

/* ---------- FRONT MATTER (TOC) ---------- */
.toc { page:frontmatter; }
.toc h1 { font-family:"Cinzel"; font-weight:bold; color:#0f5a4e; font-size:19pt;
          letter-spacing:3px; text-align:center; margin:6mm 0 2mm 0; }
.toc .rule { height:8mm; background:url("%(GRECA)s") repeat-x center; background-size:auto 100%;
             margin:0 auto 9mm auto; width:60mm; }
.toc-row { margin:0; padding:3.4pt 0; border-bottom:0.5px dotted #c9b27a; }
.toc-row a { color:#211d18; text-decoration:none; display:flex; justify-content:space-between;
             align-items:baseline; gap:8pt; font-size:11pt; }
.toc-name { font-variant:small-caps; letter-spacing:0.4px; }
.toc-page { font-family:"Cinzel"; color:#7e221d; font-size:9.5pt; flex:0 0 auto; }
.toc-l3 { padding:2pt 0 2pt 9mm; border-bottom:none; }
.toc-l3 a { color:#6b6353; font-size:9pt; }
.toc-l3 .toc-name { font-variant:normal; letter-spacing:0.2px; }
.toc-l3 .toc-page { font-size:8.5pt; color:#9a8552; }

/* ---------- BODY ---------- */
h2 { font-family:"Cinzel"; font-weight:bold; color:#0f5a4e; font-size:15.5pt;
     letter-spacing:1px; margin:0 0 5mm 0; padding:7pt 0 6pt 30pt;
     border-bottom:2px solid #b7873a; break-after:avoid;
     background:url("%(GLYPH)s") no-repeat left 4pt; background-size:20pt 20pt; }
h2 { break-before:page; }
.toc + * h2:first-of-type { break-before:auto; }
h3 { font-family:"Cinzel"; font-weight:normal; color:#7e221d; font-size:11.5pt;
     letter-spacing:0.5px; margin:6mm 0 2mm 0; break-after:avoid; }
h4 { font-family:"Cardo"; font-weight:bold; color:#0f5a4e; font-size:10.6pt;
     margin:4mm 0 1.5mm 0; break-after:avoid; }
p { margin:0 0 2.4mm 0; }
strong { color:#5a1714; }
em { color:#10463c; }
a { color:#0f5a4e; word-break:break-word; }

hr { border:none; height:9mm; background:url("%(GRECA)s") repeat-x center; background-size:auto 70%;
     margin:6mm auto; opacity:0.85; }

blockquote { margin:3mm 0; padding:2mm 5mm; border-left:3px solid #b7873a;
             background:#efe7d4; font-style:italic; }

code { font-family:"DejaVu Sans Mono",monospace; font-size:8.6pt; background:#efe7d4;
       padding:0 2px; border-radius:2px; word-break:break-all; }

ol, ul { margin:0 0 2.4mm 0; padding-left:7mm; }
li { margin:0 0 1.2mm 0; }

/* citations: tighter, wrap long urls */
h2#citations ~ ol li, .citations li { font-size:9pt; line-height:1.34; word-break:break-word; }

.figure { text-align:center; margin:5mm 0 4mm 0; break-inside:avoid; }
.figure svg { max-width:100%; height:auto; display:block; margin:0 auto; }

/* ---------- TABLES ---------- */
table { width:100%; border-collapse:collapse; margin:3mm 0 4mm 0; font-size:8.6pt;
        line-height:1.32; break-inside:auto; }
thead { display:table-header-group; }
th { background:#0f5a4e; color:#f7f1e4; font-family:"Cinzel"; font-weight:normal;
     font-size:7.8pt; letter-spacing:0.4px; text-align:left; padding:4pt 5pt;
     border:0.5px solid #0c4339; }
td { padding:3.4pt 5pt; border:0.5px solid #d8c9a0; vertical-align:top;
     overflow-wrap:break-word; text-align:left; }
tbody tr:nth-child(even) { background:#f0e8d6; }
tbody tr { break-inside:avoid; }
td em { color:#10463c; font-style:italic; }
td strong { color:#5a1714; }

.citations { margin-top:3mm; text-align:left; }
.cite-cat { font-family:"Cardo"; font-weight:bold; color:#7e221d; font-size:11pt;
            letter-spacing:0; margin:6mm 0 2.2mm 0; break-after:avoid;
            text-align:left; background:none; border-bottom:none; padding:0; }
.cite { display:flex; gap:7pt; font-size:9pt; line-height:1.36; margin:0 0 1.8mm 0; }
.cite .cn { color:#7e221d; font-family:"Cinzel"; min-width:20pt; text-align:right; flex:0 0 auto; }
.cite .ct { flex:1 1 auto; word-break:break-word; overflow-wrap:anywhere; }
'''
CSS_TEXT = (CSS_TEXT.replace("%(F)s", FONTS)
                    .replace("%(GRECA)s", GRECA)
                    .replace("%(GLYPH)s", GLYPH))

DOC = '''<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<section class="cover">
  <div class="frame"></div><div class="frame2"></div>
  <div class="inner">
    %(EMBLEM)s
    <h1>%(MAIN)s</h1>
    <div class="greca"></div>
    <h2>%(SUB)s</h2>
    <div class="tag">%(TAG)s</div>
  </div>
  <div class="strip">PATH OF EXILE  |  MESOAMERICAN RECONSTRUCTION</div>
</section>

<section class="toc">
  <h1>Contents</h1>
  <div class="rule"></div>
  %(TOC)s
</section>

%(BODY)s
</body></html>'''
DOC = (DOC.replace("%(EMBLEM)s", EMBLEM).replace("%(MAIN)s", main_title.upper())
          .replace("%(SUB)s", sub_title.upper()).replace("%(TAG)s", tagline)
          .replace("%(TOC)s", toc_html).replace("%(BODY)s", body_html))

# tag the citations <h2> with an id so the css selector can match (toc ext already ids it)
DOC = DOC.replace('id="18-citations"', 'id="citations"')
DOC = DOC.replace('href="#18-citations"', 'href="#citations"')
DOC = DOC.replace('data-target="18-citations"', 'data-target="citations"')
toc_items = [("citations" if i == "18-citations" else i, n, lv) for i, n, lv in toc_items]

pathlib.Path(os.path.join(HERE,"_doc.html")).write_text(DOC, encoding="utf-8")
fc = FontConfiguration()
styles = [CSS(string=CSS_TEXT, font_config=fc)]
# Pass 1: learn which PDF page each heading id lands on.
document = HTML(string=DOC, base_url=HERE).render(stylesheets=styles, font_config=fc)
anchor_page = {}
for page_i, page in enumerate(document.pages, start=1):
    for name in page.anchors:
        anchor_page.setdefault(name, page_i)
missing = [i for i, n, lv in toc_items if i not in anchor_page]
if missing:
    raise SystemExit("TOC anchors missing from render: " + ", ".join(missing[:12]))
DOC2 = re.sub(
    r'<span class="toc-page" data-target="([^"]+)">\?</span>',
    lambda m: '<span class="toc-page" data-target="%s">%d</span>' % (m.group(1), anchor_page[m.group(1)]),
    DOC,
)
pathlib.Path(os.path.join(HERE,"_doc.html")).write_text(DOC2, encoding="utf-8")
HTML(string=DOC2, base_url=HERE).write_pdf(
    OUT, stylesheets=styles, font_config=fc)
print("wrote", OUT, "pages", len(document.pages), "toc_anchors", len(anchor_page))
