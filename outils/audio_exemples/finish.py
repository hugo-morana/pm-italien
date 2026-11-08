"""Après normpacks : correction efr, paquets d'exemples (apply_ex), contrôle du niveau sur un échantillon."""
import json, subprocess, random, sys
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"; P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P)); byid = {r["id"]: r for r in D["rooms"]}
for f in json.load(open(S + "fix_after_norm.json")):
    x = byid[f["room"]]["niches"][f["n"]]
    if x and x["fr"] == f["fr"]: x["efr"], x["efm"] = f["efr"], f["efm"]; print("fix", f["room"], f["n"])
    else:
        for r in D["rooms"]:
            for y in r["niches"]:
                if y and y["fr"] == f["fr"] and "Tous dehors" in (y.get("efr") or ""): y["efr"], y["efm"] = f["efr"], f["efm"]; print("fix (déplacée)", r["id"])
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
subprocess.run(["python3", S + "apply_ex.py"], check=True)
sys.path.insert(0, S); import loud
D = json.load(open(P)); refs = [x[f] for r in D["rooms"] for x in r["niches"] if x for f in ("af", "ai", "ae", "ap") if isinstance(x.get(f), list)]
random.seed(3); vals = []
for p, o, l in random.sample(refs, 60):
    b = open("/home/claude/pm_italien/pm3d/" + D["packs"][p].split("?")[0], "rb").read()[o:o + l]; open(S + "chk.mp3", "wb").write(b); vals.append(loud.lufs(S + "chk.mp3"))
vals.sort(); print("LUFS échantillon : min", vals[0], "médiane", vals[30], "max", vals[-1])
