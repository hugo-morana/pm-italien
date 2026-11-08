"""harvest.py statut.txt : télécharge les audios terminés (raw/lotKKK.mp3) et les transcriptions (aud_L/raw/wordsKKK.json),
puis découpe (cut_stt) les lots qui ont les deux, et normalise le niveau des nouveaux clips."""
import json, sys, subprocess, os, glob, difflib, re
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"; os.chdir(S)
sys.path.insert(0, "aud_fr"); from align_stt import norm
F = sys.argv[1] if sys.argv[1] != "last" else max(glob.glob("/root/.claude/projects/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/tool-results/mcp-ElevenLabs-creative_get_flow_run_status-*.txt"), key=os.path.getmtime)
s = open(F).read(); d = json.loads(s); d = json.loads(d[0]["text"]) if isinstance(d, list) else d
L = json.load(open("lots.json"))
P = {k: open(f).read() for f in glob.glob("p[0-9][0-9][0-9].txt") for k in [int(f[1:4])]}
got = []
for g in d.get("generations", []):
    if g["modality"] != "audio" or g["status"] != "completed": continue
    ks = [k for k, p in P.items() if p.startswith(g["prompt"][:150])]
    if len(ks) != 1: print("? audio sans lot", g["prompt"][:50], ks); continue
    k = ks[0]; f = f"raw/lot{k:03d}.mp3"
    if not os.path.exists(f): subprocess.run(["curl", "-s", "-o", f, g["content_url"]], check=True); print("audio", k, g.get("duration_secs"))
for t in d.get("transcripts", []):
    tx = norm(re.sub(r"\[[a-z ]+\]", " ", t["text"])[:400])
    cand = [k for k in P if os.path.exists(f"raw/lot{k:03d}.mp3")]
    k = max(cand, key=lambda c: difflib.SequenceMatcher(None, tx, norm(" ".join(L[c]["T"]))[:len(tx) + 20]).ratio())
    r = difflib.SequenceMatcher(None, tx, norm(" ".join(L[k]["T"]))[:len(tx) + 20]).ratio()
    lg = L[k]["L"]; out = f"aud_{lg}/raw/words{k:03d}.json"
    if os.path.exists(out): continue
    if r < 0.6: print("! transcription douteuse", k, round(r, 2)); continue
    subprocess.run(["curl", "-s", "-o", out, t["words_download_url"]], check=True)
    w = json.load(open(out)); w = w if isinstance(w, dict) else {"words": w}; w["words"] = [x for x in w["words"] if not re.fullmatch(r"\[[a-z ]+\]", x["text"].strip())]; json.dump(w, open(out, "w"), ensure_ascii=False)
    print("mots", k, lg, len(w["words"]), round(r, 2)); got.append(k)
subprocess.run(["python3", "sync_lots.py"], check=True)
for k in got:
    lg = L[k]["L"]
    subprocess.run(f"cd aud_{lg} && PREFIX={('wf_' if lg == 'fr' else 'wi_') if k >= 163 else ('exf_' if lg == 'fr' else 'exi_')} python3 cut_stt.py {k}", shell=True, check=True)
subprocess.run(["python3", "normenc.py"], check=True)
