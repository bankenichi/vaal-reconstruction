#!/usr/bin/env python3
"""Exploratory summaries from scored T-M / T-D sheets.

Does not change the primary Wilson headlines in score_translation_battery.py.
Writes translation_battery_explore.csv and prints tables for RESULTS.md.

Exploratory: per-text rates, clash/abstain CIs, vocative-name sensitivity,
per-line hotspots, translator-slot spread, declared-confidence calibration,
token clash tokens, Fleiss kappa on vs-gold bins, methodology-effect
heterogeneity. Not a null-model p-value and not PPV.
"""
from __future__ import annotations

import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEDS = [1729, 9001, 271828, 42, 55555]
N_BOOT = 10000
BOOT_SEED = 1729

TEXT_RANGES = [
    ("T1 chant", 1, 8),
    ("T2 litany", 9, 24),
    ("T3 commander", 25, 37),
    ("T4 drill", 38, 49),
    ("T5 Kamasan", 50, 51),
]
VOCATIVE = {39, 41, 47}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n <= 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    z2 = z * z
    den = 1.0 + z2 / n
    center = (p + z2 / (2 * n)) / den
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * n)) / n) / den
    return (p, max(0.0, center - margin), min(1.0, center + margin))


def fmt(k: int, n: int) -> str:
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * p:.1f}% [{100 * lo:.1f}, {100 * hi:.1f}]"


def bootstrap_diff(a: list[int], b: list[int], seed: int = BOOT_SEED):
    rng = random.Random(seed)
    na, nb = len(a), len(b)
    obs = (sum(a) / na) - (sum(b) / nb)
    diffs = []
    for _ in range(N_BOOT):
        sa = sum(a[rng.randrange(na)] for _ in range(na)) / na
        sb = sum(b[rng.randrange(nb)] for _ in range(nb)) / nb
        diffs.append(sa - sb)
    diffs.sort()
    lo = diffs[int(0.025 * N_BOOT)]
    hi = diffs[min(N_BOOT - 1, int(0.975 * N_BOOT))]
    return obs, lo, hi


def flags(rows, pred):
    return [1 if pred(r) else 0 for r in rows]


def fleiss_kappa(items: list[list[str]], cats: list[str]) -> float:
    """items: list of length N, each a list of R category labels."""
    n = len(items)
    r = len(items[0])
    if n == 0 or r < 2:
        return float("nan")
    p = {c: 0.0 for c in cats}
    for labels in items:
        for lab in labels:
            p[lab] += 1
    tot = n * r
    for c in cats:
        p[c] /= tot
    pe = sum(v * v for v in p.values())
    ps = []
    for labels in items:
        cnt = Counter(labels)
        ps.append((sum(v * v for v in cnt.values()) - r) / (r * (r - 1)))
    pbar = sum(ps) / n
    if abs(1 - pe) < 1e-12:
        return 1.0 if abs(pbar - 1) < 1e-12 else 0.0
    return (pbar - pe) / (1 - pe)


def load() -> tuple[list[dict], list[dict]]:
    lines = list(csv.DictReader((HERE / "translation_battery_line_scores.csv").open(encoding="utf-8")))
    toks = list(csv.DictReader((HERE / "translation_battery_token_scores.csv").open(encoding="utf-8")))
    for r in lines:
        r["line_id"] = int(r["line_id"])
        r["seed"] = int(r["seed"])
    for r in toks:
        r["line_id"] = int(r["line_id"])
        r["seed"] = int(r["seed"])
    return lines, toks


def by_batt(rows, batt):
    return [r for r in rows if r["battery"] == batt]


