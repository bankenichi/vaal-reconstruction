#!/usr/bin/env python3
"""Gate 1 (strict decode) and Gate 2 (adversarial, same-language on) for the 78-row lexicon.

Decode is form-first over attached dictionaries. committed_readings.csv is joined
only after sheets are filled. Writes rerun batch CSVs, gate1_rescore_rerun.csv,
gate2_rescore_rerun.csv, and updates token_classification.csv (prerun snapshot
already frozen).
"""
from __future__ import annotations

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dict_lookup as dl  # noqa: E402
from decode_blind import decode_rows  # noqa: E402
from score import load_committed  # noqa: E402
from match_committed import fold, judge_decode, content_words, sense_match  # noqa: E402

PROTOCOL = {
    "33": ("unexplained_residue", "section 9 note: -zeh coda is a non-morphemic tail. Gate 1 forbids unexplained residue."),
    "34": ("dual_incompatible_bundle", "one H row bundles Maya ma' negation and Nahuatl ma optative."),
    "53": ("dual_incompatible_readings", "section 9 note: Ambiguous uk' drink vs puuch' crush."),
}

ROOT_FAMILIES = {
    "ik'": ["ik'bala", "ikba'yucane", "Ik'eche", "ik'el"],
    "aocmo": ["Aiokmo", "'Ayok"],
    "atl": ["atla", "Atziri"],
    "el": ["Ela", "elba"],
    "muk'": ["mucane", "mujuk'"],
    "k'ex": ["Kextal", "qexcan"],
    "ti'": ["te", "Ti"],
}


def primary_token(tok: str) -> str:
    tok = re.split(r"\s*/\s*", tok)[0].strip()
    tok = re.sub(r"\([^)]*\)", "", tok).strip()
    return tok


