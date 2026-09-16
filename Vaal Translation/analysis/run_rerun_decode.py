#!/usr/bin/env python3
"""Fill all re-run Battery A-D worksheets via form-first dict lookup.

Does not open keys or committed_readings. Writes:
  blind_test_results_rerun_s{seed}.csv              Battery A
  blind_test_results_rerun_online_s{seed}.csv       Battery B
  blind_test_results_rerun_tight_s{seed}.csv        Battery C
  blind_test_results_rerun_tight_online_s{seed}.csv Battery D
"""
from __future__ import annotations

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dict_lookup as dl  # noqa: E402
from decode_blind import decode_rows  # noqa: E402

SEEDS = [1729, 9001, 271828, 42, 55555]
CELLS = [
    ("A", "loose", "offline", "blind_test_results_rerun_s{seed}.csv"),
    ("B", "loose", "online", "blind_test_results_rerun_online_s{seed}.csv"),
    ("C", "strict", "offline", "blind_test_results_rerun_tight_s{seed}.csv"),
    ("D", "strict", "online", "blind_test_results_rerun_tight_online_s{seed}.csv"),
]


def main():
    blob = dl.load_index()
    # Priority: D and A first (selection-matched A-then-D), then B and C.
    order = ["D", "A", "B", "C"]
    cells = {c[0]: c for c in CELLS}
    for name in order:
        _, lat, acc, pat = cells[name]
        print(f"=== Battery {name} {lat}/{acc} ===")
        for seed in SEEDS:
            ws = os.path.join(HERE, f"blind_test_worksheet_rerun_s{seed}.csv")
            out = os.path.join(HERE, pat.format(seed=seed))
            with open(ws, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            filled = decode_rows(rows, lat, acc, blob)
            fields = ["id", "string", "found", "confidence", "root", "lang", "gloss", "residue", "notes"]
            with open(out, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                for row in filled:
                    w.writerow(row)
            n = len(filled)
            c = sum(1 for r in filled if r["confidence"].lower() == "c")
            s = sum(1 for r in filled if r["confidence"].lower() == "soft")
            print(f"  s{seed}: n={n} C={c} soft={s} none={n-c-s} -> {os.path.basename(out)}")


if __name__ == "__main__":
    main()
