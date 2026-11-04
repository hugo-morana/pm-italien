"""Ajoute au palais les niches dont « Mots de la phrase » a besoin (apprendre par l'exemple).

- prépositions · étage 3 : « a C_lieu » (à + ville) et « in C_lieu » (en / au + pays) ;
- formes verbales · étage 14 : participes passés manquants (fatto, stato, detto…) ;
- villes et pays : nouvelle salle, thème « geo ».

Idempotent : relancer le script ne duplique rien. Usage : python3 sources/mots_phrase.py
"""
import json, os, re, sys
from wordfreq import zipf_frequency

sys.path.insert(0, os.path.dirname(__file__))
from mots_phrase_data import PARTICIPES, PARTICIPES_EX, LIEUX

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data3d.json")
D = json.load(open(P, encoding="utf-8"))
R = D["rooms"]
I = {r["id"]: r for r in R}

occ = lambda z: int(float(f"{10 ** z / 10:.3g}")) if z else 0
low1 = lambda s: s[:1].lower() + s[1:] if s and not s[1:2].isupper() else s
AUX = set("""ho hai ha abbiamo avete hanno avevo avevi aveva avevamo avevate avevano avrò avrai avrà avremo avrete avranno
avrei avresti avrebbe avremmo avreste avrebbero abbia abbiano avessi avesse avessimo avessero aver avere avendo
sono sei è siamo siete ero eri era eravamo eravate erano sarò sarai sarà saremo sarete saranno sarei saresti sarebbe
saremmo sareste sarebbero sia siano fossi fosse fossimo foste fossero essere esser essendo stato stata stati state""".split())
SKIP = set("mi ti ci vi si lo la li le gli ne non già mai più appena sempre anche ancora proprio davvero solo poi bene forse".split())


def toks(s):
    s = re.sub(r"\(.*?\)", " ", s.lower()).replace("’", "'").replace("'", "' ")
    return [w.lstrip("'") for w in re.sub(r"[^a-zà-öø-ÿ' ]", " ", s).split() if w.lstrip("'")]


def niche(fr, it, pr, api, mc, sc, efr, efm, eit, eim, t, th, scat="", k="", zf=None, zi=None, ax=True, fo=""):
    return {"fr": fr, "it": it, "pr": pr, "api": api, "mc": mc, "sc": sc, "de": f"{re.sub(r'^(il|lo|la|gli|i|le) |^l\'', '', it)} ≈ « {mc} »",
            "fo": fo, "efr": efr, "efm": efm, "eit": eit, "eim": eim, "li": "", "t": t, "th": th, "scat": scat, "k": k,
            "zf": zf, "zi": zi, "zfe": None, "zie": None, "of": occ(zf), "oi": occ(zi), "ax": ax, "rk": 0,
            "am": None, "ap": None, "af": None, "ai": None, "px": None}


# ---------- 1. thème « Villes et pays »
th = D["themes"]
if "geo" not in th:
    D["themes"] = {**{k: v for k, v in th.items() if k not in ("grammaire", "formules", "autres")}, "geo": "Villes et pays",
                   **{k: th[k] for k in ("grammaire", "formules", "autres") if k in th}}

# ---------- 2. prépositions : a C_lieu, in C_lieu
p3 = I["prepositions_3"]["niches"]
aqn = p3[0]
zin = next(x for x in I["prepositions"]["niches"] if x and x["it"] == "in")
if not any(x and x["it"] == "a C_lieu" for x in p3):
    base = dict(t=aqn["t"], th="lieux", scat=aqn["scat"], k="tpl", ax=True)
    p3[1] = niche("à C_lieu (ville)", "a C_lieu", "a", "/a/", "« à ! »", "Un panneau routier : à Rome, 20 km. Devant une ville, « à » se dit a.",
                  "Il a fait carrière à Rome.", "à Rome", "Ha fatto carriera a Roma.", "a Roma", zf=aqn["zf"], zi=aqn["zi"],
                  fo="anglais : in / to C (ville)", **base)
    p3[2] = niche("en / au C_lieu (pays, région)", "in C_lieu", "inn", "/in/", "« inn »", "Une auberge (inn) sur la carte : en Italie, au Japon — in Italia, in Giappone.",
                  "Je vais en Italie.", "en Italie", "Vado in Italia.", "in Italia", zf=aqn["zf"], zi=zin["zi"],
                  fo="anglais : in C (pays)", **base)
    p3[1]["de"], p3[2]["de"] = "a ≈ « « à ! » »", "in ≈ « « inn » »"
    for x in p3[1:3]: x["oi"] = aqn["oi"] if x["it"] == "a C_lieu" else zin["oi"]; x["of"] = 0

# ---------- 3. formes verbales · étage 14 : participes passés
known = {}
for r in R:
    for x in r["niches"]:
        if x: known.setdefault(x["it"], []).append(r["fam"])


