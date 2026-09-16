#!/usr/bin/env python3
"""Form-first dictionary lookup over attached text lexicons.

This helper searches local extracts by SURFACE FORM. It does not load
committed_readings.csv, blind_test_key_*, master section 9, or any filled
result sheet. It does not invent etymologies: a miss is a miss.

Dictionary paths are local (uploads / VAAL_DICT_DIR / sources/dictionaries).
Those files must never be committed.

Usage:
  python3 dict_lookup.py che'
  python3 dict_lookup.py --build
  python3 dict_lookup.py --query Ixchel --access online
"""
from __future__ import annotations

import argparse
import os
import pickle
import re
import sys
import unicodedata
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("VAAL_DICT_CACHE", "/tmp/vaal_dict_index.pkl")

# Offline: Cordemex, Christenson, Campbell, Spanish-Maya, norma.
# Online extra for B/D: Nahuatl 1100 wordlist (stands in for Wired Humanities /
# Gran Diccionario; do not browse the live web unless a miss requires a cite).
DICT_FILES = {
    "cordemex": [
        "Cordemex_FULL_71b0.txt",
        "Cordemex_FULL.txt",
    ],
    "kiche": [
        "kiche_christenson_FULL_8527.txt",
        "kiche_christenson_FULL.txt",
    ],
    "nawat": [
        "nawat_Campbell_Pipil_FULL_a96f.txt",
        "nawat_Campbell_Pipil_1985_FULL.txt",
        "nawat_Campbell_Pipil_FULL.txt",
    ],
    "ilide": [
        "ilide_SpanMaya_7c66.md",
        "ilide_SpanMaya.md",
    ],
    "norma": [
        "norma_maya_1657.md",
        "norma_maya.md",
    ],
    "nahuatl1100": [
        "Nahuatl_1100_MyLittleWordLand_c1de.md",
        "Nahuatl_1100_MyLittleWordLand.md",
    ],
}

SEARCH_ROOTS = [
    os.environ.get("VAAL_DICT_DIR", ""),
    "/home/ubuntu/.cursor/projects/workspace/uploads",
    os.path.join(HERE, "..", "sources", "dictionaries"),
    "/workspace",
]

# Attested same-language affixes (standard grammar; also occur as bound forms
# in the attached dictionaries). Used only to test whether residue is an
# attested affix of the SAME language, per TIGHTENED_LATITUDE.md.
MAYA_PREFIX = {"ix", "aj", "ah", "x", "y", "u", "in", "a"}
MAYA_SUFFIX = {
    "il", "el", "al", "ul", "ol", "en", "ech", "e", "ob", "oob", "bil", "bal",
    "tal", "te", "ti", "che", "un", "ul", "ik", "ah", "eh", "i", "o", "a",
    "ane", "ba",
}
NAH_PREFIX = {"tla", "xi", "in", "mo", "te", "pan", "tla", "qui", "cu"}
NAH_SUFFIX = {
    "tl", "tli", "li", "tzin", "tzi", "can", "tlan", "ya", "ti", "liztli",
    "uh", "hua", "hua", "pan", "co", "ca", "ni", "n", "in",
}
KICHE_SUFFIX = {"ik", "aj", "il", "el", "al", "om", "ibal", "bal", "ik"}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'").replace("\u02bc", "'")
    s = s.replace("`", "")
    s = re.sub(r"[^a-z0-9']+", "", s)
    return s


def find_file(names):
    for root in SEARCH_ROOTS:
        if not root:
            continue
        for name in names:
            path = os.path.join(root, name)
            if os.path.isfile(path):
                return path
    return None


def add_entry(index, form, lang, gloss, source, raw=None):
    ff = fold(form)
    if len(ff) < 2:
        return
    if not any(v in ff for v in "aeiou"):
        return
    gloss = re.sub(r"\s+", " ", (gloss or "").strip())
    if len(gloss) < 2:
        return
    if len(gloss) > 180:
        gloss = gloss[:177] + "..."
    rec = {
        "form": form.strip(),
        "lang": lang,
        "gloss": gloss,
        "source": source,
        "raw": (raw or form).strip()[:80],
        "fold": ff,
    }
    index[ff].append(rec)


