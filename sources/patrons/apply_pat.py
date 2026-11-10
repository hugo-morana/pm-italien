"""Sons Hugo Pro des patrons syntaxiques : la phrase d'exemple FR / IT sert de son de la niche (paquet audio/pat_patrons.mp3)."""
import json, hashlib
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/"
P = "/home/claude/pm_italien/pm3d/data3d.json"; ENC = S + "aud/enc/"
D = json.load(open(P)); M = {L: json.load(open(S + f"pat_aud/aud_{L}/hp_map.json")) for L in ("fr", "it")}
r = next(r for r in D["rooms"] if r["id"] == "patrons"); blob = b""; refs = []; miss = []
for x in r["niches"]:
    if not x: continue
    for L, f, ex in (("fr", "af", "efr"), ("it", "ai", "eit")):
        fn = M[L].get(x[ex])
        if not fn: miss.append((L, x[ex])); continue
        b = open(ENC + fn, "rb").read(); refs.append((x, f, len(blob), len(b))); blob += b
name = "audio/pat_patrons.mp3"; open("/home/claude/pm_italien/pm3d/" + name, "wb").write(blob)
url = name + "?v=" + hashlib.md5(blob).hexdigest()[:8]
pi = next((i for i, u in enumerate(D["packs"]) if u.split("?")[0] == name), None)
if pi is None: D["packs"].append(url); pi = len(D["packs"]) - 1
else: D["packs"][pi] = url
for x, f, off, ln in refs: x[f] = [pi, off, ln]
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("sons", len(refs), "manquants", miss)
