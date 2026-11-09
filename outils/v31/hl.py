"""Surlignage des paramètres [v], [n], [qcs]… dans les exemples : eim / efm deviennent des segments « a|b|c »."""
import json, re, sys
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P))
W = re.compile(r"[A-Za-zÀ-ÿ0-9]+(?:['’](?=[A-Za-zÀ-ÿ]))?")
DET = set("il lo la l' i gli le un uno una un' del dello della dell' dei degli delle al allo alla all' ai agli alle dal dalla dai nel nella nei sul sulla sui mio mia miei mie tuo tua suo sua nostro nostra questo questa questi queste quel quello quella quei quelle le la les l' un une des du de d' mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs ce cet cette ces au aux".split())
ADJ = set("piccolo piccola piccoli piccole grande grandi bel bella bello begli belle nuovo nuova vecchio vecchia buon buona prossimo prossima ultimo ultima primo prima altro altra petit petite grand grande beau belle nouveau nouvelle vieux vieille bon bonne prochain prochaine dernier dernière premier première autre".split())
CLI = set("mi ti ci vi si lo la li le ne gli me te se l' m' t' s' n' c' j' y en lui leur nous vous".split())
SUBJ = {"[qcn]", "[qn]", "[S]"}
def toks(s): return [(m.group(0), m.start(), m.end()) for m in W.finditer(s)]
def tpl(t):
    t = re.sub(r"\((?![^)]*\])[^)]*\)", " ", t)
    out = []
    for m in re.finditer(r"\[\[[^\]]*\]\]|\[[^\]]+\]|[^\s\[\]]+", t):
        g = m.group(0)
        if g.startswith("["): out.append(("P", g)); continue
        for w in W.findall(g.lower()): out.append(("F", w.replace("’", "'")))
    return out
def same(a, b):
    a = a.lower().replace("’", "'"); b = b.lower().replace("’", "'")
    if a == b: return True
    for x, y in ((a, b), (b, a)):
        if x.endswith("'") and len(x) >= 2 and y.startswith(x[:-1]) and len(y) - len(x) <= 1 and "'" not in y: return True   # qu' = que, l' = la
    k = min(4, len(a), len(b))
    return k >= 3 and a[:k] == b[:k] and abs(len(a) - len(b)) <= 4
def slot(ph, ws, i, stop):
    """mots consommés par un paramètre à partir de ws[i]"""
    j = i; n = len(ws)
    if j >= min(n, stop): return j
    if ph in ("[v]", "[v inf]", "[v subj]", "[v-inf]"):
        while j < min(n, stop) - 1 and ws[j][0].lower().replace("’", "'") in CLI: j += 1
        return j + 1
    if ph == "[adj]": return j + 1
    while j < min(n, stop) - 1 and ws[j][0].lower().replace("’", "'") in DET: j += 1
    while j < min(n, stop) - 1 and ws[j][0].lower() in ADJ: j += 1
    return j + 1
def segs(sent, base, t):
    T = tpl(t); ws = toks(sent)
    if not T or not any(k == "P" for k, _ in T): return None
    on = [False] * len(ws); pos = {}; claimed = set()
    brk = [i for i in range(1, len(ws)) if re.search(r"[,;:.!?…«»()]", sent[ws[i - 1][2]:ws[i][1]])]   # ponctuation avant ws[i]
    def lim(i): return min([b for b in brk if b > i] + [len(ws)])   # première coupure après le mot i
    # 1. bloc déjà surligné
    b0 = sent.lower().find(base.lower()) if base else -1
    bw = [i for i, (w, a, e) in enumerate(ws) if b0 >= 0 and a >= b0 and e <= b0 + len(base)]
    for i in bw: on[i] = True
    # 2. ancres des mots fixes, dans l'ordre
    cur = 0
    for k, (kind, v) in enumerate(T):
        if kind != "F": continue
        hit = next((i for i in range(cur, len(ws)) if same(ws[i][0], v)), None)
        if hit is None and bw and k == next(kk for kk, (kd, _) in enumerate(T) if kd == "F"): hit = bw[0]
        if hit is not None: pos[k] = hit; on[hit] = True; cur = hit + 1
    if bw and not pos: return None
    # 3. paramètres
    for k, (kind, v) in enumerate(T):
        if kind != "P" or v in SUBJ and not any(kk < k for kk in pos): continue
        prv = max((kk for kk in pos if kk < k), default=None); nxt = min((kk for kk in pos if kk > k), default=None)
        if prv is not None:
            inb = [i for i in bw if i > pos[prv] and (nxt is None or i < pos[nxt]) and i not in claimed]
            if inb: claimed.update(inb); continue          # le paramètre est déjà dans le surlignage d'origine
            start = max([pos[prv]] + [i for i in range(len(ws)) if on[i] and i > pos[prv] and (nxt is None or i < pos[nxt])]) + 1
            stop = min(pos[nxt] if nxt is not None else len(ws), lim(start - 1))
            if nxt is not None and stop - start <= 4 and all(kd == "P" for kd, _ in T[prv + 1:nxt]):
                for i in range(start, stop): on[i] = True
                continue
            end = slot(v, ws, start, stop)
            if end - start > 4: continue
            for i in range(start, end): on[i] = True
        elif nxt is not None and v in ("[v]", "[adj]", "[v inf]", "[v subj]"):
            i = pos[nxt] - 1
            if i < 0 or pos[nxt] in brk: continue
            on[i] = True
            while i - 1 >= 0 and i not in brk and ws[i - 1][0].lower().replace("’", "'") in CLI: i -= 1; on[i] = True
    # 4. segments contigus
    out = []; i = 0
    while i < len(ws):
        if not on[i]: i += 1; continue
        j = i
        while j + 1 < len(ws) and on[j + 1] and sent[ws[j][2]:ws[j + 1][1]].strip(" ") in ("", "'", "’", "-"): j += 1
        out.append(sent[ws[i][1]:ws[j][2]]); i = j + 1
    return "|".join(out) if out else None
ch = 0; samp = []; FOC = ["non [", "ne [v] pas", "[v] pas", "si [v]", "[qn] [v]"]
for r in D["rooms"]:
    for x in r["niches"]:
        if not x or r["fam"] == "patrons": continue
        for tk, sk, mk in (("itd", "eit", "eim"), ("frd", "efr", "efm")):
            t = x.get(tk) or ""
            if "[" not in t or not x.get(sk): continue
            new = segs(x[sk], x.get(mk) or "", t)
            if new and new != x.get(mk):
                if any(w in t.lower() for w in FOC) or (len(samp) < 40 and hash(t) % 40 == 0): samp.append(f"{t}  ::  {x[sk]}  ::  {x.get(mk)}  →  {new}")
                x[mk + "_new"] = new; ch += 1
print("changés", ch)
print("\n".join(samp))
if "--write" in sys.argv:
    for r in D["rooms"]:
        for x in r["niches"]:
            if not x: continue
            for mk in ("eim", "efm"):
                if mk + "_new" in x: x[mk] = x.pop(mk + "_new")
    json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":")); print("écrit")
