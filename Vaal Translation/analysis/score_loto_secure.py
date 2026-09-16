#!/usr/bin/env python3
"""Leave-one-text-out scores and secure-line grades for the 51-line gold set.

Editorial LOTO scores (ok / partial / fail) are the recorded judgements in
LOTO_ROWS. Coverage columns are computed from training-surface overlap plus
licensed stem transfer. Secure-line grades are computed from TIER_MAP.

Usage (from this directory):
    python3 score_loto_secure.py
"""
from __future__ import annotations

import csv
import math
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOLD = HERE / "translation_battery_gold.csv"

PARTICLES = {
    "a'te", "u'te", "le", "le'", "ti", "ti'", "ka", "ta'", "u", "ma", "ma'",
    "na'", "en", "yatle",
}

# Presentative A'te / U'Te / Yatle is one §9 row. All three are particles here.
PRESENTATIVE = {"a'te", "u'te", "yatle"}

STEM_FAMILIES = {
    "ik'": ("ik'el", "ik'bala", "ikba'yucane", "ik'eche"),
    "kux": ("kuxte'", "kuxkal", "kux"),
    "muk'": ("mucane", "mujuk'", "ko'mujuk"),
    "aocmo": ("aiokmo", "'ayok"),
    "el": ("ela", "elba"),
    "k'ex": ("kextal", "qexcan"),
    "itsok": ("itsok", "itzil", "le'itzil"),
    "yutsal": ("yutsal",),
    "ts'ook": ("tzokan'te", "cha'tsoke"),
    "ibil": ("'ibil", "inib"),
    "tul_wane": ("tul", "jare'yantul"),
    "jare": ("jare", "jare'yantul"),
    "atl": ("atla", "atziri"),
}

FOLD_OF_TAG = {
    "T1": "T1",
    "T2": "T2",
    "T3": "T3",
    "T4": "T4",
    "T4x": "T4",
    "T5": "T5",
}

