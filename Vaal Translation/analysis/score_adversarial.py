import csv, re, glob, os
A=os.path.dirname(os.path.abspath(__file__))+os.sep
def cls_committed(src):
    s=src.lower()
    if s.startswith("(name") or "name)" in s: return "Name"
    if s.startswith("nah") : return "Nahuan"
    if s.startswith("rom") or "spanish" in s[:8]: return "Spanish"
    if s.startswith("k'iche") or s.startswith("kiche"): return "K'iche'"
    if s.startswith("maya") or s.startswith("classic maya") or s.startswith("yucatec"): return "Maya"
    return "Maya" if "maya" in s else ("Nahuan" if "nah" in s else "?")
def cls_adv(l):
    l=(l or "").lower()
    if "k'iche" in l or "kiche" in l or "quiche" in l: return "K'iche'"
    if "nahuatl" in l or "nawat" in l or "pipil" in l or "nahuan" in l: return "Nahuan"
    if "spanish" in l or "rom" in l or "loan" in l: return "Spanish"
    if "yucatec" in l or "maya" in l: return "Maya"
    return "?"
def strg(x): 
    x=(x or "").lower()
    return "strong" if "strong" in x else ("weak" if "weak" in x else "none")
def words(g): return set(re.findall(r"[a-z]{3,}", (g or "").lower()))

# committed worksheet
com={}
for r in csv.DictReader(open(A+"adversarial_worksheet.csv",encoding="utf-8")):
    com[r["id"]]={"token":r["token"],"cclass":cls_committed(r["current_source"]),"cgloss":r["gloss"],"conf":r["current_conf"]}
# adversary results
adv={}
for fp in sorted(glob.glob(A+"adversarial_results_batch*.csv")):
    for r in csv.DictReader(open(fp,encoding="utf-8")):
        adv[r["id"]]=r

surv=fall=name=0; falls=[]
for i,c in com.items():
    if c["cclass"]=="Name": name+=1; continue
    a=adv.get(i,{})
    strong_diff=[]
    for root_k,lang_k,gl_k,st_k in [("best_root","best_lang","best_gloss","best_strength"),
                                    ("alt_root_difflang","alt_lang","alt_gloss","alt_strength")]:
        if strg(a.get(st_k))=="strong":
            acl=cls_adv(a.get(lang_k))
            if acl!=c["cclass"] and acl!="?":
                # meaning overlap: does adversary gloss share content words with committed gloss?
                same = bool(words(a.get(gl_k)) & words(c["cgloss"]))
                strong_diff.append((a.get(root_k),acl,a.get(gl_k),"same-meaning" if same else "DIFF-meaning"))
    if strong_diff:
        fall+=1; falls.append((i,c["token"],c["cclass"],c["cgloss"],strong_diff))
    else:
        surv+=1
tested=surv+fall
print(f"Committed tokens: {len(com)} | testable (non-name): {tested} | names(N/A): {name}")
print(f"SURVIVE: {surv}  FALL: {fall}   survival rate = {surv/tested:.1%}")
diffm=[f for f in falls if any(d[3]=='DIFF-meaning' for d in f[4])]
print(f"  of the falls, {len(diffm)} involve a DIFFERENT-meaning competitor (genuine reinterpretation); {fall-len(diffm)} are same-meaning cognate competitors")
print("\n=== FALLEN TOKENS ===")
for i,tok,ccl,cg,sd in falls:
    print(f"[{i}] {tok}  (committed {ccl}: '{cg[:40]}')")
    for root,acl,ag,mm in sd:
        print(f"      vs {acl} '{root}' = '{ag[:45]}'  [{mm}]")
