"""rev 30 : ajout des mots et patrons manquants relevés dans les phrases d'exemple, puis re-tri fréquentiel des tours."""
import json, re, copy, shutil, unicodedata
from wordfreq import zipf_frequency as zipf
I = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/inv/"
P = "/home/claude/pm_italien/pm3d/data3d.json"
shutil.copy(P, I + "data3d_rev29.json")
D = json.load(open(P)); old = copy.deepcopy(D["rooms"]); REV = D["rev"]; assert REV == 29
M = json.load(open(I + "missing_final.json")); PM = json.load(open(I + "patrons_manquants.json"))

# ---------- API approximative (orthographe italienne régulière) ----------
V = "aeiouàèéìíòóùú"
def strip(c): return unicodedata.normalize("NFD", c)[0]
def g2p(w, glide=True):
    w = w.lower().replace("'", ""); out = []; i = 0
    while i < len(w):
        c = w[i]; n = w[i + 1] if i + 1 < len(w) else ""; n2 = w[i + 2] if i + 2 < len(w) else ""
        if w.startswith("gli", i) and (i + 3 == len(w) or w[i + 3] in V): out.append("ʎ"); i += 3 if i + 3 < len(w) else 2; continue
        if w.startswith("gn", i): out.append("ɲ"); i += 2; continue
        if w.startswith("sc", i) and n2 in "ieèé" and n2:
            out.append("ʃ"); i += 3 if (n2 == "i" and i + 3 < len(w) and w[i + 3] in V) else 2; continue
        if c in "cg" and n == c and n2 and n2 in "ieèéì":
            a = "tʃ" if c == "c" else "dʒ"; out.append(a[0] + a); i += 2
            if n2 == "i" and i + 1 < len(w) and w[i + 1] in V: i += 1
            continue
        if c in "cg" and n and n in "ieèéì":
            out.append("tʃ" if c == "c" else "dʒ"); i += 1
            if n == "i" and i + 1 < len(w) and w[i + 1] in V: i += 1
            continue
        if c in "cg" and n == "h": out.append("k" if c == "c" else "ɡ"); i += 2; continue
        if c == "q": out.append("k"); i += 1; continue
        if c == "c": out.append("k"); i += 1; continue
        if c == "g": out.append("ɡ"); i += 1; continue
        if c == "h": i += 1; continue
        if c == "z": out.append("ts"); i += 1; continue
        if c == "s":
            prev = out[-1] if out else ""
            if (prev and prev[-1] in "aeiou" and n in V) or (n and n in "bdgvlmnr"): out.append("z")
            else: out.append("s")
            i += 1; continue
        if c in V:
            b = strip(c)
            if b == "i" and n and n in V and out and out[-1][-1] in "aeiou": out.append("j")
            elif glide and b in "iu" and n and n in V:
                out.append("j" if b == "i" else "w") if (out and out[-1][-1] not in "aeiou") or not out else out.append(b)
            else: out.append(b)
            i += 1; continue
        if c == "x": out.append("ks"); i += 1; continue
        if c == "j": out.append("j"); i += 1; continue
        if c == "y": out.append("i"); i += 1; continue
        if c == "w": out.append("w"); i += 1; continue
        if c == "k": out.append("k"); i += 1; continue
        out.append(c); i += 1
    s = "".join(out)
    s = s.replace("tsts", "tts")
    return s
def nuclei(s, each=False): return [m.start() for m in re.finditer(r"[aeiou]" if each else r"[aeiou]+", s)]
def stress(ipa, k, each=False):
    nu = nuclei(ipa, each)
    if len(nu) < 2: return ipa
    k = max(0, min(k, len(nu) - 1)); p = nu[k]
    j = p
    while j > 0 and ipa[j - 1] not in "aeiou": j -= 1
    cons = ipa[j:p]
    if len(cons) >= 2:
        if cons[0] == cons[1] or (len(cons) >= 3 and cons[1:3] in ("tʃ", "dʒ") and cons[0] in "td"): j += 1
        elif cons in ("tʃ", "dʒ", "ts", "dz") or (cons[0] in "sz" and len(cons) <= 3): pass
        elif cons[-1] in "jw": j = p - 2 if len(cons) > 2 and cons[-3:-1] not in ("tʃ", "dʒ", "ts") else (p - 3 if len(cons) > 3 else j)
        elif cons[-1] in "rl" and cons[-2] in "pbtdkɡfv": j = p - (3 if len(cons) >= 3 and cons[-3] == "s" else 2)
        elif cons[-2:] in ("tʃ", "dʒ", "ts"): j = p - 2
        else: j = p - 1
    return ipa[:j] + "ˈ" + ipa[j:]
RAW = {"weekend": "wiˈkɛnd", "password": "ˈpaswɔrd", "jazz": "ˈdʒɛts", "thriller": "ˈtriller", "freezer": "ˈfrizer", "cracker": "ˈkrɛker",
       "playboy": "pleiˈbɔi", "cottage": "ˈkɔttedʒ", "puzzle": "ˈpattsol", "hamburger": "amˈburɡer", "mojito": "moˈxito", "social": "ˈsoʃal",
       "crêpe": "krɛp", "menu": "meˈnu", "tram": "tram", "rum": "rum", "est": "ɛst", "zoo": "ˈddzɔo", "ramadan": "ramaˈdan", "purè": "puˈrɛ"}