# Surface (folded) -> (tier_code, lex_or_soft, note)
# tier_code: H, C, C*, S, O. L is orthogonal and ignored for the grade test
# except that C+L is plain C and C+L* is C*.
TIER_MAP = {
    "atziri": ("C", "Atziri C+L", "name"),
    "ek": ("C*", "ek C*", ""),
    "te": ("C*", "te C*", ""),
    "mucane": ("C*", "mucane C*", ""),
    "vaal": ("C", "Vaal C+L", "name"),
    "teoyuxtlane": ("C", "Teoyuxtlane C", ""),
    "ascensionada": ("C", "ascensionada C", ""),
    "ascenada": ("C", "ascensionada C", ""),
    "yutsal": ("C", "Yutsal C+L", ""),
    "kilya": ("C", "kilya C+L", ""),
    "zerphi": ("C", "Zerphi C", "name"),
    "itsok": ("C", "itsok/itzil C+L", ""),
    "anab": ("C", "anab C", ""),
    "nochira": ("C*", "nochira C*", ""),
    "kextal": ("C", "Kextal C", ""),
    "xi": ("C", "xi C", ""),
    "kujkuali": ("C", "kujkuali C+L", ""),
    "ik'bala": ("C", "ik'bala C", ""),
    "ikba'yucane": ("C", "ikba'yucane C", ""),
    "ibil": ("C*", "'Ibil C+L*", ""),
    "'ibil": ("C*", "'Ibil C+L*", ""),
    "tlayeb": ("C", "tlayeb C+L", ""),
    "kutsen": ("C*", "kutsen C+L*", ""),
    "ik'el": ("C*", "ik'el C+L*", ""),
    "kifba": ("C*", "kifba C+L*", ""),
    "akal": ("C*", "akal C*", ""),
    "aiokmo": ("C", "Aiokmo C", ""),
    "til": ("C*", "til C*", ""),
    "xu'te": ("C", "xu'te C", ""),
    "tul": ("C*", "tul C*", ""),
    "jare": ("C", "jare C", ""),
    "elba": ("C", "elba C", ""),
    "kuxte'": ("C*", "kux/kuxkal/kuxte' C+L*", ""),
    "kiimil'": ("C*", "kíimil C+L*", ""),
    "kiimil": ("C*", "kíimil C+L*", ""),
    "tlaxye'": ("C", "Tlaxye' C+L", ""),
    "ma'oxe": ("C", "Ma'oxe C+L", ""),
    "le'itzil": ("C", "itsok/itzil C+L", "fused article plus itzil"),
    "xatlene": ("S", "Xatlene S+L", ""),
    "gyan'uks": ("C", "Gyan'uks C+L", ""),
    "ko'janti": ("C", "ko'janti C+L", ""),
    "yaxe": ("C", "yax/Yaxe C+L", ""),
    "chikula'": ("C*", "chikula' C+L*", ""),
    "tzokan'te": ("C*", "Tzokan'te C+L*", ""),
    "liimek": ("C", "líimek C+L", ""),
    "kuxkal": ("C*", "kux/kuxkal/kuxte' C+L*", ""),
    "yuquia": ("C", "yuquia C+L", ""),
    "eche": ("S", "Eche S §10.4", ""),
    "lu": ("S", "lu S §10.4", ""),
    "nochbe": ("S", "nochbe S §10.4", ""),
    "ki'": ("C*", "ki' C*", ""),
    "inib": ("S", "inib S §10.4", ""),
    "'ayok": ("C", "'Ayok C", ""),
    "mujuk'": ("C", "mujuk' C", ""),
    "niaach": ("C*", "náach C*", ""),
    "i'chian": ("C", "i'chian C", ""),
    "waja": ("C*", "waaj C+L*", ""),
    "u'tra": ("C", "u'tra C", ""),
    "buxa": ("S", "buxa S §10.4", ""),
    "fukuur": ("S", "fukuur S §10.4", ""),
    "daka": ("S", "daka S §10.4", ""),
    "puxe": ("S", "puxe S §10.4", ""),
    "sakilja": ("C", "sakilja C+L", ""),
    "ik'eche": ("C", "Ik'eche C", ""),
    "atla": ("C", "atla C", ""),
    "donuks": ("S", "Donuks S §10.4", ""),
    "ko'soxsal": ("S", "ko'soxsal S §10.4", ""),
    "ko'mujuk": ("S", "ko'mujuk S (muk' echo, not a §9 row)", ""),
    "cha'tsoke": ("C", "cha'tsoke C", ""),
    "xefe": ("H", "xefe H", ""),
    "yotlapek": ("C", "tlapec/yotlapek C+L", ""),
    "te'moxti": ("S", "te'moxti S §10.4", ""),
    "qexcan": ("C", "qexcan C+L", ""),
    "puyao": ("S", "puyao S §10.4", ""),
    "ich": ("C*", "ich C*", ""),
    "tlapec": ("C", "tlapec C+L", ""),
    "uch'": ("C*", "uch' C*", ""),
    "ta'nuk": ("C", "ta'nuk C", ""),
    "pu": ("S", "pu S §10.4", ""),
    "otsuks": ("S", "Otsuks S §10.9", ""),
    "ela": ("C", "Ela C", ""),
    "ukto": ("S", "ukto S §10.7", ""),
    "maax": ("C*", "máax C*", ""),
    "a'tul": ("S", "a'tul S §10.9", ""),
    "cheyel": ("S", "cheyel S §10.9", ""),
    "quxzeh": ("C*", "k'ux/quxzeh C*", ""),
    "axba": ("S", "Axba S §10.9", ""),
    "kiibsa'": ("S", "Kíibsa' S §10.9", ""),
    "tala": ("C", "tala C", ""),
    "ek'le": ("C*", "ek C* plus fused le", ""),
    "upulche": ("C*", "pul C* plus soft -che tail", ""),
    "jare'yantul": ("MIXED", "segmented", "see pieces"),
    "yan": ("O", "yan not a §9 row", ""),
}


def fold_key(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'").replace("\u02bc", "'")
    return s


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n <= 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    z2 = z * z
    den = 1.0 + z2 / n
    center = (p + z2 / (2 * n)) / den
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * n)) / n) / den
    return (p, max(0.0, center - margin), min(1.0, center + margin))


def fmt_ci(k: int, n: int) -> str:
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * p:.1f}% [{100 * lo:.1f}, {100 * hi:.1f}]"


def strip_punct(tok: str) -> str:
    t = tok.strip()
    t = t.replace("\u2026", "...")
    if t.endswith("..."):
        t = t[:-3]
    return t.strip(".,!?;:\"")


