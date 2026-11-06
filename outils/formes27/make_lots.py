"""Textes parlés des nouvelles formes (rev 27) et lots par langue."""
import json, re
L0 = json.load(open("new_items.json"))
IT_EL = {"l'": "l'amico", "un'": "un'amica", "dell'": "dell'acqua", "quest'": "quest'anno", "quell'": "quell'uomo"}
FR_EL = {"de l'": "de l'eau"}
def say(t, L):
    if L == "it" and t in IT_EL: return IT_EL[t]
    t = re.sub(r"\([^()]*\)", " ", t); t = re.sub(r"…-(là|ci)", " ", t).replace("…", " ")
    t = t.replace(" / ", ", ").replace("/", ", "); t = re.sub(r"\s+", " ", t); t = re.sub(r" ,", ",", t).strip(" ,")
    if L == "fr" and t in FR_EL: t = FR_EL[t]
    return t
SP = [{"fr": say(f, "fr"), "it": say(i, "it")} for f, i in L0]
json.dump(SP, open("spoken.json", "w"), ensure_ascii=False)
for L in ("fr", "it"):
    T = sorted({s[L] for s in SP}); import random; random.seed(3); random.shuffle(T)
    json.dump([T], open(f"aud_{L}/lots.json", "w"), ensure_ascii=False)
    print(L, len(T), sum(len(t) + 12 for t in T), T[:12])
