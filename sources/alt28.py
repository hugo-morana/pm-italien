"""rev 28 : une niche par alternative « X / Y » (expression : un mot français ; compréhension : un mot italien).
Entrée : scratchpad/alt/out0..3.json ({skip, items[{from, primary, fr, it, …}]}). Travaille sur pm3d/data3d.json.
- Fréquence : part de la source au prorata des occurrences OpenSubtitles de chaque alternative (côté qui varie).
- Chaque tour touchée est re-triée par fréquence FR (zf) ; nouvel étage si elle déborde.
- Migration : la progression de la source va à l'alternative « primary » ; les autres partent de zéro."""
import json, copy, re, math, glob
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/"
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); old = copy.deepcopy(D["rooms"]); REV = D["rev"]; assert REV == 27
OUT = [json.load(open(f)) for f in sorted(glob.glob(S + "alt/out[0-9].json"))]
byid = {r["id"]: r for r in D["rooms"]}
get = lambda k: byid[k.split(":")[0]]["niches"][int(k.split(":")[1])]

def osub(lang):
    c = {}
    for line in open(f"{S}fw/repo/content/2018/{lang}/{lang}_full.txt", encoding="utf-8"):
        w, n = line.rsplit(" ", 1); c[w] = int(n)
    return c
OS = {"it": osub("it"), "fr": osub("fr")}
def cnt(t, L):
    w = re.findall(r"[\wàâäéèêëîïôöùûüçœ']+", re.sub(r"\(.*?\)", "", t).lower())
    if len(w) != 1: return None            # expression : pas de comptage fiable
    return OS[L].get(w[0], 0)
def shares(items, L):
    vals = [x[L] for x in items]
    if len(set(vals)) == 1: return None
    c = [cnt(v, L) for v in vals]
    if any(v is None for v in c) or not sum(c): return [1 / len(items)] * len(items)
    return [max(v, 1) / sum(max(v, 1) for v in c) for v in c]

ITEMS = [it for o in OUT for it in o["items"]]
SKIP = {k for o in OUT for k in o["skip"]}
bysrc = {}
for it in ITEMS: bysrc.setdefault(it["from"], []).append(it)
for k, lst in bysrc.items():
    assert sum(1 for x in lst if x.get("primary")) == 1, k
    assert k not in SKIP, k

# alternative déjà présente ailleurs dans le palais : pas de doublon, la progression va à la niche existante
EXIST = {(x["fr"], x["it"]): f"{r['id']}:{n}" for r in D["rooms"] for n, x in enumerate(r["niches"]) if x and f"{r['id']}:{n}" not in bysrc}
reuse = {}
for k in list(bysrc):
    keep = []
    for it in bysrc[k]:
        e = EXIST.get((it["fr"], it["it"]))
        if e:
            if it.get("primary"): reuse[k] = e
        else: keep.append(it)
    bysrc[k] = keep
new = []
for k, lst in bysrc.items():
    base = get(k)
    sf, si = shares(lst, "fr"), shares(lst, "it")
    eq = [1 / len(lst)] * len(lst)
    for j, it in enumerate(lst):
        x = {kk: base.get(kk) for kk in ("t", "th", "scat", "ax", "rk", "te")}
        for kk in ("fr", "it", "pr", "api", "mc", "sc", "de", "fo", "efr", "efm", "eit", "eim"): x[kk] = it.get(kk) or ""
        x["k"] = base.get("k", ""); x["li"] = ""; x["am"] = x["ap"] = x["px"] = None
        x["af"] = base.get("af") if it["fr"] == base["fr"] else None
        x["ai"] = base.get("ai") if it["it"] == base["it"] else None
        a = (sf or si or eq)[j]; b = (si or sf or eq)[j]
        x["of"] = round((base.get("of") or 0) * a); x["oi"] = round((base.get("oi") or 0) * b)
        x["zf"] = round(math.log10(x["of"] / 100) + 3, 2) if x["of"] else base.get("zf")
        x["zi"] = round(math.log10(x["oi"] / 100) + 3, 2) if x["oi"] else base.get("zi")
        x["zfe"] = x["zie"] = None
        if base.get("tv") is not None: x["tv"] = round(base["tv"] * a, 1)
        x["_from"] = k; x["_primary"] = bool(it.get("primary")); x["_tower"] = re.sub(r"_\d+$", "", k.split(":")[0])
        new.append(x)
for k in bysrc:
    r, n = k.split(":"); byid[r]["niches"][int(n)] = None
