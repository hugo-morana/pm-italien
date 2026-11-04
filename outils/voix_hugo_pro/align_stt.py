"""Bornes de chaque texte d'un lot à partir des mots horodatés de la transcription (Scribe).
Alignement caractère par caractère (lettres seules) entre textes attendus et transcription."""
import json, re, unicodedata, difflib
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)
def bounds(texts, words):
    W = [w for w in words if w.get("type") == "word" and norm(w["text"])]
    # chaîne transcription + index du mot pour chaque caractère
    ts, ti = "", []
    for i, w in enumerate(W): n = norm(w["text"]); ts += n; ti += [i] * len(n)
    es, ei = "", []
    for k, t in enumerate(texts): n = norm(t) or "x"; es += n; ei += [k] * len(n)
    sm = difflib.SequenceMatcher(None, es, ts, autojunk=False)
    m = {}
    for a, b, n in sm.get_matching_blocks():
        for j in range(n): m[a + j] = b + j
    first, last = [None] * len(texts), [None] * len(texts)
    for a, b in m.items():
        k, wi = ei[a], ti[b]
        first[k] = wi if first[k] is None else min(first[k], wi); last[k] = wi if last[k] is None else max(last[k], wi)
    cov = [sum(1 for a in m if ei[a] == k) / max(1, ei.count(k)) for k in range(len(texts))]
    out = []
    for k in range(len(texts)):
        if first[k] is None: out.append(None); continue
        out.append((W[first[k]]["start"], W[last[k]]["end"], cov[k]))
    return out
