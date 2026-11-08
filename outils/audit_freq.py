"""Audit des fréquences : compare zf / zi à wordfreq (zipf) calculé sur le texte actuel de la niche.
Repère surtout le bug de refreq.py (fréquence calculée sur la 1re alternative « le / la … » → celle de « le »)."""
import json, re, sys, math
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
sys.path.insert(0, S)
from mp import load
WF = {"fr": load(f"{S}/wf/wordfreq/data/large_fr.msgpack.gz")[1], "it": load(f"{S}/wf/wordfreq/data/large_it.msgpack.gz")[1]}
D = json.load(open("/home/claude/pm_italien/pm3d/data3d.json"))
PH = {"fr": r"\b(qn|qc|qqpart|quelqu'un|quelque chose)\b", "it": r"\b(qcn|qcs|qualcuno|qualcosa|da qualche parte)\b"}
def toks(t, L):
    t = t.replace("’", "'").lower(); t = re.sub(r"\(.*?\)", " ", t); t = re.sub(PH[L], " ", t).replace("…", " ")
    t = re.sub(r"\b(l|d|j|m|t|s|n|c|qu|un|dell|all|nell|sull|quest|quell)'", r"\1' ", t)
    return [w for w in re.findall(r"[\wàâäéèêëîïôöùûüçœìòó']+", t)]
def zipf(t, L):
    ws = toks(t, L)
    if not ws: return None
    fs = []
    for w in ws:
        z = WF[L].get(w) if w in WF[L] else WF[L].get(w.rstrip("'"))
        if z is None: return None
        fs.append(10 ** (z - 3) if z > 3 else 10 ** (z - 3))
    f = 1 / sum(1 / x for x in fs)          # combinaison de wordfreq pour plusieurs mots
    return round(math.log10(f) + 3, 2) if f > 0 else None
if __name__ == "__main__":
    rows = []
    for r in D["rooms"]:
        for n, x in enumerate(r["niches"]):
            if not x or x.get("frp"): continue
            wf, wi = zipf(x["fr"], "fr"), zipf(x["it"], "it")
            rows.append((r["id"], n, x["fr"], x["it"], x.get("zf"), wf, x.get("zi"), wi))
    json.dump(rows, open(S + "/audit_rows.json", "w"), ensure_ascii=False)
    bad = [r for r in rows if r[4] and r[5] and r[4] - r[5] > 1.2]
    badi = [r for r in rows if r[6] and r[7] and r[6] - r[7] > 1.2]
    print("niches", len(rows), "FR surestimées", len(bad), "IT surestimées", len(badi))
    for r in sorted(bad, key=lambda r: -(r[4] - r[5]))[:60]: print("FR", r[0], r[1], r[2], "|", r[3], r[4], "→ wf", r[5])
    for r in sorted(badi, key=lambda r: -(r[6] - r[7]))[:25]: print("IT", r[0], r[1], r[2], "|", r[3], r[6], "→ wf", r[7])