def example(p, fr_pp):
    if p in PARTICIPES_EX: return PARTICIPES_EX[p]
    best = None
    for r in R:
        for x in r["niches"]:
            if not x or not x.get("eit"): continue
            t = toks(x["eit"])
            for j, w in enumerate(t):
                if w != p: continue
                k = j - 1
                while k >= 0 and t[k] in SKIP: k -= 1
                if k < 0 or t[k] not in AUX: continue
                m = next((f for f in [fr_pp.split(",")[0].split(" (")[0]] if re.search(rf"\b{re.escape(f)}", x["efr"], re.I)), None)
                if m and (best is None or len(x["eit"]) < len(best[0])): best = (x["eit"], x["efr"], m)
    return best


if "formes_14" not in I:
    rows = []
    for (p, inf, fr_pp, fr_inf, pr, api, mc, sc) in PARTICIPES:
        if any(f in ("formes", "accords") for f in known.get(p, [])): continue
        ex = example(p, fr_pp)
        if not ex: print("  sans phrase :", p); continue
        eit, efr, efm = ex
        z = zipfrequency = zipf_frequency(p, "it")
        rows.append(niche(f"{fr_pp} ({inf}, participe)", p, pr, api, f"{mc} (→ {inf.split(' / ')[0]})", f"Participe {"d'" if inf[0] in 'aeiou' else 'de '}{inf} : {fr_pp}. {sc}",
                          efr, efm, eit, p, ["verbes"], "autres", zf=z, zi=z, ax=True))
    rows.sort(key=lambda x: -x["zi"])
    f13 = I["formes_13"]
    room = {"id": "formes_14", "fr": "Les formes verbales · étage 14", "it": "Le forme verbali · tredicesimo piano",
            "decor": f13["decor"], "fam": "formes", "floor": 13, "slot": {"floor": 13, "side": "S", "x": 0}, "blocs": None,
            "niches": rows + [None] * (100 - len(rows))}
    R.append(room); I["formes_14"] = room
    print("formes_14 :", len(rows), "participes")

# ---------- 4. villes et pays
if "villes_pays" not in I:
    rows = []
    for (it, fr, pr, api, mc, sc, eit, efr, efm) in LIEUX:
        already = [x for r in R for x in r["niches"] if x and x["it"] == it]
        if already:   # déjà dans une salle de noms (la Francia, gli Stati Uniti) : rangé dans le thème, pas dupliqué
            for x in already: x["th"] = "geo"; x["t"] = sorted(set(x["t"]) | {"noms_propres"})
            continue
        bare_it = re.sub(r"^(il|lo|la|gli|i|le) |^l'", "", it); bare_fr = re.sub(r"^(le|la|les) |^l'", "", fr)
        zi, zf = zipf_frequency(bare_it, "it"), zipf_frequency(bare_fr, "fr")
        eim = next(w for w in [bare_it] if w in eit)
        rows.append(niche(fr, it, pr, api, mc, sc, efr, efm, eit, eim, ["noms", "noms_propres"], "geo", zf=zf, zi=zi, ax=False))
    rows.sort(key=lambda x: -x["zi"])
    room = {"id": "villes_pays", "fr": "Les villes et pays", "it": "Città e paesi", "short": "Villes et pays", "code": "geo", "decor": "salle des cartes : mappemondes et portulans",
            "fam": "noms", "floor": 0, "slot": {"floor": 0, "side": "S", "x": 2}, "blocs": None,
            "niches": rows + [None] * (100 - len(rows))}
    R.append(room); I["villes_pays"] = room
    print("villes_pays :", len(rows), "lieux")

# ---------- 5. rangs et liens en chaîne (dans les salles touchées, et l'entrée depuis la salle précédente)
def filled(r): return [i for i, x in enumerate(r["niches"]) if x]


def first_after(ri):
    r2 = R[(ri + 1) % len(R)]
    return r2, r2["niches"][filled(r2)[0]]


touched = ["prepositions_3", "formes_14", "villes_pays"]
for rid in touched:
    ri = next(i for i, r in enumerate(R) if r["id"] == rid); r = R[ri]; ids = filled(r)
    for rank, i in enumerate(ids, 1):
        x = r["niches"][i]
        if rid != "prepositions_3": x["rk"] = rank
        nm = re.sub(r" \(.*$", "", x["fr"])
        if rank < len(ids):
            x["li"] = f"Avec {nm} en main : {low1(r['niches'][ids[rank]]['sc'])}"
        else:
            r2, y = first_after(ri)
            x["li"] = f"Avec {nm}, on passe à la salle « {r2['fr']} », où : {low1(y['sc'])}"
    # la salle d'avant mène maintenant ici
    prev = R[ri - 1]; pid = filled(prev)[-1]; px = prev["niches"][pid]
    if prev["id"] not in touched:
        px["li"] = f"Avec {re.sub(r' \(.*$', '', px['fr'])}, on passe à la salle « {r['fr']} », où : {low1(r['niches'][ids[0]]['sc'])}"

json.dump(D, open(P, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("ok :", len(R), "salles")
