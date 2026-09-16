#!/usr/bin/env python3
"""Score T-M / T-D translation sheets against gold. Run AFTER all ten sheets exist.

Line bins: match / partial / clash / abstain, per TRANSLATION_BATTERY_PROTOCOL.md.

  match: same main predication and referents as gold (wording may differ).
  partial: same main predication / referents, different wording, or a minor
           role / sense error (for example ek' as dark rather than star).
  clash: different predication or referents.
  abstain: translator confidence is abstain, or the translation is empty.

Inter-translator compatibility does not use gold: two non-abstain translations
of the same line are compatible if their content-lemma Jaccard (after a small
synonym fold) is >= 0.30, or both are name-only vocatives of the same name.
Two abstains are compatible with each other only.

Methodology-effect interval: nonparametric bootstrap of the 255 line-slots
per battery, 10,000 resamples, 95% percentile CI on (rate_TM - rate_TD).

Usage (from this directory):
    python3 score_translation_battery.py
"""
from __future__ import annotations

import csv
import math
import random
import re
import unicodedata
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEDS = [1729, 9001, 271828, 42, 55555]
JACCARD_CUT = 0.30
N_BOOT = 10000
BOOT_SEED = 1729

STOP = {
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or", "as",
    "is", "are", "be", "this", "that", "there", "here", "yonder", "your",
    "you", "he", "she", "it", "his", "her", "its", "our", "we", "i", "me",
    "one", "ones", "thing", "place", "with", "from", "by", "into", "no",
    "not", "more", "another", "all", "who", "what", "where",
}

# Small synonym fold for gold-free Jaccard and for vs-gold keyword tests.
SYN = {
    "alive": "life", "live": "life", "living": "life", "lives": "life",
    "die": "death", "dying": "death", "dies": "death", "perish": "death",
    "perished": "death", "deceso": "death",
    "star": "star", "estrella": "star",
    "dark": "dark", "black": "dark", "darkness": "dark", "night": "dark",
    "oscura": "dark", "oscuridad": "dark",
    "wasp": "wasp", "avispa": "wasp",
    "mighty": "mighty", "strong": "mighty", "powerful": "mighty",
    "strength": "mighty", "great": "mighty",
    "buried": "buried", "bury": "buried", "enterrada": "buried",
    "flesh": "flesh", "body": "flesh", "meat": "flesh",
    "spirit": "spirit", "spirits": "spirit", "soul": "spirit",
    "heart": "heart",
    "offering": "offering", "sacrifice": "offering",
    "behold": "behold", "see": "behold", "look": "behold", "watch": "behold",
    "divine": "divine", "god": "divine", "godly": "divine", "teotl": "divine",
    "ascended": "ascend", "ascension": "ascend", "risen": "ascend",
    "ascender": "ascend", "ascenso": "ascend",
    "undying": "undying", "immortal": "undying", "evergreen": "undying",
    "deathless": "undying", "everlasting": "undying",
    "blood": "blood", "sangre": "blood",
    "chief": "chief", "commander": "chief", "jefe": "chief",
    "blaze": "blaze", "fire": "blaze", "flame": "blaze", "torch": "blaze",
    "drink": "drink", "draught": "drink", "draft": "drink",
    "white": "white", "whiteness": "white", "blancura": "white",
    "company": "company", "heap": "company", "cluster": "company",
    "people": "people", "folk": "people",
    "essence": "essence", "servant": "servant", "slave": "servant",
    "sign": "sign", "insignia": "sign", "first": "first", "green": "green",
    "turkey": "turkey", "bug": "bug", "virus": "virus", "insect": "bug",
    "shake": "shake", "ladder": "ladder",
    "cacao": "cacao", "tree": "tree",
    "waning": "wane", "wane": "wane", "decline": "wane",
    "cast": "cast", "throw": "cast", "hurl": "cast", "opposed": "cast",
    "come": "come", "coming": "come", "arrive": "come",
    "who": "who", "kill": "kill", "die2": "kill",
    "bite": "bite", "fierce": "fierce", "hate": "fierce", "pain": "fierce",
    "water": "water", "waters": "water",
    "altar": "altar", "bed": "altar",
    "red": "red", "redden": "red", "reddened": "red", "stab": "red",
    "mother": "mother", "womb": "mother",
    "children": "children", "child": "children",
    "devour": "devour", "new": "new",
    "kindle": "kindle", "worthy": "worthy",
    "countless": "countless", "many": "countless",
    "earth": "earth", "ground": "earth",
    "good": "good",
    "last": "last",
    "made": "made", "make": "made",
    "pour": "pour",
    "sweet": "sweet", "better": "sweet", "soft": "sweet",
    "house": "house",
    "nothing": "nothing",
    "raw": "raw", "fresh": "fresh",
    "end": "end",
    "remade": "remade",
    "breath": "breath",
    "sacred": "sacred",
    "watch2": "watch", "stand": "watch",
    "what": "what",
    "before": "before",
    "ash": "ash", "ember": "ember", "embers": "ember",
    "burn": "burn", "burning": "burn",
    "pine": "pine", "ocote": "pine",
    "torch2": "torch",
}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'")
    return s


