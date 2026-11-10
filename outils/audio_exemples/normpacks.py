"""Niveau homogène des voix des mots : chaque segment des paquets audio/*.mp3 (hors ex_ / w29_, reconstruits depuis enc/)
est ramené à -18 LUFS ; paquets réécrits, références [paquet, début, longueur] et empreinte ?v= mises à jour.
Reprise possible : segments déjà faits en cache seg_cache/."""
import json, os, hashlib, sys
from multiprocessing import Pool
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"; sys.path.insert(0, S); import loud
A = "/home/claude/pm_italien/pm3d/"; P = A + "data3d.json"; C = S + "seg_cache/"; os.makedirs(C, exist_ok=True)
D = json.load(open(P))
skip = lambda u: u.split("/")[1].startswith(("ex_", "w29_"))
refs = {}
for r in D["rooms"]:
    for x in r["niches"]:
        if not x: continue
        for f in ("af", "ai", "ae", "ap"):
            v = x.get(f)
            if isinstance(v, list) and not skip(D["packs"][v[0]]): refs.setdefault(v[0], []).append((x, f))
def job(a):
    pi, off, ln = a; key = C + hashlib.md5(f"{D['packs'][pi]}:{off}:{ln}".encode()).hexdigest() + ".mp3"
    if not os.path.exists(key):
        b = open(A + D["packs"][pi].split("?")[0], "rb").read()[off:off + ln]
        nb, i, g = loud.norm_bytes(b); open(key + ".t", "wb").write(nb); os.replace(key + ".t", key)
    return a, key
segs = sorted({(pi, x[f][1], x[f][2]) for pi, l in refs.items() for x, f in l})
print("paquets", len(refs), "segments", len(segs), flush=True)
out = {}
with Pool(2) as p:
    for n, (a, key) in enumerate(p.imap_unordered(job, segs, chunksize=16)):
        out[a] = key
        if n % 1000 == 0: print(n, flush=True)
for pi, l in refs.items():
    name = D["packs"][pi].split("?")[0]; blob = b""; pos = {}
    for a in sorted(k for k in out if k[0] == pi):
        b = open(out[a], "rb").read(); pos[a] = (len(blob), len(b)); blob += b
    for x, f in l:
        o, n = pos[(pi, x[f][1], x[f][2])]; x[f] = [pi, o, n]
    open(A + name, "wb").write(blob); D["packs"][pi] = name + "?v=" + hashlib.md5(blob).hexdigest()[:8]
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("fini", len(refs), "paquets")
