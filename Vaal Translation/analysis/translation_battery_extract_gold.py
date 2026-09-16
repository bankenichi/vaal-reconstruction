#!/usr/bin/env python3
"""Extract published English line translations for scoring only.

Same 51-line closed corpus as syntax_rerun_build_packets.py
(Texts 1-4 plus Kamasan Smith). Writes translation_battery_gold.csv.

Do not place this file in translator packets. Do not run this as a
translator. Score only after all ten sheets exist.

Usage (from this directory):
    python3 translation_battery_extract_gold.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE.parent / "Vaal_Reconstruction.md"
OUT = HERE / "translation_battery_gold.csv"

SOFT_MARK = re.compile(r"\\?\*")


def strip_soft_markers(vaal: str) -> str:
    s = SOFT_MARK.sub("", vaal)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("\u2026", "...")
    return s


def parse_row(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    return [c.strip() for c in line.strip("|").split("|")]


def extract(md: str) -> list[tuple[str, str, str]]:
    """Return (source_tag, vaal_surface, english) for the 51-line set."""
    lines = md.splitlines()
    out: list[tuple[str, str, str]] = []

    def take_table(start: int, vaal_idx: int, eng_idx: int, tag_prefix: str) -> int:
        i = start
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = parse_row(lines[i])
            i += 1
            if not cells or cells[0] in {"#", "Pair", "Speaker", "Group", "Vaal", "When"}:
                continue
            if set(cells[0]) <= {"-", ":"} or all(set(c) <= {"-", ":"} for c in cells):
                continue
            if vaal_idx >= len(cells) or eng_idx >= len(cells):
                continue
            vaal = strip_soft_markers(cells[vaal_idx])
            eng = cells[eng_idx].strip()
            if not vaal or not eng:
                continue
            n = sum(1 for t, _, _ in out if t.startswith(tag_prefix.split(".")[0]))
            out.append((f"{tag_prefix}.{n + 1}", vaal, eng))
        return i

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
            i = take_table(i, 1, 2, "T1")
            continue
        if section == "T2" and line.startswith("| Pair | Speaker | Vaal |"):
            i = take_table(i, 2, 3, "T2")
            continue
        if section == "T3" and line.startswith("| Group | Vaal |"):
            i = take_table(i, 1, 2, "T3")
            continue
        if section == "T4" and line.startswith("| Speaker | Vaal |"):
            i = take_table(i, 1, 2, "T4")
            continue
        if section == "T4" and line.startswith("| Vaal | English |"):
            i = take_table(i, 0, 1, "T4x")
            continue
        if section == "T5" and line.startswith("| Speaker | Vaal |"):
            i = take_table(i, 1, 2, "T5")
            section = "T5_done"
            continue
        i += 1
    return out


def main() -> None:
    rows = extract(MASTER.read_text(encoding="utf-8"))
    if len(rows) != 51:
        raise SystemExit(f"expected 51 gold lines, got {len(rows)}")
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["line_id", "source_tag", "vaal", "gold_en"])
        w.writeheader()
        for n, (tag, vaal, eng) in enumerate(rows, 1):
            w.writerow(
                {
                    "line_id": n,
                    "source_tag": tag,
                    "vaal": vaal,
                    "gold_en": eng,
                }
            )
    print(f"wrote {OUT.name}: {len(rows)} lines (scoring only)")


if __name__ == "__main__":
    main()