def strip_brackets(s: str) -> str:
    return re.sub(r"\[[^\]]*\]", " ", s or "")


def tokens(s: str) -> list[str]:
    s = fold(strip_brackets(s))
    s = re.sub(r"[^a-z0-9']+", " ", s)
    out = []
    for w in s.split():
        w = w.strip("'")
        if len(w) < 2:
            continue
        if w in STOP:
            continue
        out.append(SYN.get(w, w))
    return out


def has_any(text: str, words: list[str]) -> bool:
    t = fold(strip_brackets(text))
    t = re.sub(r"[^a-z0-9']+", " ", t)
    padded = f" {t} "
    for w in words:
        w = fold(w)
        if " " in w:
            if w in t:
                return True
        else:
            if re.search(rf"\b{re.escape(w)}\b", padded):
                return True
    return False


def has_all_groups(text: str, groups: list[list[str]]) -> bool:
    return all(has_any(text, g) for g in groups)


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


def bootstrap_diff(a: list[int], b: list[int], n_boot: int = N_BOOT, seed: int = BOOT_SEED):
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


def is_abstain(conf: str, trans: str) -> bool:
    c = (conf or "").strip().lower()
    if c == "abstain":
        return True
    if not (trans or "").strip():
        return True
    return False


def score_vs_gold(lid: int, trans: str, conf: str) -> str:
    """Rubric vs published English. Conservative: default clash."""
    if is_abstain(conf, trans):
        return "abstain"
    t = trans

    # Vocative queen's name (gold is exactly Atziri!).
    if lid in {39, 41, 47}:
        if has_any(t, ["atziri"]) and len(tokens(t)) <= 2:
            return "match"
        if has_any(t, ["atziri"]):
            return "partial"
        return "clash"

    if lid == 1:
        if has_all_groups(t, [["atziri"], ["star", "estrella"], ["vaal"], ["mighty", "strong", "powerful", "great"]]):
            return "match"
        if has_any(t, ["atziri"]) and has_any(t, ["vaal"]) and has_any(t, ["star", "estrella"]):
            return "partial"
        if has_any(t, ["atziri"]) and has_any(t, ["vaal"]) and has_any(t, ["dark", "black", "night", "darkness"]):
            return "partial"
        return "clash"

    if lid == 2:
        if has_any(t, ["divine", "god", "godly", "god-place", "teotl"]) and has_any(
            t, ["ascend", "ascended", "ascension", "risen"]
        ) and has_any(t, ["utzaal", "utzal", "yutsal", "good place", "all-good", "todo es bueno"]):
            return "match"
        if has_any(t, ["divine", "god", "god-place"]) and has_any(t, ["ascend", "ascended", "ascension", "risen"]):
            return "partial"
        if has_any(t, ["utzaal", "good place", "all-good"]) and has_any(t, ["divine", "god", "god-place"]):
            return "partial"
        return "clash"

    if lid == 3:
        if has_any(t, ["atziri"]) and has_any(t, ["zerphi"]) and has_any(
            t, ["undying", "immortal", "evergreen", "deathless", "everlasting"]
        ):
            return "match"
        if has_any(t, ["atziri"]) and has_any(t, ["zerphi"]) and has_any(t, ["green", "undying", "immortal"]):
            return "partial"
        return "clash"

    if lid == 4:
        blood = has_any(t, ["blood", "sangre"])
        transform = has_any(t, ["transform", "change", "remade", "worthy"])
        spirit = has_any(t, ["spirit", "soul"])
        servants = has_any(t, ["servant", "servants", "all"])
        if blood and transform and (spirit or servants):
            return "match"
        if blood or (transform and spirit):
            return "partial"
        return "clash"

    if lid == 5:
        if has_any(t, ["atziri"]) and has_any(t, ["vaal"]) and has_any(
            t, ["undying", "immortal", "breath"]
        ):
            return "match" if has_any(t, ["undying", "immortal"]) and has_any(t, ["breath"]) else "partial"
        return "clash"

    if lid == 6:
        flesh = has_any(t, ["flesh", "body"])
        heart = has_any(t, ["heart"])
        dark = has_any(t, ["dark", "black", "night"])
        offering = has_any(t, ["offering", "sacrifice"])
        if flesh and heart and dark:
            return "match"
        if (flesh or heart or offering) and dark:
            return "partial"
        return "clash"

    if lid == 7:
        if has_any(t, ["atziri"]) and has_any(t, ["risen", "ascend", "ascended", "ascension"]) and has_any(
            t, ["water", "waters", "pond", "eternal"]
        ):
            return "match"
        if has_any(t, ["atziri"]) and (
            has_any(t, ["risen", "ascend", "ascended"]) or has_any(t, ["water", "waters", "pond"])
        ):
            return "partial"
        return "clash"

    if lid == 8:
        if has_any(t, ["no more", "no longer", "never"]) and (
            has_any(t, ["burn", "ash", "ember", "embers"]) or has_any(t, ["end", "ending"])
        ):
            return "match" if has_any(t, ["burn", "ash", "ember"]) else "partial"
        return "clash"

    if lid == 9:
        life = has_any(t, ["life", "live", "alive", "living"])
        death = has_any(t, ["death", "die", "dying", "perish"])
        cacao = has_any(t, ["cacao", "cocoa", "tree"])
        if life and death and not cacao:
            return "match"
        if life and death:
            return "partial"
        if death and not cacao:
            return "partial"
        return "clash"

    if lid == 10:
        if has_any(t, ["vaal"]) and has_any(t, ["people", "folk", "nation"]):
            return "match"
        return "clash"

    if lid == 11:
        if has_any(t, ["spirit", "spirits"]) and has_any(t, ["countless", "many", "numberless"]):
            return "match"
        if has_any(t, ["spirit", "spirits"]):
            return "partial"
        return "clash"

    if lid == 12:
        if has_any(t, ["atziri"]) and has_any(t, ["essence"]):
            return "match"
        if has_any(t, ["atziri"]) and has_any(t, ["essence", "core"]):
            return "partial"
        return "clash"

    if lid == 13:
        if has_any(t, ["kindle", "ignite", "light"]) and has_any(t, ["worthy", "good"]):
            return "match"
        if has_any(t, ["kindle", "worthy"]):
            return "partial"
        return "clash"

    if lid == 14:
        if has_any(t, ["children", "child"]) and has_any(t, ["new"]) and has_any(t, ["devour", "come"]):
            return "match"
        if has_any(t, ["children", "child"]) or has_any(t, ["devour"]):
            return "partial"
        return "clash"

    if lid == 15:
        if has_any(t, ["flesh", "body"]) and has_any(t, ["behold", "see", "here", "there"]):
            return "match"
        if has_any(t, ["flesh", "body"]):
            return "partial"
        return "clash"

    if lid == 16:
        if has_any(t, ["spirit", "soul"]) and has_any(t, ["behold", "see", "here", "there"]):
            return "match"
        if has_any(t, ["spirit", "soul"]):
            return "partial"
        return "clash"

    if lid == 17:
        if has_any(t, ["first", "green", "blue-green"]) and has_any(t, ["sign", "insignia"]):
            return "match"
        if has_any(t, ["sign", "insignia", "first"]):
            return "partial"
        return "clash"

    if lid == 18:
        if has_any(t, ["last"]) and has_any(t, ["spirit", "soul"]):
            return "match"
        if has_any(t, ["spirit", "soul"]) or has_any(t, ["last"]):
            return "partial"
        return "clash"

    if lid == 19:
        if has_any(t, ["earth", "ground", "buried"]) and has_any(t, ["behold", "see", "those"]):
            return "match"
        if has_any(t, ["earth", "ground"]):
            return "partial"
        return "clash"

    if lid == 20:
        if has_any(t, ["good place", "utzaal", "all-good", "goodness"]) or (
            has_any(t, ["good"]) and has_any(t, ["place", "stands"])
        ):
            return "match"
        if has_any(t, ["good", "utzaal", "all-good"]):
            return "partial"
        return "clash"

    if lid == 21:
        if has_any(t, ["dark", "black"]) and has_any(t, ["offering", "sacrifice"]):
            return "match"
        if has_any(t, ["dark", "offering", "sacrifice"]):
            return "partial"
        return "clash"

    if lid == 22:
        if has_any(t, ["dark", "black"]) and has_any(t, ["heart"]):
            return "match"
        if has_any(t, ["dark", "heart"]):
            return "partial"
        return "clash"

    if lid == 23:
        if has_any(t, ["living", "life", "alive", "live"]) and has_any(
            t, ["behold", "see", "there", "here"]
        ):
            return "match"
        if has_any(t, ["living", "life", "alive"]):
            return "partial"
        return "clash"

    if lid == 24:
        if has_any(t, ["made", "make", "created"]) and has_any(t, ["behold", "see", "there"]):
            return "match"
        if has_any(t, ["made", "created"]):
            return "partial"
        return "clash"

    if lid == 25:
        if has_any(t, ["pour", "pour it out", "echar"]) and has_any(t, ["all", "we"]):
            return "match"
        if has_any(t, ["pour", "echar"]):
            return "partial"
        return "clash"

    if lid == 26:
        if has_any(t, ["sweet", "delight"]) and has_any(t, ["flesh", "body"]):
            return "match"
        if has_any(t, ["sweet", "flesh"]):
            return "partial"
        return "clash"

    if lid == 27:
        if has_any(t, ["nothing", "no more"]) and has_any(t, ["strength", "mighty"]) and has_any(
            t, ["house"]
        ):
            return "match"
        if has_any(t, ["strength", "mighty", "house"]):
            return "partial"
        return "clash"

    if lid == 28:
        if has_any(t, ["offering", "sacrifice"]) and has_any(t, ["another", "other"]):
            return "match"
        if has_any(t, ["offering", "another"]):
            return "partial"
        return "clash"

    if lid == 29:
        if has_any(t, ["blaze", "flame", "fire", "glory"]):
            return "match"
        return "clash"

    if lid == 30:
        if has_any(t, ["draught", "drink", "bring"]):
            return "match" if has_any(t, ["draught", "drink"]) else "partial"
        return "clash"

    if lid == 31:
        if has_any(t, ["atziri"]) and (
            has_any(t, ["white", "whiteness"]) or has_any(t, ["drink", "water"])
        ) and has_any(t, ["heart", "undying", "no more"]):
            return "match"
        if has_any(t, ["atziri"]) and has_any(t, ["white", "drink", "undying", "heart"]):
            return "partial"
        return "clash"

    if lid == 32:
        if has_any(t, ["breath"]) or has_any(t, ["sacred", "draught", "drink", "water"]):
            if has_any(t, ["breath"]) and has_any(t, ["water", "drink", "draught"]):
                return "match"
            return "partial"
        return "clash"

    if lid == 33:
        if has_any(t, ["drink"]) and has_any(t, ["raw", "fresh"]):
            return "match"
        if has_any(t, ["drink", "raw", "fresh"]):
            return "partial"
        return "clash"

    if lid == 34:
        if has_any(t, ["drink"]) and has_any(t, ["strength", "mighty"]):
            return "match"
        if has_any(t, ["drink", "strength"]):
            return "partial"
        return "clash"

    if lid == 35:
        chief = has_any(t, ["chief", "commander", "jefe"])
        blood = has_any(t, ["blood"])
        end = has_any(t, ["end", "finish"])
        vaal = has_any(t, ["vaal"])
        if chief and vaal and (blood or end):
            return "match"
        if chief or blood:
            return "partial"
        return "clash"

    if lid == 36:
        if has_any(t, ["red", "redden", "reddened"]) and has_any(t, ["offering", "sacrifice"]):
            return "match"
        if has_any(t, ["red", "offering"]):
            return "partial"
        return "clash"

    if lid == 37:
        if has_any(t, ["altar", "bed"]) and has_any(t, ["blood", "drink", "red"]):
            return "match" if has_any(t, ["blood", "drink"]) else "partial"
        if has_any(t, ["blood", "altar", "drink"]):
            return "partial"
        return "clash"

    if lid == 38:
        if has_any(t, ["company", "fall in"]) and has_any(t, ["last"]) and has_any(t, ["spirit"]):
            return "match"
        if has_any(t, ["last"]) and has_any(t, ["spirit"]):
            return "partial"
        if has_any(t, ["spirit"]):
            return "partial"
        return "clash"

    if lid == 40:
        living = has_any(t, ["living", "life", "alive"])
        dark = has_any(t, ["dark", "black"])
        torch = has_any(t, ["torch", "pine", "burn", "blaze", "ocote"])
        who = has_any(t, ["who"])
        if living and dark and who:
            return "match" if torch else "partial"
        if who and (living or torch or dark):
            return "partial"
        if who:
            return "partial"
        return "clash"

    if lid == 42:
        if has_any(t, ["who"]) and has_any(t, ["company", "heap"]):
            return "partial"
        if has_any(t, ["who"]):
            return "partial"
        return "clash"

    if lid in {43, 45}:
        if has_any(t, ["mighty", "strong", "powerful"]) and has_any(
            t, ["behold", "see", "there", "here"]
        ):
            return "match"
        if has_any(t, ["mighty", "strong", "powerful"]):
            return "partial"
        return "clash"

    if lid == 44:
        if has_any(t, ["who"]) and has_any(t, ["watch", "stand", "guard"]):
            return "match"
        if has_any(t, ["who"]):
            return "partial"
        return "clash"

    if lid == 46:
        if has_any(t, ["who"]) and has_any(t, ["mighty", "strong"]) and has_any(t, ["dark", "black"]):
            return "match"
        if has_any(t, ["who"]) and has_any(t, ["mighty", "dark", "black"]):
            return "partial"
        if has_any(t, ["who"]):
            return "partial"
        return "clash"

    if lid == 48:
        if has_any(t, ["company", "heap"]) and has_any(t, ["bite", "fierce", "hate", "pain"]):
            return "partial"
        if has_any(t, ["bite", "fierce"]):
            return "partial"
        return "clash"

    if lid == 49:
        if has_any(t, ["what"]) and has_any(t, ["kill", "die", "death"]):
            return "match"
        if has_any(t, ["what", "kill"]):
            return "partial"
        return "clash"

    if lid == 50:
        dark = has_any(t, ["dark", "black", "night"])
        come = has_any(t, ["come", "coming", "arrive"])
        wane = has_any(t, ["wane", "waning", "decline", "dwindle"])
        if dark and (come or wane):
            return "match" if (come and wane) or (dark and wane) else "partial"
        if dark:
            return "partial"
        return "clash"

    if lid == 51:
        if has_any(t, ["dark", "black"]) and has_any(t, ["cast", "throw", "hurl", "down"]):
            return "match"
        if has_any(t, ["dark", "black"]):
            return "partial"
        return "clash"

    return "clash"


