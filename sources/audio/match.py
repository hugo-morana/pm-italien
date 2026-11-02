"""Associe aux niches et aux phrases les sons Anki (français son / italien son). Écrit audio/match.json."""
import sqlite3, re, json, collections, html
A = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/anki"
names = json.load(open(f"{A}/media_names.json")); idx = {n: i for i, n in enumerate(names)}
c = sqlite3.connect(f"{A}/col.db"); c.create_collation("unicase", lambda a, b: (a.lower() > b.lower()) - (a.lower() < b.lower()))
F = collections.defaultdict(dict)
for nt, o, nm in c.execute("select ntid,ord,name from fields"): F[nt][o] = nm
def clean(v): v = re.sub(r"\[sound:[^\]]+\]", "", v); v = re.sub(r"<br\s*/?>|</div>", " ", v); v = re.sub(r"<[^>]+>", "", v); return re.sub(r"\s+", " ", html.unescape(v)).strip()
NOTE = {}
for nid, mid, flds in c.execute("select id,mid,flds from notes"):
    f = {F[mid].get(i, "?"): v for i, v in enumerate(flds.split("\x1f"))}
    snd = lambda k: [s for s in re.findall(r"\[sound:([^\]]+)\]", f.get(k, "")) if s in idx]
    itv = [clean(x) for x in re.split(r"<br\s*/?>|</div>|<div>", f.get("italien", ""))]
    itv = [x for x in itv if x]
    NOTE[nid] = {"fr": clean(f.get("français", "")), "it": clean(f.get("italien", "")), "itv": itv, "sfr": snd("français son"), "sit": snd("italien son")}
PH = r"\b(C\d?(lieu|adj|date|langue|heure|nationalité|nb|qn|âge|mois/saison|marque|pronom|temps|moment)?|S\d?|V\d?(inf|pp|imp|sub|sbj|op|fut|ant|cond|p|ps3|ing)?|SV|SVC|COS2)\b(?![’'])"
lab = lambda s: re.sub(r"…(\s*…)+", "…", re.sub(r"\s+", " ", re.sub(PH, "…", s))).strip()
norm = lambda s: re.sub(r"[^\w…]+", " ", s.replace("’", "'").lower()).strip()
BYFR = collections.defaultdict(list)
for nid, n in NOTE.items():
    if n["fr"]: BYFR[norm(lab(n["fr"]))].append(nid); BYFR[norm(n["fr"])].append(nid)
itnorm = lambda s: norm(re.sub(r"\(.*?\)", "", lab(s).split(" / ")[0]))
D = json.load(open("/home/claude/pm_italien/data_italien.json"))
out = {"niches": {}, "phrases": {}}; st = collections.Counter()
for p in D["pieces"]:
    for n in p["niches"]:
        if n.get("libre"): continue
        cand = []
        for k in {norm(n["fr"]), norm(n.get("texte_source") or ""), norm(lab(n.get("texte_source") or ""))}:
            if k: cand += BYFR.get(k, [])
        cand = [x for x in dict.fromkeys(cand)]
        sfr = next((NOTE[x]["sfr"][0] for x in cand if NOTE[x]["sfr"]), None)
        sit = None
        for x in cand:   # son italien seulement si le texte italien d'Anki est celui de la niche
            nv = [itnorm(v) for v in [NOTE[x]["it"]] + NOTE[x]["itv"][:1]] + [itnorm(re.split(r"\s+(?=[a-zàèéìòù']+ …)|\(", NOTE[x]["it"])[0])]
            if NOTE[x]["sit"] and any(v and v in (itnorm(n["cible"]), itnorm(n["cible"].split(" / ")[0])) for v in nv):
                sit = NOTE[x]["sit"][0]; break
        key = f'{p["id"]}:{n["n"]}'
        if sfr or sit: out["niches"][key] = {"fr": sfr, "it": sit}
        st["niche_fr"] += bool(sfr); st["niche_it"] += bool(sit); st["niches"] += 1
        for k, e in enumerate(n.get("phrases") or []):
            no = NOTE.get(e.get("anki_id"))
            if not no: continue
            s1 = no["sfr"][0] if no["sfr"] else None
            s2 = no["sit"][0] if no["sit"] and norm(no["it"]) == norm(e["it"]) else None
            if s1 or s2: out["phrases"][f"{key}:{k}"] = {"fr": s1, "it": s2}
            st["ph_fr"] += bool(s1); st["ph_it"] += bool(s2); st["phrases"] += 1
json.dump(out, open("/home/claude/pm_italien/audio/match.json", "w"), ensure_ascii=False)
print(dict(st)); print("fichiers distincts", len({v for d in out.values() for x in d.values() for v in x.values() if v}))
if __name__ == "__main__" and len(__import__("sys").argv) > 1:
    k = 0
    for p in D["pieces"]:
        for n in p["niches"]:
            if n.get("libre"): continue
            cand = [x for kk in {norm(n["fr"]), norm(n.get("texte_source") or "")} if kk for x in BYFR.get(kk, [])]
            for x in cand:
                if NOTE[x]["sit"] and f'{p["id"]}:{n["n"]}' not in out["niches"] or (NOTE[x]["sit"] and not out["niches"].get(f'{p["id"]}:{n["n"]}', {}).get("it")):
                    print(n["fr"], "|", n["cible"], "|| anki:", NOTE[x]["it"]); k += 1; break
            if k > 40: break
        if k > 40: break