def parse_cordemex(path, index):
    source = "Cordemex"
    head_re = re.compile(
        r"([A-Z'][A-Z'0-9]*(?:[ \-][A-Z'][A-Z'0-9]*){0,2})\s+"
        r"(\d+(?:\s*,\s*\d+)*)[-\.]?\s*:\s*(.{3,160})"
    )
    current_es = None
    maya_ref = re.compile(r"^([a-z'áéíóúñü][a-z'áéíóúñü\s]{1,36}?)\s+\d+\b")
    allcaps = re.compile(r"^[A-ZÁÉÍÓÚÑÜ ]{3,40}$")
    # Spanish-Maya reverse occupies the second half (OCR ~line 165000+).
    REVERSE_FROM = 165000
    with open(path, encoding="utf-8", errors="replace") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.replace("\x0c", " ").strip()
            if not line:
                continue
            m = head_re.search(line)
            if m:
                form = m.group(1).replace(" ", "")
                gloss = m.group(3)
                gloss = re.split(r"\d+\.\s+[A-Z']", gloss)[0]
                add_entry(index, form, "Yucatec Maya", gloss, source, line)
                if " " in m.group(1) or "-" in m.group(1):
                    add_entry(index, re.sub(r"[\s\-]+", "", m.group(1)), "Yucatec Maya", gloss, source, line)
            if re.search(r"\bix\s+chel\b", line, re.I):
                add_entry(index, "ixchel", "Yucatec Maya", line[:140], source, line)
            if lineno >= REVERSE_FROM:
                if allcaps.match(line) and not any(ch.isdigit() for ch in line):
                    current_es = re.sub(r"\s+", " ", line).title()
                    continue
                if current_es:
                    m2 = maya_ref.match(line)
                    if m2:
                        form = m2.group(1).strip()
                        bits = form.split()
                        add_entry(index, bits[0], "Yucatec Maya", current_es, source, line)
                        if len(bits) == 2:
                            add_entry(index, "".join(bits), "Yucatec Maya", current_es, source, line)


def parse_kiche(path, index):
    source = "Christenson K'iche'"
    # alkabal (n) tax
    rec_re = re.compile(
        r"^(-?[^\s(]+(?:\s[^\s(]+){0,3})\s+\(([^)]{1,24})\)\s+(.{2,200})$"
    )
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.replace("\x0c", "").strip()
            m = rec_re.match(line)
            if not m:
                continue
            form = m.group(1).strip().lstrip("-")
            pos = m.group(2)
            gloss = m.group(3)
            lang = "K'iche'"
            if "span" in pos.lower() or "span" in form.lower():
                lang = "Spanish"
            add_entry(index, form.split()[0], lang, gloss, source, line)


def parse_nawat(path, index):
    source = "Campbell Pipil/Nawat"
    sd_re = re.compile(
        r"^\((?:SD|C|C,\s*SD|SD,\s*C)\)\s+(\S+)(?:\s+(.{0,80}))?$"
    )
    cn_re = re.compile(
        r"CN(?:\s+cf\.?)?\s+\(?([A-Za-z:\'\-]+)",
        re.I,
    )
    cn_quote = re.compile(r"[\"“]([^\"”]{3,80})")
    quoted = re.compile(r'^([A-Za-z:\'\-]+)\s+"([^"]{2,80})"')
    pending_form = None
    pending_es = ""
    pending_cn = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.replace("\x0c", "").strip()
            if not line:
                continue
            m = cn_re.search(line)
            if m:
                form = m.group(1)
                q = cn_quote.search(line)
                gloss = (q.group(1) if q else "").strip()
                if not gloss:
                    pending_cn = form
                    continue
                add_entry(index, form, "Nahuatl", gloss, source + " CN", line)
                continue
            if pending_cn:
                q = cn_quote.search(line)
                extra = (q.group(1) if q else line)[:80]
                add_entry(index, pending_cn, "Nahuatl", extra, source + " CN", line)
                pending_cn = None
                continue
            m = sd_re.match(line)
            if m:
                if pending_form:
                    gloss = pending_es or ""
                    add_entry(index, pending_form, "Nawat", gloss, source)
                pending_form = re.split(r"[,;]", m.group(1))[0]
                pending_form = pending_form.replace(":", "")
                pending_es = (m.group(2) or "").strip()
                continue
            mq = quoted.match(line)
            if mq:
                add_entry(index, mq.group(1), "Nawat", mq.group(2), source, line)
                continue
            if pending_form and re.match(r"^[A-Za-z][A-Za-z ,;'\-]{2,80}$", line):
                if not pending_es:
                    pending_es = line
                else:
                    pending_es = pending_es + "; " + line
                add_entry(index, pending_form, "Nawat", pending_es, source)
                pending_form = None
                pending_es = ""


