import random, collections, csv, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SEED = int(sys.argv[1])
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
REAL_COMMITTED = ["Atziri","ik'el","mucane","kutsen","tlayeb","Kuxkal","tala","ek","Ela",
"elba","mujuk'","naach","kifba","itsok","kilya","qexcan","pochiti","sakilja","Kextal","til",
"Maax","ti","jare","Otsuks","kahk","quxzeh","Guatelitzi","Eztli","ta'nuk","cha'tsoke"]
words=[w.lower() for w in CORPUS]; big=[w for w in words if len(w)>=4]
K=2; START,END="\x02","\x03"
model=collections.defaultdict(collections.Counter)
for w in words:
    s=START*K+w+END
    for i in range(len(s)-K): model[s[i:i+K]][s[i+K]]+=1
def ok(s):
    return (4<=len(s)<=10 and s not in words and "''" not in s and not s.startswith("'")
            and not any(rw in s for rw in big) and any(v in s for v in "aeiou"))
def gen(rng):
    for _ in range(800):
        ctx=START*K; out=[]
        while len(out)<=11:
            nxt=model.get(ctx)
            if not nxt: break
            ch=rng.choices(list(nxt),weights=list(nxt.values()))[0]
            if ch==END: break
            out.append(ch); ctx=(ctx+ch)[-K:]
        s="".join(out).strip("'")
        if ok(s): return s
    return None
rng=random.Random(SEED); seen=set(); pseudo=[]
while len(pseudo)<100:
    s=gen(rng)
    if s and s not in seen: seen.add(s); pseudo.append(s)
items=[("pseudo",s) for s in pseudo]+[("real",w) for w in REAL_COMMITTED]
random.Random(SEED+1).shuffle(items)
with open(os.path.join(HERE, f"blind_test_worksheet_s{SEED}.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["id","string","found(Y/N)","root","lang","gloss","confidence"])
    for i,(t,s) in enumerate(items,1): w.writerow([i,s,"","","","",""])
with open(os.path.join(HERE, f"blind_test_key_s{SEED}.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["id","type","string"])
    for i,(t,s) in enumerate(items,1): w.writerow([i,t,s])
print(f"seed {SEED}: wrote worksheet_s{SEED} and key_s{SEED} ({len(items)} rows)")
