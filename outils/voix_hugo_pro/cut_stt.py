"""Découpe un lot à partir de la transcription horodatée. Usage : cut_stt.py k [URL_audio] [URL_words] (préfixe de fichier selon PREFIX)."""
import json, sys, hashlib, subprocess, os
from align_stt import bounds
PREFIX = os.environ.get("PREFIX", "hf_")
k = int(sys.argv[1]); f = f"raw/lot{k:03d}.mp3"; wf = f"raw/words{k:03d}.json"
ENC = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/aud/enc"
if len(sys.argv) > 2 and sys.argv[2] != "-": subprocess.run(["curl", "-s", "-o", f, sys.argv[2]], check=True)
if len(sys.argv) > 3: subprocess.run(["curl", "-s", "-o", wf, sys.argv[3]], check=True)
T = json.load(open("lots.json"))[k]; W = json.load(open(wf))["words"]
B = bounds(T, W)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
M = json.load(open("hp_map.json")); D = set(json.load(open("done_v4.json"))); bad = []
for i, t in enumerate(T):
    b = B[i]
    prev_end = B[i - 1][1] if i and B[i - 1] else 0; next_start = B[i + 1][0] if i + 1 < len(T) and B[i + 1] else dur
    if not b or (b[2] < 0.6 and not (prev_end <= b[0] + 0.01 and b[1] <= next_start + 0.01)) or b[1] - b[0] > 6: bad.append((i, t, b)); continue
    a = max(b[0] - 0.10, (prev_end + b[0]) / 2); e = min(b[1] + 0.15, (b[1] + next_start) / 2)
    d = e - a; fn = PREFIX + hashlib.sha1(t.encode()).hexdigest()[:16] + ".mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.2f}", "-to", f"{e:.2f}", "-i", f, "-af", "afade=t=out:st=%.2f:d=0.04" % max(0, d - 0.04),
                    "-ac", "1", "-ar", "22050", "-b:a", "40k", "-f", "mp3", f"{ENC}/{fn}"], check=True)
    M[t] = fn; D.add(t)
json.dump(M, open("hp_map.json", "w"), ensure_ascii=False); json.dump(sorted(D), open("done_v4.json", "w"), ensure_ascii=False)
print(f"lot {k} : {len(T) - len(bad)}/{len(T)} clips ; total {len(D)}" + (f" ; à revoir : {bad}" if bad else ""))
