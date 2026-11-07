"""Textes parlés des nouvelles alternatives (rev 28) et lots par langue."""
import json, re, random
N = json.load(open("need_audio.json"))
def say(t, L):
    if L == "fr": t = re.sub(r"\bqqpart\b", "quelque part", t); t = re.sub(r"\bqn\b", "quelqu'un", t); t = re.sub(r"\bqc\b", "quelque chose", t)
    else: t = re.sub(r"\bqcn\b", "qualcuno", t); t = re.sub(r"\bqcs\b", "qualcosa", t)
    t = re.sub(r"\([^()]*\)", " ", t); t = re.sub(r"…-(là|ci)", " ", t).replace("…", " ")
    t = t.replace(" / ", ", ").replace("/", ", "); t = re.sub(r"\s+", " ", t); t = re.sub(r" ([,.!?])", r"\1" if L == "it" else r" \1", t)
    t = re.sub(r" ,", ",", t).strip(" ,")
    return t
SP = {L: {t: say(t, L) for t in N[L]} for L in ("fr", "it")}
json.dump(SP, open("spoken.json", "w"), ensure_ascii=False)
for L in ("fr", "it"):
    M = json.load(open(f"aud_{L}/hp_map.json"))
    T = sorted({s for s in SP[L].values() if s and s not in M}); random.seed(5); random.shuffle(T)
    lots, cur, n = [], [], 0
    for t in T:
        if cur and (n + len(t) + 12 > 4000 or len(cur) >= 180): lots.append(cur); cur, n = [], 0
        cur.append(t); n += len(t) + 12
    if cur: lots.append(cur)
    json.dump(lots, open(f"aud_{L}/lots.json", "w"), ensure_ascii=False)
    print(L, len(T), "textes", len(lots), "lots", [sum(len(t) + 12 for t in l) for l in lots])
