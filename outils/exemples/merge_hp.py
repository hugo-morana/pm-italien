"""Ajoute au hp.json (texte -> clip) les clips découpés par transcription."""
import json
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"
M = json.load(open(S + "hp.json"))
for lg in ("fr", "it"): M[lg].update(json.load(open(S + f"aud_{lg}/hp_map.json")))
json.dump(M, open(S + "hp.json", "w"), ensure_ascii=False); print({k: len(v) for k, v in M.items()})
