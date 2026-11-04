"""Coupe un lot en n textes par programmation dynamique : coupes choisies parmi les pauses, score = longueur de pause − écart à la durée attendue (proportionnelle au nombre de syllabes)."""
import numpy as np, re
def syl(t): return max(1, len(re.findall(r"[aeiouàèéìíòóù]+", t.lower())))
def segment(db, texts, frac=0.45):
    nf = len(db); floor, peak = np.percentile(db, 10), np.percentile(db, 95); thr = floor + frac * (peak - floor)
    q = db < thr; P = []; i = 0
    while i < nf:
        if q[i]:
            j = i
            while j < nf and q[j]: j += 1
            if i > 0 and j < nf and j - i >= 4: P.append((i, j))
            i = j
        else: i += 1
    start = int(np.argmax(db > thr)); end = nf - int(np.argmax(db[::-1] > thr))
    n = len(texts); w = np.array([syl(t) + 1.5 for t in texts], float)   # +1.5 : pause et attaque
    exp = w / w.sum() * (end - start)                                        # longueur attendue (trames) texte + pause
    C = len(P); mid = np.array([(a + b) / 2 for a, b in P]); plen = np.array([b - a for a, b in P], float)
    INF = 1e18; cost = np.full((n, C), INF); back = np.zeros((n, C), int)
    cum = np.cumsum(exp)
    for c in range(C):   # premier texte se termine à la pause c
        d = mid[c] - start; cost[0, c] = ((d - exp[0]) / max(8, exp[0])) ** 2 * 4 - np.log(plen[c])
    for t in range(1, n - 1):
        lo = np.searchsorted(mid, start + cum[t] - 0.25 * (end - start) - 200); hi = np.searchsorted(mid, start + cum[t] + 0.25 * (end - start) + 200)
        prev = cost[t - 1]
        for c in range(max(lo, t), min(hi, C)):
            d = mid[c] - mid[:c]; pen = ((d - exp[t]) / max(8, exp[t])) ** 2 * 4 - np.log(plen[c])
            tot = prev[:c] + pen; k = int(np.argmin(tot)); cost[t, c] = tot[k]; back[t, c] = k
    # dernier texte : de la dernière coupe à la fin
    last = cost[n - 2] + ((end - mid - exp[n - 1]) / np.maximum(8, exp[n - 1])) ** 2 * 4
    c = int(np.argmin(last)); cuts = [c]
    for t in range(n - 2, 0, -1): c = back[t, c]; cuts.append(c)
    cuts = cuts[::-1]
    S = []; a = start
    for c in cuts: S.append([a, P[c][0]]); a = P[c][1]
    S.append([a, end])
    # contrôle : pire écart relatif de durée
    r = [((b - a) / max(1, e)) for (a, b), e in zip(S, exp)]
    return S, float(np.min(r)), float(np.max(r))
