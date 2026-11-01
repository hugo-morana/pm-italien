"""Construit pm3d/data3d.json (ordre de la boucle) à partir de data_italien.json."""
import json
d = json.load(open("/home/claude/pm_italien/data_italien.json"))
pc = {p["id"]: p for p in d["pieces"]}
# lien final de la boucle : adverbes_2 -> noms 00
x = [n for n in pc["adverbes_2"]["niches"] if not n.get("libre")][-1]
x["lien"] = "La balance bascule dans l'escalier et roule jusqu'au marché des noms, niche 00 : le Cosaque et sa chose."
json.dump(d, open("/home/claude/pm_italien/data_italien.json", "w"), ensure_ascii=False, indent=1)
TOUR = ["noms", "verbes", "adjectifs", "determinants", "pronoms", "conjonctions", "prepositions", "adverbes",
        "basiques_1", "basiques_2", "basiques_3", "basiques_4", "basiques_5", "courantes_1",
        "modales_1", "modales_2", "modales_3", "modales_4", "modales_5", "incises_1", "incises_2", "incises_3", "incises_4",
        "noms_2", "verbes_2", "adjectifs_2", "adverbes_2"]
assert sorted(TOUR) == sorted(pc), set(pc) ^ set(TOUR)
# emplacement de chaque pièce : (étage, côté du couloir, rang le long du couloir)
SLOT = {pid: (0, "N", k) for k, pid in enumerate(TOUR[:8])}          # rez-de-chaussée, rangée nord : les mots
SLOT.update({f"basiques_{k}": (k - 1, "S", 7) for k in range(1, 6)})  # tours : une salle par étage
SLOT.update({"courantes_1": (0, "S", 6)})
SLOT.update({f"modales_{k}": (k - 1, "S", 5) for k in range(1, 6)})
SLOT.update({f"incises_{k}": (k - 1, "S", 4) for k in range(1, 5)})
SLOT.update({"noms_2": (1, "N", 0), "verbes_2": (1, "N", 1), "adjectifs_2": (1, "S", 1), "adverbes_2": (1, "S", 0)})
assert len(set(SLOT.values())) == len(SLOT) == len(TOUR)
FAM = lambda pid: ("noms" if pid.startswith("noms") else "verbes" if pid.startswith("verbes") else
                   "adjectifs" if pid.startswith(("adjectifs", "determinants")) else "pronoms" if pid == "pronoms" else
                   "conjonctions" if pid == "conjonctions" else "prepositions" if pid == "prepositions" else
                   "adverbes" if pid.startswith("adverbes") else "incises" if pid.startswith("incises") else "expressions")
def r1(v): return round(v, 2) if isinstance(v, (int, float)) else None
rooms = []
for pid in TOUR:
    p = pc[pid]
    filled = [n for n in p["niches"] if not n.get("libre")]
    rank = {n["n"]: i + 1 for i, n in enumerate(sorted(filled, key=lambda n: -(n.get("zipf_fr") or 0)))}
    N = []
    for n in p["niches"]:
        if n.get("libre"): N.append(None); continue
        zf, zi = n["zipf"]["fr"], n["zipf"]["it"]
        N.append({"fr": n["fr"], "it": n["cible"], "pr": n.get("prononciation", ""), "api": n.get("api", ""),
                  "mc": n.get("mot_cle", ""), "sc": n.get("scene", ""), "de": n.get("decryptage", ""), "fo": n.get("formes", ""),
                  "efr": n.get("exemple_fr", ""), "efm": n.get("exemple_fr_mot") or "", "eit": n.get("exemple_cible", ""), "eim": n.get("exemple_cible_mot") or "",
                  "li": n.get("lien", ""), "t": n.get("tags", []), "zf": r1(zf.get("parle")), "zi": r1(zi.get("parle")),
                  "zfe": r1(zf.get("ecrit")), "zie": r1(zi.get("ecrit")), "of": (n.get("occ100M") or {}).get("fr", {}).get("parle"),
                  "oi": (n.get("occ100M") or {}).get("it", {}).get("parle"), "ax": bool(n.get("approx")), "rk": rank[n["n"]],
                  "am": n.get("audio_mot"), "ap": n.get("audio_phrase")})
    while len(N) < 100: N.append(None)
    rooms.append({"id": pid, "fr": p["titre_fr"], "it": p["titre_cible"], "decor": p.get("decor", ""), "fam": FAM(pid),
                  "floor": SLOT[pid][0], "slot": {"floor": SLOT[pid][0], "side": SLOT[pid][1], "x": SLOT[pid][2]}, "blocs": p.get("blocs"), "niches": N})
json.dump({"langue": "italien", "rooms": rooms}, open("/home/claude/pm_italien/pm3d/data3d.json", "w"), ensure_ascii=False, separators=(",", ":"))
import os; print(os.path.getsize("/home/claude/pm_italien/pm3d/data3d.json") // 1024, "Ko", sum(1 for r in rooms for n in r["niches"] if n))
