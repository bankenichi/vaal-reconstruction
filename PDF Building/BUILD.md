# The Vaal Tongue, PDF build assets

This folder holds everything needed to regenerate `The_Vaal_Tongue.pdf` from the
master Markdown document. The build is self-contained: with these files in place,
one command produces the styled PDF.

## Contents

- `build_pdf.py`, the build script. It converts the Markdown to HTML, applies the
  full theme, and renders the PDF with WeasyPrint. The CSS theme and the three
  original SVG visuals are embedded inside this file as strings.
- `Vaal_Reconstruction.md`, the master source document, is the build input. It lives in the project root and is NOT shipped inside `Vaal_PDF_build_assets.zip` (so the bundle never carries a stale copy of the master); place the current master beside `build_pdf.py` before building.
- `fonts/`, the two typefaces used by the theme.
- `assets/`, standalone copies of the three SVG visuals, for inspection or editing.


## TOC page numbers

WeasyPrint's CSS `target-counter` often prints 0 for TOC entries on this stack.
`build_pdf.py` uses a two-pass render: pass 1 records `page.anchors` page numbers;
pass 2 substitutes those integers into `.toc-page` spans, then writes the PDF.
## Dependencies

Python 3 with four packages:

    pip install weasyprint markdown fonttools pypdf

WeasyPrint also relies on the system libraries Pango, Cairo, and GDK-Pixbuf, which
ship by default on most Linux distributions. `markdown` does the Markdown-to-HTML
step, `fonttools` is only needed if you want to regenerate the Cinzel static
weights (see below), and `pypdf` is used for the page-count check.

## Fonts

Both families are under the SIL Open Font License.

- Cardo (Regular, Bold, Italic) is the body text, chosen for its wide linguistic
  diacritic coverage. Source: Google Fonts, `ofl/cardo`.
- Cinzel (Regular, Bold) is the display and heading face, an engraved-capitals
  look. Source: Google Fonts, `ofl/cinzel`. Upstream now ships only a variable
  font, `Cinzel.ttf`. The static Regular and Bold here were instantiated from it
  with fonttools:

      python3 -c "from fontTools.ttLib import TTFont; \
      from fontTools.varLib.instancer import instantiateVariableFont as inst; \
      [(lambda f: (inst(f, {'wght': w}, inplace=True), f.save(n)))(TTFont('Cinzel.ttf')) \
       for w, n in [(400, 'Cinzel-Regular.ttf'), (700, 'Cinzel-Bold.ttf')]]"

  The variable source `Cinzel.ttf` is kept in `fonts/` so the statics can be
  rebuilt at any time.

## Visuals

All three SVGs are original geometry. None reproduces copyrighted or real-world
artwork.

- `cover_emblem.svg`, the cover medallion: a stepped temple, a sun disc, an
  offering drop, and flanking glyph blocks inside a rayed ring.
- `greca_divider.svg`, the stepped-fret (greca) divider used on the cover and the
  contents page.
- `glyph_block.svg`, the small block that marks each section heading.

In `build_pdf.py` these are embedded as strings: the emblem inline, the divider
and glyph as data URIs. The standalone files in `assets/` are the same artwork,
broken out for editing. If you change an SVG, paste the new content back into the
matching string in `build_pdf.py`; the script does not read the `assets/` folder.

## Build

Keep `build_pdf.py`, `Vaal_Reconstruction.md`, and the `fonts/` folder together,
then run:

    python3 build_pdf.py

The output is `The_Vaal_Tongue.pdf`, written next to the script. Paths are computed
relative to the script location, so the folder can live anywhere.

## Notes for editors

- The document follows three hard formatting rules: no em dashes, no middots, no
  emojis. The build adds none of these; keep the source clean.
- Citations are rendered manually from the numbered list so the printed numbers
  stay locked to the source values (1 to 53). An HTML ordered list would renumber
  and break every in-text reference, so do not switch to one.
- Avoid bold spans that wrap italics, that is, a double-asterisk run with a
  single-asterisk italic nested inside. The Markdown parser mis-nests that
  combination and leaks italics across the whole paragraph. Keep emphasis flat: a
  phrase is either bold or italic, not bold with italics inside it.
## Windows note (Layla)

WeasyPrint needs the GTK3 runtime DLLs on PATH. Install
[GTK for Windows Runtime Environment](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)
(default location C:\Program Files\GTK3-Runtime Win64), then either add its in
folder to the user PATH or prepend it for the build session:

    $env:PATH = "C:\Program Files\GTK3-Runtime Win64\bin;$env:PATH"
    python build_pdf.py

The build script expects citations under ## 18. Citations.

