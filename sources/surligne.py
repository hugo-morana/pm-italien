"""Repère dans chaque phrase d'exemple la forme du mot étudié (FR et IT)."""
import json, re, sys, csv
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))
fr_forms, it_forms = {}, {}
for r in csv.DictReader(open(f"{S}/pl/Lexique383/Lexique383.tsv", encoding="utf-8"), delimiter="\t"):
    if r["cgram"] == "NOM": fr_forms.setdefault(r["lemme"], set()).add(r["ortho"])
for r in csv.DictReader(open(f"{S}/ita/itwac_nouns_lemmas_notail_2_0_0.csv", encoding="latin-1")):
    it_forms.setdefault(r["lemma"], set()).add(r["Form"])
# formes manquantes ou irrégulières, ajoutées à la main
EXTRA_FR = {"oeil": {"œil", "yeux"}, "coeur": {"cœur"}, "dieu": {"Dieu"}}
TOK = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœ]+")
def trouve(phrase, formes):
    fl = {f.lower() for f in formes}
    for m in TOK.finditer(phrase):
        if m.group(0).lower() in fl: return m.group(0)
    return None
manq = []
for r in d["pieces"][0]["niches"]:
    ff = set().union(*(fr_forms.get(k, set()) | EXTRA_FR.get(k, set()) for k in r["lex"]))
    fi = it_forms.get(r["lemme_it"], set()) | {r["lemme_it"]}
    r["exemple_fr_mot"] = trouve(r["exemple_fr"], ff)
    r["exemple_cible_mot"] = trouve(r["exemple_cible"], fi)
    if not r["exemple_fr_mot"] or not r["exemple_cible_mot"]:
        manq.append((r["n"], r["fr"], r["exemple_fr"], r["exemple_fr_mot"], r["exemple_cible"], r["exemple_cible_mot"]))
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
for m in manq: print(m)
print(len(manq), "à revoir")
