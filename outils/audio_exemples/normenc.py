"""Normalise en place (-18 LUFS) les clips de enc/ pas encore traités ; registre norm_done.json."""
import json, os, glob, shutil, sys
from multiprocessing import Pool
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"; os.chdir(S); sys.path.insert(0, S)
import loud
R = S + "norm_done.json"; done = set(json.load(open(R))) if os.path.exists(R) else set()
def job(fn):
    src = S + "enc/" + fn; tmp = S + "enc/.n_" + fn
    i, g = loud.norm_file(src, tmp); os.replace(tmp, src); return fn, i, g
todo = sorted(os.path.basename(f) for f in glob.glob(S + "enc/*.mp3") if os.path.basename(f) not in done)
with Pool(2) as p:
    for fn, i, g in p.imap_unordered(job, todo, chunksize=8): done.add(fn)
json.dump(sorted(done), open(R, "w")); print("normalisés", len(todo), "total", len(done))
