"""Applique les tournures réécrites et les nouveaux sons à pm3d/data3d.json.
fro/ito : forme d'origine (trous S V C) ; fr/it : forme affichée ; af/ai : clips Hugo Pro, en paquets audio/t_<salle>.mp3."""
import json, hashlib, os, re
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/"
P = "/home/claude/pm_italien/pm3d/data3d.json"; AUD = "/home/claude/pm_italien/pm3d/audio/"; ENC = S + "aud/enc/"
D = json.load(open(P)); byid = {r["id"]: r for r in D["rooms"]}
out = {o["key"]: o for j in range(4) for o in json.load(open(S + f"slots/out{j}.json"))}
SP = json.load(open(S + "slots/spoken.json"))
M = {L: json.load(open(S + f"slots/aud_{L}/hp_map.json")) for L in ("fr", "it")}
TOK = re.compile(r"(?<![\w’'])(?:S|V|C)\d?(?:_[a-zàéèâ]+)?(?![\w’'])")
packs = {}; miss = {"fr": 0, "it": 0}
for key, o in out.items():
    rid, n = key.split(":"); x = byid[rid]["niches"][int(n)]
    assert not TOK.search(o["fr"]) and not TOK.search(o["it"]), o
    x.setdefault("fro", x["fr"]); x.setdefault("ito", x["it"]); x["fr"], x["it"] = o["fr"], o["it"]
    for L, f in (("fr", "af"), ("it", "ai")):
        fn = M[L].get(SP[key][L])
        if not fn: miss[L] += 1; x[f] = None; continue   # ancien son (« S V C ») retiré : la voix de l'appareil lit la forme développée en attendant
        packs.setdefault(rid, []).append((x, f, open(ENC + fn, "rb").read()))
for rid, lst in packs.items():
    blob = b""; refs = []
    for x, f, b in lst: refs.append((x, f, len(blob), len(b))); blob += b
    name = f"audio/t_{rid}.mp3"; open("/home/claude/pm_italien/pm3d/" + name, "wb").write(blob)
    url = name + "?v=" + hashlib.md5(blob).hexdigest()[:8]
    pi = next((i for i, u in enumerate(D["packs"]) if u.split("?")[0] == name), None)
    if pi is None: D["packs"].append(url); pi = len(D["packs"]) - 1
    else: D["packs"][pi] = url
    for x, f, off, ln in refs: x[f] = [pi, off, ln]
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("tournures", len(out), "paquets", len(packs), "sans son", miss)