def main():
    blob = dl.load_index()
    tokens = []
    with open(os.path.join(HERE, "token_classification_prerun.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tokens.append({"id": r["id"], "token": r["token"], "string": primary_token(r["token"])})

    # Gate 1 decode (surface only)
    filled = decode_rows(tokens, "strict", "online", blob)
    by_id = {r["id"]: r for r in filled}

    # Write batches of 20
    fields = ["id", "token", "found", "root", "lang", "gloss", "confidence", "residue", "notes"]
    batch, bno = [], 1
    for t, rec in zip(tokens, filled):
        batch.append({
            "id": t["id"], "token": t["token"], "found": rec["found"], "root": rec["root"],
            "lang": rec["lang"], "gloss": rec["gloss"], "confidence": rec["confidence"],
            "residue": rec["residue"], "notes": rec["notes"],
        })
        if len(batch) == 20:
            path = os.path.join(HERE, f"strict_committed_results_rerun_batch{bno}.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(batch)
            print(f"wrote {path} n={len(batch)}")
            batch, bno = [], bno + 1
    if batch:
        path = os.path.join(HERE, f"strict_committed_results_rerun_batch{bno}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(batch)
        print(f"wrote {path} n={len(batch)}")

    # Gate 2: lookup alts
    adv_fields = ["id", "token", "best_root", "best_lang", "best_gloss", "best_strength",
                  "alt_root_difflang", "alt_lang", "alt_gloss", "alt_strength"]
    adv_rows = []
    for t in tokens:
        hit = dl.lookup(t["string"], latitude="strict", access="online", blob=blob)
        alts = hit.get("alts") or []
        best_root, best_lang, best_gloss, best_st = hit["root"], hit["lang"], hit["gloss"], ""
        if hit["confidence"].lower() == "c":
            best_st = "strong"
        elif hit["confidence"].lower() == "soft":
            best_st = "weak"
        else:
            best_st = "none"
        alt = {"root": "none", "lang": "none", "gloss": "none", "st": "none"}
        for a in alts:
            g = a.get("gloss") or ""
            if dl.gloss_quality(g) < 2:
                continue
            if fold(a.get("form") or "") == fold(best_root or "") and sense_match(best_gloss, g):
                continue
            if sense_match(best_gloss, g):
                continue
            alt = {"root": a["form"], "lang": a["lang"], "gloss": g, "st": "strong"}
            break
        adv_rows.append({
            "id": t["id"], "token": t["token"],
            "best_root": best_root or "none", "best_lang": best_lang or "none",
            "best_gloss": best_gloss or "none", "best_strength": best_st,
            "alt_root_difflang": alt["root"], "alt_lang": alt["lang"],
            "alt_gloss": alt["gloss"], "alt_strength": alt["st"],
        })

    for i in range(0, len(adv_rows), 20):
        bno = i // 20 + 1
        path = os.path.join(HERE, f"adversarial_results_rerun_batch{bno}.csv")
        chunk = adv_rows[i:i + 20]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=adv_fields)
            w.writeheader()
            w.writerows(chunk)
        print(f"wrote {path} n={len(chunk)}")

    # Score against committed readings (after decode)
    committed = load_committed(os.path.join(HERE, "committed_readings.csv"))
    g1_fields = ["id", "token", "legacy_confidence", "recovery", "reason", "committed_root",
                 "committed_gloss", "dec_root", "dec_lang", "dec_gloss", "gate1_strict",
                 "gate1_where", "gate2_adversarial", "gate2_note", "protocol", "tier"]
    g2_fields = ["id", "token", "outcome", "committed_class", "competitor_root",
                 "competitor_lang", "competitor_kind", "competitor_gloss"]
    g1_out, g2_out, class_out = [], [], []
    lore_ids = set()
    prerun = {}
    with open(os.path.join(HERE, "token_classification_prerun.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            prerun[r["id"]] = r
            if "+L" in (r.get("tier") or "") or (r.get("tier") or "").endswith("L"):
                lore_ids.add(r["id"])

    n_h = n_cs = n_c = n_s = 0
    for t, rec, adv in zip(tokens, filled, adv_rows):
        cr = committed.get(fold(t["string"])) or committed.get(fold(t["token"]))
        if cr is None:
            for part in re.split(r"[/;()]", t["token"]):
                part = part.strip()
                if part:
                    cr = committed.get(fold(part))
                    if cr:
                        break
        if cr is None:
            j = {"recovery": "unscorable", "reason": "no_committed_row", "confidence": rec["confidence"],
                 "dec_root": rec["root"], "dec_lang": rec["lang"], "dec_gloss": rec["gloss"]}
        else:
            j = judge_decode(cr, rec)
        proto = PROTOCOL.get(t["id"])
        g1 = "fail"
        g1_note = j.get("reason") or ""
        if j["recovery"] == "yes":
            g1 = "pass"
            g1_note = "recovery=yes"
        if proto:
            g1 = f"pass;protocol_{proto[0]}" if g1 == "pass" else f"fail;protocol_{proto[0]}"
            if j["recovery"] == "yes":
                g1 = f"pass;protocol_{proto[0]}"
                # protocol demotion: cannot be H
        # names
        cclass = (cr or {}).get("lang") or ""
        is_name = "name" in cclass.lower() or "(name" in ((cr or {}).get("source") or "").lower()

        fall = adv["alt_strength"] == "strong" and adv["alt_root_difflang"] not in ("", "none")
        if is_name:
            g2 = "n/a"
            g2_note = "proper name; Gate 2 not applicable"
        elif fall:
            g2 = "fall"
            g2_note = f"DIFF-meaning: {adv['alt_lang']} {adv['alt_root_difflang']} = {adv['alt_gloss'][:60]}"
        else:
            g2 = "survive"
            g2_note = "no strong different-meaning competitor written by the lookup"

        # Tier
        lore = t["id"] in lore_ids or "+L" in (prerun[t["id"]].get("tier") or "")
        proto_blocks_h = bool(proto) and j["recovery"] == "yes"
        if g1.startswith("pass") and g2 == "survive" and not proto_blocks_h:
            tier = "H+L" if lore else "H"
            n_h += 1
        elif g2 == "fall":
            tier = "C+L*" if lore else "C*"
            n_cs += 1
        elif (prerun[t["id"]].get("tier") or "").startswith("S"):
            tier = "S+L" if lore else "S"
            n_s += 1
        else:
            tier = "C+L" if lore else "C"
            n_c += 1
        if t["id"] == "62" and j["recovery"] != "yes":
            # pul: artifact exists in this epoch; still C if recovery failed
            pass

        g1_out.append({
            "id": t["id"], "token": t["token"],
            "legacy_confidence": rec["confidence"],
            "recovery": j["recovery"], "reason": j.get("reason") or "",
            "committed_root": (cr or {}).get("root") or "",
            "committed_gloss": (cr or {}).get("gloss") or "",
            "dec_root": rec["root"], "dec_lang": rec["lang"], "dec_gloss": rec["gloss"],
            "gate1_strict": g1,
            "gate1_where": f"strict_committed_results_rerun id={t['id']} {g1_note}",
            "gate2_adversarial": g2, "gate2_note": g2_note,
            "protocol": proto[0] if proto else "",
            "tier": tier,
        })
        g2_out.append({
            "id": t["id"], "token": t["token"],
            "outcome": "N/A" if g2 == "n/a" else ("FALL" if g2 == "fall" else "SURVIVE"),
            "committed_class": cclass,
            "competitor_root": adv["alt_root_difflang"] if fall else "",
            "competitor_lang": adv["alt_lang"] if fall else "",
            "competitor_kind": "DIFF-meaning" if fall else "",
            "competitor_gloss": adv["alt_gloss"] if fall else "",
        })
        class_out.append({
            "id": t["id"], "token": t["token"],
            "gate1_strict": g1 if g1.startswith("pass") or g1.startswith("fail") else g1,
            "gate2_adversarial": g2,
            "tier": tier,
        })

    with open(os.path.join(HERE, "gate1_rescore_rerun.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=g1_fields)
        w.writeheader()
        w.writerows(g1_out)
    with open(os.path.join(HERE, "gate2_rescore_rerun.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=g2_fields)
        w.writeheader()
        w.writerows(g2_out)
    with open(os.path.join(HERE, "token_classification.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "token", "gate1_strict", "gate2_adversarial", "tier"])
        w.writeheader()
        w.writerows(class_out)

    rec_yes = sum(1 for r in g1_out if r["recovery"] == "yes")
    proto_clean = sum(1 for r in g1_out if r["tier"].startswith("H"))
    print(f"Gate 1 recovery yes={rec_yes}/78 protocol-clean H={proto_clean}")
    print(f"tiers H={n_h} C*={n_cs} C={n_c} S={n_s}")
    print("updated token_classification.csv (prerun snapshot preserved)")


if __name__ == "__main__":
    main()
