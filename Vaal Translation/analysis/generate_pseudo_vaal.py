#!/usr/bin/env python3
"""
generate_pseudo_vaal.py  --  null-model string generator for the Vaal reconstruction.

Purpose: produce phonotactically Vaal-like strings that carry NO designed meaning,
so the decoding pipeline can be run on them to measure its false-positive rate
(how often it "finds" an attested root for a string that was never built from one).

Unbiasedness guarantees:
  1. The phonotactic model is trained ONLY on authentic Vaal surface forms
     (in-game strings + confirmed names). It never sees any source dictionary,
     so it cannot be steered toward real Maya/Nahuatl/K'iche'/Spanish roots.
  2. Fixed RNG seed -> the list is fully reproducible; no cherry-picking is possible.
  3. Filters remove only fragments and strings that embed a whole real root (>=4 chars);
     they do not select FOR or AGAINST decodability.
Re-run to regenerate the identical set: python3 generate_pseudo_vaal.py (optional args: seed shuffle-seed; with no arguments this reproduces the canonical seed-1729 set)
"""
import random, collections, csv, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1729
SHUF_SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 2718

# --- Authentic Vaal SURFACE forms (romanized tokens as they appear in game / as names).
CORPUS = """
Atziri Otsuks Tzokan'te u'te A'te Yatle ik'el Kuxkal tlayeb kutsen Ela ukto Maax ka ti
a'tul cheyel mucane quxzeh Axba Kiibsa' ta' en Gyan'uks Donuks puxe daka jare fukuur soxsal
puyao te'moxti nochbe inib buxa Eche lu Aiokmo akal anab ascensionada atla cha'tsoke chikula'
ek elba Eztli Pilli Guatelitzi Ibil ich ikba'yucane ik'bala Ik'eche itsok itzil kifba kiimil
kilya ko'janti kujkuali liimek Ma'oxe mujuk' naach nochira pochiti qexcan sakilja ta'nuk tala
Teoyuxtlane til Tlaxye' Kextal uch' yuquia yutsal Xatlene Xibaqua Atzoatl Kuetzakala Quemalani
Xolotl Tizoc Cotan Axilo Mektul Ahuatotli Xomatl tatlat xomaplat xictep cutlotl azcado huatat
quiquate zahua moti taak'iin kahk tche ka'tse ipkaat koriek xecwa Napuatzi Doryani Zolin Zelina
Kamasa Kopec Ketzuli Tetzlapokal Arakaali Kishara
""".split()

# Real committed tokens used as PLANTS in the blind worksheet (known-good positives).
REAL_COMMITTED = ["Atziri","ik'el","mucane","kutsen","tlayeb","Kuxkal","tala","ek","Ela",
"elba","mujuk'","naach","kifba","itsok","kilya","qexcan","pochiti","sakilja","Kextal","til",
"Maax","ti","jare","Otsuks","kahk","quxzeh","Guatelitzi","Eztli","ta'nuk","cha'tsoke"]

words = [w.lower() for w in CORPUS]
realwords_big = [w for w in words if len(w) >= 4]
K = 2
START, END = "\x02", "\x03"
model = collections.defaultdict(collections.Counter)
for w in words:
    s = START*K + w + END
    for i in range(len(s)-K):
        model[s[i:i+K]][s[i+K]] += 1

def ok(s):
    if not (4 <= len(s) <= 10): return False
    if s in words: return False
    if "''" in s or s.startswith("'"): return False
    if any(rw in s for rw in realwords_big): return False
    if not any(v in s for v in "aeiou"): return False
    return True

def gen(rng):
    for _ in range(800):
        ctx = START*K; out=[]
        while len(out) <= 11:
            nxt = model.get(ctx)
            if not nxt: break
            ch = rng.choices(list(nxt), weights=list(nxt.values()))[0]
            if ch == END: break
            out.append(ch); ctx=(ctx+ch)[-K:]
        s = "".join(out).strip("'")
        if ok(s): return s
    return None

rng = random.Random(SEED)
seen=set(); pseudo=[]
while len(pseudo) < 100:
    s = gen(rng)
    if s and s not in seen:
        seen.add(s); pseudo.append(s)

# 1) the plain test set
with open(os.path.join(HERE, "pseudo_vaal_test_set.txt"),"w",encoding="utf-8") as f:
    f.write(f"# 100 pseudo-Vaal strings (null model). Seed {SEED}. See NULL_MODEL_PROTOCOL.md\n")
    for i,s in enumerate(pseudo,1): f.write(f"{i:3d}. {s}\n")

# 2) blind worksheet: pseudo + real committed, shuffled, labels hidden
items = [("pseudo",s) for s in pseudo] + [("real",w) for w in REAL_COMMITTED]
shuf = random.Random(SHUF_SEED)
shuf.shuffle(items)
with open(os.path.join(HERE, f"blind_test_worksheet_s{SEED}.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["id","string","found_root?(Y/N)","proposed_root","source_lang","gloss","confidence(C/soft)"])
    for i,(t,s) in enumerate(items,1): w.writerow([i,s,"","","","",""])
with open(os.path.join(HERE, f"blind_test_key_s{SEED}.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["id","type","string"])
    for i,(t,s) in enumerate(items,1): w.writerow([i,t,s])

print(f"wrote pseudo_vaal_test_set.txt (100), blind_test_worksheet_s{SEED}.csv and blind_test_key_s{SEED}.csv ({len(items)} items)")
