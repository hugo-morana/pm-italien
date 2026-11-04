"""stt_extract.py fichier_resultat k [k2 ...] : extrait les transcriptions (dans l'ordre des sessions) vers raw/wordsKKK.json"""
import json, sys
s = open(sys.argv[1]).read()
try: d = json.loads(s)
except Exception:
    d = json.loads(s[s.index("{"):])
if isinstance(d, list): d = json.loads(d[0]["text"])
tr = d.get("transcripts", [])
print("statut", d.get("all_completed"), "transcriptions", len(tr))
gid = [g["id"] for g in d.get("generations", [])]
import difflib
from align_stt import norm
L = json.load(open("lots.json")); cand = [int(x) for x in sys.argv[2:]]
def best(t):
    tx = norm(t["text"][:300]); return max(cand, key=lambda k: difflib.SequenceMatcher(None, tx, norm(" ".join(L[k])[:300])).ratio())
for t in tr:
    k = best(t)
    import subprocess
    out = f"raw/words{int(k):03d}.json"
    subprocess.run(["curl", "-s", "-o", out, t["words_download_url"]], check=True)
    w = json.load(open(out)); w = w if isinstance(w, dict) else {"words": w}; json.dump(w, open(out, "w"), ensure_ascii=False)
    print(k, len(w["words"]), "mots ; fin", w["words"][-1]["end"])
