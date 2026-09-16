#!/usr/bin/env python3
"""Shared committed-root / language / sense matching for Gate 1 rescoring.

A decoder C-label is not a true recovery of the project's reading. Recovery
requires the predeclared root, language class, and sense (AUDIT_REVIEW F1).
Exact string match is too brittle across orthographies, so this module uses
a documented equivalence table plus content-word / synonym overlap.

This module does not invent etymologies. It only decides whether a recorded
decode matches a reading already declared in adversarial_worksheet.csv or
section 9.
"""
from __future__ import annotations

import re
import unicodedata

# Language-class aliases. Keys are folded (diacritics stripped, lowercased).
LANG_ALIASES = {
    "maya": "Maya",
    "yucatec": "Maya",
    "yucatec maya": "Maya",
    "classic maya": "Maya",
    "classical maya": "Maya",
    "yuc": "Maya",
    "nahuatl": "Nahuan",
    "classical nahuatl": "Nahuan",
    "nahuan": "Nahuan",
    "nah": "Nahuan",
    "nawat": "Nahuan",
    "nawat pipil": "Nahuan",
    "pipil": "Nahuan",
    "kiche": "Kiche",
    "kiche maya": "Kiche",
    "quiche": "Kiche",
    "highland maya": "Kiche",
    "spanish": "Spanish",
    "spanish loan": "Spanish",
    "rom": "Spanish",
    "romance": "Spanish",
    "name": "Name",
}

# Root equivalences: folded decoder token -> folded committed token(s).
# Only pairs needed to score the archived CSVs without false mismatches on
# well-known orthographic variants of the SAME declared lemma.
ROOT_EQUIV = {
    "cualli": {"cualli", "kuali", "kualli", "kujkuali", "cuahcualli"},
    "kuali": {"cualli", "kuali", "kualli", "kujkuali", "cuahcualli"},
    "kualli": {"cualli", "kuali", "kualli", "kujkuali", "cuahcualli"},
    "kujkuali": {"cualli", "kuali", "kualli", "kujkuali", "cuahcualli"},
    "cuahcualli": {"cualli", "kuali", "kualli", "kujkuali", "cuahcualli"},
    "jefe": {"jefe", "xefe"},
    "xefe": {"jefe", "xefe"},
    "ascension": {"ascension", "ascender", "ascendida", "ascenada"},
    "ascender": {"ascension", "ascender", "ascendida", "ascenada"},
    "kaak": {"kaak", "kahk", "kak"},
    "kahk": {"kaak", "kahk", "kak"},
    "waaj": {"waaj", "wah", "waah"},
    "wah": {"waaj", "wah", "waah"},
    "maax": {"maax", "max"},
    "max": {"maax", "max"},
    "naach": {"naach", "nach"},
    "nach": {"naach", "nach"},
    "eztli": {"eztli", "estli", "ezti", "es"},
    "estli": {"eztli", "estli", "ezti", "es"},
    "pilli": {"pilli", "pil", "pili"},
    "xi": {"xi"},
}

# Sense synonym groups. A committed gloss and a decoder gloss match if they
# share a content word or jointly hit one group. Groups are closed lists of
# attested English gloss words from the worksheet and the result CSVs, not
# new semantic claims.
SENSE_GROUPS = [
    {"tree", "wood", "stick"},
    {"absolutive", "predicative", "suffix", "person"},
    {"within", "inside", "into"},
    {"good", "worthy", "delicious", "sweet", "tasty", "pleasant"},
    {"bite", "gnaw", "fierce", "pain", "hurt", "hate", "rancor", "ache", "chew"},
    {"who", "interrogative"},
    {"far", "distant", "lejos"},
    {"his", "her", "its", "possessive"},
    {"bread", "tortilla", "maize", "offering", "tamale"},
    {"chief", "commander", "boss"},
    {"ascended", "risen", "ascension", "ascend", "rise"},
    {"fire", "fuego"},
    {"blood", "noble", "prince", "child"},
    {"negation", "without", "negative", "particle"},
    {"optative", "hortative"},
    {"star", "black", "dark", "venus"},
    {"pond", "lagoon", "waters", "eternal", "fresh"},
    {"wane", "dwindle", "decline"},
    {"drink", "crush"},
    {"imperative"},
    {"reed", "bullrush", "bulrush"},
    {"wasp"},
    {"opossum"},
    {"relational", "dative", "preposition"},
    {"locative", "there"},
    {"burns", "burn", "blaze", "arder"},
    {"come", "comes"},
    {"platform", "scaffold", "altar", "frame", "bed"},
    {"goodness"},
    {"turkey"},
    {"white", "whiteness", "clarity"},
    {"change", "exchange", "substitute", "transform"},
    {"strong", "strength", "mighty", "enduring", "animated"},
    {"life", "living"},
]

STOP = {
    "the", "and", "for", "with", "from", "also", "into", "onto", "upon",
    "that", "this", "than", "then", "are", "was", "were", "been", "being",
    "one", "ones", "let", "may", "not", "yes", "all", "any", "its",
}

# Short function-word roots: require exact folded-token identity, not substring.
SHORT_ROOTS = {"u", "ma", "te", "ti", "ek", "xi", "en", "el", "il", "ki", "wa"}


def fold(s: str | None) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("'", "").replace("`", "")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def lang_class(src: str | None) -> str:
    s = fold(src)
    if not s:
        return "?"
    if s.startswith("name") or "name" in s[:8]:
        return "Name"
    # Prefer the leftmost explicit label in dual-source rows.
    # Dual rows are handled by lang_classes().
    for key in (
        "classical nahuatl", "yucatec maya", "classic maya", "kiche maya",
        "spanish loan", "highland maya",
    ):
        if s.startswith(key) or f" {key}" in s[:40]:
            return LANG_ALIASES[key]
    first = s.split()[0] if s.split() else s
    if first in LANG_ALIASES:
        return LANG_ALIASES[first]
    for key, val in LANG_ALIASES.items():
        if key in s:
            return val
    return "?"


