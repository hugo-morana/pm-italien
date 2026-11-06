"""rev 27 : une niche par forme (ma / mon / mes ; un / uno / una / un' …) et déterminants rangés avec les adjectifs.
Entrée : scratchpad/split/out.json (skip / items / reuse / delete). Travaille sur pm3d/data3d.json.
- Fréquence de chaque forme : part de la source au prorata des occurrences de la forme dans OpenSubtitles IT.
- Les tours touchées sont re-triées par fréquence FR (zf) ; la salle « determinants » rejoint la tour des adjectifs.
- Migration : la progression de la source va à sa forme « primary » ; les autres formes partent de zéro."""
import json, copy, re, math
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/"
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); old = copy.deepcopy(D["rooms"]); REV = D["rev"]; assert REV == 26
O = json.load(open(S + "split/out.json"))
byid = {r["id"]: r for r in D["rooms"]}
get = lambda k: byid[k.split(":")[0]]["niches"][int(k.split(":")[1])]

def osub(lang):
    c = {}
    for line in open(f"{S}fw/repo/content/2018/{lang}/{lang}_full.txt", encoding="utf-8"):
        w, n = line.rsplit(" ", 1); c[w] = int(n)
    return c
OS_IT = osub("it")
def cnt(it):
    w = re.sub(r"\(.*?\)", "", it).strip().lower().split()
    return OS_IT.get(w[-1], 0) if w else 0

# --- nouvelles niches
groups = {}
for it in O["items"]: groups.setdefault(it["primary"] if it.get("primary") else it["from"][0], []).append(it)
src_of = {}
for it in O["items"]:
    for f in it["from"]: src_of.setdefault(f, []).append(it)
new = []
for it in O["items"]:
    base = get(it.get("primary") or it["from"][0])
    sib = [j for j in O["items"] if (j.get("primary") or j["from"][0]) == (it.get("primary") or it["from"][0])]
    tot = sum(cnt(j["it"]) for j in sib) or 1
    share = (cnt(it["it"]) / tot) if tot > 1 else 1 / len(sib)
    x = {k: base.get(k) for k in ("t", "th", "scat", "ax", "rk", "tv", "te")}
    for k in ("fr", "it", "pr", "api", "mc", "sc", "de", "fo", "efr", "efm", "eit", "eim"): x[k] = it.get(k)
    x["k"] = ""; x["li"] = ""; x["am"] = x["ap"] = x["af"] = x["ai"] = x["px"] = None
    x["oi"] = round((base.get("oi") or 0) * share); x["of"] = round((base.get("of") or 0) * share)
    x["zi"] = round(math.log10(x["oi"] / 100) + 3, 2) if x["oi"] else base.get("zi")
    x["zf"] = round(math.log10(x["of"] / 100) + 3, 2) if x["of"] else base.get("zf")
    x["zfe"] = x["zie"] = None
    if base.get("tv") is not None: x["tv"] = round(base["tv"] * share, 1)
    x["_from"] = it["from"]; x["_primary"] = it.get("primary")
    fam = byid[(it.get("primary") or it["from"][0]).split(":")[0]]["fam"]
    if fam == "adjectifs" and "determinants" in (it.get("primary") or it["from"][0]): fam = "adjectifs"
    x["_fam"] = fam
    new.append(x)

# --- formes réutilisées qui étaient des tournures (« la mia cosa = ma chose ») : deviennent la forme seule
REFORM = {"la mia": "ma", "la tua": "ta", "la sua": "sa"}
retts = []
for ru in O.get("reuse", []):
    x = get(ru["key"])
    if x.get("k") == "tpl" and ru["form"] in REFORM:
        x["it"], x["fr"], x["k"] = ru["form"], REFORM[ru["form"]], ""
        x.pop("ito", None); x.pop("fro", None); x["af"] = x["ai"] = None; retts.append(x)
# --- suppression des sources splittées
dele = set(O["delete"])
for k in dele:
    r, n = k.split(":"); byid[r]["niches"][int(n)] = None

FIXE = {"adjectifs": set(range(90, 100))}
TOWERS = {"adjectifs": ["adjectifs"] + [f"adjectifs_{k}" for k in range(2, 7)] + ["determinants"],
          "pronoms": ["pronoms", "pronoms_2"], "noms": ["noms"] + [f"noms_{k}" for k in range(2, 23)]}
for b in ("adverbes", "prepositions", "conjonctions", "verbes"):
    TOWERS[b] = [r["id"] for r in D["rooms"] if re.fullmatch(b + r"(_\d+)?", r["id"])]
ORD = ["primo", "secondo", "terzo", "quarto", "quinto", "sesto", "settimo", "ottavo", "nono", "decimo"]
moves = {}
def place(base, extra):
    ids = [i for i in TOWERS[base] if i in byid]
    pool = [(rid, i, x) for rid in ids for i, x in enumerate(byid[rid]["niches"]) if x and i not in FIXE.get(rid, ())] + [(None, None, x) for x in extra]
    pool.sort(key=lambda t: -(t[2].get("zf") if t[2].get("zf") is not None else -9))
    keep = [i for i in ids if i != "determinants"]
    slots = sum(100 - len(FIXE.get(i, ())) for i in keep)
    while slots < len(pool):
        k = len(keep) + 1; last = byid[keep[-1]]
        r = {"id": f"{base}_{k}", "fr": re.sub(r" · étage \d+$", "", last["fr"]) + f" · étage {k}", "it": re.sub(r" · .*$", "", last["it"]) + f" · {ORD[min(k - 1, 9)]} piano",
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
    if "determinants" in ids:
        for i, x in enumerate(old[[o["id"] for o in old].index("determinants")]["niches"]): pass
for base in TOWERS:
    extra = [x for x in new if x["_fam"] == base]
    if extra or base in ("adjectifs",): place(base, extra)
assert all(x.get("_at") for x in new), [x["it"] for x in new if not x.get("_at")]
D["rooms"] = [r for r in D["rooms"] if r["id"] != "determinants"]
# progression : source -> forme primary ; doublons fusionnés -> leur forme ; formes déjà existantes (reuse) -> cette niche
prim = {x["_primary"]: x["_at"] for x in new if x["_primary"]}
for f, at in prim.items(): moves[f] = at
for x in new:
    for f in x["_from"]:
        if f not in prim and f not in moves: moves[f] = x["_at"]
for ru in O.get("reuse", []):
    for f in ru["from"]:
        if f not in moves: moves[f] = moves.get(ru["key"], ru["key"])
for k in dele:
    if k not in moves: moves[k] = "_suppr:0"
for x in new:
    for k in ("_from", "_primary", "_fam", "_at"): x.pop(k, None)
D["rev"] = REV + 1; D["migr"].append({"rev": REV + 1, "moves": moves, "ids": [r["id"] for r in old]})
json.dump(moves, open("/home/claude/pm_italien/tri/moves_rev27.json", "w"), ensure_ascii=False, indent=0)

# liens de chaîne là où la niche suivante a changé
def seq(rs):
    s = [(r, i, x) for r in rs for i, x in enumerate(r["niches"]) if x]
    return s, {(x["fr"], x["it"]): (s[(k + 1) % len(s)][2]["fr"], s[(k + 1) % len(s)][2]["it"], s[(k + 1) % len(s)][0]["id"] == r["id"]) for k, (r, i, x) in enumerate(s)}
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
json.dump([[x["fr"], x["it"]] for x in new + retts], open(S + "split/new_items.json", "w"), ensure_ascii=False)
print("nouvelles", len(new), "supprimées", len(dele), "déplacées", len(moves), "liens", nl, "salles", len(D["rooms"]))
