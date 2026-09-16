#!/usr/bin/env python3
"""Score the adversarial (Gate 2) pass.

AUDIT_REVIEW N3: the previous scorer counted a competitor only when the
adversary's language class differed from the committed class. Same-language
homophones (ek wasp vs ek' star; akal quarrel vs pond) and alternate
segmentations were invisible.

A FALL is now a strong attested competitor whose meaning does not overlap the
committed gloss, regardless of language class. Same-meaning cognates remain
corroboration, not competition. Alternate segmentations that yield a different
meaning also fall.

Residual limit: the archived CSVs store one best root and one alt-language
root. Competitors the adversary never wrote down cannot be recovered without
re-running decoders. That gap is reported, not invented.
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) + os.sep

try:
    from match_committed import cls_committed_fn
except Exception:
    pass

from match_committed import (
    lang_class, lang_classes, content_words, sense_match, fold,
)


def cls_committed(src):
    classes = lang_classes(src)
    if "Name" in classes:
        return "Name"
    if "Nahuan" in classes and "Maya" not in classes and "Spanish" not in classes and "Kiche" not in classes:
        return "Nahuan"
    if "Spanish" in classes and len(classes) == 1:
        return "Spanish"
    if "Kiche" in classes and "Maya" not in classes:
        return "Kiche"
    if "Maya" in classes and "Nahuan" not in classes:
        return "Maya"
    # Dual-source: keep a joined label; Gate 2 no longer filters on inequality.
    return "+".join(sorted(classes))


def cls_adv(l):
    return lang_class(l)


def strg(x):
    x = (x or "").lower()
    if "strong" in x:
        return "strong"
    if "weak" in x:
        return "weak"
    return "none"


def looks_like_alt_segmentation(committed_root: str, adv_root: str) -> bool:
    """True when the adversary joins two content roots the committed parse does not.

    Slash spellings (maax/max, nach/naach) are orthographic variants, not
    segmentations. A plus-join counts only if it introduces a new content root.
    """
    a = (adv_root or "").lower()
    if "+" not in a and " or " not in a:
        return False
    ctoks = set(re.findall(r"[a-z]{3,}", fold(committed_root)))
    atoks = set(re.findall(r"[a-z]{3,}", fold(adv_root)))
    extra = atoks - ctoks
    affixish = {t for t in extra if t.startswith("el") or t in {"tal", "bal", "il", "ane", "ti"}}
    return bool(extra - affixish)


def load():
    com = {}
    with open(HERE + "adversarial_worksheet.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            com[r["id"]] = {
                "token": r["token"],
                "cclass": cls_committed(r["current_source"]),
                "classes": lang_classes(r["current_source"]),
                "cgloss": r["gloss"],
                "csource": r["current_source"],
                "conf": r["current_conf"],
            }
    adv = {}
    for fp in sorted(glob.glob(HERE + "adversarial_results_batch*.csv")):
        with open(fp, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                adv[r["id"]] = r
    return com, adv


def competitors_for(c, a):
    """List strong different-meaning competitors, any language class."""
    out = []
    slots = [
        ("best_root", "best_lang", "best_gloss", "best_strength"),
        ("alt_root_difflang", "alt_lang", "alt_gloss", "alt_strength"),
    ]
    extra = c["csource"] + " " + c["cgloss"]
    for root_k, lang_k, gl_k, st_k in slots:
        if strg(a.get(st_k)) != "strong":
            continue
        root = a.get(root_k) or ""
        lang = a.get(lang_k) or ""
        gloss = a.get(gl_k) or ""
        if not root or root.lower() == "none":
            continue
        same_meaning = sense_match(c["cgloss"], gloss, extra)
        alt_seg = looks_like_alt_segmentation(c["csource"], root)
        # Same-meaning hits are corroboration even when the adversary writes a
        # plus-join or a slash variant. Only a different meaning competes.
        if same_meaning:
            continue
        acl = cls_adv(lang)
        same_lang = acl in c["classes"] or acl == "?"
        kind = []
        if not same_lang and acl != "?":
            kind.append("cross-language")
        if same_lang:
            kind.append("same-language")
        if alt_seg:
            kind.append("alt-segmentation")
        if not same_meaning:
            kind.append("DIFF-meaning")
        out.append({
            "root": root,
            "lang": acl,
            "gloss": gloss,
            "same_lang": same_lang,
            "alt_seg": alt_seg,
            "kind": "+".join(kind) or "competitor",
        })
    return out


def main():
    com, adv = load()
    surv = fall = name = 0
    falls = []
    rows = []
    for i, c in com.items():
        if c["cclass"] == "Name" or c["classes"] == {"Name"}:
            name += 1
            rows.append((i, c["token"], "N/A", "name", []))
            continue
        a = adv.get(i, {})
        comps = competitors_for(c, a)
        if comps:
            fall += 1
            falls.append((i, c["token"], c["cclass"], c["cgloss"], comps))
            rows.append((i, c["token"], "FALL", c["cclass"], comps))
        else:
            surv += 1
            rows.append((i, c["token"], "SURVIVE", c["cclass"], []))
    tested = surv + fall
    print(f"Committed tokens: {len(com)} | testable (non-name): {tested} | names(N/A): {name}")
    print(f"SURVIVE: {surv}  FALL: {fall}   survival rate = {surv/tested:.1%}" if tested else "no testable")
    same_lang_falls = [f for f in falls if any(d["same_lang"] for d in f[4])]
    cross_falls = [f for f in falls if any((not d["same_lang"]) for d in f[4])]
    altseg_falls = [f for f in falls if any(d["alt_seg"] for d in f[4])]
    print(f"  falls involving a same-language competitor: {len(same_lang_falls)}")
    print(f"  falls involving a cross-language competitor: {len(cross_falls)}")
    print(f"  falls involving an alternate segmentation: {len(altseg_falls)}")
    print("RESIDUAL LIMIT: only competitors written in adversarial_results_batch*.csv can be scored. Homophones a decoder never recorded (for example Gate-1 wasp on ek) are not invented here.")
    print("\n=== FALLEN TOKENS ===")
    for i, tok, ccl, cg, sd in falls:
        print(f"[{i}] {tok}  (committed {ccl}: '{cg[:40]}')")
        for d in sd:
            print(f"      vs {d['lang']} '{d['root']}' = '{d['gloss'][:45]}'  [{d['kind']}]")
    out_path = HERE + "gate2_rescore.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "token", "outcome", "committed_class", "competitor_root", "competitor_lang", "competitor_kind", "competitor_gloss"])
        for i, tok, outcome, ccl, comps in rows:
            if not comps:
                w.writerow([i, tok, outcome, ccl, "", "", "", ""])
            else:
                for d in comps:
                    w.writerow([i, tok, outcome, ccl, d["root"], d["lang"], d["kind"], d["gloss"]])
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
