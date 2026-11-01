"""Fréquences Zipf génériques, toutes classes de mots, au niveau du lemme.
FR : Lexique 3.83 (livres = écrit, films), OpenSubtitles 2018 (sous-titres), wordfreq (mixte) ; parlé = moyenne films + sous-titres.
IT : itWaC (écrit, lemmes N/ADJ/V), OpenSubtitles 2018 (parlé), wordfreq (mixte).
Formes ambiguës : on ne compte que la part de la forme qui relève de la classe visée."""
import csv, math, sys
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
sys.path.insert(0, S)
from mp import load
z = lambda pm: round(math.log10(pm) + 3, 2) if pm and pm > 0 else None

LX = list(csv.DictReader(open(f"{S}/pl/Lexique383/Lexique383.tsv", encoding="utf-8"), delimiter="\t"))
FORM_ALL = {}
for r in LX:
    FORM_ALL[r["ortho"]] = FORM_ALL.get(r["ortho"], 0) + float(r["freqfilms2"]) + float(r["freqlivres"])

def _osub(lang):
    c, tot = {}, 0
    for line in open(f"{S}/fw/repo/content/2018/{lang}/{lang}_full.txt", encoding="utf-8"):
        w, n = line.rsplit(" ", 1); n = int(n); tot += n; c[w] = n
    return {w: n / tot * 1e6 for w, n in c.items()}
OS = {"fr": _osub("fr"), "it": _osub("it")}
WF = {"fr": load(f"{S}/wf/wordfreq/data/large_fr.msgpack.gz")[1], "it": load(f"{S}/wf/wordfreq/data/large_it.msgpack.gz")[1]}
wfpm = lambda lg, w: 10 ** (WF[lg][w] - 3) if w in WF[lg] else 0

def fr(lemmes, cgrams, exclure=(), formes_seules=None):
    """lemmes : lemmes Lexique ; cgrams : classes (VER, AUX, ADJ, ADV, PRO:per…) ; exclure : formes à ignorer ;
    formes_seules : ne garder que ces formes (pour les mots-outils à une seule forme)."""
    livres = films = os_ = wf = 0
    for r in LX:
        if r["lemme"] not in lemmes or r["cgram"] not in cgrams: continue
        o = r["ortho"]
        if o in exclure or (formes_seules and o not in formes_seules): continue
        fl, ff = float(r["freqlivres"]), float(r["freqfilms2"])
        livres += fl; films += ff
        part = min(1, (fl + ff) / FORM_ALL[o]) if FORM_ALL.get(o) else 1
        os_ += OS["fr"].get(o, 0) * part; wf += wfpm("fr", o) * part
    if not films: return None
    return {"ecrit": z(livres), "films": z(films), "soustitres": z(os_), "global": z(wf),
            "parle": round((z(films) + z(os_ or films)) / 2, 2)}

# Formes italiennes ambiguës entre plusieurs classes : part estimée de l'emploi visé
PART_IT = {"sei": 0.75, "stato": 0.8, "fine": 0.3, "porta": 0.55, "parte": 0.35, "ora": 0.75, "volta": 0.1,
           "solo": 0.4, "piano": 0.4, "giusto": 0.6, "certo": 0.4, "bene": 0.0, "proprio": 0.3, "tanto": 0.3,
           "molto": 0.2, "poco": 0.3, "troppo": 0.3, "altro": 0.6, "vero": 0.7, "sicuro": 0.6, "forte": 0.6,
           "presto": 0.1, "dato": 0.6, "fatto": 0.7, "detto": 0.7, "visto": 0.6, "corso": 0.5, "posto": 0.2,
           "letto": 0.4, "conto": 0.4, "senti": 0.9, "vista": 0.4, "via": 0.1, "male": 0.3}
_IW = {}
def _itwac(cls):
    if cls in _IW: return _IW[cls]
    fn = {"N": "itwac_nouns_lemmas_notail_2_0_0.csv", "ADJ": "itwac_adj_lemmas_notail_2_1_0.csv",
          "V": "itwac_verbs_lemmas_notail_2_1_0.csv"}[cls]
    raw = open(f"{S}/ita/{fn}", "rb").read()
    try: txt = raw.decode("utf-8")
    except UnicodeDecodeError: txt = raw.decode("latin-1")
    form, lem = {}, {}
    for r in csv.DictReader(txt.splitlines()):
        pm = float(r["fpmw"]); f = r["Form"].lower()
        form[f] = form.get(f, 0) + pm
        dd = lem.setdefault(r["lemma"].lower(), {}); dd[f] = dd.get(f, 0) + pm
    ref = [w for w in sorted(form, key=lambda w: -form[w])[:400] if wfpm("it", w)]
    rat = sorted(form[w] / wfpm("it", w) for w in ref)
    cal = rat[int(len(rat) * 0.75)]  # calibrage : les formes non ambiguës sont dans le quart haut du rapport
    _IW[cls] = (form, lem, cal)
    return _IW[cls]

def it(lemme=None, cls=None, formes=None, part=None):
    """Avec cls (N/ADJ/V) : lemme itWaC, formes et part « classe » calibrées.
    Sans cls (mots-outils) : formes données ; part = dict facultatif de corrections manuelles."""
    part = part or {}
    if cls:
        form, lem, cal = _itwac(cls)
        fs = lem.get(lemme.lower())
        if not fs:  # lemme absent (comparatif rangé sous un autre lemme, mot étiqueté ailleurs) : formes données
            fs = {o: form.get(o, 0) for o in (formes or [lemme])}
        ecr = sum(fs.values()) or None; os_ = wf = 0
        for o in fs:
            if cls == "N": p = part.get(o, min(1, form[o] / (cal * wfpm("it", o))) if wfpm("it", o) else 1)
            else: p = part.get(o, PART_IT.get(o, 1))
            os_ += OS["it"].get(o, 0) * p; wf += wfpm("it", o) * p
        return {"ecrit": z(ecr), "parle": z(os_), "global": z(wf)}
    os_ = wf = 0
    for o in formes:
        p = part.get(o, 1); os_ += OS["it"].get(o, 0) * p; wf += wfpm("it", o) * p
    return {"ecrit": None, "parle": z(os_), "global": z(wf)}
