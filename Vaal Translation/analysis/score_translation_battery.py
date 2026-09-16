#!/usr/bin/env python3
"""Score translation-battery sheets against gold. Run AFTER all ten sheets exist.

Reads:
  translation_battery_gold.csv
  translation_battery_TM_s{seed}.csv and translation_battery_TD_s{seed}.csv
  translation_battery_line_scores.csv (required: human/LLM rubric scores)

Writes:
  translation_battery_score_summary.csv
  prints Wilson CIs and bootstrap difference CIs

Do not run this while a translator is drafting.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEDS = [1729, 9001, 271828, 42, 55555]
BINS = ("match", "partial", "clash", "abstain")


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n <= 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    z2 = z * z
    den = 1.0 + z2 / n
    center = (p + z2 / (2 * n)) / den
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * n)) / n) / den
    return (p, max(0.0, center - margin), min(1.0, center + margin))


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fmt_ci(k: int, n: int) -> str:
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {100*p:.1f}% [{100*lo:.1f}, {100*hi:.1f}]"


def bootstrap_diff(a: list[int], b: list[int], n_boot: int = 10000, seed: int = 1729) -> tuple[float, float, float]:
    rng = random.Random(seed)
    na, nb = len(a), len(b)
    obs = (sum(a) / na) - (sum(b) / nb)
    diffs = []
    for _ in range(n_boot):
        sa = sum(a[rng.randrange(na)] for _ in range(na)) / na
        sb = sum(b[rng.randrange(nb)] for _ in range(nb)) / nb
        diffs.append(sa - sb)
    diffs.sort()
    lo = diffs[int(0.025 * n_boot)]
    hi = diffs[min(n_boot - 1, int(0.975 * n_boot))]
    return obs, lo, hi


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scores", default=str(HERE / "translation_battery_line_scores.csv"))
    args = p.parse_args()
    scores = load_csv(Path(args.scores))
    by_batt = defaultdict(list)
    by_line = defaultdict(lambda: defaultdict(list))
    for r in scores:
        batt = r["battery"].strip().upper()
        bin_ = r["line_bin"].strip().lower()
        if bin_ not in BINS:
            raise SystemExit(f"bad line_bin {bin_!r} in {r}")
        by_batt[batt].append(bin_)
        by_line[batt][int(r["line_id"])].append(bin_)

    print("## Line-slot vs gold (Wilson 95%)")
    flags = {}
    for batt in ("TM", "TD"):
        bins = by_batt[batt]
        n = len(bins)
        m = sum(1 for b in bins if b == "match")
        mp = sum(1 for b in bins if b in {"match", "partial"})
        flags[batt] = {
            "match": [1 if b == "match" else 0 for b in bins],
            "mp": [1 if b in {"match", "partial"} else 0 for b in bins],
        }
        print(f"{batt} match: {fmt_ci(m, n)}")
        print(f"{batt} match+partial: {fmt_ci(mp, n)}")

    print("\n## Per-line match rate across 5 translators")
    for batt in ("TM", "TD"):
        rates = []
        for lid in range(1, 52):
            bs = by_line[batt][lid]
            if len(bs) != 5:
                raise SystemExit(f"{batt} line {lid} has {len(bs)} scores")
            rates.append(sum(1 for b in bs if b == "match") / 5.0)
        rates_sorted = sorted(rates)
        med = rates_sorted[len(rates_sorted) // 2]
        q1 = rates_sorted[len(rates_sorted) // 4]
        q3 = rates_sorted[(3 * len(rates_sorted)) // 4]
        mean = sum(rates) / len(rates)
        # Wilson on rounded mean count is not the inferential unit; report mean/median.
        print(
            f"{batt} per-line match fraction: mean={mean:.3f} median={med:.3f} IQR=[{q1:.3f}, {q3:.3f}]"
        )

    print("\n## Methodology effect (TM minus TD), bootstrap 10000 line-slots")
    for label, key in (("match", "match"), ("match+partial", "mp")):
        obs, lo, hi = bootstrap_diff(flags["TM"][key], flags["TD"][key])
        print(f"{label}: {obs:+.3f}  95% percentile CI [{lo:+.3f}, {hi:+.3f}]")

    if any("pair_compatible" in r for r in scores):
        print("\n## Inter-translator (from scores file, if present)")


if __name__ == "__main__":
    main()
