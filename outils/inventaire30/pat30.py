"""Son des 14 nouveaux patrons (rev 30) : af/ai = son de l'exemple FR/IT, paquet audio/w30_patrons.mp3."""
import json, re, hashlib
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"; P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); M = json.load(open(S + "hp.json"))
def clean(t): t = re.sub(r"\s+", " ", (t or "")).strip(); return t if not t or t[-1] in ".!?…»" else t + "."
items = []
for r in D["rooms"]:
    if r["fam"] != "patrons": continue
    for x in r["niches"]:
        if x and x.get("nv"):
            for L, k, f in (("fr", "efr", "af"), ("it", "eit", "ai")):
                fn = M[L].get(clean(x[k])); assert fn, (L, x[k]); items.append((x, f, fn))
blob = b""; refs = []
for x, f, fn in items: b = open(S + "enc/" + fn, "rb").read(); refs.append((x, f, len(blob), len(b))); blob += b
name = "audio/w30_patrons.mp3"; open("/home/claude/pm_italien/pm3d/" + name, "wb").write(blob)
url = name + "?v=" + hashlib.md5(blob).hexdigest()[:8]
pi = next((i for i, u in enumerate(D["packs"]) if u.split("?")[0] == name), None)
if pi is None: D["packs"].append(url); pi = len(D["packs"]) - 1
else: D["packs"][pi] = url
for x, f, o, l in refs: x[f] = [pi, o, l]; x["ae" if f == "af" else "ap"] = [pi, o, l]
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("patrons", len(items) // 2)
