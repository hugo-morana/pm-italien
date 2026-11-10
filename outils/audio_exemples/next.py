"""next.py G : prend les 2 prochains lots FR et 2 IT non faits pour le groupe G (1 = A,B / E,F ; 2 = C,D / G,H), écrit les prompts et les affiche."""
import json, sys, os, subprocess
S = "/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/ex/"; os.chdir(S)
L = json.load(open("lots.json")); Q = json.load(open("queue.json")) if os.path.exists("queue.json") else {"taken": []}
done = lambda k: os.path.exists(f"aud_{L[k]['L']}/raw/words{k:03d}.json")
todo = [k for k in [28] + list(range(30, 163)) if not done(k) and k not in Q["taken"]]
fr = [k for k in todo if L[k]["L"] == "fr"][:2]; it = [k for k in todo if L[k]["L"] == "it"][:2]
N = {"1": ["A RdFjwrYMzsSpHKDrUB0U", "B ZGWLhv6YrDCz8EPw4Z0v", "E KbSS24qGwhvFEPSVXkNZ", "F p3hz4yqnek9VHnXoBIDE"],
     "2": ["C ylgPgRce8XSIgSuQzWzp", "D 4SkVzSB5ngnFR8AzS8uU", "G 1EZRyPmrpIlRFhhQHO5r", "H fXc7CQUx2pgKKWlwbZV8"]}[sys.argv[1]]
ks = fr + it; Q["taken"] += ks; json.dump(Q, open("queue.json", "w"))
subprocess.run(["python3", "prompt.py"] + [str(k) for k in ks], capture_output=True)
print("restants après :", len(todo) - len(ks))
for node, k in zip(N, ks): print(f"=== {k} {L[k]['L']} -> {node}\n" + open(f"p{k:03d}.txt").read())
