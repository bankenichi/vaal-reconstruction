#!/usr/bin/env python3
"""Rescore Gate 1 against the predeclared committed reading.

Reads:
  adversarial_worksheet.csv          declared root / lang / gloss
  strict_committed_results_batch*.csv  archived strict decodes (61 rows)
  adversarial_results_batch*.csv       Gate 2
  BATTERY_E names (hardcoded attested exact lexemes)
  Battery D tight-online Eztli rows (documented override)

Writes:
  committed_readings.csv
  gate1_rescore.csv
  token_classification.csv
  RESCORE_OUTPUT.md

Does not re-run blind decoders. Rows that lack root/lang/gloss are labelled
unscorable rather than guessed.
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from match_committed import (
    extract_quoted_root, judge_decode, lang_classes, fold,
)
from score_adversarial import load as load_adv, competitors_for

# Protocol demotions (HARDENING_PROTOCOL / AUDIT_REVIEW F6). These are not
# new etymologies: they rest on the entries' own notes.
PROTOCOL = {
    "33": {  # k'ux (quxzeh)
        "flag": "unexplained_residue",
        "note": "section 9 note: -zeh coda is a non-morphemic tail. Gate 1 forbids unexplained residue.",
    },
    "34": {  # ma
        "flag": "dual_incompatible_bundle",
        "note": "one H row bundles Maya ma' negation and Nahuatl ma optative.",
    },
    "53": {  # uch' / pu uch'
        "flag": "dual_incompatible_readings",
        "note": "section 9 note: Ambiguous uk' drink vs puuch' crush. A hardened entry cannot carry two incompatible readings.",
    },
}

# pul / puul was published as a Gate-1 pass with no decode in any result file.
PUL = {
    "id": "62",
    "token": "pul / puul",
    "source": 'Maya pul / puul "to throw, cast, hurl"[36]',
    "gloss": "throw, cast, cast down",
    "lang": "Maya",
}

BATTERY_E = [
    {
        "id": "63",
        "token": "Quecholli",
        "source": "Nah. quecholli (roseate spoonbill; the 14th veintena)[10][54]",
        "gloss": "precious-feather bird / the weapon-month (a Vaal mace)",
        "lang": "Nahuatl",
        "gate1": "pass",
        "gate1_note": "Battery E 5/5 exact attested lexeme quecholli",
        "gate2": "survive",
        "lore": True,
    },
    {
        "id": "64",
        "token": "Panquetzaliztli",
        "source": "Nah. pan(tli) banner + quetza raise + -liztli[10][55]",
        "gloss": "the raising of banners (15th veintena; a Vaal mace)",
        "lang": "Nahuatl",
        "gate1": "pass",
        "gate1_note": "Battery E 5/5 exact attested compound",
        "gate2": "survive",
        "lore": True,
    },
    {
        "id": "65",
        "token": "Ixchel",
        "source": 'Yucatec Ix- (fem./agentive) + Chel "rainbow" (the goddess Ix Chel)[7][56]',
        "gloss": "the Godstealer (a Vaal citizen; later the Trialmaster)",
        "lang": "Yucatec Maya",
        "gate1": "pass",
        "gate1_note": "Battery E 5/5 attested theonym Ix Chel",
        "gate2": "survive",
        "lore": True,
    },
]

# Section 9 rows that were L-only (AUDIT_REVIEW F5). L is a tag, not a tier.
# None of these were in the 61-row strict decode; gates stay pending.
L_ONLY = [
    ("66", "chikula'", "Maya", 'Maya chikul "sign, omen"[7]', "sign, omen", "C+L"),
    ("67", "Gyan'uks", "Nahuatl", 'Nah. yancuic "new"[10]', "the new ones -> (your) new children", "C+L"),
    ("68", "kíimil", "Maya", "Maya kíimil[7]", "death, the dead", "C+L"),
    ("69", "ko'janti", "Maya", 'Maya ko\' "come" + han- "eat" + -ti[7]', "come, devour", "C+L"),
    ("70", "kux / kuxkal / kuxte'", "Maya", "Maya kuxtal[7]", "life, the living", "C+L"),
    ("71", "le / le'", "Maya", "Yucatec article le...o'[7]", "the", "C+L"),
    ("72", "líimek", "Maya", 'Maya lu\'um "earth"[7]', "those in the earth, the dead", "C+L"),
    ("73", "Ma'oxe", "Maya", "Maya ma' without + xok count[7]", "the countless / numberless spirits", "C+L"),
    ("74", "Tlaxye'", "Nahuatl", "Nah. tlal- / tlacah[10]", "land, people", "C+L"),
    ("75", "Tzokan'te / tzok", "Maya", "Maya ts'ook[7]", "end, the last", "C+L"),
    ("76", "Xatlene", "Nahuatl", 'Nah. xotla "to kindle, blaze, glow"[10]', "kindle! / the kindler", "S+L"),
    ("77", "yax / Yaxe", "Maya", "Maya yax[7]", "first, new, green", "C+L"),
    ("78", "yuquia", "Nahuatl", 'Nah. yocoya "create, devise"[10]', "the made, the wrought", "C+L"),
]

# Plant-token aliases used in the 30-item null-model real arm.
PLANT_ALIASES = {
    "Eztli": "Eztli Pilli",
    "Maax": "máax",
    "maax": "máax",
    "naach": "náach",
    "ti": "Ti",
    "kahk": "k'áak' (kahk)",
    "quxzeh": "k'ux (quxzeh)",
    "Kuxkal": "kux / kuxkal / kuxte'",
}


def load_worksheet():
    rows = []
    with open(os.path.join(HERE, "adversarial_worksheet.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def load_strict():
    out = {}
    for fp in sorted(glob.glob(os.path.join(HERE, "strict_committed_results_batch*.csv"))):
        with open(fp, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out[r["id"]] = r
    return out


def eztli_battery_d_override():
    """Eztli is soft in the 61-row strict CSV but C at matching root in Battery D.

    Count how many tight-online (Battery D) and tight-offline (Battery C) rows
    for string Eztli recover eztli/blood.
    """
    hits = []
    for kind, globpat in (
        ("D_online", "blind_test_results_tight_online_s*.csv"),
        ("C_offline", "blind_test_results_tight_s*.csv"),
    ):
        for fp in sorted(glob.glob(os.path.join(HERE, globpat))):
            with open(fp, encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    tok = (r.get("string") or r.get("token") or "")
                    if tok.lower() == "eztli":
                        hits.append((kind, os.path.basename(fp), r))
    committed = {
        "token": "Eztli Pilli",
        "root": "eztli pilli",
        "lang": "Nahuatl",
        "gloss": "blood; noble, prince",
        "source": 'Nah. eztli "blood" + pilli "noble, prince"[10]',
        "lang_classes": lang_classes("Nahuatl"),
    }
    scored = []
    for kind, fn, r in hits:
        j = judge_decode(committed, r)
        scored.append((kind, fn, j, r))
    return scored


def build_committed_csv(ws_rows):
    path = os.path.join(HERE, "committed_readings.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "token", "aliases", "committed_root", "committed_lang", "committed_gloss", "source"])
        seen_tokens = {}
        for r in ws_rows:
            root = extract_quoted_root(r["current_source"])
            aliases = []
            tok = r["token"]
            seen_tokens[fold(tok)] = r["id"]
            # split slash variants
            for part in re.split(r"\s*/\s*", tok):
                p = part.strip()
                if p and fold(p) != fold(tok):
                    aliases.append(p)
            w.writerow([r["id"], tok, ";".join(aliases), root, r["current_source"], r["gloss"], r["current_source"]])
        w.writerow([PUL["id"], PUL["token"], "pul;puul", "pul puul", PUL["source"], PUL["gloss"], PUL["source"]])
        for e in BATTERY_E:
            w.writerow([e["id"], e["token"], "", extract_quoted_root(e["source"]), e["lang"], e["gloss"], e["source"]])
        for i, tok, lang, src, gloss, _tier in L_ONLY:
            w.writerow([i, tok, "", extract_quoted_root(src), lang, gloss, src])
        # plant aliases as extra rows pointing at the same reading
        # (score.py looks up by folded token / alias column; add alias names)
        extra_aliases = [
            ("15", "Eztli", "Eztli Pilli"),
            ("35", "Maax", "máax"),
            ("38", "naach", "náach"),
            ("47", "ti", "Ti"),
            ("26", "kahk", "k'áak' (kahk)"),
            ("33", "quxzeh", "k'ux (quxzeh)"),
            ("70", "Kuxkal", "kux / kuxkal / kuxte'"),
        ]
        for cid, alias, _canon in extra_aliases:
            # already have aliases column; rewrite would be messy. Append alias-only rows.
            pass
    # Re-write with aliases column filled for plants.
    # Simpler: append alias rows that duplicate the parent reading.
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_id = {r["id"]: r for r in rows}
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "token", "aliases", "committed_root", "committed_lang", "committed_gloss", "source"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
        # plant-only names that are not already tokens
        plant_map = {
            "Eztli": "15",
            "Maax": "35",
            "naach": "38",
            "ti": "47",
            "kahk": "26",
            "quxzeh": "33",
            "Kuxkal": "70",
        }
        for alias, cid in plant_map.items():
            parent = by_id[cid]
            if fold(alias) == fold(parent["token"]):
                continue
            w.writerow({
                "id": cid,
                "token": alias,
                "aliases": "",
                "committed_root": parent["committed_root"],
                "committed_lang": parent["committed_lang"],
                "committed_gloss": parent["committed_gloss"],
                "source": parent["source"],
            })
    return path


def tier_of(gate1, gate2, proto_flag, lore, pending=False, soft=False):
    L = "+L" if lore else ""
    if pending:
        return ("S+L" if soft else "C+L") if lore else ("S" if soft else "C")
    if soft:
        return "S+L" if lore else "S"
    if proto_flag:
        if gate2 == "fall":
            return "C+L*" if lore else "C*"
        return "C" + L
    if gate1 == "pass" and gate2 == "survive":
        return "H" + L
    if gate2 == "fall":
        return "C+L*" if lore else "C*"
    return "C" + L


def main():
    ws = load_worksheet()
    strict = load_strict()
    build_committed_csv(ws)
    com_adv, adv = load_adv()

    eztli_rows = eztli_battery_d_override()
    eztli_d_yes = sum(1 for kind, fn, j, r in eztli_rows if kind == "D_online" and (j["recovery"] == "yes" or (r.get("confidence") or "").strip().lower() == "c"))
    eztli_c_yes = sum(1 for kind, fn, j, r in eztli_rows if kind == "C_offline" and j["recovery"] == "yes")
    eztli_d_c = sum(1 for kind, fn, j, r in eztli_rows if kind == "D_online" and (r.get("confidence") or "").strip().lower() == "c")
    eztli_d_n = sum(1 for kind, _, _, _ in eztli_rows if kind == "D_online")

    recs = []
    for r in ws:
        i = r["id"]
        committed = {
            "token": r["token"],
            "root": extract_quoted_root(r["current_source"]),
            "lang": r["current_source"],
            "gloss": r["gloss"],
            "source": r["current_source"],
            "lang_classes": lang_classes(r["current_source"]),
        }
        dec = strict.get(i, {})
        j = judge_decode(committed, dec)
        # Gate 1 decision
        if i == "15":
            # Eztli Pilli: strict CSV is soft (matching roots, labelled soft).
            # Battery D: 5/5 C. Offline tight also recovers blood/eztli.
            gate1 = "pass"
            gate1_where = (
                f"strict_committed CSV confidence=soft (root {dec.get('root')!r} gloss {dec.get('gloss')!r}); "
                f"override: Battery D tight-online C on Eztli in {eztli_d_c}/{eztli_d_n} seeds "
                f"(recovery-scorable yes={eztli_c_yes} in Battery C offline where columns exist). "
                f"AUDIT_REVIEW O2 documented this upgrade; retained because the recovered root is eztli/blood, not a homophone."
            )
            j["recovery"] = "yes"
            j["reason"] = "battery_d_override_matching_root"
        elif j["recovery"] == "yes":
            gate1 = "pass"
            gate1_where = f"strict_committed_results id={i} recovery=yes ({j['reason']})"
        elif j["recovery"] == "unscorable":
            gate1 = "unscorable"
            gate1_where = f"strict_committed_results id={i} C but empty root/lang/gloss"
        else:
            gate1 = "fail"
            gate1_where = f"strict_committed_results id={i} {j['reason']} dec_root={j['dec_root']!r} dec_lang={j['dec_lang']!r} dec_gloss={j['dec_gloss']!r}"

        proto = PROTOCOL.get(i)
        if proto and gate1 == "pass":
            gate1_where += f" | PROTOCOL {proto['flag']}: {proto['note']} (Gate-1 decoder match stands; H forbidden)"

        # Gate 2 from existing adversarial CSV
        arow = adv.get(i, {})
        crow = com_adv.get(i, {
            "token": r["token"],
            "cclass": "?",
            "classes": committed["lang_classes"],
            "cgloss": r["gloss"],
            "csource": r["current_source"],
        })
        comps = competitors_for(crow, arow) if crow.get("cclass") != "Name" else []
        if "Name" in committed["lang_classes"] or crow.get("cclass") == "Name":
            gate2 = "n/a"
            gate2_note = "proper name; Gate 2 not applicable"
        elif comps:
            gate2 = "fall"
            gate2_note = "; ".join(f"{d['kind']}: {d['lang']} {d['root']} = {d['gloss'][:40]}" for d in comps)
        else:
            gate2 = "survive"
            gate2_note = "no strong different-meaning competitor in archived adversarial CSV"

        lore = "L" in (r.get("current_conf") or "")
        pending = False
        g1_for_tier = "fail" if proto and gate1 == "pass" else gate1
        # Protocol: decoder may have matched, but H requires a clean Gate 1.
        if proto:
            g1_for_tier = "fail"
        tier = tier_of(g1_for_tier if gate1 != "unscorable" else "fail", gate2, bool(proto), lore)
        recs.append({
            "id": i,
            "token": r["token"],
            "gate1_strict": gate1 if not proto else f"{gate1};protocol_{proto['flag']}",
            "gate2_adversarial": gate2,
            "tier": tier,
            "legacy_confidence": (dec.get("confidence") or "none"),
            "recovery": j["recovery"],
            "reason": j["reason"],
            "dec_root": j["dec_root"],
            "dec_lang": j["dec_lang"],
            "dec_gloss": j["dec_gloss"],
            "committed_root": committed["root"],
            "committed_gloss": r["gloss"],
            "gate1_where": gate1_where,
            "gate2_note": gate2_note,
            "protocol": proto["flag"] if proto else "",
        })

    # pul: no decode artifact
    recs.append({
        "id": "62",
        "token": PUL["token"],
        "gate1_strict": "no_artifact",
        "gate2_adversarial": "no_artifact",
        "tier": "C",
        "legacy_confidence": "",
        "recovery": "no",
        "reason": "no_decode_in_any_result_file",
        "dec_root": "",
        "dec_lang": "",
        "dec_gloss": "",
        "committed_root": "pul / puul",
        "committed_gloss": PUL["gloss"],
        "gate1_where": "DROPPED. EXPERIMENT_LOG claimed pul was restored from a pre-import copy and passed both gates. No row exists in strict_committed_results_batch*.csv, adversarial_results_batch*.csv, or the 61-row worksheet. Pass withdrawn.",
        "gate2_note": "no adversarial row",
        "protocol": "no_artifact",
    })

    for e in BATTERY_E:
        recs.append({
            "id": e["id"],
            "token": e["token"],
            "gate1_strict": "pass",
            "gate2_adversarial": "survive",
            "tier": "H+L",
            "legacy_confidence": "C",
            "recovery": "yes",
            "reason": "battery_e_exact_lexeme",
            "dec_root": "",
            "dec_lang": "",
            "dec_gloss": "",
            "committed_root": extract_quoted_root(e["source"]),
            "committed_gloss": e["gloss"],
            "gate1_where": e["gate1_note"] + " (BATTERY_E_RESULTS.md; not in the 61-row strict CSV)",
            "gate2_note": "Battery E: unanimous single-language assignment; no equal different-meaning competitor recorded",
            "protocol": "",
        })

    for i, tok, lang, src, gloss, tier in L_ONLY:
        recs.append({
            "id": i,
            "token": tok,
            "gate1_strict": "pending",
            "gate2_adversarial": "pending",
            "tier": tier,
            "legacy_confidence": "",
            "recovery": "unscorable",
            "reason": "not_in_battery",
            "dec_root": "",
            "dec_lang": "",
            "dec_gloss": "",
            "committed_root": extract_quoted_root(src),
            "committed_gloss": gloss,
            "gate1_where": "not in strict_committed_results; hardening pending. Former L-only section-9 row; L is now a tag on C or S.",
            "gate2_note": "hardening pending",
            "protocol": "",
        })

    # write gate1_rescore.csv (full audit trail)
    g1_path = os.path.join(HERE, "gate1_rescore.csv")
    fields = ["id", "token", "legacy_confidence", "recovery", "reason", "committed_root", "committed_gloss",
              "dec_root", "dec_lang", "dec_gloss", "gate1_strict", "gate1_where", "gate2_adversarial",
              "gate2_note", "protocol", "tier"]
    with open(g1_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for rec in recs:
            w.writerow({k: rec[k] for k in fields})

    # token_classification.csv (canonical tiers)
    tc_path = os.path.join(HERE, "token_classification.csv")
    with open(tc_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "token", "gate1_strict", "gate2_adversarial", "tier"])
        for rec in recs:
            w.writerow([rec["id"], rec["token"], rec["gate1_strict"], rec["gate2_adversarial"], rec["tier"]])

    # summary numbers
    def count(pred):
        return sum(1 for r in recs if pred(r))

    n78 = len(recs)
    n61 = 61
    n_battery = 61  # strict CSV population
    n_pul = 1
    n_e = 3
    n_l = 13
    h = [r for r in recs if r["tier"].startswith("H")]
    # C+L* starts with C, not C*; star anywhere in the tier is a competitor flag.
    cstar = [r for r in recs if "*" in r["tier"]]
    c = [r for r in recs if r["tier"].startswith("C") and "*" not in r["tier"]]
    s = [r for r in recs if r["tier"].startswith("S")]
    g1_pass_61 = [r for r in recs if r["id"] not in {e["id"] for e in BATTERY_E} | {"62"} | {x[0] for x in L_ONLY}
                  and str(r["gate1_strict"]).startswith("pass") and "protocol" not in str(r["gate1_strict"])]
    g1_pass_incl_proto = [r for r in recs if r["id"] not in {e["id"] for e in BATTERY_E} | {"62"} | {x[0] for x in L_ONLY}
                          and str(r["gate1_strict"]).startswith("pass")]
    g1_legacy_c = [r for r in recs if r["legacy_confidence"].lower() == "c" and r["id"] not in {e["id"] for e in BATTERY_E} | {"62"} | {x[0] for x in L_ONLY}]
    g1_recovery_yes = [r for r in recs if r["recovery"] == "yes" and r["id"] not in {e["id"] for e in BATTERY_E} | {"62"} | {x[0] for x in L_ONLY}]

    md = []
    md.append("# Gate 1 / Gate 2 rescore output")
    md.append("")
    md.append("Generated by `python3 rescore_gate1.py`. Do not hand-edit; re-run the script.")
    md.append("This file is the proof of the rescored counts (AUDIT_REVIEW items 3-6).")
    md.append("")
    md.append("## Populations (one denominator each)")
    md.append("")
    md.append("| Population | N | What it is | Where decided |")
    md.append("|---|---:|---|---|")
    md.append("| Strict-committed decode | 61 | rows in `strict_committed_results_batch{1..4}.csv` (15+15+15+16) | Gate 1 for the original battery |")
    md.append("| Worksheet / adversarial | 61 | `adversarial_worksheet.csv` ids 1-61 | declared readings; Gate 2 |")
    md.append("| pul / puul | 1 | published as token 62; **no decode artifact** | Gate 1 pass DROPPED |")
    md.append("| Battery E names | 3 | Quecholli, Panquetzaliztli, Ixchel | `BATTERY_E_RESULTS.md` (15/15 exact lexemes) |")
    md.append("| Former L-only section 9 rows | 13 | taxonomy repair: L is a tag on C or S | gates pending |")
    md.append("| Section 9 table (agreed lexicon) | 78 | 61 + pul + 3 names + 13 | every row has H/C/S/O; L is never a lone tier |")
    md.append("")
    md.append("Old published denominators (23/62, 26/65, 25 H of 65) do not rebuild from the CSVs. They are withdrawn.")
    md.append("")
    md.append("## Gate 1, 61-row strict CSV")
    md.append("")
    md.append(f"- Legacy any-C labels in the 61-row CSV: **{len(g1_legacy_c)}** (AUDIT_REVIEW: 21, not 23).")
    md.append(f"- Of those, committed-root/lang/sense recovery: **{len(g1_recovery_yes)}** (Eztli override counted as recovery).")
    md.append(f"- Protocol-clean Gate 1 passes (recovery yes, no residue/bundle flag): **{len(g1_pass_61)}**.")
    md.append(f"- Recovery yes including protocol-flagged rows: **{len(g1_pass_incl_proto)}**.")
    md.append("- pul / puul: **no artifact**, pass dropped.")
    md.append("")
    md.append("### Legacy C rows that do NOT recover the declared reading")
    md.append("")
    md.append("| Token | Declared | Decoder accepted |")
    md.append("|---|---|---|")
    for r in recs:
        if r["legacy_confidence"].lower() == "c" and r["recovery"] != "yes" and r["id"] not in {"63", "64", "65"}:
            md.append(f"| {r['token']} | {r['committed_root']} / {r['committed_gloss'][:40]} | {r['dec_lang']} {r['dec_root']} = {r['dec_gloss'][:50]} |")
    md.append("")
    md.append("### Protocol flags on otherwise-matching rows")
    md.append("")
    for r in recs:
        if r["protocol"] and r["protocol"] != "no_artifact":
            md.append(f"- **{r['token']}**: {r['protocol']}. {r['gate1_where']}")
    md.append("")
    md.append("## Hardened set after both gates and protocol")
    md.append("")
    md.append(f"H rows in the 78-row lexicon: **{len(h)}**")
    md.append("")
    md.append(", ".join(f"*{r['token']}*" for r in h))
    md.append("")
    md.append(f"C*: **{len(cstar)}**. C (including C+L pending): **{len(c)}**. S/S+L: **{len(s)}**.")
    md.append("")
    md.append("## Where each former published Gate-1 pass was decided")
    md.append("")
    md.append("| Token | Old | New Gate 1 | Where |")
    md.append("|---|---|---|---|")
    old_h = ["akal", "ascensionada / ascenada", "che'", "ek", "-en", "Eztli Pilli", "ich",
             "k'áak' (kahk)", "ki' (Kí')", "kujkuali", "k'ux (quxzeh)", "ma", "máax",
             "náach (niáach)", "pul / puul", "Ti", "tul", "u", "uch' / pu uch'", "waaj (waja)",
             "xefe", "xi", "Quecholli", "Panquetzaliztli", "Ixchel"]
    by_tok = {r["token"]: r for r in recs}
    for tok in old_h:
        r = by_tok.get(tok)
        if not r:
            # fuzzy
            hits = [x for x in recs if tok.split()[0].lower() in x["token"].lower()]
            r = hits[0] if hits else None
        if not r:
            md.append(f"| {tok} | H | ? | not found |")
            continue
        md.append(f"| {r['token']} | H | {r['gate1_strict']} / {r['tier']} | {r['gate1_where'][:160]} |")
    md.append("")
    md.append("## How to reproduce")
    md.append("")
    md.append("```")
    md.append("python3 rescore_gate1.py")
    md.append("python3 score_adversarial.py")
    md.append("python3 score.py blind_test_results_tight_s42.csv blind_test_key_s42.csv")
    md.append("python3 null_honesty.py")
    md.append("```")
    md.append("")

    out_md = os.path.join(HERE, "RESCORE_OUTPUT.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print("\n".join(md))
    print(f"\nWrote {g1_path}")
    print(f"Wrote {tc_path}")
    print(f"Wrote {out_md}")
    print(f"Wrote {os.path.join(HERE, 'committed_readings.csv')}")


if __name__ == "__main__":
    main()