def parse_ilide(path, index):
    source = "ilide Spanish-Maya"
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if ":" not in line:
                continue
            left, right = line.split(":", 1)
            left = left.strip()
            right = right.strip()
            if not left or not right:
                continue
            # Spanish headword is a loan-palette form.
            sp = left.split("(")[0].strip()
            if " " not in sp and 2 <= len(fold(sp)) <= 12:
                add_entry(index, sp, "Spanish", "Spanish: " + right[:80], source, line)
            for maya in re.split(r"[,;]", right):
                maya = maya.strip()
                maya = re.sub(r"\([^)]*\)", "", maya).strip()
                if not maya or " " in maya:
                    continue
                if 2 <= len(fold(maya)) <= 12:
                    add_entry(index, maya, "Yucatec Maya", left, source, line)


def parse_nahuatl1100(path, index):
    source = "Nahuatl 1100 wordlist"
    row = re.compile(r"^\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|")
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = row.match(line.strip())
            if not m:
                continue
            words, gloss = m.group(1).strip(), m.group(2).strip()
            if words.lower() in {"word", "---"}:
                continue
            for w in re.split(r"[;,]", words):
                w = re.sub(r"\([^)]*\)", "", w).strip()
                w = w.replace("(xic-)", "").replace("(o-)", "").strip()
                if 2 <= len(fold(w)) <= 16:
                    add_entry(index, w, "Nahuatl", gloss, source, line)


def parse_norma(path, index):
    """Orthography standard: harvest isolated Maya example words, weak gloss."""
    source = "norma_maya"
    # Only index explicit `word : gloss` style lines if present.
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if ":" not in line:
                continue
            left, right = line.split(":", 1)
            left = left.strip().lstrip("•").strip()
            if " " in left or len(fold(left)) < 3:
                continue
            if re.match(r"^[0-9.]+$", left):
                continue
            add_entry(index, left, "Yucatec Maya", right.strip()[:80], source, line)


def build_index():
    index = defaultdict(list)
    loaded = []
    parsers = {
        "cordemex": parse_cordemex,
        "kiche": parse_kiche,
        "nawat": parse_nawat,
        "ilide": parse_ilide,
        "norma": parse_norma,
        "nahuatl1100": parse_nahuatl1100,
    }
    for key, names in DICT_FILES.items():
        path = find_file(names)
        if not path:
            print(f"WARN: no file for {key} ({names})", file=sys.stderr)
            continue
        parsers[key](path, index)
        loaded.append(f"{key}:{os.path.basename(path)}")
    # Dedup identical fold+lang+gloss
    for k, recs in list(index.items()):
        seen = set()
        uniq = []
        for r in recs:
            sig = (r["fold"], r["lang"], r["gloss"][:60])
            if sig in seen:
                continue
            seen.add(sig)
            uniq.append(r)
        index[k] = uniq
    blob = {"index": dict(index), "loaded": loaded}
    os.makedirs(os.path.dirname(CACHE) or ".", exist_ok=True)
    with open(CACHE, "wb") as f:
        pickle.dump(blob, f, protocol=4)
    n = sum(len(v) for v in index.values())
    print(f"indexed {n} entries under {len(index)} folded forms from {loaded}")
    print(f"cache {CACHE}")
    return blob


def load_index():
    if os.path.isfile(CACHE):
        with open(CACHE, "rb") as f:
            return pickle.load(f)
    return build_index()


def variants(surface: str) -> list[str]:
    """Strict-safe variants: length doubling, apostrophe on/off, j/h, loan x~j."""
    f = fold(surface)
    out = {f, f.replace("'", "")}
    collapsed = re.sub(r"([aeiou])\1+", r"\1", f)
    out.add(collapsed)
    out.add(collapsed.replace("'", ""))
    extra = set()
    for k in list(out):
        extra.add(k.replace("j", "h"))
        extra.add(k.replace("h", "j"))
        if "f" in k:
            extra.add(k.replace("x", "j"))
    out |= extra
    return [x for x in out if x]


def vowel_shift(s: str) -> list[str]:
    """One licensed raise/lower (loose latitude only)."""
    pairs = [("a", "e"), ("e", "i"), ("o", "u"), ("a", "u"), ("e", "a"),
             ("i", "e"), ("u", "o"), ("u", "a")]
    out = []
    chars = list(s)
    for i, ch in enumerate(chars):
        for a, b in pairs:
            if ch == a:
                t = chars[:]
                t[i] = b
                out.append("".join(t))
    return out


