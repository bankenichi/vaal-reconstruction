#!/usr/bin/env python3
"""Score a blind null-model result file against its key.

Legacy behaviour (AUDIT_REVIEW F1): count any decoder `C` on a real token as a
true positive, ignoring root / lang / gloss. That hole is closed here.

Default: print BOTH the legacy any-C rates (so Batteries A-D remain
reproducible) AND a committed-recovery TPR when a committed-readings table is
available and the result rows carry root/lang/gloss.

Pseudo items have no designed meaning, so a `C` on pseudo is always a false
positive. Committed-match applies only to the real arm.

Usage:
  python3 score.py <results.csv> <key.csv>
  python3 score.py <results.csv> <key.csv> --committed committed_readings.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    from match_committed import judge_decode, lang_classes, extract_quoted_root
except ImportError:
    sys.path.insert(0, HERE)
    from match_committed import judge_decode, lang_classes, extract_quoted_root


def load_committed(path: str) -> dict:
    """Map folded aliases / tokens to a committed reading dict."""
    from match_committed import fold
    table = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rec = {
                "token": r.get("token") or "",
                "root": r.get("committed_root") or extract_quoted_root(r.get("source")),
                "lang": r.get("committed_lang") or r.get("source") or "",
                "gloss": r.get("committed_gloss") or r.get("gloss") or "",
                "source": r.get("source") or "",
                "lang_classes": lang_classes(r.get("committed_lang") or r.get("source") or ""),
            }
            names = [r.get("token") or ""]
            names += [a.strip() for a in (r.get("aliases") or "").split(";") if a.strip()]
            for n in names:
                table[fold(n)] = rec
    return table


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("res_path")
    p.add_argument("key_path")
    p.add_argument("--committed", default=os.path.join(HERE, "committed_readings.csv"),
                   help="committed-readings table (default: analysis/committed_readings.csv)")
    args = p.parse_args(argv)

    res = {}
    with open(args.res_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            res[r["id"]] = r
    key = {}
    with open(args.key_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key[r["id"]] = r

    committed = {}
    if args.committed and os.path.exists(args.committed):
        committed = load_committed(args.committed)

    P = dict(C=0, soft=0, none=0, Y=0, n=0)
    R = dict(C=0, soft=0, none=0, Y=0, n=0)
    Rmatch = dict(yes=0, no=0, unscorable=0, n=0)

    for i, kr in key.items():
        t = kr.get("type")
        d = res.get(i, {})
        c = (d.get("confidence") or "").strip().lower()
        found = (d.get("found(Y/N)") or d.get("found") or "").strip().upper()
        tgt = P if t == "pseudo" else R
        tgt["n"] += 1
        if c == "c":
            tgt["C"] += 1
        elif c == "soft":
            tgt["soft"] += 1
        else:
            tgt["none"] += 1
        if found == "Y":
            tgt["Y"] += 1
        if t != "pseudo" and committed:
            Rmatch["n"] += 1
            token = kr.get("string") or kr.get("token") or d.get("string") or d.get("token") or ""
            from match_committed import fold
            rec = committed.get(fold(token))
            if rec is None:
                Rmatch["unscorable"] += 1
            else:
                j = judge_decode(rec, d)
                Rmatch[j["recovery"]] = Rmatch.get(j["recovery"], 0) + 1

    fpr_c = P["C"] / P["n"] if P["n"] else 0
    fpr_soft = (P["C"] + P["soft"]) / P["n"] if P["n"] else 0
    tpr_c = R["C"] / R["n"] if R["n"] else 0
    tpr_found = R["Y"] / R["n"] if R["n"] else 0
    print(f"PSEUDO n={P['n']}: C={P['C']} soft={P['soft']} none={P['none']} | REAL n={R['n']}: C={R['C']} soft={R['soft']} none={R['none']}")
    print(f"FPR(C)={fpr_c:.2f}  FPR(C+soft)={fpr_soft:.2f}  TPR(C,any-root)={tpr_c:.2f}  TPR(found)={tpr_found:.2f}  Discrimination(C,any-root)={tpr_c-fpr_c:+.2f}")
    print("NOTE: TPR(C,any-root) is the legacy F1 scorer (any C counts, even a different lemma).")
    if committed and Rmatch["n"]:
        tpr_m = Rmatch["yes"] / Rmatch["n"]
        print(f"COMMITTED-RECOVERY (real arm only): yes={Rmatch['yes']} mismatch={Rmatch['no']} unscorable={Rmatch['unscorable']} n={Rmatch['n']}  TPR(recovery)={tpr_m:.2f}")
        print("Unscorable = C/soft/none rows with no committed table hit, or C with empty root/lang/gloss.")
    elif not committed:
        print("No committed-readings table loaded; recovery TPR not computed.")


if __name__ == "__main__":
    main()
