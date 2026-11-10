"""Inventaire des phrases d'exemple italiennes : mots (lemme + classe) et patron syntaxique."""
import json, re, collections, spacy, pickle
from wordfreq import zipf_frequency
nlp = spacy.load("it_core_news_lg")
S = json.load(open("sents.json"))
D = json.load(open("/home/claude/pm_italien/pm3d/data3d.json"))

POSFR = {"NOUN": "nom", "VERB": "verbe", "AUX": "verbe (auxiliaire)", "ADJ": "adjectif", "ADV": "adverbe",
         "ADP": "préposition", "CCONJ": "conjonction de coordination", "SCONJ": "conjonction de subordination",
         "PRON": "pronom", "DET": "déterminant", "NUM": "numéral", "INTJ": "interjection", "PROPN": "nom propre"}

def low1(s): return s[:1].lower() + s[1:]

# ---------- bibliothèque : lemmes présents ----------
def clean_it(t):
    t = re.sub(r"\([^)]*\)", " ", t)
    t = re.sub(r"\b(qcn|qcs)\b( altro)?", " ", t)
    return re.sub(r"\s+", " ", t).strip(" !?.,;:…")

lib = collections.defaultdict(set)          # lemme -> {room:slot}
libform = collections.defaultdict(set)      # forme exacte (minuscule) -> {room:slot}
docs = list(nlp.pipe([clean_it(x["it"]) for r in D["rooms"] for x in r["niches"] if x], batch_size=256))
k = 0
for r in D["rooms"]:
    for i, x in enumerate(r["niches"]):
        if not x: continue
        d = docs[k]; k += 1
        key = f"{r['id']}:{i}"
        for t in d:
            if t.is_punct: continue
            lib[low1(t.lemma_).lower()].add(key); libform[t.text.lower()].add(key)
        # formes déclarées
        for f in re.split(r"[,;/]| pl\. | f\. ", x.get("fo") or ""):
            f = f.strip().lower()
            if f and len(f.split()) <= 2: libform[f.split()[-1]].add(key)

# ---------- patron d'une phrase ----------
SUBJ = {"nsubj", "nsubj:pass", "csubj"}
def clause_sig(v, d):
    """Signature d'une proposition dont la tête est v."""
    ch = list(v.children)
    deps = {c.dep_ for c in ch}
    parts = []
    cop = [c for c in ch if c.dep_ == "cop"]
    neg = any(c.dep_ == "advmod" and c.lemma_ in ("non",) for c in ch)
    subj = any(c.dep_ in SUBJ for c in ch) or (v.morph.get("Person") and v.morph.get("Mood") != ["Imp"])
    mood = (v.morph.get("Mood") or [""])[0]
    vf = (v.morph.get("VerbForm") or [""])[0]
    if mood == "Imp": parts.append("impératif")
    if any(c.dep_ in ("expl", "expl:impers") and c.lower_ == "si" for c in ch): parts.append("si impersonnel")
    if "nsubj:pass" in deps or any(c.dep_ == "aux:pass" for c in ch): parts.append("passif")
    if neg: parts.append("négation")
    if cop:
        base = "être + adjectif" if v.pos_ == "ADJ" else ("être + nom" if v.pos_ in ("NOUN", "PROPN", "PRON") else "être + complément")
    elif v.pos_ in ("VERB", "AUX"):
        if "obj" in deps and "iobj" in deps: base = "verbe + COD + COI"
        elif "obj" in deps: base = "verbe + COD"
        elif "iobj" in deps: base = "verbe + COI"
        elif "obl" in deps: base = "verbe + complément prépositionnel"
        else: base = "verbe seul"
        if any(c.dep_ == "aux" and c.lemma_ in ("stare",) for c in ch) and vf == "Ger": base = "stare + gérondif"
        if any(c.dep_ == "xcomp" for c in ch):
            x = next(c for c in ch if c.dep_ == "xcomp")
            m = [c.lower_ for c in x.children if c.dep_ == "mark"]
            if x.pos_ in ("VERB", "AUX") and (x.morph.get("VerbForm") or [""])[0] == "Inf":
                base = f"verbe + {m[0]} + infinitif" if m else ("modal/verbe + infinitif")
            else: base = "verbe + attribut"
        if any(c.dep_ == "aux" and c.lemma_ in ("potere", "dovere", "volere", "sapere") for c in ch) and vf == "Inf":
            base = "modal + infinitif"
        if any(c.lemma_ == "fare" and c.dep_ == "aux" for c in ch) and vf == "Inf": base = "fare + infinitif (causatif)"
    else:
        base = "phrase nominale"
    if not subj and mood != "Imp" and cop == [] and v.pos_ in ("VERB", "AUX") and vf == "Fin": parts.append("sujet implicite")
    return base, parts