PARTICLES = {
    "a'te", "ate", "u'te", "ute", "le", "le'", "ti", "ti'", "ka", "ta'",
    "u", "ma", "ma'", "na'", "en",
}
NAME_KEEP = {"atziri", "zerphi", "vaal"}

# Gold load-bearing glosses by line (from published English, scoring only).
GOLD_TOKENS = {
    1: {"ek": ["star"], "mucane": ["mighty", "strong"]},
    2: {"teoyuxtlane": ["divine", "god"], "ascensionada": ["ascend"], "yutsal": ["utzaal", "good"]},
    3: {"kilya": ["undying", "evergreen", "green"], "ma": ["undying", "not"]},
    4: {"itsok": ["blood"], "kextal": ["transform", "change"], "kujkuali": ["worthy", "good"], "ik'bala": ["spirit"]},
    5: {"ikba'yucane": ["undying", "breath"]},
    6: {"'ibil": ["flesh"], "kutsen": ["offering"], "ik'el": ["spirit", "self"], "kifba": ["heart"], "tlayeb": ["dark"]},
    7: {"ascenada": ["risen", "ascend"], "akal": ["water", "pond", "eternal"]},
    8: {"aiokmo": ["no more", "never"], "elba": ["burn", "ember", "out"]},
    9: {"kuxte'": ["life", "live", "alive"], "kíimil'": ["death", "die"]},
    10: {"tlaxye'": ["people", "folk"]},
    11: {"ma'oxe": ["countless", "many"], "ik'el": ["spirit"]},
    12: {"le'itzil": ["essence"]},
    13: {"xatlene": ["kindle"], "kujkuali": ["worthy"]},
    14: {"gyan'uks": ["new", "children"], "ko'janti": ["devour", "come"]},
    15: {"'ibil": ["flesh"]},
    16: {"ik'el": ["spirit"]},
    17: {"yaxe": ["first", "green"], "chikula'": ["sign"]},
    18: {"tzokan'te": ["last"], "ik'el": ["spirit"]},
    19: {"líimek": ["earth"]},
    20: {"yutsal": ["good"], "yatle": ["stands", "there"]},
    21: {"tlayeb": ["dark"], "kutsen": ["offering"]},
    22: {"tlayeb": ["dark"], "kifba": ["heart"]},
    23: {"kuxkal": ["living", "life"]},
    24: {"yuquia": ["made"]},
    25: {"eche": ["pour"], "nochbe": ["all"]},
    26: {"kí'": ["sweet"], "inib": ["flesh"]},
    27: {"mujuk'": ["strength"], "mucane": ["mighty"], "niáach": ["deep", "far"], "i'chian": ["house"]},
    28: {"waja": ["offering"], "buxa": ["another"]},
    29: {"fukuur": ["blaze", "flame", "fire"]},
    30: {"daka": ["draught", "drink"], "puxe": ["draught", "bring"], "xi": ["bring"]},
    31: {"kifba": ["heart"], "kilya": ["undying"], "sakilja": ["white", "drink"]},
    32: {"ik'eche": ["breath"], "sakilja": ["sacred", "white", "water"], "donuks": ["draught", "drink"]},
    33: {"donuks": ["drink"], "ko'soxsal": ["raw", "fresh"]},
    34: {"donuks": ["drink"], "ko'mujuk": ["strength"]},
    35: {"cha'tsoke": ["end"], "itsok": ["blood"], "xefe": ["chief", "commander", "jefe"], "yotlapek": ["altar"]},
    36: {"puyao": ["red", "offering"]},
    37: {"tlapec": ["altar"], "puyao": ["red"], "itsok": ["blood"], "uch'": ["drink"], "ta'nuk": ["great"]},
    38: {"otsuks": ["company"], "tzokan'te": ["last"], "ik'el": ["spirit"]},
    40: {"kuxkal": ["living"], "kutsen": ["offering"], "tlayeb": ["dark"], "ela": ["burn"], "ukto": ["torch", "pine"], "máax": ["who"]},
    42: {"otsuks": ["company"], "máax": ["who"]},
    43: {"mucane": ["mighty"]},
    44: {"máax": ["who"], "cheyel": ["watch", "stand"]},
    45: {"mucane": ["mighty"]},
    46: {"máax": ["who"], "tlayeb": ["dark"], "mucane": ["mighty"]},
    48: {"otsuks": ["company"], "quxzeh": ["bite", "fierce"]},
    49: {"axba": ["what"], "kíibsa'": ["kill", "die"]},
    50: {"ek": ["dark", "black", "star"], "tala": ["come"], "jare'yantul": ["wane", "waning"]},
    51: {"ek'le": ["dark", "black"], "upulché": ["cast", "throw"]},
}


