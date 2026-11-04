"""Lot v4 : télécharge (si besoin), découpe par programmation dynamique (dp.py), encode, met à jour hp_map.json. Usage : cut_energy.py k [URL]"""
import json, sys, hashlib, subprocess, os
from cut import load
from dp import segment
k = int(sys.argv[1]); f = f"raw/lot{k:03d}.mp3"
ENC = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/aud/enc"
if len(sys.argv) > 2: subprocess.run(["curl", "-s", "-o", f, sys.argv[2]], check=True)
T = json.load(open("lots.json"))[k]; db = load(f); nf = len(db)
S, rmin, rmax = segment(db, T)
if rmin < 0.3 or rmax > 2.2: print(f"lot {k} : découpage douteux ({rmin:.2f}–{rmax:.2f}) — rien écrit"); sys.exit(1)
M = json.load(open("hp_map.json")); D = set(json.load(open("done_v4.json")))
for t, (a, b) in zip(T, S):
    a2, b2 = max(0, a - 5), min(nf, b + 12); dur = (b2 - a2) / 100
    fn = "hp_" + hashlib.sha1(t.encode()).hexdigest()[:16] + ".mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a2 / 100:.2f}", "-to", f"{b2 / 100:.2f}", "-i", f, "-af", "afade=t=out:st=%.2f:d=0.04" % max(0, dur - 0.04),
                    "-ac", "1", "-ar", "22050", "-b:a", "40k", "-f", "mp3", f"{ENC}/{fn}"], check=True)
    M[t] = fn; D.add(t)
json.dump(M, open("hp_map.json", "w"), ensure_ascii=False); json.dump(sorted(D), open("done_v4.json", "w"), ensure_ascii=False)
print(f"lot {k} : {len(T)} clips ({rmin:.2f}–{rmax:.2f}) ; total v4 {len(D)}")
