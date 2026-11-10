"""Sons Hugo Pro des alternatives séparées (rev 28) : paquets audio/f28_<salle>.mp3."""
import json, hashlib, os
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/"
P = "/home/claude/pm_italien/pm3d/data3d.json"; ENC = S + "aud/enc/"
D = json.load(open(P)); N = json.load(open(S + "alt/need_audio.json")); SP = json.load(open(S + "alt/spoken.json"))
M = {L: json.load(open(S + f"alt/aud_{L}/hp_map.json")) for L in ("fr", "it")}
packs = {}; miss = []
for r in D["rooms"]:
    for x in r["niches"]:
        if not x: continue
        for L, f in (("fr", "af"), ("it", "ai")):
            if x.get(f) or x[L] not in SP[L]: continue
            fn = M[L].get(SP[L][x[L]])
            if not fn: miss.append((L, x[L])); continue
            packs.setdefault(r["id"], []).append((x, f, open(ENC + fn, "rb").read()))
for rid, lst in packs.items():
    blob = b""; refs = []
    for x, f, b in lst: refs.append((x, f, len(blob), len(b))); blob += b
    name = f"audio/f28{os.environ.get("TAG", "a")}_{rid}.mp3"; open("/home/claude/pm_italien/pm3d/" + name, "wb").write(blob)
    url = name + "?v=" + hashlib.md5(blob).hexdigest()[:8]
    pi = next((i for i, u in enumerate(D["packs"]) if u.split("?")[0] == name), None)
    if pi is None: D["packs"].append(url); pi = len(D["packs"]) - 1
    else: D["packs"][pi] = url
    for x, f, off, ln in refs: x[f] = [pi, off, ln]
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("paquets", len(packs), "manquants", len(miss), miss[:10])
