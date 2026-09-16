import csv, sys
res_path, key_path = sys.argv[1], sys.argv[2]
res={}
with open(res_path,encoding="utf-8") as f:
    for r in csv.DictReader(f):
        res[r["id"]]={"conf":(r.get("confidence") or "").strip().lower(),
                      "found":(r.get("found(Y/N)") or r.get("found") or "").strip().upper()}
key={}
with open(key_path,encoding="utf-8") as f:
    for r in csv.DictReader(f): key[r["id"]]=r["type"]
P=dict(C=0,soft=0,none=0,Y=0,n=0); R=dict(C=0,soft=0,none=0,Y=0,n=0)
for i,t in key.items():
    d=res.get(i,{}); c=d.get("conf",""); found=d.get("found","")
    tgt=P if t=="pseudo" else R; tgt["n"]+=1
    if c=="c": tgt["C"]+=1
    elif c=="soft": tgt["soft"]+=1
    else: tgt["none"]+=1
    if found=="Y": tgt["Y"]+=1
fpr_c=P["C"]/P["n"]; fpr_soft=(P["C"]+P["soft"])/P["n"]; tpr_c=R["C"]/R["n"]; tpr_found=R["Y"]/R["n"]
print(f"PSEUDO n={P['n']}: C={P['C']} soft={P['soft']} none={P['none']} | REAL n={R['n']}: C={R['C']} soft={R['soft']} none={R['none']}")
print(f"FPR(C)={fpr_c:.2f}  FPR(C+soft)={fpr_soft:.2f}  TPR(C)={tpr_c:.2f}  TPR(found)={tpr_found:.2f}  Discrimination(C)={tpr_c-fpr_c:+.2f}")
