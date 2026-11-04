"""Rattache les enregistrements ElevenLabs « Hugo Pro » (scratchpad el/hp_map.json : texte lu → fichier) aux niches sans son italien Anki."""
import json, re
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad"
M = json.load(open(f"{S}/el/hp_map.json")); P = "/home/claude/pm_italien/data_italien.json"; d = json.load(open(P))
D3 = json.load(open("/home/claude/pm_italien/pm3d/data3d.json")); K = json.load(open(f"{S}/el/mots_it.json"))["cles"]
pos = {}
for t, keys in K.items():
    for k in keys: pos[k] = t
# clés data3d (salle:n) → texte ; même numérotation que data_italien (ordre TOUR, mêmes ids)
k = 0
for p in d["pieces"]:
    for n in p["niches"]:
        if n.get("libre"): continue
        t = pos.get(f"{p['id']}:{n['n']}")
        if t and t in M: n["audio_hp"] = {"it": M[t]}; k += 1
        elif "audio_hp" in n and not (t and t in M): pass
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1); print("niches avec la voix Hugo Pro :", k)
