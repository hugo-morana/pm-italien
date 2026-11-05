"""rev 26 : les formes accordées rejoignent leur classe (pluriels de noms → tour des noms ; féminins/pluriels
d'adjectifs → tour des adjectifs qualificatifs). Chaque tour est re-triée entièrement par fréquence FR décroissante
(zf), les couleurs MemoHugoDate (adjectifs 90-99) restent fixes. Travaille sur pm3d/data3d.json ; migration de la
progression, des pièces choisies et de la position ; liens de chaîne réécrits là où la niche suivante a changé."""
import json, copy, re
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); old = copy.deepcopy(D["rooms"]); assert D["rev"] == 25
byid = {r["id"]: r for r in D["rooms"]}
ACC = [f"accords_{k}" for k in range(1, 5)]
NOMS = ["noms"] + [f"noms_{k}" for k in range(2, 21)]
ADJ = ["adjectifs"] + [f"adjectifs_{k}" for k in range(2, 6)]
FIXE = {"adjectifs": set(range(90, 100))}
acc = [(rid, i, x) for rid in ACC for i, x in enumerate(byid[rid]["niches"]) if x]
to_noms = [a for a in acc if "noms" in a[2]["t"]]; to_adj = [a for a in acc if "noms" not in a[2]["t"]]
assert all("adjectifs" in a[2]["t"] for a in to_adj)
for _, _, x in to_adj: x["scat"] = x.get("scat") or "adjectifs_qualificatifs"
ORD = ["", "primo", "secondo", "terzo", "quarto", "quinto", "sesto", "settimo", "ottavo", "nono", "decimo", "undicesimo", "dodicesimo", "tredicesimo",
       "quattordicesimo", "quindicesimo", "sedicesimo", "diciassettesimo", "diciottesimo", "diciannovesimo", "ventesimo", "ventunesimo", "ventiduesimo", "ventitreesimo"]
moves = {}; added = []
def tower(ids, extra, base, mk):
    pool = [(rid, i, x) for rid in ids for i, x in enumerate(byid[rid]["niches"]) if x and i not in FIXE.get(rid, ())] + extra
    pool.sort(key=lambda t: -(t[2].get("zf") if t[2].get("zf") is not None else -9))   # tri stable
    slots = sum(100 - len(FIXE.get(rid, ())) for rid in ids)
    while slots < len(pool):
        k = len(ids) + 1; r = mk(k); byid[r["id"]] = r; ids = ids + [r["id"]]; added.append((base, r)); slots += 100
    it = iter(pool)
    for rid in ids:
        r = byid[rid]; new = [None] * 100
        for n in range(100):
            if n in FIXE.get(rid, ()): new[n] = r["niches"][n]; continue
            t = next(it, None)
            if t is None: continue
            orid, oi, x = t; new[n] = x
            if f"{orid}:{oi}" != f"{rid}:{n}": moves[f"{orid}:{oi}"] = f"{rid}:{n}"
        r["niches"] = new
    assert next(it, None) is None
    return ids
mkn = lambda k: {"id": f"noms_{k}", "fr": f"Les noms · étage {k}", "it": f"I nomi · {ORD[k - 1]} piano", "decor": f"marché italien, étage {k - 1}",
                 "fam": "noms", "floor": k - 1, "slot": {"floor": k - 1, "side": "N", "x": 0}, "blocs": None, "niches": [None] * 100}
mka = lambda k: {"id": f"adjectifs_{k}", "fr": f"Les adjectifs · étage {k}", "it": f"Gli aggettivi · {ORD[k - 1]} piano", "decor": f"galerie de peinture, étage {k - 1}",
                 "fam": "adjectifs", "floor": k - 1, "slot": {"floor": k - 1, "side": "N", "x": 2}, "blocs": None, "niches": [None] * 100}
nids = tower(NOMS, to_noms, "noms_20", mkn); aids = tower(ADJ, to_adj, "adjectifs_5", mka)
rooms = [r for r in D["rooms"] if r["id"] not in ACC]
for base, r in added:   # nouvelles salles juste après le dernier étage existant de la tour
    at = [x["id"] for x in rooms].index(base) + 1
    while at < len(rooms) and rooms[at]["id"] in [a[1]["id"] for a in added]: at += 1
    rooms.insert(at, r)
# salles vides éventuelles (tour plus courte) : supprimées
rooms = [r for r in rooms if any(r["niches"]) or r["fam"] not in ("noms", "adjectifs")]
D["rooms"] = rooms
D["rev"] = 26; D["migr"].append({"rev": 26, "moves": moves, "ids": [r["id"] for r in old]})
json.dump(moves, open("/home/claude/pm_italien/tri/moves_rev26.json", "w"), ensure_ascii=False, indent=0)
def seq(rs):
    s = [(r, i, x) for r in rs for i, x in enumerate(r["niches"]) if x]
    return s, {(x["fr"], x["it"]): (s[(k + 1) % len(s)][2]["fr"], s[(k + 1) % len(s)][2]["it"], s[(k + 1) % len(s)][0]["id"] == r["id"]) for k, (r, i, x) in enumerate(s)}
_, onx = seq(old); S, nnx = seq(D["rooms"])
CON = ["Depuis {c}, regarde : {s}", "Avec {c} en main : {s}", "Après {c} vient la scène suivante : {s}"]
low = lambda s: (s[0].lower() + s[1:]).rstrip(". ") if s else s
fin = lambda t: t[:-1] if t[-2:] in ("!.", "?.", "….") else t
nl = 0
for k, (r, i, x) in enumerate(S):
    key = (x["fr"], x["it"])
    if onx.get(key) == nnx[key]: continue
    c = re.sub(r"\s*\((?:[^()]*), (?:pluriel|féminin|masculin|féminin pluriel|masculin pluriel)\)\s*$", "", x["fr"]).replace(" …", "").replace("…", "").strip()
    r2, i2, nx = S[(k + 1) % len(S)]
    x["li"] = fin(f"Avec {c}, on passe à la salle « {r2['fr']} », où : {low(nx['sc'])}." if r2 is not r else CON[k % 3].format(c=c, s=low(nx["sc"])) + ".")
    nl += 1
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("noms +", len(to_noms), "adjectifs +", len(to_adj), "salles ajoutées", [r["id"] for _, r in added], "déplacées", len(moves), "liens réécrits", nl, "salles", len(D["rooms"]))
# nettoyage : « (anno, pluriel) » retiré des liens
pat = re.compile(r"\s*\([^()]*, (?:féminin pluriel|masculin pluriel|pluriel|féminin|masculin)\)(?=[ ,:.])")
D = json.load(open(P))
for r in D["rooms"]:
    for x in r["niches"]:
        if x and x.get("li"): x["li"] = pat.sub("", x["li"])
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