for k in reuse:
    if k not in bysrc: r, n = k.split(":"); byid[r]["niches"][int(n)] = None

ORD = ["primo", "secondo", "terzo", "quarto", "quinto", "sesto", "settimo", "ottavo", "nono", "decimo", "undicesimo", "dodicesimo",
       "tredicesimo", "quattordicesimo", "quindicesimo", "sedicesimo", "diciassettesimo", "diciottesimo", "diciannovesimo", "ventesimo",
       "ventunesimo", "ventiduesimo", "ventitreesimo", "ventiquattresimo", "venticinquesimo", "ventiseiesimo", "ventisettesimo"]
FIXE = {"adjectifs": set(range(90, 100))}
def tower(base): return [r["id"] for r in D["rooms"] if re.fullmatch(re.escape(base) + r"(_\d+)?", r["id"])]
moves = {}
def place(base, extra):
    ids = tower(base)
    pool = [(rid, i, x) for rid in ids for i, x in enumerate(byid[rid]["niches"]) if x and i not in FIXE.get(rid, ())] + [(None, None, x) for x in extra]
    pool.sort(key=lambda t: -(t[2].get("zf") if t[2].get("zf") is not None else -9))
    keep = list(ids); slots = sum(100 - len(FIXE.get(i, ())) for i in keep)
    while slots < len(pool):
        k = len(keep) + 1; last = byid[keep[-1]]
        r = {"id": f"{base}_{k}", "fr": re.sub(r" · étage \d+$", "", last["fr"]) + f" · étage {k}", "it": re.sub(r" · .*$", "", last["it"]) + f" · {ORD[min(k - 2, len(ORD) - 1)]} piano",
             "decor": last["decor"], "fam": last["fam"], "floor": last["floor"] + 1, "slot": dict(last["slot"], floor=last["slot"]["floor"] + 1), "blocs": None, "niches": [None] * 100}
        byid[r["id"]] = r; D["rooms"].insert(D["rooms"].index(last) + 1, r); keep.append(r["id"]); slots += 100
    it = iter(pool)
    for rid in keep:
        r = byid[rid]; nn = [None] * 100
        for n in range(100):
            if n in FIXE.get(rid, ()): nn[n] = r["niches"][n]; continue
            t = next(it, None)
            if t is None: continue
            orid, oi, x = t; nn[n] = x
            if orid is None: x["_at"] = f"{rid}:{n}"
            elif f"{orid}:{oi}" != f"{rid}:{n}": moves[f"{orid}:{oi}"] = f"{rid}:{n}"
        r["niches"] = nn
    assert next(it, None) is None
for base in sorted({x["_tower"] for x in new}): place(base, [x for x in new if x["_tower"] == base])
assert all(x.get("_at") for x in new)
for x in new:
    if x["_primary"]: moves[x["_from"]] = x["_at"]
for k, e in reuse.items(): moves[k] = moves.get(e, e)
for k in bysrc:   # source dont aucune alternative n'est « primary » parmi les nouvelles niches : première nouvelle niche
    if k not in moves:
        first = next((x for x in new if x["_from"] == k), None)
        if first: moves[k] = first["_at"]
for x in new:
    for kk in ("_from", "_primary", "_tower", "_at"): x.pop(kk, None)
D["rev"] = REV + 1; D["migr"].append({"rev": REV + 1, "moves": moves, "ids": [r["id"] for r in old]})
json.dump(moves, open("/home/claude/pm_italien/tri/moves_rev28.json", "w"), ensure_ascii=False, indent=0)

# liens de chaîne là où la niche suivante a changé
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
    c = re.sub(r"\s*\([^()]*\)\s*$", "", x["fr"]).replace("…", "").strip()
    r2, i2, nx = SQ[(k + 1) % len(SQ)]
    x["li"] = fin(f"Avec {c}, on passe à la salle « {r2['fr']} », où : {low(nx['sc'])}." if r2 is not r else CON[k % 3].format(c=c, s=low(nx["sc"])) + ".")
    nl += 1
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
need = {"fr": sorted({x["fr"] for x in new if not x["af"]}), "it": sorted({x["it"] for x in new if not x["ai"]})}
json.dump(need, open(S + "alt/need_audio.json", "w"), ensure_ascii=False)
print("sources", len(bysrc), "skip", len(SKIP), "nouvelles", len(new), "déplacées", len(moves), "liens", nl, "salles", len(D["rooms"]),
      "audio à faire FR", len(need["fr"]), "IT", len(need["it"]))
