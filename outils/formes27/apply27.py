"""Sons Hugo Pro des formes séparées (rev 27) : paquets audio/f27_<salle>.mp3."""
import json, hashlib
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/"
P = "/home/claude/pm_italien/pm3d/data3d.json"; ENC = S + "aud/enc/"
D = json.load(open(P)); NI = json.load(open(S + "split/new_items.json")); SP = json.load(open(S + "split/spoken.json"))
M = {L: json.load(open(S + f"split/aud_{L}/hp_map.json")) for L in ("fr", "it")}
want = {(f, i): sp for (f, i), sp in zip(NI, SP)}
packs = {}; miss = []
for r in D["rooms"]:
    for x in r["niches"]:
        if not x or (x["fr"], x["it"]) not in want: continue
        sp = want[(x["fr"], x["it"])]
        for L, f in (("fr", "af"), ("it", "ai")):
            fn = M[L].get(sp[L])
            if not fn: miss.append((L, sp[L])); continue
            packs.setdefault(r["id"], []).append((x, f, open(ENC + fn, "rb").read()))
for rid, lst in packs.items():
    blob = b""; refs = []
    for x, f, b in lst: refs.append((x, f, len(blob), len(b))); blob += b
    name = f"audio/f27_{rid}.mp3"; open("/home/claude/pm_italien/pm3d/" + name, "wb").write(blob)
    url = name + "?v=" + hashlib.md5(blob).hexdigest()[:8]
    pi = next((i for i, u in enumerate(D["packs"]) if u.split("?")[0] == name), None)
    if pi is None: D["packs"].append(url); pi = len(D["packs"]) - 1
    else: D["packs"][pi] = url
    for x, f, off, ln in refs: x[f] = [pi, off, ln]
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("paquets", len(packs), "manquants", miss)
