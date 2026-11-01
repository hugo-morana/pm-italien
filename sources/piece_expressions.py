"""Pièces Incises : lit incises_N.txt (13 colonnes) et construit une pièce.
Colonnes : texte de la liste | italien | prononciation | API | mot-clé | scène | décryptage | registre | ex FR | mot FR | ex IT | mot IT | lien
Usage : python3 piece_incises.py N id titre position sous_categorie [début_ordre]"""
import json, math, re, sys
exec(open("/home/claude/pm_italien/outils.py").read())
S_ = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"

def etiquette(t):
    if not t.startswith("S V C"):
        return re.sub(r"\s+", " ", re.sub(r"\bS ?V ?C\b|\bS Vsub\b|\bS Vsbj\b|\bS V\b|\bSV\b|\bV S\b|\bVinf\b|\bVpp\b|\bVop\b|\bVsub\b|\bVsbj\b|\bVcond\b|\bC(?:lieu|date|adj|2)?\b(?!')|^S\b(?= a )", "…", t)).strip()
    return _etiq_inc(t)

def _etiq_inc(t):
    t = t.replace("Disons… C", "Disons… …")
    if t.startswith("S, "):
        return "…, " + t[3:].replace(", V C.", ", …")
    if t.startswith("S V C"):
        return "… " + t[5:].strip().rstrip(".").strip()
    return re.sub(r"\s*S V C\s*([.?]?)$", lambda m: " …" + ("?" if m.group(1) == "?" else ""), t).strip()

def it_coeur(s):
    s = re.sub(r"\(.*?\)", " ", s).replace("…", " ").replace("?", " ").replace(":", " ").replace(",", " ").replace(".", " ").replace("!", " ")
    return re.sub(r"\s+", " ", s).strip().lower()

def construit(fichier, pid, titre, pos, souscat, ordre_attendu=None, titre_cible="Le espressioni", decor="place du marché (piazza)", famille="expressions"):
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
        def _cas(ph, m):
            if m in ph: return m
            k = ph.lower().find(m.lower())
            return ph[k:k + len(m)] if k >= 0 else m
        mfr, mit = _cas(efr, mfr), _cas(eit, mit)
        for a, b in ((efr, mfr), (eit, mit)): assert b in a, (texte, a, b)
        t2 = re.sub(r"\(.*?\)", " ", texte); t2 = re.sub(r"\bS ?V ?C\b|\bS Vsub\b|\bS Vsbj\b|\bS V\b|\bSV\b|\bV S\b|\bVinf\b|\bVpp\b|\bVop\b|\bVsub\b|\bVsbj\b|\bVcond\b|\bC(?:lieu|date|adj|2)?\b(?!')|^S\b(?= a )", " ", t2.replace("Disons… C", "Disons")).replace("/", " ")
        if texte.startswith("S, "): t2 = texte[3:].replace(", V C.", "")
        coeur = re.sub(r"\s+", " ", re.sub(r"[…?.:,!()]", " ", t2)).strip()
        f = fr_spec("PH=" + coeur.lower()); i = it_spec("PH=" + it_coeur(itl))
        assert f["parle"] or not coeur, (texte, f, i)
        f.pop("approx", None); i.pop("approx", None)
        tags = [famille, sc]
        niches.append(dict(n=len(niches), fr=etiquette(texte), texte_source=texte, cible=itl, prononciation=pr, api="/" + api + "/",
            mot_cle=mc, scene=scn, decryptage=de, formes=reg, exemple_fr=efr, exemple_fr_mot=mfr, exemple_cible=eit,
            exemple_cible_mot=mit, lien=li, categorie=famille, sous_categories=[sc], tags=sorted(set(tags)),
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
    d["pieces"].insert(pos, {"id": pid, "titre_fr": titre, "titre_cible": titre_cible, "decor": decor,
        "ordre": "fréquence orale estimée (≈), décroissante", "famille": famille,
        "blocs": [souscat.replace("expressions_", "")] * 10, "niches": niches})
    json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
    print("ok", pid, len(frs), "remplies")


if __name__ == "__main__" and sys.argv[1].startswith("m"):
    S_ = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
    sel = json.load(open(f"{S_}/modales_sel.json"))["sel2"]
    k = int(sys.argv[1][1:])
    d0 = json.load(open("/home/claude/pm_italien/data_italien.json"))
    pos = [p["id"] for p in d0["pieces"]].index("courantes_1") + k
    construit(f"/home/claude/pm_italien/expr_modales_{k}.txt", f"modales_{k}", f"Les expressions modales ({k})", pos,
              "expressions_modales", sel[(k - 1) * 100:k * 100])
elif __name__ == "__main__":
    S_ = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
    sel = json.load(open(f"{S_}/basiques_sel.json"))["sel"]
    k = int(sys.argv[1])
    construit(f"/home/claude/pm_italien/expr_basiques_{k}.txt", f"basiques_{k}", f"Les expressions basiques ({k})", 7 + k,
              "expressions_basiques", sel[(k - 1) * 100:k * 100])
