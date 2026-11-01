"""Pièces Incises : lit incises_N.txt (13 colonnes) et construit une pièce.
Colonnes : texte de la liste | italien | prononciation | API | mot-clé | scène | décryptage | registre | ex FR | mot FR | ex IT | mot IT | lien
Usage : python3 piece_incises.py N id titre position sous_categorie [début_ordre]"""
import json, math, re, sys
exec(open("/home/claude/pm_italien/outils.py").read())
S_ = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"

def etiquette(t):
    t = t.replace("Disons… C", "Disons… …")
    if t.startswith("S, "):
        return "…, " + t[3:].replace(", V C.", ", …")
    if t.startswith("S V C"):
        return "… " + t[5:].strip().rstrip(".").strip()
    return re.sub(r"\s*S V C\s*([.?]?)$", lambda m: " …" + ("?" if m.group(1) == "?" else ""), t).strip()

def it_coeur(s):
    s = re.sub(r"\(.*?\)", " ", s).replace("…", " ").replace("?", " ").replace(":", " ").replace(",", " ").replace(".", " ").replace("!", " ")
    return re.sub(r"\s+", " ", s).strip().lower()

def construit(fichier, pid, titre, pos, souscat, ordre_attendu=None, debut=0, libres_apres=None, extra=None):
    P = "/home/claude/pm_italien/data_italien.json"
    d = json.load(open(P))
    niches = []
    lignes = [l for l in open(fichier, encoding="utf-8").read().split("\n") if l.strip()]
    for l in lignes:
        p = l.split("|")
        if len(p) == 1 and p[0].startswith("#libre"):
            niches.append(dict(n=len(niches), libre=True, fr="libre", cible="", lien="")); continue
        assert len(p) == 14 or len(p) == 13, (len(p), l[:50])
        if len(p) == 13: p.insert(0, souscat)
        sc, texte, itl, pr, api, mc, scn, de, reg, efr, mfr, eit, mit, li = p
        for a, b in ((efr, mfr), (eit, mit)): assert b in a, (texte, a, b)
        t2 = texte.replace("S V C", " ").replace("Disons… C", "Disons")
        if texte.startswith("S, "): t2 = texte[3:].replace(", V C.", "")
        coeur = re.sub(r"\s+", " ", re.sub(r"[…?.:,]", " ", t2)).strip()
        f = fr_spec("PH=" + coeur.lower()); i = it_spec("PH=" + it_coeur(itl))
        assert f["parle"] and i["parle"], (texte, f, i)
        f.pop("approx", None); i.pop("approx", None)
        tags = ["incises", sc] + (["incises_milieu"] if sc == "incises_milieu" else [])
        niches.append(dict(n=len(niches), fr=etiquette(texte), texte_source=texte, cible=itl, prononciation=pr, api="/" + api + "/",
            mot_cle=mc, scene=scn, decryptage=de, formes=reg, exemple_fr=efr, exemple_fr_mot=mfr, exemple_cible=eit,
            exemple_cible_mot=mit, lien=li, categorie="incises", sous_categories=[sc], tags=sorted(set(tags)),
            audio_mot=None, audio_phrase=None, zipf={"fr": f, "it": i}, zipf_fr=f["parle"], zipf_cible=i["parle"],
            zipf_source="estimé (locution)", approx=True,
            occ100M={lg: {k: int(round(10 ** (v - 1), -int(math.floor(v - 1)) + 2)) for k, v in s.items() if isinstance(v, float)}
                     for lg, s in {"fr": f, "it": i}.items()}))
    if ordre_attendu:
        got = [x["texte_source"] for x in niches if not x.get("libre")]
        assert got == ordre_attendu, [(k, a, b) for k, (a, b) in enumerate(zip(got, ordre_attendu)) if a != b][:3]
    for k in range(len(niches), 100):
        niches.append(dict(n=k, libre=True, fr="libre", cible="", lien=""))
    frs = [x["fr"] for x in niches if not x.get("libre")]
    assert len(set(frs)) == len(frs), [x for x in frs if frs.count(x) > 1]
    d["pieces"] = [p for p in d["pieces"] if p["id"] != pid]
    d["pieces"].insert(pos, {"id": pid, "titre_fr": titre, "titre_cible": "Gli incisi", "decor": "loggia des orateurs",
        "ordre": "fréquence orale estimée (≈), décroissante", "famille": "incises",
        "blocs": [souscat.replace("incises_", "")] * 10, "niches": niches})
    json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
    print("ok", pid, len(frs), "remplies")

if __name__ == "__main__":
    ordre = json.load(open(f"{S_}/incises.json"))
    intro = [x["texte"] for x in ordre["introductive"] if x["texte"] != "De toute façon S V C."]
    concl = [x["texte"] for x in ordre["conclusive"]]
    n = sys.argv[1]
    if n == "1": construit("/home/claude/pm_italien/incises_1.txt", "incises_1", "Les incises (1)", 8, "incises_introductives", intro[:100])
    if n == "2": construit("/home/claude/pm_italien/incises_2.txt", "incises_2", "Les incises (2)", 9, "incises_introductives", intro[100:200])
    if n == "3": construit("/home/claude/pm_italien/incises_3.txt", "incises_3", "Les incises (3)", 10, "incises_introductives")
    if n == "4": construit("/home/claude/pm_italien/incises_4.txt", "incises_4", "Les incises (4)", 11, "incises_conclusives", concl)
