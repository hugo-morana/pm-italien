"""rev 29 : correction des fréquences FR aberrantes puis re-tri des tours par fréquence.
- Bug d'origine (refreq.py) : la fréquence des niches « X / Y » était calculée sur la 1re alternative seule
  (« le / la secrétaire » → fréquence de « le »), et les découpes suivantes ont hérité de ces valeurs.
- Règle : niche d'un seul mot (hors verbes à l'infinitif, comptés au lemme, et hors patrons), si zf dépasse de plus
  de 1,0 le zipf wordfreq du mot français, zf ← zipf wordfreq (même échelle : médiane des écarts = 0,0).
- Puis chaque tour est re-triée par zf (moves enregistrés, progression conservée)."""
import json, re, copy, sys, math
sys.path.insert(0, "/home/claude/pm_italien/tri")
import audit_freq as A
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); old = copy.deepcopy(D["rooms"]); REV = D["rev"]; assert REV == 28
ART = r"^(le|la|les|l'|un|une|des|du|de la)\s+|^l'"
def single(t):
    t = re.sub(r"\(.*?\)", "", t).strip().lower().replace("’", "'"); t = re.sub(ART, "", t).strip()
    return t if re.fullmatch(r"[\wàâäéèêëîïôöùûüçœ'-]+", t) else None
fixed = []
for r in D["rooms"]:
    if r["fam"] in ("verbes", "patrons"): continue
    for n, x in enumerate(r["niches"]):
        if not x or x.get("k"): continue
        w = single(x["fr"])
        if w and x.get("zf") and w in A.WF["fr"] and x["zf"] - A.WF["fr"][w] > 1.0:
            z = A.WF["fr"][w]; fixed.append((r["id"], n, x["fr"], x["zf"], z))
            x["zf"] = z; x["of"] = round(10 ** (z - 3) * 100)
print("corrigées", len(fixed))
for f in fixed: print("  ", f)
# re-tri de toutes les tours
FIXE = {"adjectifs": set(range(90, 100))}
bases = []
for r in D["rooms"]:
    b = re.sub(r"_\d+$", "", r["id"])
    if b not in bases: bases.append(b)
byid = {r["id"]: r for r in D["rooms"]}
moves = {}
for base in [b for b in bases if b != "villes_pays"]:
    ids = [r["id"] for r in D["rooms"] if re.fullmatch(re.escape(base) + r"(_\d+)?", r["id"])]
    pool = [(rid, i, x) for rid in ids for i, x in enumerate(byid[rid]["niches"]) if x and i not in FIXE.get(rid, ())]
    pool.sort(key=lambda t: -(t[2].get("zf") if t[2].get("zf") is not None else -9))
    it = iter(pool)
    for rid in ids:
        r = byid[rid]; nn = [None] * 100
        for n in range(100):
            if n in FIXE.get(rid, ()): nn[n] = r["niches"][n]; continue
            t = next(it, None)
            if t is None: continue
            orid, oi, x = t; nn[n] = x
            if f"{orid}:{oi}" != f"{rid}:{n}": moves[f"{orid}:{oi}"] = f"{rid}:{n}"
        r["niches"] = nn
    assert next(it, None) is None
D["rev"] = REV + 1; D["migr"].append({"rev": REV + 1, "moves": moves, "ids": [r["id"] for r in old]})
# liens de chaîne là où la niche suivante a changé
def seq(rs):
    s = [(r, i, x) for r in rs for i, x in enumerate(r["niches"]) if x]
    return s, {(x["fr"], x["it"]): (s[(k + 1) % len(s)][2]["fr"], s[(k + 1) % len(s)][2]["it"]) for k, (r, i, x) in enumerate(s)}
_, onx = seq(old); SQ, nnx = seq(D["rooms"])
CON = ["Depuis {c}, regarde : {s}", "Avec {c} en main : {s}", "Après {c} vient la scène suivante : {s}"]
low = lambda s: (s[0].lower() + s[1:]).rstrip(". ") if s else s
fin = lambda t: t[:-1] if t[-2:] in ("!.", "?.", "….") else t
nl = 0
for k, (r, i, x) in enumerate(SQ):
    key = (x["fr"], x["it"])
    if onx.get(key) == nnx[key] and x.get("li"): continue
    c = x.get("frp") or re.sub(r"\s*\([^()]*\)\s*$", "", x["fr"]).replace("…", "").strip()
    r2, i2, nx = SQ[(k + 1) % len(SQ)]
    x["li"] = fin(f"Avec {c}, on passe à la salle « {r2['fr']} », où : {low(nx['sc'])}." if r2 is not r else CON[k % 3].format(c=c, s=low(nx["sc"])) + ".")
    nl += 1
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(moves, open("/home/claude/pm_italien/tri/moves_rev29.json", "w"), ensure_ascii=False)
print("déplacées", len(moves), "liens", nl)
