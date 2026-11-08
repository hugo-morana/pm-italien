import json, sys, re
L = json.load(open("/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/lots.json"))
for k in map(int, sys.argv[1:]):
    l = L[k]; open(f"/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/p{k:03d}.txt", "w").write(("[slowly] " if k >= 165 else "") + " [pause] ".join(re.sub(r"([.!?…»])\.$", r"\1", t) for t in l["T"]))
    print(k, l["L"], len(l["T"]))