def score_token_notes(lid: int, notes: str) -> list[dict]:
    """Score offered glosses in notes for load-bearing gold tokens."""
    gold = GOLD_TOKENS.get(lid, {})
    nfold = fold(notes or "")
    out = []
    for tok, senses in gold.items():
        tf = fold(tok)
        if tf not in nfold and tok.lower() not in (notes or "").lower():
            continue
        # offered: look for a synonym of the gold sense in notes near this token.
        bin_ = "clash"
        if any(has_any(notes, [s]) for s in senses):
            bin_ = "match"
        elif tok in {"ek", "ek'le"} and has_any(notes, ["dark", "black", "star"]):
            bin_ = "partial"
        elif has_any(notes, ["opaque", "no hit", "no dict", "unattested", "abstain"]):
            # mentioned but not glossed as content
            if re.search(rf"{re.escape(tok)}[^\n]{{0,80}}(opaque|no hit|no dict)", notes or "", re.I):
                bin_ = "abstain"
        out.append({"token": tok, "token_bin": bin_})
    return out


def load_sheet(batt: str, seed: int) -> list[dict]:
    path = HERE / f"translation_battery_{batt}_s{seed}.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if len(rows) != 51:
        raise SystemExit(f"{path.name} has {len(rows)} rows")
    return rows