def api(it, pr):
    ws = re.sub(r"\(.*?\)", "", it).split(); ps = pr.split()
    ps = [None] * (len(ws) - len(ps)) + ps if len(ps) <= len(ws) else ps[-len(ws):]
    out = []
    for w, p in zip(ws, ps):
        if w.lower() in RAW: out.append(RAW[w.lower()]); continue
        ipa = g2p(w); nn = len(nuclei(ipa)); each = False
        if p:
            sy = p.split("-"); k = next((i for i, s in enumerate(sy) if s == s.upper() and re.search(r"[A-ZÀÈÉÌÒÙ]", s)), None)
            if len(sy) > nn:
                ipa2 = g2p(w, glide=False)
                if len(nuclei(ipa2, True)) == len(sy): ipa, nn, each = ipa2, len(sy), True
            k = (nn - (len(sy) - k)) if k is not None else nn - 2
        else: k = nn - 2 if nn >= 2 else None
        out.append(stress(ipa, k, each) if k is not None and nn >= 2 else ipa)
    return "/" + " ".join(out).replace("ˈˈ", "ˈ") + "/"

# ---------- niches ----------
SC = {"noms": "", "verbes": "", "adjectifs": "adjectifs_qualificatifs", "adverbes": "adverbes", "pronoms": "pronoms_personnels_sujets", "conjonctions": "conjonctions_subordination_conséquence"}
ART = r"^(il|lo|la|l'|i|gli|le)\s*"
def zfr(fr):
    h = re.sub(r"\s*[,;(].*", "", fr); h = re.sub(r"^(le|la|les|l'|un|une)\s*", "", h).strip()
    return round(zipf(h, "fr"), 2)
def of(z): return round(10 ** (z - 3) * 100) if z else 0
new = {}
for m in M:
    head = re.sub(ART, "", m["it"]).strip()
    fam = m["fam"]; loc = " " in head and fam == "adverbes"
    scat = "locutions_adverbiales" if loc else ("adjectifs_indéfinis" if m["lemma"] == "altrui" else SC[fam])
    zi = round(zipf(head, "it"), 2); zf = zfr(m["fr"]) or zi; zf = round(min(zf, zi + 1.0), 2) if zi else zf
    x = {"fr": m["fr"], "it": m["it"], "pr": m["pr"], "api": api(m["it"], m["pr"]), "mc": m["mc"], "sc": m["sc"],
         "de": f"{head} ≈ « {m['mc']} »", "fo": "", "efr": m["efr"], "efm": m["efm"], "eit": m["eit"], "eim": m["eim"], "li": "",
         "t": [fam] + ([scat] if scat and scat != fam else []), "th": m["th"], "scat": scat, "k": "loc" if loc else "",
         "zf": zf, "zi": zi, "zfe": None, "zie": None, "of": of(zf), "oi": of(zi), "ax": False, "rk": None, "am": None,
         "ap": None, "af": None, "ai": None, "px": None, "ae": None, "nv": 30}
    new.setdefault(fam, []).append(x)
# patrons : fréquence calée sur les patrons existants (corpus des exemples)
pt = []
for p in PM:
    to = max(0.5, round(p["n"] * 0.25, 1)); zi = round(5.0 + __import__("math").log10(to) * 0.9, 2)
    pt.append({"fr": p["fr"], "it": p["it"], "frp": p["frp"], "itp": p["itp"], "code": p["code"], "pr": p["pr"], "api": api(p["eim"], p["pr"]) if len(p["pr"].split()) <= len(p["eim"].split()) else "",
               "mc": p["mc"], "sc": p["sc"], "de": p["de"], "fo": p["fo"], "efr": p["efr"], "efm": p["efm"], "eit": p["eit"], "eim": p["eim"], "li": "",
               "t": ["patrons", p["scat"]], "th": "syntaxe", "scat": p["scat"], "k": "", "zf": zi, "zi": zi, "zfe": None, "zie": None, "of": of(zi), "oi": of(zi),
               "tw": to, "to": to, "ax": True, "rk": None, "am": None, "ap": None, "af": None, "ai": None, "px": None, "tv": None, "te": 1, "frd": p["frp"], "itd": p["itp"], "ae": None, "nv": 30})
new["patrons"] = pt

