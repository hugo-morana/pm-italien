"""Construit un étage supplémentaire : python3 -I construit.py <txt> <scores.json> <pid> <base> <titre_fr> <titre_cible> <decor> <categorie> [FR=affiché,...] [IT=affiché,...]"""
import json, math, sys
P = "/home/claude/pm_italien/data_italien.json"
txt, scj, pid, base, titre, titre_c, decor, cat = sys.argv[1:9]
ovr = dict(x.split("=", 1) for a in sys.argv[9:] for x in a.split(";") if x)
d = json.load(open(P))
sc = json.load(open(scj))
L = [l.split("|") for l in open(txt, encoding="utf-8").read().strip().split("\n")]
assert len(L) == len(sc) and all(len(x) == 12 for x in L), (len(L), len(sc), [k for k, x in enumerate(L) if len(x) != 12])
occ = lambda v: int(round(10 ** (v - 1), -int(math.floor(v - 1)) + 2))
niches = []
for k, (s, l) in enumerate(zip(sc, L)):
    fr, pr, api, mc, scn, de, fo, efr, mfr, eit, mit, li = l
    s_fr = ovr.get("FR:" + s["fr"], s["fr"]); cible = ovr.get("IT:" + s["cible"], s["cible"])
    assert fr == s_fr, (k, fr, s_fr)
    assert mfr in efr and mit in eit, (fr, efr, mfr, eit, mit)
    niches.append(dict(n=k, fr=fr, cible=cible, prononciation=pr, api=f"/{api}/", mot_cle=mc, scene=scn, decryptage=de,
        formes=fo, exemple_fr=efr, exemple_fr_mot=mfr, exemple_cible=eit, exemple_cible_mot=mit, lien=li,
        categorie=cat, sous_categories=[s.get("sc", cat)], tags=[s["sc"]] if s.get("sc") else [], audio_mot=None, audio_phrase=None,
        lex=s["lex"], lemme_it=s["lemme_it"], zipf={"fr": s["zf"], "it": s["zi"]}, zipf_fr=s["zf"]["parle"], zipf_cible=s["zi"]["parle"],
        zipf_source="mesuré", **({"approx": True} if s.get("approx_it") else {}), occ100M={lg: {a: occ(v) for a, v in z.items() if isinstance(v, float)} for lg, z in (("fr", s["zf"]), ("it", s["zi"]))}))
for k in range(len(niches), 100): niches.append(dict(n=k, libre=True, fr="libre", cible="", lien=""))
autres = {n["cible"]: p["id"] for p in d["pieces"] if p["id"] != pid for n in p["niches"] if not n.get("libre")}
print("traductions déjà présentes ailleurs :", [(n["cible"], autres[n["cible"]]) for n in niches if n.get("cible") in autres])
d["pieces"] = [p for p in d["pieces"] if p["id"] != pid]
ids = [p["id"] for p in d["pieces"]]
i = max(k for k, x in enumerate(ids) if x == base or x.startswith(base + "_")) + 1
d["pieces"].insert(i, {"id": pid, "titre_fr": titre, "titre_cible": titre_c, "decor": decor,
    "ordre": "mots suivants · Zipf FR parlé (Lexique 3 films + OpenSubtitles), décroissant", "famille": cat, "niches": niches})
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print("ok", pid, sum(1 for n in niches if not n.get("libre")))
