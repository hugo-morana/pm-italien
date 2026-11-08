"""Recopie lots.json (global) en aud_fr/lots.json et aud_it/lots.json indexés par numéro de lot, et relie les fichiers bruts."""
import json, os
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"
L = json.load(open(S + "lots.json"))
for lg in ("fr", "it"):
    json.dump([l["T"] if l["L"] == lg else [] for l in L], open(S + f"aud_{lg}/lots.json", "w"), ensure_ascii=False)
    for l in L:
        src = S + f"raw/lot{l['id']:03d}.mp3"; dst = S + f"aud_{lg}/raw/lot{l['id']:03d}.mp3"
        if l["L"] == lg and os.path.exists(src) and not os.path.exists(dst): os.symlink(src, dst)