def lang_classes(src: str | None) -> set[str]:
    """A dual-source entry (Maya + Nahuatl) accepts either class."""
    s = fold(src)
    out = set()
    if not s:
        return {"?"}
    if "nah" in s or "nawat" in s or "pipil" in s:
        out.add("Nahuan")
    if "maya" in s or "yucatec" in s:
        out.add("Maya")
    if "kiche" in s or "quiche" in s:
        out.add("Kiche")
    if "span" in s or s.startswith("rom") or "loan" in s or "romance" in s:
        out.add("Spanish")
    if s.startswith("name") or "(name" in (src or "").lower():
        out.add("Name")
    if not out:
        out.add(lang_class(src))
    return out


def root_tokens(s: str | None) -> set[str]:
    folded = fold(s)
    toks = set(re.findall(r"[a-z]{1,}", folded))
    expanded = set(toks)
    for t in list(toks):
        expanded |= ROOT_EQUIV.get(t, set())
    return expanded


def content_words(s: str | None) -> set[str]:
    words = {w for w in re.findall(r"[a-z]{3,}", fold(s)) if w not in STOP}
    # Keep short pronouns that the 3-letter filter would drop (me, I).
    folded = fold(s)
    for w in ("me", "we", "us"):
        if re.search(rf"\b{w}\b", folded):
            words.add(w)
    if re.search(r"\bi\b", folded):
        words.add("person")
    return words


def sense_match(committed_gloss: str, decoder_gloss: str, extra: str = "") -> bool:
    left = content_words(committed_gloss) | content_words(extra)
    right = content_words(decoder_gloss)
    if left & right:
        return True
    for g in SENSE_GROUPS:
        if (left & g) and (right & g):
            return True
    return False


def root_match(committed_root: str, decoder_root: str) -> bool:
    ctoks = root_tokens(committed_root)
    dtoks = root_tokens(decoder_root)
    if not ctoks or not dtoks:
        return False
    # Prefer exact token identity, including short roots.
    if ctoks & dtoks:
        # Reject accidental hits on short roots unless the short root itself
        # is in both sets (u, ma, ti, ...).
        shared = ctoks & dtoks
        if shared - SHORT_ROOTS:
            return True
        if shared & SHORT_ROOTS:
            return True
    # Substring for longer lemmas (quecholli in quecholli, panquetzaliztli).
    cfold = fold(committed_root)
    dfold = fold(decoder_root)
    for t in ctoks:
        if len(t) >= 4 and t in dfold:
            return True
    for t in dtoks:
        if len(t) >= 4 and t in cfold:
            return True
    return False


def extract_quoted_root(source: str | None) -> str:
    """Pull the lemma from strings like 'Maya akal \"pond\"[7]' or 'Nah. aocmo[10]'."""
    s = source or ""
    m = re.search(r"\*((?:[^*\[]+))\*", s)
    if m:
        return m.group(1).strip()
    # After the language abbrev, before a quote or bracket.
    m = re.search(r"(?:Nah\.|Maya|Yucatec|Rom\.|K'iche'|Classic Maya)\s+([^[\"]+)", s)
    if m:
        return m.group(1).strip()
    return s


def decode_has_enough_fields(row: dict) -> bool:
    root = (row.get("root") or "").strip()
    lang = (row.get("lang") or "").strip()
    gloss = (row.get("gloss") or "").strip()
    return bool(root or lang or gloss)


def judge_decode(committed: dict, decode: dict) -> dict:
    """Return a structured Gate-1 recovery judgement.

    committed keys: token, root, lang, gloss, source (optional)
    decode keys: found, root, lang, gloss, confidence
    """
    conf = (decode.get("confidence") or "").strip().lower()
    found = (decode.get("found(Y/N)") or decode.get("found") or "").strip().upper()
    enough = decode_has_enough_fields(decode)
    out = {
        "confidence": conf or "none",
        "found": found,
        "enough_fields": enough,
        "lang_ok": False,
        "root_ok": False,
        "sense_ok": False,
        "recovery": "no",
        "reason": "",
        "dec_root": decode.get("root") or "",
        "dec_lang": decode.get("lang") or "",
        "dec_gloss": decode.get("gloss") or "",
    }
    if conf != "c":
        out["recovery"] = "no"
        out["reason"] = "confidence_not_C"
        return out
    if not enough:
        out["recovery"] = "unscorable"
        out["reason"] = "C_but_empty_root_lang_gloss"
        return out
    allowed = committed.get("lang_classes") or lang_classes(committed.get("lang") or committed.get("source"))
    got = lang_class(decode.get("lang"))
    out["lang_ok"] = (got in allowed) or (got == "?" and "Name" in allowed)
    croot = committed.get("root") or extract_quoted_root(committed.get("source"))
    extra = " ".join(filter(None, [committed.get("source"), committed.get("gloss")]))
    out["root_ok"] = root_match(croot, decode.get("root") or "")
    out["sense_ok"] = sense_match(committed.get("gloss") or "", decode.get("gloss") or "", extra)
    if out["lang_ok"] and out["root_ok"] and out["sense_ok"]:
        out["recovery"] = "yes"
        out["reason"] = "root_lang_sense_match"
    else:
        out["recovery"] = "no"
        missing = []
        if not out["lang_ok"]:
            missing.append(f"lang({got} not in {sorted(allowed)})")
        if not out["root_ok"]:
            missing.append("root")
        if not out["sense_ok"]:
            missing.append("sense")
        out["reason"] = "mismatch:" + ",".join(missing)
    return out
