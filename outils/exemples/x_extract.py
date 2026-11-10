"""x_extract.py fichier L:k [L:k ...] : comme stt_extract, candidats répartis entre aud_fr et aud_it."""
import json, sys, difflib, subprocess, sys as _s
_s.path.insert(0, "aud_fr"); from align_stt import norm
s = open(sys.argv[1]).read()
try: d = json.loads(s)
except Exception: d = json.loads(s[s.index("{"):])
if isinstance(d, list): d = json.loads(d[0]["text"])
tr = d.get("transcripts", []); print("statut", d.get("all_completed"), "transcriptions", len(tr))
cand = [(c.split(":")[0], int(c.split(":")[1])) for c in sys.argv[2:]]
L = {l: json.load(open(f"aud_{l}/lots.json")) for l in ("fr", "it")}
import os
ORDER = os.environ.get("ORDER")   # ORDER=1 : transcriptions dans l'ordre des sessions données
for i, t in enumerate(tr):
    tx = norm(t["text"][:300])
    if ORDER: l, k = cand[i]
    else: l, k = max(cand, key=lambda c: difflib.SequenceMatcher(None, tx, norm(" ".join(L[c[0]][c[1]])[:300])).ratio())
    r = difflib.SequenceMatcher(None, tx, norm(" ".join(L[l][k])[:300])).ratio()
    if r < 0.5: print("  ! correspondance faible", l, k, round(r, 2))
    out = f"aud_{l}/raw/words{k:03d}.json"
    subprocess.run(["curl", "-s", "-o", out, t["words_download_url"]], check=True)
    w = json.load(open(out)); w = w if isinstance(w, dict) else {"words": w}; json.dump(w, open(out, "w"), ensure_ascii=False)
    print(l, k, len(w["words"]), "mots ; fin", w["words"][-1]["end"])