def main() -> None:
    lines, toks = load()
    out_rows = []

    def emit(section, battery, metric, k, n, extra=""):
        p, lo, hi = wilson(int(k) if k != "" else 0, int(n) if n else 0)
        rec = {
            "section": section,
            "battery": battery,
            "metric": metric,
            "k": k,
            "n": n,
            "p": "" if k == "" else p,
            "lo": "" if k == "" else lo,
            "hi": "" if k == "" else hi,
            "note": extra,
        }
        out_rows.append(rec)
        return rec

    print("## Exploratory: clash / abstain (Wilson 95%)")
    for batt in ("TM", "TD"):
        rows = by_batt(lines, batt)
        n = len(rows)
        for name, pred in (
            ("clash", lambda r: r["line_bin"] == "clash"),
            ("abstain", lambda r: r["line_bin"] == "abstain"),
            ("partial", lambda r: r["line_bin"] == "partial"),
        ):
            k = sum(1 for r in rows if pred(r))
            emit("bin", batt, name, k, n)
            print(f"  {batt} {name}: {fmt(k, n)}")

    print("\n## Exploratory: methodology effect on clash / abstain (bootstrap)")
    tm, td = by_batt(lines, "TM"), by_batt(lines, "TD")
    for label, pred in (
        ("clash", lambda r: r["line_bin"] == "clash"),
        ("abstain", lambda r: r["line_bin"] == "abstain"),
        ("match", lambda r: r["line_bin"] == "match"),
        ("match+partial", lambda r: r["line_bin"] in {"match", "partial"}),
    ):
        obs, lo, hi = bootstrap_diff(flags(tm, pred), flags(td, pred))
        emit("diff", "TM-TD", label, "", 255, f"{obs:+.4f} [{lo:+.4f}, {hi:+.4f}]")
        print(f"  {label}: {obs:+.4f}  [{lo:+.4f}, {hi:+.4f}]")

    print("\n## Exploratory: drop vocative Atziri! lines 39/41/47")
    for batt in ("TM", "TD"):
        rows = [r for r in by_batt(lines, batt) if r["line_id"] not in VOCATIVE]
        n = len(rows)
        m = sum(1 for r in rows if r["line_bin"] == "match")
        mp = sum(1 for r in rows if r["line_bin"] in {"match", "partial"})
        emit("no_vocative", batt, "match", m, n)
        emit("no_vocative", batt, "match+partial", mp, n)
        print(f"  {batt} match {fmt(m, n)}; match+partial {fmt(mp, n)}")
    tm_nv = [r for r in tm if r["line_id"] not in VOCATIVE]
    td_nv = [r for r in td if r["line_id"] not in VOCATIVE]
    obs, lo, hi = bootstrap_diff(
        flags(tm_nv, lambda r: r["line_bin"] in {"match", "partial"}),
        flags(td_nv, lambda r: r["line_bin"] in {"match", "partial"}),
    )
    print(f"  TM-TD match+partial (no vocative): {obs:+.4f} [{lo:+.4f}, {hi:+.4f}]")

    print("\n## Exploratory: per-text match+partial")
    for name, a, b in TEXT_RANGES:
        for batt in ("TM", "TD"):
            rows = [r for r in by_batt(lines, batt) if a <= r["line_id"] <= b]
            n = len(rows)
            m = sum(1 for r in rows if r["line_bin"] == "match")
            mp = sum(1 for r in rows if r["line_bin"] in {"match", "partial"})
            ab = sum(1 for r in rows if r["line_bin"] == "abstain")
            cl = sum(1 for r in rows if r["line_bin"] == "clash")
            emit("per_text", batt, f"{name}_match", m, n)
            emit("per_text", batt, f"{name}_mp", mp, n)
            print(
                f"  {name} {batt}: match {fmt(m, n)}; mp {fmt(mp, n)}; "
                f"clash {cl}/{n}; abstain {ab}/{n}"
            )
        tm_t = [r for r in tm if a <= r["line_id"] <= b]
        td_t = [r for r in td if a <= r["line_id"] <= b]
        obs, lo, hi = bootstrap_diff(
            flags(tm_t, lambda r: r["line_bin"] in {"match", "partial"}),
            flags(td_t, lambda r: r["line_bin"] in {"match", "partial"}),
        )
        print(f"    TM-TD mp: {obs:+.3f} [{lo:+.3f}, {hi:+.3f}]")

    print("\n## Exploratory: per-line hotspots (5 translators)")
    print("line  gold_short  TM_bins  TD_bins  TM-TD_mp")
    hotspots = []
    for lid in range(1, 52):
        gold = next(r["gold_en"] for r in lines if r["line_id"] == lid)
        tm_b = Counter(r["line_bin"] for r in tm if r["line_id"] == lid)
        td_b = Counter(r["line_bin"] for r in td if r["line_id"] == lid)
        tm_mp = tm_b["match"] + tm_b["partial"]
        td_mp = td_b["match"] + td_b["partial"]
        hotspots.append((td_mp - tm_mp, lid, gold, tm_b, td_b, tm_mp, td_mp))
        short = gold.replace("\n", " ")[:42]
        print(
            f"  {lid:2}  {short:<42}  TM {dict(tm_b)}  TD {dict(td_b)}  "
            f"mp {tm_mp}/5 vs {td_mp}/5"
        )

    print("\n  Largest T-M advantage (mp count):")
    for delta, lid, gold, tm_b, td_b, tm_mp, td_mp in sorted(hotspots)[:8]:
        if tm_mp >= td_mp:
            print(f"    L{lid} mp {tm_mp}/5 vs {td_mp}/5  ({gold[:50]})")
    print("  Largest T-D advantage (mp count):")
    for delta, lid, gold, tm_b, td_b, tm_mp, td_mp in sorted(hotspots, reverse=True)[:8]:
        if td_mp > tm_mp:
            print(f"    L{lid} mp {tm_mp}/5 vs {td_mp}/5  ({gold[:50]})")

    print("\n  Unanimous clash (5/5) both batteries:")
    both_clash = []
    for lid in range(1, 52):
        tm_cl = sum(1 for r in tm if r["line_id"] == lid and r["line_bin"] == "clash")
        td_cl = sum(1 for r in td if r["line_id"] == lid and r["line_bin"] == "clash")
        if tm_cl == 5 and td_cl == 5:
            gold = next(r["gold_en"] for r in lines if r["line_id"] == lid)
            both_clash.append((lid, gold))
            print(f"    L{lid}  {gold[:60]}")
    emit("hotspot", "both", "unanimous_clash_lines", len(both_clash), 51)

    print("\n## Exploratory: translator-slot match+partial")
    for batt in ("TM", "TD"):
        rates = []
        for seed in SEEDS:
            rows = [r for r in by_batt(lines, batt) if r["seed"] == seed]
            mp = sum(1 for r in rows if r["line_bin"] in {"match", "partial"})
            rates.append(mp / 51)
            emit("slot", batt, f"s{seed}_mp", mp, 51)
            print(f"  {batt} s{seed}: {fmt(mp, 51)}")
        rates.sort()
        print(f"    {batt} slot mp range {rates[0]:.3f} to {rates[-1]:.3f}")

    print("\n## Exploratory: declared confidence vs vs-gold bin")
    for batt in ("TM", "TD"):
        rows = by_batt(lines, batt)
        print(f"  {batt}")
        for conf in ("high", "medium", "low", "abstain"):
            sub = [r for r in rows if (r["confidence"] or "").strip().lower() == conf]
            n = len(sub)
            if n == 0:
                continue
            m = sum(1 for r in sub if r["line_bin"] == "match")
            mp = sum(1 for r in sub if r["line_bin"] in {"match", "partial"})
            cl = sum(1 for r in sub if r["line_bin"] == "clash")
            emit("calibration", batt, f"conf_{conf}_match", m, n)
            emit("calibration", batt, f"conf_{conf}_mp", mp, n)
            print(f"    {conf} n={n}: match {fmt(m, n)}; mp {fmt(mp, n)}; clash {cl}/{n}")

    print("\n## Exploratory: Fleiss kappa on vs-gold bins (5 translators, 51 lines)")
    cats = ["match", "partial", "clash", "abstain"]
    for batt in ("TM", "TD"):
        items = []
        for lid in range(1, 52):
            labels = [
                next(
                    r["line_bin"]
                    for r in by_batt(lines, batt)
                    if r["line_id"] == lid and r["seed"] == seed
                )
                for seed in SEEDS
            ]
            items.append(labels)
        k = fleiss_kappa(items, cats)
        emit("kappa", batt, "fleiss_vs_gold_bin", "", 51, f"{k:.3f}")
        print(f"  {batt} Fleiss kappa = {k:.3f}")

    print("\n## Exploratory: pairwise same vs-gold bin (not Jaccard)")
    from itertools import combinations

    for batt in ("TM", "TD"):
        same = 0
        n = 0
        for lid in range(1, 52):
            labels = [
                next(
                    r["line_bin"]
                    for r in by_batt(lines, batt)
                    if r["line_id"] == lid and r["seed"] == seed
                )
                for seed in SEEDS
            ]
            for i, j in combinations(range(5), 2):
                n += 1
                if labels[i] == labels[j]:
                    same += 1
        emit("same_bin", batt, "pairwise_same_gold_bin", same, n)
        print(f"  {batt} same-bin {fmt(same, n)}")

    print("\n## Exploratory: token clash hotspots (offered glosses)")
    for batt in ("TM", "TD"):
        recs = [r for r in toks if r["battery"] == batt]
        by_tok = defaultdict(Counter)
        for r in recs:
            by_tok[r["token"]][r["token_bin"]] += 1
        ranked = sorted(
            by_tok.items(),
            key=lambda kv: (-kv[1]["clash"], -sum(kv[1].values()), kv[0]),
        )
        print(f"  {batt} tokens with most clash offers:")
        for tok, c in ranked[:12]:
            n = sum(c.values())
            print(f"    {tok}: clash {c['clash']}/{n}  {dict(c)}")

    path = HERE / "translation_battery_explore.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["section", "battery", "metric", "k", "n", "p", "lo", "hi", "note"]
        )
        w.writeheader()
        w.writerows(out_rows)
    print(f"\nwrote {path.name} ({len(out_rows)} rows)")


if __name__ == "__main__":
    main()
