"""Scores Zipf réels par niche, au niveau du lemme.
FR : Lexique 3.83 (freqlemlivres = écrit, freqlemfilms2 = films), OpenSubtitles 2018 (sous-titres films et séries),
     wordfreq (mélange : Wikipédia, sous-titres, actualités, livres, web, réseaux sociaux).
IT : itWaC (web écrit, lemmes de noms), OpenSubtitles 2018, wordfreq.
Formes homographes (porte verbe, point négation, ora adverbe…) : part « nom » estimée par Lexique (FR) ou itWaC (IT)."""
import csv, json, math, sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad")
from mp import load
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
z = lambda pm: round(math.log10(pm) + 3, 2) if pm > 0 else None

# --- Lexique
LX = list(csv.DictReader(open(f"{S}/pl/Lexique383/Lexique383.tsv", encoding="utf-8"), delimiter="\t"))
lex_lem, form_nom, form_all, lem_forms = {}, {}, {}, {}
for r in LX:
    o = r["ortho"]; f = float(r["freqfilms2"]) + float(r["freqlivres"])
    form_all[o] = form_all.get(o, 0) + f
    if r["cgram"] == "NOM":
        form_nom[o] = form_nom.get(o, 0) + f
        lex_lem.setdefault(r["lemme"], (float(r["freqlemlivres"]), float(r["freqlemfilms2"])))
        lem_forms.setdefault(r["lemme"], set()).add(o)
share_fr = lambda o: min(1, form_nom.get(o, 0) / form_all[o]) if form_all.get(o) else 1

# --- OpenSubtitles
def osub(lang):
    c, tot = {}, 0
    for line in open(f"{S}/fw/repo/content/2018/{lang}/{lang}_full.txt", encoding="utf-8"):
        w, n = line.rsplit(" ", 1); n = int(n); tot += n
        c[w] = n
    return {w: n / tot * 1e6 for w, n in c.items()}
OS_FR, OS_IT = osub("fr"), osub("it")
_, WF_FR = load(f"{S}/wf/wordfreq/data/large_fr.msgpack.gz")
_, WF_IT = load(f"{S}/wf/wordfreq/data/large_it.msgpack.gz")
wfpm = lambda W, w: 10 ** (W[w] - 3) if w in W else 0

# --- itWaC noms
IW_form, IW_lem = {}, {}
for r in csv.DictReader(open(f"{S}/ita/itwac_nouns_lemmas_notail_2_0_0.csv", encoding="latin-1")):
    pm = float(r["fpmw"]); IW_form[r["Form"]] = IW_form.get(r["Form"], 0) + pm
    d_ = IW_lem.setdefault(r["lemma"], {}); d_[r["Form"]] = d_.get(r["Form"], 0) + pm
# Calibrage itWaC / wordfreq sur des noms sans homographe, pour isoler la part « nom » des formes ambiguës
_ref = ["casa", "acqua", "città", "famiglia", "macchina", "settimana", "libro", "scuola", "mamma", "guerra",
        "amore", "testa", "polizia", "storia", "idea", "fratello", "sorella", "telefono", "dottore", "mattina"]
_r = sorted(IW_form[w] / wfpm(WF_IT, w) for w in _ref)
CAL_IT = _r[len(_r) // 2]
share_it = lambda o: min(1, IW_form.get(o, 0) / (CAL_IT * wfpm(WF_IT, o))) if wfpm(WF_IT, o) else 1

def scores_fr(lemmes):
    livres = films = os_ = wf = 0
    for L in lemmes:
        l, f = lex_lem[L]; livres += l; films += f
        for o in lem_forms[L]:
            s = share_fr(o); os_ += OS_FR.get(o, 0) * s; wf += wfpm(WF_FR, o) * s
    return {"ecrit": z(livres), "films": z(films), "soustitres": z(os_), "global": z(wf),
            "parle": round((z(films) + z(os_)) / 2, 2)}

def scores_it(lemme):
    forms = IW_lem.get(lemme)
    if not forms: return None
    ecr = sum(forms.values()); os_ = wf = 0
    for o in forms:
        s = share_it(o); os_ += OS_IT.get(o, 0) * s; wf += wfpm(WF_IT, o) * s
    return {"ecrit": z(ecr), "parle": z(os_), "global": z(wf)}

if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(a, scores_fr(a.split("+")) if a in lex_lem or "+" in a else scores_it(a))
