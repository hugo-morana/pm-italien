"""Rattache chaque phrase Anki à la niche dont le mot (ou l'expression) y figure ; écrit phrases/assoc.json."""
import csv, json, re, collections
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
BEST = {}
for r in csv.DictReader(open(f"{S}/pl/Lexique383/Lexique383.tsv", encoding="utf-8"), delimiter="\t"):
    f = float(r["freqfilms2"]) + float(r["freqlivres"])
    if r["ortho"] not in BEST or f > BEST[r["ortho"]][1]: BEST[r["ortho"]] = (r["lemme"], f)
FORCE = {"suis": "être", "es": "être", "est": "être", "été": "être", "tu": "tu", "fait": "faire", "as": "avoir", "a": "avoir", "vis": "vivre", "sens": "sentir", "peux": "pouvoir", "veux": "vouloir", "dois": "devoir", "sais": "savoir"}
lemme = lambda w: FORCE.get(w) or BEST.get(w, (w, 0))[0]
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("œ", "oe").lower()).strip()
toks = lambda s: re.findall(r"[a-zàâäçéèêëîïôöùûüÿæœ-]+", norm(s).replace("'", "' "))
D = json.load(open("/home/claude/pm_italien/data_italien.json"))
KEYS = []   # (type, clé, pid, n, zipf)
ART = r"^((le|la|les|un|une|des|du|de la|se)\s+|l'|s')"
for p in D["pieces"]:
    for n in p["niches"]:
        if n.get("libre"): continue
        z = n.get("zipf_fr") or 0
        for alt in re.split(r"\s*/\s*", re.sub(r"\(.*?\)", "", n["fr"])):
            a = norm(alt).replace("…", " ").strip(" ?!.,;:")
            a = re.sub(ART, "", a).strip()
            if not a: continue
            w = toks(a)
            if len(w) >= 2: KEYS.append(("multi", " ".join(w), p["id"], n["n"], z, len(w)))
            elif len(w) == 1 and len(w[0]) > 2 and z < 6.2: KEYS.append(("mot", w[0], p["id"], n["n"], z, 1))
multi = [k for k in KEYS if k[0] == "multi" and k[5] >= 2 and len(k[1]) > 6]
mots = collections.defaultdict(list)
for k in KEYS:
    if k[0] == "mot":
        mots[k[1]].append(k)
PH = json.load(open(f"{S}/anki/phrases.json"))
out, nomatch = [], 0
for x in PH:
    fr = x["f"]["français"].strip(); t = toks(fr); txt = " " + " ".join(t) + " "
    cands = []
    for k in multi:
        if " " + k[1] + " " in txt: cands.append((-(k[4] - 0.3 * (k[5] - 1)), k))
    lem = {lemme(w) for w in t}
    for l in lem:
        for k in mots.get(l, []): cands.append((-k[4], k))
    if not cands: nomatch += 1; continue
    cands.sort(key=lambda c: c[0], reverse=True)
    k = cands[0][1]
    out.append({"id": x["id"], "fr": fr, "it": x["f"].get("italien", "").strip(), "en": x["f"].get("anglais", "").strip(),
                "pid": k[2], "n": k[3], "cle": k[1]})
json.dump(out, open("/home/claude/pm_italien/phrases/assoc.json", "w"), ensure_ascii=False, indent=0)
c = collections.Counter((o["pid"], o["n"]) for o in out)
print("rattachées", len(out), "sans niche", nomatch, "niches touchées", len(c), "max par niche", c.most_common(5))