def pattern(d):
    roots = [t for t in d if t.dep_ == "ROOT"]
    if not roots: return "fragment", []
    root = roots[0]
    feats = []
    text = d.text.strip()
    if text.endswith("?"):
        wh = [t for t in d if t.lower_ in ("chi", "che", "cosa", "dove", "quando", "come", "perché", "quanto", "quanta", "quanti", "quante", "quale", "quali") and t.i <= root.i + 1 and t.i < 3]
        feats.append(f"question ({wh[0].lower_}…)" if wh else "question oui/non")
    elif text.endswith("!") and (root.morph.get("Mood") or [""])[0] != "Imp": feats.append("exclamation")
    if root.pos_ in ("VERB", "AUX", "ADJ", "NOUN", "PRON", "PROPN", "ADV") and any(c.dep_ in ("cop",) for c in root.children) or root.pos_ in ("VERB", "AUX"):
        base, parts = clause_sig(root, d)
    else:
        base, parts = "phrase nominale", []
    feats += parts
    sub = []
    for t in d:
        if t.dep_ in ("ccomp", "csubj"):
            m = [c.lower_ for c in t.children if c.dep_ == "mark"]
            mood = (t.morph.get("Mood") or [""])[0]
            if (t.morph.get("VerbForm") or [""])[0] == "Inf": sub.append(f"complétive {m[0] if m else ''} + infinitif".replace("  ", " "))
            else: sub.append(f"complétive {m[0] if m else '(sans che)'} + {'subjonctif' if mood == 'Sub' else 'indicatif/conditionnel'}")
        elif t.dep_ == "advcl":
            m = [c for c in t.children if c.dep_ == "mark"]
            mk = " ".join(c.lower_ for c in m) if m else ""
            vf = (t.morph.get("VerbForm") or [""])[0]; mood = (t.morph.get("Mood") or [""])[0]
            if vf == "Ger": sub.append("circonstancielle au gérondif")
            elif vf == "Inf": sub.append(f"circonstancielle {mk} + infinitif")
            elif vf == "Part": sub.append("circonstancielle au participe")
            else: sub.append(f"circonstancielle {mk or '(sans conjonction)'} + {'subjonctif' if mood == 'Sub' else 'indicatif/conditionnel'}")
        elif t.dep_ == "acl:relcl":
            rel = [c.lower_ for c in t.subtree if c.tag_ in ("PR",) or c.lower_ in ("che", "cui", "dove", "quale", "quali", "chi")]
            sub.append(f"relative ({rel[0] if rel else 'che'})")
        elif t.dep_ == "acl" and (t.morph.get("VerbForm") or [""])[0] == "Inf": sub.append("nom + di/da + infinitif")
        elif t.dep_ == "conj" and t.head == root and t.pos_ in ("VERB", "AUX"):
            cc = [c.lower_ for c in t.children if c.dep_ == "cc"]
            sub.append(f"coordination ({cc[0] if cc else 'juxtaposition'})")
        elif t.dep_ == "parataxis" and t.head == root: sub.append("juxtaposition")
        elif t.dep_ in ("dislocated",): sub.append("dislocation")
    if any(t.lower_ in ("più", "meno") for t in d) and any(t.lower_ in ("di", "che", "del", "della", "dei") for t in d): sub.append("comparatif")
    sub = sorted(set(sub))
    key = " ; ".join([base] + feats + sub)
    return key, [base] + feats + sub

udocs = {}
uniq = sorted({s["eit"] for s in S})
for t, d in zip(uniq, nlp.pipe(uniq, batch_size=256)): udocs[t] = d

items = collections.defaultdict(lambda: {"n": 0, "pos": collections.Counter(), "forms": collections.Counter(), "ex": []})
rows = []; pats = collections.defaultdict(lambda: {"n": 0, "ex": []})
for s in S:
    d = udocs[s["eit"]]
    key, comps = pattern(d)
    words = []
    for t in d:
        if t.is_punct or t.is_space or t.like_num or t.pos_ in ("SYM", "X", "SPACE", "PUNCT"): continue
        lem = low1(t.lemma_).lower() if t.pos_ != "PROPN" else t.lemma_
        pos = t.pos_
        words.append(f"{lem} ({POSFR.get(pos, pos)})")
        it = items[(lem, pos)]; it["n"] += 1; it["forms"][t.text] += 1
        if len(it["ex"]) < 3 and s["eit"] not in it["ex"]: it["ex"].append(s["eit"])
    p = pats[key]; p["n"] += 1
    if len(p["ex"]) < 3: p["ex"].append(s["eit"])
    p["comps"] = comps
    rows.append(dict(s, pat=key, words=words))

pickle.dump(dict(rows=rows, items={k: dict(v) for k, v in items.items()}, pats=dict(pats),
                 lib={k: sorted(v) for k, v in lib.items()}, libform={k: sorted(v) for k, v in libform.items()}),
            open("inv.pkl", "wb"))
print("phrases", len(rows), "items", len(items), "patrons", len(pats))
