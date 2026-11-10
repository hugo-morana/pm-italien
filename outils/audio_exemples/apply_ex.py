"""Sons Hugo Pro des phrases d'exemple (ae = exemple FR, ap = exemple IT) : un paquet par salle, audio/ex_<salle>.mp3 ;
et des mots qui n'avaient pas encore de voix (af / ai) dans audio/w29_<salle>.mp3. Idempotent : on reconstruit tout."""
import json, hashlib, re
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); M = json.load(open(S + "hp.json"))
def clean(t): t = re.sub(r"\s+", " ", (t or "")).strip(); return t if not t or t[-1] in ".!?…»" else t + "."
def say(t): t = re.sub(r"\([^()]*\)", " ", t).replace(" / ", ", "); return re.sub(r"\s+", " ", t).strip(" ,") + "."
def pack(name, items):
    blob = b""; refs = []
    for x, f, fn in items: b = open(S + "enc/" + fn, "rb").read(); refs.append((x, f, len(blob), len(b))); blob += b
    open("/home/claude/pm_italien/pm3d/" + name, "wb").write(blob)
    url = name + "?v=" + hashlib.md5(blob).hexdigest()[:8]
    pi = next((i for i, u in enumerate(D["packs"]) if u.split("?")[0] == name), None)
    if pi is None: D["packs"].append(url); pi = len(D["packs"]) - 1
    else: D["packs"][pi] = url
    for x, f, off, ln in refs:
        if callable(f): f([pi, off, ln])
        else: x[f] = [pi, off, ln]
NH = {(a, b, c) for a, b, c, *_ in json.load(open(S + "../non_hp.json"))}   # sons Anki (autre voix) à remplacer
ne = nw = 0
for r in D["rooms"]:
    ex, wd = [], []
    for ni, x in enumerate(r["niches"]):
        if not x: continue
        if x.get("frp"): x["ae"], x["ap"] = x.get("af"), x.get("ai"); continue
        for L, k, f in (("fr", "efr", "ae"), ("it", "eit", "ap")):
            fn = M[L].get(clean(x.get(k)))
            if fn: ex.append((x, f, fn))
        for L, k, f in (("fr", "fr", "af"), ("it", "it", "ai")):
            if not x.get(f) or (r["id"], ni, f) in NH or (isinstance(x.get(f), list) and D["packs"][x[f][0]].startswith("audio/w29_")):
                fn = M[L].get(say(x[k]))
                if fn and fn.startswith("w"): wd.append((x, f, fn))
        for e in x.get("px") or []:
            for L, i, j in (("fr", 0, 2), ("it", 1, 3)):
                fn = M[L].get(clean(e[i]))
                if e[j] and fn and fn.startswith("w"): wd.append((x, (lambda v, e=e, j=j: e.__setitem__(j, v)), fn))
    if ex: pack(f"audio/ex_{r['id']}.mp3", ex); ne += len(ex)
    if wd: pack(f"audio/w29_{r['id']}.mp3", wd); nw += len(wd)
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("exemples", ne, "mots", nw)
