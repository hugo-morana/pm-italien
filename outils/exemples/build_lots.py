"""Lots ElevenLabs des phrases d'exemple (efr / eit), du plus fréquent au plus rare, + les mots sans voix Hugo Pro."""
import json, re
D = json.load(open("/home/claude/pm_italien/pm3d/data3d.json"))
N = [x for r in D["rooms"] for x in r["niches"] if x]
N.sort(key=lambda x: -max(x.get("zf") or 0, x.get("zi") or 0))
def clean(t): t = re.sub(r"\s+", " ", (t or "")).strip(); return t if not t or t[-1] in ".!?…»" else t + "."
seen = {"fr": {}, "it": {}}
for x in N:
    if x.get("frp"): continue                       # patrons : l'exemple a déjà son son (af / ai)
    for L, k in (("fr", "efr"), ("it", "eit")):
        t = clean(x.get(k))
        if t and t not in seen[L]: seen[L][t] = len(seen[L])
lots = []
for L in ("fr", "it"):
    cur, n = [], 0
    for t in seen[L]:
        if cur and (n + len(t) + 10 > 4200 or len(cur) >= 110): lots.append({"L": L, "T": cur}); cur, n = [], 0
        cur.append(t); n += len(t) + 10
    if cur: lots.append({"L": L, "T": cur})
# alterner FR / IT pour que les deux langues avancent ensemble
fr = [l for l in lots if l["L"] == "fr"]; it = [l for l in lots if l["L"] == "it"]
order = [l for pair in zip(fr, it) for l in pair] + fr[len(it):] + it[len(fr):]
for i, l in enumerate(order): l["id"] = i
json.dump(order, open("lots.json", "w"), ensure_ascii=False)
print("lots", len(order), "FR", len(fr), "IT", len(it), "phrases", len(seen["fr"]), len(seen["it"]))
