"""Retire les variables S V C des liens de chaîne (li), des équivalents anglais (fo) et des décryptages (de)."""
import json, re
P = "/home/claude/pm_italien/pm3d/data3d.json"; D = json.load(open(P))
TOK = re.compile(r"(?<![\w’'«])(?:S|V|C)\d?(?:_[a-zàéèâ]+)?(?![\w’'])")
clean = lambda s: s.replace(" …", "").replace("…", "").strip()
M = {}
for r in D["rooms"]:
    for x in r["niches"]:
        if x and "fro" in x: M[clean(x["fro"])] = clean(x["fr"])
keys = sorted(M, key=len, reverse=True)
GEN_FR = [(r"\bV_inf\b", "faire"), (r"\bV_pp\b", "fait"), (r"\bV_sub\b", "fasse"), (r"\bV\d?_[a-z]+\b", "faire"), (r"\bC\d?_lieu\b", "qqpart"), (r"\bC\d?_[a-zâé]+\b", "qc"),
          (r"(?<![\w’'«])S\d?(?![\w’'])", "qn"), (r"(?<![\w’'«])V\d?(?![\w’'])", "fait"), (r"(?<![\w’'«])C\d?(?![\w’'])", "qc")]
GEN_EN = [(r"\bVinf\b", "do"), (r"\bVpp\b", "done"), (r"\bVing\b", "doing"), (r"\bVsub\b", "do"), (r"\bV\d?_inf\b", "do"), (r"\bV\d?_pp\b", "done"), (r"\bV\d?_ger\b", "doing"), (r"\bV\d?_[a-z]+\b", "do"),
          (r"\bC\d?_lieu\b", "somewhere"), (r"\bC2\b", "sb"), (r"\bC\d?_[a-zâé]+\b", "sth"), (r"(?<![\w’'«])S\d?(?![\w’'])", "sb"), (r"(?<![\w’'«])V\d?(?![\w’'])", "does"), (r"(?<![\w’'«])C\d?(?![\w’'])", "sth")]
def gen(s, rules):
    for a, b in rules: s = re.sub(a, b, s)
    return s
n = {"li": 0, "fo": 0, "de": 0}
for r in D["rooms"]:
    for x in r["niches"]:
        if not x: continue
        li = x.get("li") or ""
        if TOK.search(li):
            for k in keys:
                if TOK.search(k) and k in li: li = li.replace(k, M[k])
            x["li"] = gen(li, GEN_FR); n["li"] += 1
        fo = x.get("fo") or ""
        if TOK.search(fo) or re.search(r"\bV(inf|pp|ing|sub)\b", fo):
            if fo.startswith("anglais"): x["fo"] = gen(fo, GEN_EN)
            else: x["fo"] = gen(fo, GEN_FR)
            n["fo"] += 1
        de = x.get("de") or ""
        if TOK.search(de): x["de"] = de.replace("S = sujet", "qcn = qualcuno"); n["de"] += 1
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print(n)
left = [(f, x[f]) for r in D["rooms"] for x in r["niches"] if x for f in ("li", "fo", "de") if TOK.search(x.get(f) or "")]
print("restants", len(left), left[:5])
