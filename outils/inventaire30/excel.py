import pickle, json, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
P = pickle.load(open("inv.pkl", "rb")); R = pickle.load(open("items_checked.pkl", "rb"))
D = json.load(open("data3d_rev29.json"))
NI = {f"{r['id']}:{i}": x for r in D["rooms"] for i, x in enumerate(r["niches"]) if x}
ROOMFR = {r["id"]: r["fr"] for r in D["rooms"]}
POSFR = {"NOUN": "nom", "VERB": "verbe", "AUX": "auxiliaire", "ADJ": "adjectif", "ADV": "adverbe", "ADP": "préposition",
         "CCONJ": "conj. coordination", "SCONJ": "conj. subordination", "PRON": "pronom", "DET": "déterminant",
         "NUM": "numéral", "INTJ": "interjection", "PROPN": "nom propre"}

# ---- couverture des structures élémentaires (patrons) ----
COV = json.load(open("cover.json"))
HEAD = Font(bold=True, color="FFFFFF"); FILL = PatternFill("solid", fgColor="2F5D50")
RED = PatternFill("solid", fgColor="F6D5D0"); GREEN = PatternFill("solid", fgColor="DDEFE3")

def sheet(wb, title, cols, rows, widths, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title; ws.append(cols)
    for c in ws[1]: c.font = HEAD; c.fill = FILL; c.alignment = Alignment(vertical="center", wrap_text=True)
    for r in rows: ws.append(r)
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    return ws

def libref(keys):
    keys = sorted(keys)[:3]
    return " ; ".join(f"{ROOMFR[k.split(':')[0]]} n°{int(k.split(':')[1]) + 1} « {NI[k]['it']} »" for k in keys)

# ---------- inventaire ----------
wb = Workbook()
rows = []
for s in P["rows"]:
    comps = P["pats"][s["pat"]]["comps"]
    rows.append([ROOMFR[s["room"]], s["n"] + 1, s["it"], s["eit"], s["efr"], s["pat"], " · ".join(s["words"])])
sheet(wb, "Phrases", ["Salle", "N°", "Niche (it)", "Phrase italienne", "Phrase française", "Patron (structures)", "Mots (lemme + classe)"],
      rows, [28, 5, 22, 45, 45, 45, 70], first=True)

rows = []
for (lem, pos), v in sorted(R.items(), key=lambda kv: (-kv[1]["n"], kv[0])):
    pres = "nom propre (non compté)" if pos == "PROPN" else ("numéral (non compté)" if pos == "NUM" else ("oui" if v["hit"] else "NON"))
    where = ""
    if v["hit"] and pos not in ("PROPN", "NUM"):
        keys = set()
        for h in v["hit"]: keys |= set(P["lib"].get(h, []) or P["libform"].get(h, []))
        where = libref(keys) if keys else ""
    rows.append([v["lemma"], POSFR.get(pos, pos), v["n"], round(v["z"], 2), ", ".join(list(v["forms"])[:5]), pres, where, v["ex"][0]])
ws = sheet(wb, "Mots", ["Lemme", "Classe", "Occurrences", "Fréquence (zipf it)", "Formes rencontrées", "Dans le palais ?", "Où (niche)", "Exemple"],
           rows, [20, 18, 12, 12, 30, 14, 60, 50])
for row in ws.iter_rows(min_row=2):
    row[5].fill = RED if row[5].value == "NON" else (GREEN if row[5].value == "oui" else PatternFill())

comp = collections.Counter(); compex = {}
for k, v in P["pats"].items():
    for c in v["comps"]:
        comp[c] += v["n"]; compex.setdefault(c, v["ex"][0])
rows = []
for c, n in comp.most_common():
    cv = COV.get(c)
    rows.append([c, n, compex[c], "oui" if cv else "NON", libref([cv]) if cv and cv in NI else (cv or "")])
ws = sheet(wb, "Structures", ["Structure élémentaire", "Phrases", "Exemple", "Dans le palais ?", "Niche correspondante"], rows, [45, 10, 50, 14, 70])
for row in ws.iter_rows(min_row=2): row[3].fill = RED if row[3].value == "NON" else GREEN

rows = [[k, v["n"], " | ".join(v["ex"])] for k, v in sorted(P["pats"].items(), key=lambda kv: -kv[1]["n"])]
sheet(wb, "Patrons complets", ["Patron (combinaison de structures)", "Phrases", "Exemples"], rows, [70, 10, 90])
wb.save("Inventaire_phrases_exemple.xlsx")

# ---------- manquants ----------
wb = Workbook()
M = json.load(open("missing_final.json")); W = json.load(open("where.json"))
rows = [[m["it"], m["fr"], m["classe"], m["n"], m["z"], (lambda w: f"{w[1]} n°{w[2]}" if w else m["salle"])(W.get(m["it"]+"|"+m["fr"])), m["eit"], m["efr"], m.get("note", "")] for m in sorted(M, key=lambda m: -m["z"])]
sheet(wb, "Mots manquants", ["Mot italien", "Traduction", "Classe", "Occurrences", "Fréquence (zipf it)", "Ajouté dans", "Exemple", "Traduction de l'exemple", "Note"],
      rows, [22, 24, 14, 11, 12, 20, 50, 50, 30], first=True)
PM = json.load(open("patrons_manquants.json"))
rows = [[p["it"], p["fr"], p["structure"], p["n"], p["eit"], p["efr"], (lambda w: f"{w[1]} n°{w[2]}" if w else "")(W.get(p["it"]+"|"+p["fr"]))] for p in PM]
sheet(wb, "Patrons manquants", ["Patron (it)", "Patron (fr)", "Structure", "Phrases concernées", "Exemple", "Traduction", "Ajouté dans"], rows, [40, 40, 34, 12, 45, 45, 26])
EX = json.load(open("exclus.json"))
rows = [[e["lemma"], e["classe"], e["forms"], e["raison"], e["ex"]] for e in EX]
sheet(wb, "Écartés", ["Lemme détecté", "Classe", "Formes", "Raison", "Exemple"], rows, [20, 14, 25, 40, 60])
wb.save("Manquants_palais.xlsx")
print("ok")