def compatible(a: dict, b: dict) -> bool:
    if a["line_bin"] == "abstain" and b["line_bin"] == "abstain":
        return True
    if a["line_bin"] == "abstain" or b["line_bin"] == "abstain":
        return False
    ta, tb = tokens(a["translation"]), tokens(b["translation"])
    sa, sb = set(ta), set(tb)
    if not sa and not sb:
        return True
    if not sa or not sb:
        return False
    j = len(sa & sb) / len(sa | sb)
    return j >= JACCARD_CUT


def main() -> None:
    gold_path = HERE / "translation_battery_gold.csv"
    gold = {int(r["line_id"]): r for r in csv.DictReader(gold_path.open(encoding="utf-8"))}
    if len(gold) != 51:
        raise SystemExit(f"gold has {len(gold)} lines")

    line_rows = []
    token_rows = []
    sheets = {}
    for batt in ("TM", "TD"):
        for seed in SEEDS:
            rows = load_sheet(batt, seed)
            sheets[(batt, seed)] = rows
            for r in rows:
                lid = int(r["line_id"])
                trans = r.get("translation") or ""
                conf = r.get("confidence") or ""
                notes = r.get("notes") or ""
                bin_ = score_vs_gold(lid, trans, conf)
                line_rows.append(
                    {
                        "battery": batt,
                        "seed": seed,
                        "line_id": lid,
                        "vaal": gold[lid]["vaal"],
                        "gold_en": gold[lid]["gold_en"],
                        "translation": trans,
                        "confidence": conf,
                        "line_bin": bin_,
                    }
                )
                for tr in score_token_notes(lid, notes):
                    token_rows.append(
                        {
                            "battery": batt,
                            "seed": seed,
                            "line_id": lid,
                            "token": tr["token"],
                            "token_bin": tr["token_bin"],
                        }
                    )

    line_path = HERE / "translation_battery_line_scores.csv"
    with line_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(line_rows[0].keys()))
        w.writeheader()
        w.writerows(line_rows)

    tok_path = HERE / "translation_battery_token_scores.csv"
    if token_rows:
        with tok_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(token_rows[0].keys()))
            w.writeheader()
            w.writerows(token_rows)

    # Pairwise compatibility (no gold).
    pair_rows = []
    four_of_five = {"TM": 0, "TD": 0}
    for batt in ("TM", "TD"):
        for lid in range(1, 52):
            recs = []
            for seed in SEEDS:
                r = sheets[(batt, seed)][lid - 1]
                recs.append(
                    {
                        "seed": seed,
                        "translation": r.get("translation") or "",
                        "line_bin": score_vs_gold(
                            lid, r.get("translation") or "", r.get("confidence") or ""
                        ),
                    }
                )
            for i, j in combinations(range(5), 2):
                ok = compatible(recs[i], recs[j])
                pair_rows.append(
                    {
                        "battery": batt,
                        "line_id": lid,
                        "seed_a": recs[i]["seed"],
                        "seed_b": recs[j]["seed"],
                        "compatible": int(ok),
                    }
                )
            # clique of size >= 4 among 5
            found = False
            for combo in combinations(range(5), 4):
                if all(
                    compatible(recs[x], recs[y]) for x, y in combinations(combo, 2)
                ):
                    found = True
                    break
            if found:
                four_of_five[batt] += 1

    pair_path = HERE / "translation_battery_pairwise.csv"
    with pair_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pair_rows[0].keys()))
        w.writeheader()
        w.writerows(pair_rows)

    summary = []
    flags = {}
    print("## Line-slot vs gold (Wilson 95%)")
    print("N = 5 translators x 51 lines = 255 line-slots per battery.")
    for batt in ("TM", "TD"):
        bins = [r["line_bin"] for r in line_rows if r["battery"] == batt]
        n = len(bins)
        counts = Counter(bins)
        m = counts["match"]
        mp = counts["match"] + counts["partial"]
        flags[batt] = {
            "match": [1 if r["line_bin"] == "match" else 0 for r in line_rows if r["battery"] == batt],
            "mp": [
                1 if r["line_bin"] in {"match", "partial"} else 0
                for r in line_rows
                if r["battery"] == batt
            ],
        }
        print(f"{batt} bins: {dict(counts)}")
        print(f"{batt} match: {fmt_ci(m, n)}")
        print(f"{batt} match+partial: {fmt_ci(mp, n)}")
        summary.append({"battery": batt, "metric": "match", "k": m, "n": n, **dict(zip(["p", "lo", "hi"], wilson(m, n)))})
        summary.append({"battery": batt, "metric": "match+partial", "k": mp, "n": n, **dict(zip(["p", "lo", "hi"], wilson(mp, n)))})

        rates = []
        for lid in range(1, 52):
            bs = [r["line_bin"] for r in line_rows if r["battery"] == batt and r["line_id"] == lid]
            rates.append(sum(1 for b in bs if b == "match") / 5.0)
        rates_sorted = sorted(rates)
        med = rates_sorted[len(rates_sorted) // 2]
        q1 = rates_sorted[len(rates_sorted) // 4]
        q3 = rates_sorted[(3 * len(rates_sorted)) // 4]
        mean = sum(rates) / len(rates)
        print(
            f"{batt} per-line match fraction across 5 translators: "
            f"mean={mean:.3f} median={med:.3f} IQR=[{q1:.3f}, {q3:.3f}]"
        )

    print("\n## Methodology effect (TM minus TD), bootstrap 10000 line-slots")
    for label, key in (("match", "match"), ("match+partial", "mp")):
        obs, lo, hi = bootstrap_diff(flags["TM"][key], flags["TD"][key])
        print(f"{label}: {obs:+.4f}  95% percentile CI [{lo:+.4f}, {hi:+.4f}]")
        summary.append(
            {
                "battery": "TM-TD",
                "metric": label + "_diff",
                "k": "",
                "n": 255,
                "p": obs,
                "lo": lo,
                "hi": hi,
            }
        )

    print("\n## Inter-translator (no gold)")
    print(f"Compatibility: content-lemma Jaccard >= {JACCARD_CUT}, or both abstain.")
    for batt in ("TM", "TD"):
        recs = [r for r in pair_rows if r["battery"] == batt]
        k = sum(r["compatible"] for r in recs)
        n = len(recs)
        print(f"{batt} pairwise compatible: {fmt_ci(k, n)} (N = 10 pairs x 51 lines = 510)")
        print(f"{batt} lines with a 4/5 compatible clique: {fmt_ci(four_of_five[batt], 51)}")
        summary.append(
            {
                "battery": batt,
                "metric": "pairwise_compatible",
                "k": k,
                "n": n,
                **dict(zip(["p", "lo", "hi"], wilson(k, n))),
            }
        )
        summary.append(
            {
                "battery": batt,
                "metric": "four_of_five",
                "k": four_of_five[batt],
                "n": 51,
                **dict(zip(["p", "lo", "hi"], wilson(four_of_five[batt], 51))),
            }
        )

    if token_rows:
        print("\n## Load-bearing token glosses offered in notes (secondary)")
        for batt in ("TM", "TD"):
            recs = [r for r in token_rows if r["battery"] == batt]
            n = len(recs)
            m = sum(1 for r in recs if r["token_bin"] == "match")
            mp = sum(1 for r in recs if r["token_bin"] in {"match", "partial"})
            print(f"{batt} token match: {fmt_ci(m, n)}")
            print(f"{batt} token match+partial: {fmt_ci(mp, n)}")

    sum_path = HERE / "translation_battery_score_summary.csv"
    with sum_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["battery", "metric", "k", "n", "p", "lo", "hi"])
        w.writeheader()
        w.writerows(summary)
    print(f"\nwrote {line_path.name}, {tok_path.name}, {pair_path.name}, {sum_path.name}")


if __name__ == "__main__":
    main()