# ---------- placement : fin de tour, salles ajoutées si besoin ----------
ORD = "primo secondo terzo quarto quinto sesto settimo ottavo nono decimo undicesimo dodicesimo tredicesimo quattordicesimo quindicesimo sedicesimo diciassettesimo diciottesimo diciannovesimo ventesimo ventunesimo ventiduesimo ventitreesimo ventiquattresimo venticinquesimo".split()
byid = {r["id"]: r for r in D["rooms"]}
def tower(base): return [r for r in D["rooms"] if re.fullmatch(re.escape(base) + r"(_\d+)?", r["id"])]
added_rooms = []
for base, xs in new.items():
    T = tower(base); q = list(xs)
    for r in T:
        for n in range(100):
            if not q: break
            if r["niches"][n] is None and not (r["id"] == "adjectifs" and n >= 90): r["niches"][n] = q.pop(0)
    while q:
        last = T[-1]; k = int(re.search(r"_(\d+)$", last["id"]).group(1)) if "_" in last["id"] else 1
        fl = last["floor"] + 1; nid = f"{base}_{k + 1}"
        nr = {"id": nid, "fr": re.sub(r"étage \d+", f"étage {k + 1}", last["fr"]), "it": re.sub(r"· \w+ piano", f"· {ORD[fl]} piano", last["it"]),
              "decor": re.sub(r"étage \d+", f"étage {fl}", last["decor"]), "fam": last["fam"], "floor": fl, "slot": dict(last["slot"], floor=fl), "blocs": None,
              "niches": [None] * 100}
        for n in range(100):
            if q: nr["niches"][n] = q.pop(0)
        D["rooms"].insert(D["rooms"].index(last) + 1, nr); T.append(nr); byid[nid] = nr; added_rooms.append(nid)
print("salles ajoutées", added_rooms)

# ---------- re-tri de toutes les tours touchées ----------
FIXE = {"adjectifs": set(range(90, 100))}
moves = {}; oldpos = {}
for r in old:
    for i, x in enumerate(r["niches"]):
        if x: oldpos[id(x)] = None
# identifie chaque niche ancienne par (id salle, index) avant tri
tag = {}
for r in D["rooms"]:
    for i, x in enumerate(r["niches"]):
        if x and "nv" not in x: tag[id(x)] = f"{r['id']}:{i}"
for base in new:
    T = tower(base)
    pool = [x for r in T for i, x in enumerate(r["niches"]) if x and i not in FIXE.get(r["id"], ())]
    pool.sort(key=lambda x: -(x.get("zf") if x.get("zf") is not None else -9))
    it = iter(pool)
    for r in T:
        nn = [None] * 100
        for n in range(100):
            if n in FIXE.get(r["id"], ()): nn[n] = r["niches"][n]; continue
            x = next(it, None)
            if x is None: continue
            nn[n] = x
            o = tag.get(id(x))
            if o and o != f"{r['id']}:{n}": moves[o] = f"{r['id']}:{n}"
        r["niches"] = nn
    assert next(it, None) is None
for r in D["rooms"]:
    for i, x in enumerate(r["niches"]):
        if x and x.get("nv") and r["fam"] != "patrons":
            # rang : position dans la tour
            pass
# rang des nouvelles niches = rang moyen des voisines de même fréquence
for base in new:
    if base == "patrons": continue
    T = tower(base); seq = [x for r in T for x in r["niches"] if x]
    for k, x in enumerate(seq):
        if x.get("nv"):
            nb = [y["rk"] for y in seq[max(0, k - 6):k + 7] if not y.get("nv") and isinstance(y.get("rk"), (int, float))]
            x["rk"] = int(sorted(nb)[len(nb) // 2]) if nb else None
D["rev"] = REV + 1; D["migr"].append({"rev": REV + 1, "moves": moves, "ids": [r["id"] for r in old]})

# ---------- liens de chaîne ----------
def seq(rs):
    s = [(r, i, x) for r in rs for i, x in enumerate(r["niches"]) if x]
    return s, {(x["fr"], x["it"]): (s[(k + 1) % len(s)][2]["fr"], s[(k + 1) % len(s)][2]["it"]) for k, (r, i, x) in enumerate(s)}
_, onx = seq(old); SQ, nnx = seq(D["rooms"])
CON = ["Depuis {c}, regarde : {s}", "Avec {c} en main : {s}", "Après {c} vient la scène suivante : {s}"]
low = lambda s: (s[0].lower() + s[1:]).rstrip(". ") if s else s
fin = lambda t: t[:-1] if t[-2:] in ("!.", "?.", "….") else t
nl = 0
for k, (r, i, x) in enumerate(SQ):
    key = (x["fr"], x["it"])
    if onx.get(key) == nnx[key] and x.get("li"): continue
    c = x.get("frp") or re.sub(r"\s*\([^()]*\)\s*$", "", x["fr"]).replace("…", "").strip()
    r2, i2, nx = SQ[(k + 1) % len(SQ)]
    x["li"] = fin(f"Avec {c}, on passe à la salle « {r2['fr']} », où : {low(nx['sc'])}." if r2 is not r else CON[k % 3].format(c=c, s=low(nx["sc"])) + ".")
    nl += 1
# emplacement final pour l'Excel
where = {}
for r in D["rooms"]:
    for i, x in enumerate(r["niches"]):
        if x and x.get("nv"): where[(x["it"], x["fr"])] = (r["id"], r["fr"], i + 1)
json.dump({f"{a}|{b}": v for (a, b), v in where.items()}, open(I + "where.json", "w"), ensure_ascii=False)
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(moves, open(I + "moves_rev30.json", "w"), ensure_ascii=False)
print("nouvelles", sum(len(v) for v in new.values()), "déplacées", len(moves), "liens", nl)
