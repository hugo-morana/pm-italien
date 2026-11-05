"""rev 25 : fusionne « expressions basiques » (basiques_1..6) et « expressions courantes » (courantes_1..5)
en une seule tour « expressions courantes » (courantes_1..10), triée par fréquence FR décroissante.
Travaille directement sur pm3d/data3d.json (référence publiée) ; écrit tri/moves_rev25.json,
ajoute l'étape de migration de la progression et réécrit les liens de chaîne dont la niche suivante a changé."""
import json, copy
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); old = copy.deepcopy(D["rooms"])
assert D["rev"] == 24
OLD_IDS = [f"basiques_{k}" for k in range(1, 7)] + [f"courantes_{k}" for k in range(1, 6)]
byid = {r["id"]: r for r in D["rooms"]}
pool = [(rid, i, x) for rid in OLD_IDS for i, x in enumerate(byid[rid]["niches"]) if x]
pool.sort(key=lambda t: -(t[2]["zf"] if t[2].get("zf") is not None else (t[2].get("zi") or 0) - 9))   # tri stable : basiques d'abord à égalité
ORD = ["", "primo", "secondo", "terzo", "quarto", "quinto", "sesto", "settimo", "ottavo", "nono"]
nrooms = -(-len(pool) // 100); new_rooms = []; moves = {}
for k in range(nrooms):
    chunk = pool[k * 100:(k + 1) * 100]
    r = {"id": f"courantes_{k + 1}", "fr": "Les expressions courantes" + (f" · étage {k + 1}" if k else ""),
         "it": "Le espressioni" + (f" · {ORD[k]} piano" if k else ""), "decor": "place du marché (piazza)", "fam": "expressions",
         "floor": k, "slot": {"floor": k, "side": "S", "x": 6}, "blocs": None, "niches": [None] * 100}
    for n, (rid, i, x) in enumerate(chunk):
        x["t"] = [t for t in x["t"] if t != "expressions_basiques"]
        if "expressions_courantes" not in x["t"]: x["t"].insert(x["t"].index("expressions") + 1 if "expressions" in x["t"] else len(x["t"]), "expressions_courantes")
        x["scat"] = "expressions_courantes"
        r["niches"][n] = x
        if f"{rid}:{i}" != f"{r['id']}:{n}": moves[f"{rid}:{i}"] = f"{r['id']}:{n}"
    new_rooms.append(r)
# place la tour à l'emplacement de l'ancienne salle basiques_1 dans l'ordre de visite
at = [r["id"] for r in D["rooms"]].index("basiques_1")
rest = [r for r in D["rooms"] if r["id"] not in OLD_IDS]
D["rooms"] = rest[:at] + new_rooms + rest[at:]
D["scorder"]["expressions"] = [s for s in D["scorder"]["expressions"] if s != "expressions_basiques"]
D["rev"] = 25; D["migr"].append({"rev": 25, "moves": moves})
json.dump(moves, open("/home/claude/pm_italien/tri/moves_rev25.json", "w"), ensure_ascii=False, indent=0)
# liens de chaîne : réécrits là où la niche suivante (ou le changement de salle) a changé
def seq(rooms):
    s = [(r, i, x) for r in rooms for i, x in enumerate(r["niches"]) if x]
    return s, {(x["fr"], x["it"]): (s[(k + 1) % len(s)][2]["fr"], s[(k + 1) % len(s)][2]["it"], s[(k + 1) % len(s)][0]["id"] == r["id"]) for k, (r, i, x) in enumerate(s)}
_, onx = seq(old); S, nnx = seq(D["rooms"])
CON = ["Depuis {c}, regarde : {s}", "Avec {c} en main : {s}", "Après {c} vient la scène suivante : {s}"]
low = lambda s: (s[0].lower() + s[1:]).rstrip(". ") if s else s
nl = 0
for k, (r, i, x) in enumerate(S):
    key = (x["fr"], x["it"])
    if onx.get(key) == nnx[key]: continue
    c = x["fr"].replace(" …", "").replace("…", "").strip(); r2, i2, nx = S[(k + 1) % len(S)]
    x["li"] = (lambda t: t[:-1] if t[-2:] in ("!.", "?.", "….") else t)(f"Avec {c}, on passe à la salle « {r2['fr']} », où : {low(nx['sc'])}." if r2 is not r else CON[k % 3].format(c=c, s=low(nx["sc"])) + ".")
    nl += 1
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("niches", len(pool), "salles", nrooms, "déplacées", len(moves), "liens réécrits", nl, "salles au total", len(D["rooms"]))
