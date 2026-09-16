#!/usr/bin/env python3
"""Build gloss-blind syntax-panel packets from the canonical master.

Extracts the closed syntactic corpus defined in master section 3.2 and
counted in section 17.5: connected Vaal utterances in Texts 1-4 plus the
Kamasan Smith lines in Text 5 (51 lines). Ahuatotli and Mektul skill-cries
are excluded (section 3.2: not weighted).

English translations, speaker names, and project glosses are not written
into the analyst packets.

Scramble: Python 3 random.Random(1729); for each numbered line in order,
split on whitespace, shuffle tokens in place, rejoin with a single space.
Punctuation stays attached to the token it belonged to. Single-token lines
are unchanged. Seed 1729 is the archived control seed from SYN-2.

Usage (from this directory):
    python3 syntax_rerun_build_packets.py
"""
from __future__ import annotations

import csv
import random
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE.parent / "Vaal_Reconstruction.md"
SEED = 1729

# Soft-token asterisks in the master are written as \* in markdown.
SOFT_MARK = re.compile(r"\\?\*")


def strip_soft_markers(vaal: str) -> str:
    """Remove project soft-parse asterisks; keep apostrophes and punctuation."""
    s = SOFT_MARK.sub("", vaal)
    s = re.sub(r"\s+", " ", s).strip()
    # Collapse ellipsis variants to a single ascii ellipsis token-tail.
    s = s.replace("\u2026", "...")
    return s


def parse_row(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    cells = [c.strip() for c in line.strip("|").split("|")]
    return cells


def extract_vaal_from_tables(md: str) -> list[tuple[str, str]]:
    """Return (source_tag, vaal_surface) for the 51-line closed corpus.

    Table layouts in the master:
      Text 1: # | Vaal | English
      Text 2: Pair | Speaker | Vaal | English
      Text 3: Group | Vaal | English
      Text 4 catechism: Speaker | Vaal | English
      Text 4 one-offs: Vaal | English
      Text 5 Kamasan: Speaker | Vaal | English
    """
    lines = md.splitlines()
    out: list[tuple[str, str]] = []

    def take_table(start: int, vaal_idx: int, tag_prefix: str) -> int:
        i = start
        # skip header and separator
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = parse_row(lines[i])
            i += 1
            if not cells or cells[0] in {"#", "Pair", "Speaker", "Group", "Vaal", "When"}:
                continue
            if set(cells[0]) <= {"-", ":"} or all(set(c) <= {"-", ":"} for c in cells):
                continue
            if vaal_idx >= len(cells):
                continue
            vaal = strip_soft_markers(cells[vaal_idx])
            if not vaal:
                continue
            n = sum(1 for t, _ in out if t.startswith(tag_prefix.split(".")[0]))
            out.append((f"{tag_prefix}.{n + 1}", vaal))
        return i

    # Walk by section headers so we do not pick up later tables (lexicon, etc.).
    section = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## 4."):
            section = "T1"
        elif line.startswith("## 5."):
            section = "T2"
        elif line.startswith("## 6."):
            section = "T3"
        elif line.startswith("## 7."):
            section = "T4"
        elif line.startswith("## 8."):
            section = "T5"
        elif line.startswith("## 9."):
            break

        if section == "T1" and line.startswith("| # | Vaal |"):
            i = take_table(i, 1, "T1")
            continue
        if section == "T2" and line.startswith("| Pair | Speaker | Vaal |"):
            i = take_table(i, 2, "T2")
            continue
        if section == "T3" and line.startswith("| Group | Vaal |"):
            i = take_table(i, 1, "T3")
            continue
        if section == "T4" and line.startswith("| Speaker | Vaal |"):
            i = take_table(i, 1, "T4")
            continue
        if section == "T4" and line.startswith("| Vaal | English |"):
            i = take_table(i, 0, "T4x")
            continue
        if section == "T5" and line.startswith("| Speaker | Vaal |"):
            # Kamasan Smith only (first table under section 8). Stop after it.
            i = take_table(i, 1, "T5")
            section = "T5_done"
            continue
        i += 1
    return out


def tokenize(surface: str) -> list[str]:
    return [t for t in surface.split() if t]


def form_key(token: str) -> str:
    """Case-folded form with trailing punctuation stripped, for grouping spellings."""
    t = token.strip()
    t = t.rstrip(".,!?;:…")
    t = t.rstrip(".")
    return t.casefold()


def main() -> None:
    md = MASTER.read_text(encoding="utf-8")
    rows = extract_vaal_from_tables(md)
    if len(rows) != 51:
        raise SystemExit(f"expected 51 closed-corpus lines, got {len(rows)}")

    numbered = [(i + 1, tag, vaal) for i, (tag, vaal) in enumerate(rows)]
    token_count = sum(len(tokenize(vaal)) for _, _, vaal in numbered)
    if token_count != 186:
        # Do not silently drift from the published 51/186 count; fail loud.
        raise SystemExit(f"expected 186 tokens, got {token_count}")

    corpus_path = HERE / "syntax_rerun_corpus_real.txt"
    with corpus_path.open("w", encoding="utf-8") as f:
        f.write("# Gloss-blind syntax corpus (real order)\n")
        f.write("# Closed set: Texts 1-4 plus Kamasan Smith (master section 3.2).\n")
        f.write("# Numbered surface lines only. No English translations.\n")
        f.write("# Built by syntax_rerun_build_packets.py from Vaal_Reconstruction.md.\n")
        f.write(f"# Lines: {len(numbered)}. Whitespace tokens: {token_count}.\n")
        f.write("\n")
        for n, tag, vaal in numbered:
            f.write(f"{n}\t{vaal}\n")

    # Form-only token inventory from the corpus (not from committed_readings).
    counts: Counter[str] = Counter()
    spellings: dict[str, Counter[str]] = {}
    for _, _, vaal in numbered:
        for tok in tokenize(vaal):
            key = form_key(tok)
            counts[key] += 1
            spellings.setdefault(key, Counter())[tok] += 1

    tokens_path = HERE / "syntax_rerun_tokens_form_only.csv"
    with tokens_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "form_key",
                "attested_spellings",
                "count",
            ]
        )
        for key in sorted(counts, key=lambda k: (-counts[k], k)):
            attested = "; ".join(
                f"{sp} x{c}" if c > 1 else sp
                for sp, c in spellings[key].most_common()
            )
            w.writerow([key, attested, counts[key]])

    rng = random.Random(SEED)
    scrambled_path = HERE / "syntax_rerun_corpus_scrambled_s1729.txt"
    with scrambled_path.open("w", encoding="utf-8") as f:
        f.write("# Syntax corpus, word order shuffled within each line.\n")
        f.write(f"# Procedure: random.Random({SEED}); split on whitespace; shuffle; rejoin.\n")
        f.write("# Same line numbers as the real packet. Vocabulary preserved.\n")
        f.write("# Built by syntax_rerun_build_packets.py.\n")
        f.write("\n")
        for n, tag, vaal in numbered:
            toks = tokenize(vaal)
            rng.shuffle(toks)
            f.write(f"{n}\t{' '.join(toks)}\n")

    print(f"wrote {corpus_path.name}: {len(numbered)} lines, {token_count} tokens")
    print(f"wrote {tokens_path.name}: {len(counts)} form keys")
    print(f"wrote {scrambled_path.name}: seed {SEED}")


if __name__ == "__main__":
    main()
