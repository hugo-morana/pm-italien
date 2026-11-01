"""Outils communs aux pièces de mots-outils (déterminants, pronoms, conjonctions, prépositions, adverbes).
Specs FR : « CG=forme1,forme2;CG2=… » (Lexique), « OS=jeton:part » (OpenSubtitles seul), « PH=locution » (estimation).
Specs IT : « forme:part,… » ou « PH=locuzione ».
Locutions : fréquence estimée comme wordfreq, 1 / Σ(1/f) des mots qui la composent (affichée avec ≈)."""
import json, math, re
exec(open("/home/claude/pm_italien/freq2.py").read())

def _toks(lg, phrase):
    out = []
    for w in phrase.split():
        if "'" in w and OS[lg].get(w, 0) >= 1: out.append(w); continue
        m = re.match(r"^([a-zà-ÿ]+')(.+)$", w)
        if m and m.group(1) in OS[lg]: out += [m.group(1), m.group(2)]
        elif m: out.append(m.group(2))
        else: out.append(w)
    return out

def _hh(vals):
    return 1 / sum(1 / v for v in vals) if vals and all(v > 0 for v in vals) else 0

def phrase(lg, p):
    t = _toks(lg, p)
    os_ = _hh([OS[lg].get(x, 0) for x in t]); wf = _hh([wfpm(lg, x) for x in t])
    return os_, wf

def fr_spec(spec):
    if spec.startswith("OS="):
        w, p = spec[3:].split(":"); pm = OS["fr"].get(w, 0) * float(p)
        return {"ecrit": None, "films": None, "soustitres": z(pm), "global": z(wfpm("fr", w) * float(p)), "parle": z(pm), "approx": True}
    if spec.startswith("PH="):
        os_, wf = phrase("fr", spec[3:])
        return {"ecrit": None, "films": None, "soustitres": z(os_), "global": z(wf), "parle": z(os_), "approx": True}
    lem, cg = set(), set()
    for part in spec.split(";"):
        c, fs = part.split("="); cg.add(c); lem |= set(fs.split(","))
    return fr(lem, cg)

def it_spec(spec):
    if spec.startswith("PH="):
        os_, wf = phrase("it", spec[3:])
        return {"ecrit": None, "parle": z(os_), "global": z(wf), "approx": True}
    pairs = [x.rsplit(":", 1) for x in spec.split(",")]
    return it(formes=[a for a, b in pairs], part={a: float(b) for a, b in pairs})

def build(D, pid, pos, titre_fr, titre_cible, decor, ordre, blocs, prefixe, categorie):
    P = "/home/claude/pm_italien/data_italien.json"
    d = json.load(open(P))
    niches = []
    for line in [l for l in D.strip().split("\n") if l.strip()]:
        p = line.split("|")
        if len(p) == 2:
            niches.append(dict(n=int(p[0]), libre=True, fr="libre", cible="", lien="")); continue
        assert len(p) == 17, (len(p), line[:30])
        n, sc_, fsp, frl, itl, isp, pr, api, mc, sc, de, fo, efr, mfr, eit, mit, li = p
        assert int(n) == len(niches), (n, len(niches), frl)
        f, i = fr_spec(fsp), it_spec(isp)
        assert f and f["parle"] and i and i["parle"], (frl, f, i)
        for a, b in ((efr, mfr), (eit, mit)): assert b in a, (frl, a, b)
        cats = [c.strip() for c in sc_.split("·")]
        cats = [c if "_" in c or c == categorie else prefixe + c for c in cats]
        approx = bool(f.pop("approx", False) or i.pop("approx", False))
        niches.append(dict(n=int(n), fr=frl, cible=itl, prononciation=pr, api="/" + api + "/", mot_cle=mc, scene=sc,
            decryptage=de, formes=fo, exemple_fr=efr, exemple_fr_mot=mfr, exemple_cible=eit, exemple_cible_mot=mit, lien=li,
            categorie=categorie, sous_categories=cats, audio_mot=None, audio_phrase=None, zipf={"fr": f, "it": i},
            zipf_fr=f["parle"], zipf_cible=i["parle"], zipf_source="estimé (locution)" if approx else "mesuré", approx=approx,
            occ100M={lg: {k: int(round(10 ** (v - 1), -int(math.floor(v - 1)) + 2)) for k, v in s.items() if isinstance(v, float)} for lg, s in {"fr": f, "it": i}.items()}))
    for k in range(len(niches), 100):
        niches.append(dict(n=k, libre=True, fr="libre", cible="", lien=""))
    frs = [x["fr"] for x in niches if not x.get("libre")]
    assert len(set(frs)) == len(frs), [x for x in frs if frs.count(x) > 1]
    d["pieces"] = [p for p in d["pieces"] if p["id"] != pid]
    d["pieces"].insert(pos, {"id": pid, "titre_fr": titre_fr, "titre_cible": titre_cible, "decor": decor, "ordre": ordre,
                             "blocs": blocs, "niches": niches})
    json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
    print("ok", pid, len(frs), "remplies")
