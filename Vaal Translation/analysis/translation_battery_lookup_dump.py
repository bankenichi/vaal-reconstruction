#!/usr/bin/env python3
"""Dump form-first dictionary hits for the 51-line surface corpus.

Reads only syntax_rerun_corpus_real.txt (or a packet corpus.txt).
Does not open committed_readings.csv, the master, gold, or result sheets.

Writes token_lookup_dump.csv: raw attested hits by surface form.
No project glosses. No C/soft grades (those are methodology).

Usage (from this directory):
    VAAL_DICT_DIR=/tmp/vaal_dicts python3 translation_battery_lookup_dump.py
"""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dict_lookup as dl  # noqa: E402

CORPUS = HERE / "syntax_rerun_corpus_real.txt"
OUT = HERE / "translation_battery_token_lookup_dump.csv"
MAX_HITS = 12


def corpus_forms(path: Path) -> list[str]:
    forms = []
    seen = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" not in line:
            continue
        _, vaal = line.split("\t", 1)
        for tok in vaal.split():
            key = dl.fold(tok.rstrip(".,!?;:…"))
            if not key or key in seen:
                continue
            seen.add(key)
            forms.append(tok.rstrip(".,!?;:…"))
    return forms


def main() -> None:
    os.environ.setdefault("VAAL_DICT_DIR", "/tmp/vaal_dicts")
    blob = dl.load_index()
    forms = corpus_forms(CORPUS)
    rows = []
    for surface in forms:
        hits = dl.hits_for(surface, blob["index"], access="online", latitude="loose")
        hits.sort(key=lambda h: (-len(h.get("fold") or ""), h.get("lang") or "", h.get("form") or ""))
        if not hits:
            rows.append(
                {
                    "surface": surface,
                    "rank": 0,
                    "form": "",
                    "lang": "",
                    "gloss": "",
                    "source": "",
                    "kind": "",
                    "residue": "",
                    "note": "no attested form hit in attached dictionaries",
                }
            )
            continue
        for i, h in enumerate(hits[:MAX_HITS], 1):
            gloss = (h.get("gloss") or "")[:160]
            gloss = (
                gloss.replace("\u2014", "-")
                .replace("\u2013", "-")
                .replace("\u00b7", " ")
            )
            rows.append(
                {
                    "surface": surface,
                    "rank": i,
                    "form": h.get("form") or "",
                    "lang": h.get("lang") or "",
                    "gloss": gloss,
                    "source": h.get("source") or "",
                    "kind": h.get("kind") or "",
                    "residue": h.get("residue") or "",
                    "note": "",
                }
            )
    fields = ["surface", "rank", "form", "lang", "gloss", "source", "kind", "residue", "note"]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    n_surf = len(forms)
    n_miss = sum(1 for r in rows if r["rank"] == 0)
    print(f"wrote {OUT.name}: {len(rows)} hit-rows for {n_surf} surfaces; {n_miss} misses")


if __name__ == "__main__":
    main()