def affixes_for(lang: str) -> tuple[set[str], set[str]]:
    l = (lang or "").lower()
    if "nah" in l or "nawat" in l or "pipil" in l:
        return NAH_PREFIX, NAH_SUFFIX
    if "k'iche" in l or "kiche" in l:
        return set(), KICHE_SUFFIX
    if "span" in l:
        return set(), set()
    return MAYA_PREFIX, MAYA_SUFFIX


def coverage(surface_f: str, lemma_f: str, lang: str) -> tuple[str, str]:
    """Return (kind, residue). kind in exact, affix, prefix, suffix, none."""
    if not lemma_f or not surface_f:
        return "none", surface_f
    if surface_f == lemma_f:
        return "exact", ""
    prefs, sufs = affixes_for(lang)
    if surface_f.startswith(lemma_f):
        rest = surface_f[len(lemma_f):]
        if rest in sufs and len(lemma_f) >= 3 and len(rest) >= 2:
            return "affix", ""
        return "prefix", rest
    if surface_f.endswith(lemma_f):
        rest = surface_f[:-len(lemma_f)] if lemma_f else surface_f
        if rest in prefs and len(lemma_f) >= 3 and len(rest) >= 2:
            return "affix", ""
        return "suffix", rest
    if lemma_f in surface_f and len(lemma_f) >= 4:
        i = surface_f.find(lemma_f)
        rest = surface_f[:i] + "+" + surface_f[i + len(lemma_f):]
        return "infix", rest.strip("+")
    return "none", surface_f


def hits_for(surface: str, index: dict, access: str, latitude: str) -> list[dict]:
    """Ranked attested hits. access=offline|online, latitude=loose|strict."""
    blob_index = index
    f0 = fold(surface)
    keys = set(variants(surface))
    if latitude == "loose":
        for k in list(keys):
            keys.update(vowel_shift(k))
            # coda drop of -tl / -tli / -li / -ks (licensed loose only)
            for coda in ("tli", "tl", "li", "ks", "s"):
                if k.endswith(coda) and len(k) - len(coda) >= 3:
                    keys.add(k[: -len(coda)])
    recs = []
    seen = set()
    for k in keys:
        for r in blob_index.get(k, []):
            if access == "offline" and r["source"].startswith("Nahuatl 1100"):
                continue
            sig = (r["fold"], r["lang"], r["gloss"][:40], r["source"])
            if sig in seen:
                continue
            seen.add(sig)
            kind, residue = coverage(k.replace("'", ""), r["fold"].replace("'", ""), r["lang"])
            recs.append({**r, "match_key": k, "kind": kind, "residue": residue})
    # Also: lemmas that are prefixes of the surface (len>=4) even if not exact key
    if latitude == "loose" or True:
        fstrip = f0.replace("'", "")
        for n in range(min(len(fstrip), 10), 3, -1):
            pref = fstrip[:n]
            for r in blob_index.get(pref, []):
                if access == "offline" and r["source"].startswith("Nahuatl 1100"):
                    continue
                sig = (r["fold"], r["lang"], r["gloss"][:40], r["source"])
                if sig in seen:
                    continue
                seen.add(sig)
                kind, residue = coverage(fstrip, r["fold"].replace("'", ""), r["lang"])
                recs.append({**r, "match_key": pref, "kind": kind, "residue": residue})
    return recs


def gloss_quality(g: str) -> int:
    """Rank definition-like glosses above reverse-index cross-refs. Not sense-led."""
    g = (g or "").strip()
    gl = g.lower()
    score = 0
    if len(g) >= 12:
        score += 2
    if len(g) >= 24:
        score += 1
    if re.search(r"\b(el|la|los|las|de|del|un|una|que|para|por|con|to|the|of|or)\b", gl):
        score += 4
    if re.search(r"\b(ar|er|ir)\b", gl) or "ar " in gl or gl.endswith("ar"):
        score += 1
    if re.match(r"^[A-Za-z']{2,16}$", g) and not re.search(r"\s", g):
        score -= 6
    if "..." in g:
        score -= 1
    if re.search(r"\b(juan|como |idem)\b", gl):
        score -= 4
    return score


