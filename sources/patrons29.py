"""Nouvelle classe « patrons syntaxiques » : une salle de 40 niches (onglet « Patrons a mesurer » de l'atlas des
structures du français), avec l'équivalent italien de chaque structure.
Fréquences : le classeur ne chiffre pas les patrons complets ; on part des relations UD publiées (French GSD pour
l'écrit, Rhapsodie pour l'oral, pour 1 000 phrases / unités) et on attribue à chaque patron une part estimée de sa
relation (taux w / o dans patrons_src.py). Conversion en échelle de type Zipf comme les mots du palais :
1 000 phrases ≈ 15 000 mots, donc par million de mots = taux × 1e6 / 15 000, zipf = log10(par million) + 3.
- zf (expression, français parlé) : taux oral ; zi (compréhension de l'italien) : moyenne écrit / oral (estimation,
  pas de corpus italien dans le classeur)."""
import json, math, re, sys
sys.path.insert(0, "/home/claude/pm_italien/tri")
from patrons_src import P
F = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(F))
assert not any(r["id"] == "patrons" for r in D["rooms"])
pm = lambda r: r * 1e6 / 15000
z = lambda r: round(math.log10(pm(r)) + 3, 2)
SLUG = {"Simple": "simples", "Complétive": "complétives", "Relative": "relatives", "Circonstancielle": "circonstancielles",
        "Coordination": "coordination", "Oral": "oral", "Enchâssement": "enchâssement"}
items = []
for (code, fam, frp, itp, fr, it, de, fo, pr, api, mc, sc, efr, efm, eit, eim, w, o) in P:
    items.append({"fr": fr, "it": it, "frd": frp, "itd": itp, "frp": frp, "itp": itp, "code": code, "pr": pr, "api": api, "mc": mc, "sc": sc,
                  "de": de, "fo": fo, "efr": efr, "efm": efm, "eit": eit, "eim": eim, "li": "",
                  "t": ["patrons", "patrons_" + SLUG[fam]], "th": "syntaxe", "scat": "patrons_" + SLUG[fam], "k": "",
                  "zf": z(o), "zi": z((w + o) / 2), "zfe": None, "zie": None, "of": round(pm(o) * 100), "oi": round(pm((w + o) / 2) * 100),
                  "tw": w, "to": o, "ax": True, "rk": None, "am": None, "ap": None, "af": None, "ai": None, "px": None, "tv": None, "te": 1})
items.sort(key=lambda x: -x["zf"])
room = {"id": "patrons", "fr": "Les patrons syntaxiques", "it": "Gli schemi sintattici", "short": "Patrons", "code": "pat",
        "decor": "cabinet de l'architecte : plans et maquettes", "fam": "patrons", "floor": 0, "slot": {"floor": 0, "side": "N", "x": 3},
        "blocs": None, "niches": items + [None] * (100 - len(items))}
D["rooms"].append(room)
D["themes"]["syntaxe"] = "Syntaxe"
D["scorder"]["patrons"] = ["patrons", "patrons_simples", "patrons_complétives", "patrons_relatives", "patrons_circonstancielles",
                           "patrons_coordination", "patrons_oral", "patrons_enchâssement"]
# liens de chaîne : dans la salle, puis depuis la dernière niche de la salle précédente
CON = ["Depuis {c}, regarde : {s}", "Avec {c} en main : {s}", "Après {c} vient la scène suivante : {s}"]
low = lambda s: (s[0].lower() + s[1:]).rstrip(". ") if s else s
for k, x in enumerate(items):
    nx = items[(k + 1) % len(items)]
    x["li"] = CON[k % 3].format(c="« " + x["frp"] + " »", s=low(nx["sc"])) + "."
prev = D["rooms"][-2]; last = [x for x in prev["niches"] if x][-1]
c = re.sub(r"\s*\([^()]*\)\s*$", "", last["fr"]).replace("…", "").strip()
last["li"] = f"Avec {c}, on passe à la salle « {room['fr']} », où : {low(items[0]['sc'])}."
json.dump(D, open(F, "w"), ensure_ascii=False, separators=(",", ":"))
print("salle", room["id"], "niches", len(items), "salles", len(D["rooms"]))
for x in items: print(x["code"], x["zf"], x["zi"], x["frp"], "|", x["itp"])