def tokenize(vaal: str) -> list[str]:
    return [strip_punct(t) for t in vaal.split() if strip_punct(t)]


def fold_text(tag: str) -> str:
    prefix = tag.split(".")[0]
    return FOLD_OF_TAG[prefix]


def load_gold() -> list[dict]:
    rows = []
    with GOLD.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["line_id"] = int(r["line_id"])
            r["fold"] = fold_text(r["source_tag"])
            r["tokens"] = tokenize(r["vaal"])
            rows.append(r)
    if len(rows) != 51:
        raise SystemExit(f"expected 51 gold lines, got {len(rows)}")
    return rows


def tokens_by_fold(rows: list[dict]) -> dict[str, set[str]]:
    out = defaultdict(set)
    for r in rows:
        for t in r["tokens"]:
            out[r["fold"]].add(fold_key(t))
    return dict(out)


def families_of(folded: str) -> list[str]:
    return [fam for fam, members in STEM_FAMILIES.items() if folded in members]


def lookup_tier(folded: str) -> tuple[str, str]:
    if folded in TIER_MAP:
        code, name, _ = TIER_MAP[folded]
        return code, name
    # 'ibil without leading quote
    alt = folded[1:] if folded.startswith("'") else "'" + folded
    if alt in TIER_MAP:
        code, name, _ = TIER_MAP[alt]
        return code, name
    return "?", f"unmapped:{folded}"


# Editorial LOTO scores: held-out text only. Gold of the held-out text is the
# scoring key, not a search key. Reasons name training evidence.
LOTO_ROWS = {
    1: ("partial", "mucane and Vaal known from T3/T4 and T2/T3; ek in T5 is dark not star; te T1-only"),
    2: ("fail", "Teoyuxtlane and ascensionada are T1-only; yutsal in T2 is the good-place piece only"),
    3: ("partial", "kilya undying from T3; Zerphi T1-only; free ma is T1-only"),
    4: ("partial", "itsok blood T3, kujkuali worthy T2, xi T3, ik'bala via ik' in T2/T4; Kextal via qexcan T3 is a stem hit not the vocative transform-us; anab and nochira T1-only"),
    5: ("partial", "Vaal known; ikba'yucane via ik' spirit/breath in T2/T3; deathless compound not in training"),
    6: ("ok", "A'te 'Ibil tlayeb kutsen / ik'el tlayeb kifba all attested in T2 with the same referents"),
    7: ("fail", "ascenada and akal are T1-only"),
    8: ("partial", "Aiokmo via 'Ayok T3; tul and jare via T5 jare'yantul; elba via Ela T4; til and xu'te T1-only"),
    9: ("partial", "kuxte' via kuxkal living in T4; kíimil' is T2-only"),
    10: ("fail", "Tlaxye' people is T2-only; leftover le Vaal is not the published predication"),
    11: ("partial", "ik'el spirits from T1/T4; Ma'oxe countless is T2-only"),
    12: ("partial", "Atziri known; le'itzil via itsok blood in T1/T3, not the T2 essence wording"),
    13: ("partial", "kujkuali worthy from T1; Xatlene kindle is T2-only"),
    14: ("fail", "Gyan'uks and ko'janti are T2-only"),
    15: ("ok", "A'te 'Ibil is in T1 with flesh"),
    16: ("ok", "A'te ik'el is in T1 with spirit"),
    17: ("fail", "Yaxe and chikula' are T2-only"),
    18: ("ok", "Tzokan'te ik'el last spirit is in T4"),
    19: ("fail", "líimek is T2-only; presentative alone does not recover those in the earth"),
    20: ("partial", "Yatle there-stands from T3; Yutsal Utzaal from T1, not the lowercase good-place wording"),
    21: ("ok", "Tlayeb kutsen is in T1"),
    22: ("ok", "Tlayeb kifba is in T1"),
    23: ("ok", "U'Te kuxkal living matches T4 A'te Kuxkal"),
    24: ("fail", "yuquia is T2-only"),
    25: ("fail", "Eche lu nochbe are T3-only; nochi in T1 nochira does not recover pour it out"),
    26: ("partial", "inib via 'Ibil flesh in T1/T2; Kí' sweet is T3-only"),
    27: ("partial", "'Ayok via Aiokmo T1; ta' en in T4; mucane mighty in T1/T4; mujuk' via muk'; niáach i'chian T3-only"),
    28: ("partial", "presentative and Yatle from T1/T2; waja, u'tra, buxa T3-only"),
    29: ("fail", "fukuur is T3-only"),
    30: ("fail", "daka and puxe are T3-only; xi from T1 does not recover the draught"),
    31: ("partial", "'Ayok, kifba, Atziri, kilya from T1/T2; sakilja white drink is T3-only"),
    32: ("partial", "Ik'eche via ik' in T1/T2; atla via Atziri water-stem in T1; sakilja and donuks T3-only"),
    33: ("fail", "Donuks and ko'soxsal are T3-only"),
    34: ("partial", "ko'mujuk via mucane/muk' strength in T1/T4; Donuks T3-only"),
    35: ("partial", "xi, itsok, Vaal from T1; cha'tsoke via Tzokan'te ts'ook in T2/T4; qexcan via Kextal T1; xefe, yotlapek, te'moxti T3-only"),
    36: ("fail", "puyao is T3-only"),
    37: ("fail", "only itsok blood is in training; tlapec, puyao, uch', ta'nuk, ich are T3-only"),
    38: ("partial", "Tzokan'te u'te ik'el last spirit from T2; Otsuks T4-only"),
    39: ("ok", "vocative Atziri is in T1/T2/T3"),
    40: ("partial", "Kuxkal tlayeb kutsen from T2/T1; Ela via elba T1; ukto, Máax, a'tul T4-only"),
    41: ("ok", "vocative Atziri is in T1/T2/T3"),
    42: ("fail", "Otsuks, Máax, a'tul are T4-only"),
    43: ("ok", "U'te mucane mighty from T1/T3 with the presentative"),
    44: ("fail", "Máax and cheyel are T4-only"),
    45: ("ok", "U'te mucane as line 43"),
    46: ("partial", "tlayeb mucane from T1/T3; Máax T4-only so the interrogative is missing"),
    47: ("ok", "vocative Atziri is in T1/T2/T3"),
    48: ("fail", "Otsuks and quxzeh are T4-only"),
    49: ("fail", "Axba and Kíibsa' are T4-only; ta' en in T3 does not recover kill"),
    50: ("partial", "jare and tul from T1 (and so, waning); ek in T1 is star not dark; tala T5-only; yan not in training lexicon"),
    51: ("fail", "upulché pul is T5-only and is not tul; ek'le cannot be licensed as dark from T1 star"),
}


