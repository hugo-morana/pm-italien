"""Applique de nouveaux mnémos (mc, sc) et réécrit les liens de chaîne des niches précédentes."""
import json, re, sys
P = "/home/claude/pm_italien/pm3d/data3d.json"; D = json.load(open(P))
B = {r["id"]: r for r in D["rooms"]}; ch = set()
for f in sys.argv[1:]:
    for line in open(f, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip(): continue
        k, mc, sc = line.split("|"); rid, n = k.split(":"); x = B[rid]["niches"][int(n)]
        x["mc"] = mc; x["sc"] = sc; ch.add(id(x))
SQ = [(r, i, x) for r in D["rooms"] for i, x in enumerate(r["niches"]) if x]
CON = ["Depuis {c}, regarde : {s}", "Avec {c} en main : {s}", "Après {c} vient la scène suivante : {s}"]
low = lambda s: (s[0].lower() + s[1:]).rstrip(". ") if s else s
fin = lambda t: t[:-1] if t[-2:] in ("!.", "?.", "….") else t
nl = 0
for k, (r, i, x) in enumerate(SQ):
    r2, i2, nx = SQ[(k + 1) % len(SQ)]
    if id(nx) not in ch: continue
    c = x.get("frp") or re.sub(r"\s*\([^()]*\)\s*$", "", x["fr"]).replace("…", "").strip()
    x["li"] = fin(f"Avec {c}, on passe à la salle « {r2['fr']} », où : {low(nx['sc'])}." if r2 is not r else CON[k % 3].format(c=c, s=low(nx["sc"])) + ".")
    nl += 1
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":")); print("mnémos", len(ch), "liens", nl)
