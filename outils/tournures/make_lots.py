"""Construit les textes parlés (abréviations développées) et les lots par langue."""
import json, re, glob
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/slots/"
out = [o for j in range(4) for o in json.load(open(S + f"out{j}.json"))]
def say(t, L):
    if L == "fr": t = re.sub(r"\bqqpart\b", "quelque part", t); t = re.sub(r"\bqn\b", "quelqu'un", t); t = re.sub(r"\bqc\b", "quelque chose", t)
    else: t = re.sub(r"\bqcn\b", "qualcuno", t); t = re.sub(r"\bqcs\b", "qualcosa", t)
    t = re.sub(r"\([^()]*\)", " ", t).replace("…", " ").replace(" / ", ", ").replace("/", ", ")
    t = re.sub(r"\s+([,.!?;:])", r"\1" if L == "it" else r" \1", t); t = re.sub(r"\s+", " ", t).strip(" ,")
    t = re.sub(r" ([,.])", r"\1", t)
    return t
SP = {}
for L in ("fr", "it"):
    texts = sorted({say(o[L], L) for o in out}, key=len)
    for o in out: SP.setdefault(o["key"], {})[L] = say(o[L], L)
    import random; random.seed(7); random.shuffle(texts)
    lots, cur, n = [], [], 0
    for t in texts:
        if cur and (n + len(t) + 12 > 4200 or len(cur) >= 200): lots.append(cur); cur, n = [], 0
        cur.append(t); n += len(t) + 12
    if cur: lots.append(cur)
    json.dump(lots, open(S + f"aud_{L}/lots.json", "w"), ensure_ascii=False)
    print(L, len(texts), "textes", len(lots), "lots", [sum(len(t) for t in l) for l in lots][:3])
json.dump(SP, open(S + "spoken.json", "w"), ensure_ascii=False)