def load_bearing_pieces(tokens: list[str]) -> list[tuple[str, str, str]]:
    """Return (surface, folded, tier_code) for load-bearing pieces.

    jare'yantul is segmented because the published English and §8 notes
    treat it as three content words. Other fused forms stay whole.
    """
    out = []
    for t in tokens:
        folded = fold_key(t)
        if folded in PARTICLES or folded in PRESENTATIVE:
            continue
        if folded == "jare'yantul":
            out.append((t + "[jare']", "jare", "C"))
            out.append((t + "[yan]", "yan", "O"))
            out.append((t + "[tul]", "tul", "C*"))
            continue
        code, _ = lookup_tier(folded)
        out.append((t, folded, code))
    return out


def line_grade(pieces: list[tuple[str, str, str]]) -> str:
    if not pieces:
        return "working"
    codes = [p[2] for p in pieces]
    if any(c == "O" for c in codes):
        return "opaque-blocked"
    if any(c in {"C*", "S", "?"} for c in codes):
        return "fragile"
    if all(c == "H" for c in codes):
        return "secure"
    if all(c in {"H", "C"} for c in codes):
        return "working"
    return "fragile"


def main() -> None:
    rows = load_gold()
    by_fold = tokens_by_fold(rows)
    folds = ["T1", "T2", "T3", "T4", "T5"]

    loto_out = HERE / "loto_line_scores.csv"
    with loto_out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "line_id",
                "held_out",
                "source_tag",
                "vaal",
                "score",
                "known_exact",
                "stem_transfer",
                "unknown",
                "reason",
            ],
        )
        w.writeheader()
        counts = {fold: Counterish() for fold in folds}
        overall = Counterish()
        for r in rows:
            held = r["fold"]
            train_toks = set()
            for other in folds:
                if other != held:
                    train_toks |= by_fold[other]
            train_fams = set()
            for t in train_toks:
                train_fams.update(families_of(t))
            known, xfer, unknown = [], [], []
            for t in r["tokens"]:
                folded = fold_key(t)
                if folded in PARTICLES:
                    if folded in train_toks or (
                        folded in PRESENTATIVE and (train_toks & PRESENTATIVE)
                    ):
                        known.append(t)
                    else:
                        unknown.append(t + "[particle]")
                    continue
                if folded in train_toks:
                    known.append(t)
                    continue
                fams = families_of(folded)
                if fams and any(fam in train_fams for fam in fams):
                    xfer.append(t)
                    continue
                unknown.append(t)
            score, reason = LOTO_ROWS[r["line_id"]]
            w.writerow(
                {
                    "line_id": r["line_id"],
                    "held_out": held,
                    "source_tag": r["source_tag"],
                    "vaal": r["vaal"],
                    "score": score,
                    "known_exact": " ".join(known),
                    "stem_transfer": " ".join(xfer),
                    "unknown": " ".join(unknown),
                    "reason": reason,
                }
            )
            counts[held].add(score)
            overall.add(score)

    secure_out = HERE / "secure_line_tags.csv"
    with secure_out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "line_id",
                "source_tag",
                "vaal",
                "gold_en",
                "grade",
                "load_bearing",
                "tiers",
                "worst",
            ],
        )
        w.writeheader()
        gcounts = Counterish()
        for r in rows:
            pieces = load_bearing_pieces(r["tokens"])
            grade = line_grade(pieces)
            gcounts.add(grade)
            load_s = []
            tier_s = []
            for surf, folded, code in pieces:
                name = lookup_tier(folded)[1] if folded != "yan" else "yan O"
                if folded == "yan":
                    name = "yan O (not a §9 row)"
                load_s.append(surf)
                tier_s.append(f"{folded}:{code}")
            worst = "H"
            order = {"O": 4, "S": 3, "C*": 2, "C": 1, "H": 0, "?": 3}
            if pieces:
                worst = max((p[2] for p in pieces), key=lambda c: order.get(c, 0))
            w.writerow(
                {
                    "line_id": r["line_id"],
                    "source_tag": r["source_tag"],
                    "vaal": r["vaal"],
                    "gold_en": r["gold_en"],
                    "grade": grade,
                    "load_bearing": " | ".join(load_s),
                    "tiers": " ".join(tier_s),
                    "worst": worst,
                }
            )

    print("LOTO overall")
    print("  ok        ", fmt_ci(overall.n["ok"], overall.total))
    print("  ok+partial", fmt_ci(overall.n["ok"] + overall.n["partial"], overall.total))
    print("  fail      ", fmt_ci(overall.n["fail"], overall.total))
    print("LOTO per fold")
    macros_ok = []
    macros_op = []
    for fold in folds:
        c = counts[fold]
        n = c.total
        print(f"  {fold} n={n} ok={c.n['ok']} partial={c.n['partial']} fail={c.n['fail']}")
        print(f"       ok {fmt_ci(c.n['ok'], n)}")
        print(f"       ok+partial {fmt_ci(c.n['ok'] + c.n['partial'], n)}")
        macros_ok.append(c.n["ok"] / n)
        macros_op.append((c.n["ok"] + c.n["partial"]) / n)
    print(f"  macro-average ok {100 * sum(macros_ok) / 5:.1f}%")
    print(f"  macro-average ok+partial {100 * sum(macros_op) / 5:.1f}%")
    print("SECURE-LINE")
    n = gcounts.total
    for g in ("secure", "working", "fragile", "opaque-blocked"):
        print(f"  {g:16} {fmt_ci(gcounts.n[g], n)}")
    unmapped = []
    for r in rows:
        for t in r["tokens"]:
            folded = fold_key(t)
            if folded in PARTICLES:
                continue
            if folded == "jare'yantul":
                continue
            if lookup_tier(folded)[0] == "?":
                unmapped.append((r["line_id"], t, folded))
    if unmapped:
        print("UNMAPPED", unmapped)
    else:
        print("all load-bearing tokens mapped")
    print(f"wrote {loto_out.name} and {secure_out.name}")


class Counterish:
    def __init__(self) -> None:
        self.n = defaultdict(int)
        self.total = 0

    def add(self, key: str) -> None:
        self.n[key] += 1
        self.total += 1


if __name__ == "__main__":
    main()
