import json, math
P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))
sc = json.load(open("/home/claude/pm_italien/etages/noms2_scores.json"))
L = [l.split("|") for l in open("/home/claude/pm_italien/etages/noms2.txt", encoding="utf-8").read().strip().split("\n")]
assert len(L) == 100 and all(len(x) == 12 for x in L), [len(x) for x in L]
occ = lambda v: int(round(10 ** (v - 1), -int(math.floor(v - 1)) + 2))
niches = []
for k, (s, l) in enumerate(zip(sc, L)):
    fr, pr, api, mc, scn, de, fo, efr, mfr, eit, mit, li = l
    assert fr == s["fr"], (k, fr, s["fr"])
    assert mfr in efr and mit in eit, (fr, efr, mfr, eit, mit)
    niches.append(dict(n=k, fr=fr, cible=s["cible"], prononciation=pr, api=f"/{api}/", mot_cle=mc, scene=scn, decryptage=de,
        formes=fo, exemple_fr=efr, exemple_fr_mot=mfr, exemple_cible=eit, exemple_cible_mot=mit, lien=li,
        categorie="noms", sous_categories=["noms"], tags=[], audio_mot=None, audio_phrase=None,
        lex=s["lex"], lemme_it=s["lemme_it"], zipf={"fr": s["zf"], "it": s["zi"]}, zipf_fr=s["zf"]["parle"], zipf_cible=s["zi"]["parle"],
        zipf_source="mesuré", occ100M={lg: {a: occ(v) for a, v in z.items() if isinstance(v, float)} for lg, z in (("fr", s["zf"]), ("it", s["zi"]))}))
cib = {n["cible"] for p in d["pieces"] for n in p["niches"] if not n.get("libre")}
dup = [n["cible"] for n in niches if n["cible"] in cib and not any(p["id"] == "noms_2" for p in d["pieces"])]
print("doublons de traduction avec d'autres pièces :", dup)
d["pieces"] = [p for p in d["pieces"] if p["id"] != "noms_2"]
i = [p["id"] for p in d["pieces"]].index("noms") + 1
d["pieces"].insert(i, {"id": "noms_2", "titre_fr": "Les noms · étage 2", "titre_cible": "I nomi · primo piano",
    "decor": "marché italien, étage de la loggia", "ordre": "mots 101 à 200 · Zipf FR parlé (Lexique 3 films + OpenSubtitles), décroissant",
    "famille": "noms", "niches": niches})
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print("ok noms_2", len(niches))