def grade(surface: str, hits: list[dict], latitude: str) -> dict:
    """Assign found/confidence/root/lang/gloss/residue/notes from hits.

    STRICT C: exact or same-language affix covering the whole surface.
    LOOSE C: strict C, or one licensed vowel/coda change with full coverage,
             or exact Spanish loan.
    soft: attested lemma of length >=4 as prefix/suffix with residue.
    none: nothing attested at this latitude.
    Empty C never happens: C always carries root/lang/gloss.
    """
    empty = {
        "found": "N", "confidence": "none", "root": "", "lang": "",
        "gloss": "", "residue": "", "notes": "no attested form hit",
        "alts": [],
    }
    if not hits:
        return empty

    def is_spanish(h):
        return "span" in (h["lang"] or "").lower()

    exact = [h for h in hits if h["kind"] == "exact"]
    affix = [h for h in hits if h["kind"] == "affix"]
    pref = [h for h in hits if h["kind"] in {"prefix", "suffix", "infix"} and len(h["fold"]) >= 4]

    def pick(h, conf, note):
        alts = []
        for a in hits:
            if a is h:
                continue
            if a["fold"] == h["fold"] and a["lang"] == h["lang"] and a["gloss"][:20] == h["gloss"][:20]:
                continue
            alts.append(a)
        return {
            "found": "Y",
            "confidence": conf,
            "root": h["form"],
            "lang": h["lang"],
            "gloss": h["gloss"],
            "residue": h.get("residue") or "",
            "notes": f"{note}; source={h['source']}; kind={h['kind']}",
            "alts": alts,
        }

    # Exact Spanish is C at both latitudes (loan palette; not labelled pure noise).
    sp_exact = [h for h in exact if is_spanish(h)]
    if sp_exact:
        return pick(sp_exact[0], "C", "exact Spanish loan-palette hit")

    if exact:
        # Prefer longer lemmas; prefer Maya then Nahuatl then K'iche'.
        exact.sort(key=lambda h: (-gloss_quality(h["gloss"]), -len(h["fold"])))
        return pick(exact[0], "C", "exact folded match (length/glottal only)")

    if affix:
        affix.sort(key=lambda h: (-gloss_quality(h["gloss"]), -len(h["fold"])))
        return pick(affix[0], "C", "root plus attested same-language affix, no residue")

    if latitude == "strict":
        if pref:
            pref.sort(key=lambda h: (-len(h["fold"]), -gloss_quality(h["gloss"])))
            h = pref[0]
            return pick(h, "soft", "attested root with unexplained residue under strict rules")
        return empty

    # loose
    if pref:
        pref.sort(key=lambda h: (-len(h["fold"]), -gloss_quality(h["gloss"])))
        h = pref[0]
        rest = (h.get("residue") or "")
        rest = rest.replace("+", "")
        # Licensed loose C: residue is a single coda/vowel leftover of length 1
        # that is a known romanization tail, or empty after one shift.
        if rest in {"s", "ks", "uks", "tl", "to", "h", "k"}:
            return pick(h, "C", "loose: attested root plus licensed coda leftover")
        if len(h["fold"]) >= 4 and len(rest) <= 2:
            return pick(h, "soft", "loose: attested root with small leftover")
        if len(h["fold"]) >= 4:
            return pick(h, "soft", "loose: attested root as substring")
    return empty


def lookup(surface: str, latitude: str = "strict", access: str = "offline", blob=None) -> dict:
    blob = blob or load_index()
    hits = hits_for(surface, blob["index"], access, latitude)
    return grade(surface, hits, latitude)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query", nargs="?")
    p.add_argument("--build", action="store_true")
    p.add_argument("--access", choices=["offline", "online"], default="offline")
    p.add_argument("--latitude", choices=["loose", "strict"], default="strict")
    args = p.parse_args(argv)
    if args.build or not os.path.isfile(CACHE):
        blob = build_index()
    else:
        blob = load_index()
    if not args.query:
        return
    rec = lookup(args.query, latitude=args.latitude, access=args.access, blob=blob)
    print(f"query={args.query} lat={args.latitude} access={args.access}")
    print(f"  found={rec['found']} conf={rec['confidence']}")
    print(f"  root={rec['root']!r} lang={rec['lang']!r} gloss={rec['gloss']!r}")
    print(f"  residue={rec['residue']!r}")
    print(f"  notes={rec['notes']}")
    if rec.get("alts"):
        print(f"  alts={len(rec['alts'])}")
        for a in rec["alts"][:8]:
            print(f"    {a['form']} [{a['lang']}] {a['gloss'][:60]} ({a['kind']})")


if __name__ == "__main__":
    main()
