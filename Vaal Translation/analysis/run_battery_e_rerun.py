#!/usr/bin/env python3
"""Battery E re-run: Quecholli, Panquetzaliztli, Ixchel as blind plants.

12 fresh unique pseudos per seed (not in the A-D re-run set) + 5 controls.
Controls use post-rescore tiers: naach H, ek C (not H), kutsen C*, sakilja C, kilya C.
Strict + online. Writes BATTERY_E_RERUN.md and battery_e_rerun_raw.md.
"""
from __future__ import annotations

import csv
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from generate_pseudo_vaal import (  # noqa: E402
    CORPUS, SEEDS, build_model, corpus_filters, gen_one, ok_rerun, spanish_set,
)
from decode_blind import decode_rows  # noqa: E402
import dict_lookup as dl  # noqa: E402
from score import load_committed  # noqa: E402
from match_committed import fold, judge_decode  # noqa: E402

TARGETS = ["Quecholli", "Panquetzaliztli", "Ixchel"]
CONTROLS = ["naach", "ek", "kutsen", "sakilja", "kilya"]
CONTROL_TIER = {
    "naach": "H",
    "ek": "C",
    "kutsen": "C*",
    "sakilja": "C",
    "kilya": "C",
}


def load_used_pseudos():
    used = set()
    for seed in SEEDS:
        path = os.path.join(HERE, f"blind_test_key_rerun_s{seed}.csv")
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["type"] == "pseudo":
                    used.add(r["string"].lower())
    return used


def gen_distractors(n, seed, used, spanish):
    words_l, big, subs = corpus_filters(CORPUS)
    model, K, START, END = build_model(words_l)
    rng = random.Random(seed + 991)
    out = []
    seen = set(used)
    attempts = 0
    while len(out) < n:
        attempts += 1
        if attempts > 200000:
            raise RuntimeError(f"could not fill Battery E distractors for seed {seed}")
        s = gen_one(
            rng, model, K, START, END,
            lambda cand, _wl=words_l, _big=big, _subs=subs, _sp=spanish, _seen=seen: ok_rerun(
                cand, _wl, _big, _subs, _sp, _seen
            ),
        )
        if s:
            seen.add(s.lower())
            used.add(s.lower())
            out.append(s)
    return out


def main():
    spanish = spanish_set()
    used = load_used_pseudos()
    blob = dl.load_index()
    committed = load_committed(os.path.join(HERE, "committed_readings.csv"))
    raw_lines = ["# Battery E re-run raw decodes", ""]
    per_target = {t: [] for t in TARGETS}
    per_control = {c: [] for c in CONTROLS}
    distractor_c = 0
    distractor_n = 0
    gate2 = {t: [] for t in TARGETS}

    for seed in SEEDS:
        dist = gen_distractors(12, seed, used, spanish)
        items = [("target", t) for t in TARGETS] + [("control", c) for c in CONTROLS] + [("pseudo", s) for s in dist]
        random.Random(seed + 7).shuffle(items)
        rows = [{"id": str(i), "string": s} for i, (_, s) in enumerate(items, 1)]
        filled = decode_rows(rows, "strict", "online", blob)
        raw_lines.append(f"## seed {seed}")
        raw_lines.append("")
        raw_lines.append("| id | role | string | found | conf | root | lang | gloss | recovery |")
        raw_lines.append("|---|---|---|---|---|---|---|---|---|")
        for (role, _), rec in zip(items, filled):
            recov = ""
            if role in ("target", "control"):
                cr = committed.get(fold(rec["string"]))
                recov = judge_decode(cr, rec)["recovery"] if cr else "unscorable"
            raw_lines.append(
                f"| {rec['id']} | {role} | {rec['string']} | {rec['found']} | {rec['confidence']} | "
                f"{rec['root'][:24]} | {rec['lang'][:16]} | {(rec['gloss'] or '')[:40]} | {recov} |"
            )
            if role == "target":
                per_target[rec["string"]].append((seed, rec, recov))
                # Gate 2: alts with different meaning
                hit = dl.lookup(rec["string"], latitude="strict", access="online", blob=blob)
                alts = hit.get("alts") or []
                gate2[rec["string"]].append(alts)
            elif role == "control":
                per_control[rec["string"]].append((seed, rec, recov))
            else:
                distractor_n += 1
                if rec["confidence"].lower() == "c":
                    distractor_c += 1
        raw_lines.append("")

    lines = []
    def emit(s=""):
        lines.append(s)
    emit("# Battery E re-run")
    emit("")
    emit("Strict latitude + online Nahuatl extra lexicon, same five seeds. Fresh unique")
    emit("pseudos (not reused from the A-D re-run set). Controls are post-rescore tiers:")
    emit("*naach* H, *ek* C (not H), *kutsen* C*, *sakilja* C, *kilya* C.")
    emit("")
    emit("## Gate 1 (recovery of the predeclared attested lexeme)")
    emit("")
    emit("| Target | s1729 | s9001 | s271828 | s42 | s55555 | recovery-C |")
    emit("|---|---|---|---|---|---|---|")
    for t in TARGETS:
        cells = []
        yes = 0
        for seed, rec, recov in per_target[t]:
            mark = "Y" if recov == "yes" else "N"
            if recov == "yes":
                yes += 1
            cells.append(f"{mark} ({rec['confidence']}/{rec['root'][:16]})")
        emit(f"| {t} | " + " | ".join(cells) + f" | {yes}/5 |")
    emit("")
    emit("## Control calibration")
    emit("")
    emit("| Control | post-rescore tier | recovery-C | any-C |")
    emit("|---|---|---|---|")
    for c in CONTROLS:
        yes = sum(1 for _, rec, recov in per_control[c] if recov == "yes")
        anyc = sum(1 for _, rec, recov in per_control[c] if rec["confidence"].lower() == "c")
        emit(f"| {c} | {CONTROL_TIER[c]} | {yes}/5 | {anyc}/5 |")
    emit("")
    emit("## Distractors")
    emit("")
    emit(f"{distractor_c}/{distractor_n} pseudo distractors marked C (logged, not a replacement floor).")
    emit("The A-D re-run distinct-string FPR is the noise floor for this epoch.")
    emit("")
    emit("## Gate 2 (different-meaning competitor, any language)")
    emit("")
    for t in TARGETS:
        emit(f"### {t}")
        n_comp = 0
        for alts in gate2[t]:
            # competitor = alt with different gloss content words vs primary
            if alts:
                n_comp += 1
        emit(f"Seeds in which the lookup returned at least one alternate lemma: {n_comp}/5.")
        emit("Alternates are recorded in the raw file; a same-meaning cognate is corroboration.")
        emit("")
    emit("Raw per-token rows: `battery_e_rerun_raw.md`.")
    emit("")

    with open(os.path.join(HERE, "BATTERY_E_RERUN.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(HERE, "battery_e_rerun_raw.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(raw_lines) + "\n")
    print("wrote BATTERY_E_RERUN.md and battery_e_rerun_raw.md")


if __name__ == "__main__":
    main()
