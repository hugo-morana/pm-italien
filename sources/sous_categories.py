"""Étiquettes de sous-catégories conformes à la liste de l'utilisateur (fautes de frappe corrigées),
avec la hiérarchie parent → enfants. Chaque niche reçoit ses étiquettes et tous leurs ancêtres."""
import json, re
P = "/home/claude/pm_italien/data_italien.json"

# Liste de l'utilisateur, par famille ; (enfant, parent). Les étiquettes marquées « ajout » ne figurent pas dans sa liste.
ARBRE = {
 "adjectifs": [("adjectifs", None), ("adjectifs_qualificatifs", "adjectifs"), ("adjectifs_couleurs", "adjectifs_qualificatifs"),
   ("adjectifs_démonstratifs", "adjectifs"), ("adjectifs_exclamatifs", "adjectifs"), ("adjectifs_indéfinis", "adjectifs"),
   ("adjectifs_interrogatifs", "adjectifs"), ("adjectifs_numéraux", "adjectifs"), ("adjectifs_cardinaux", "adjectifs_numéraux"),
   ("adjectifs_ordinaux", "adjectifs_numéraux"), ("adjectifs_possessifs", "adjectifs"), ("adjectifs_relatifs", "adjectifs"),
   ("articles", "adjectifs")],
 "pronoms": [("pronoms", None), ("pronoms_adverbiaux", "pronoms"), ("pronoms_démonstratifs", "pronoms"), ("pronoms_indéfinis", "pronoms"),
   ("pronoms_interrogatifs", "pronoms"), ("pronoms_personnels", "pronoms"), ("pronoms_personnels_sujets", "pronoms_personnels"),
   ("pronoms_personnels_toniques", "pronoms_personnels"), ("pronoms_personnels_compléments", "pronoms_personnels"),
   ("pronoms_personnels_compléments_directs", "pronoms_personnels_compléments"),
   ("pronoms_personnels_compléments_indirects", "pronoms_personnels_compléments"),
   ("pronoms_personnels_réfléchis", "pronoms_personnels"), ("pronoms_possessifs", "pronoms"), ("pronoms_relatifs", "pronoms"),
   ("pronoms_relatifs_directs", "pronoms_relatifs"), ("pronoms_relatifs_indirects", "pronoms_relatifs"), ("locutions_pronominales", "pronoms")],
 "conjonctions": [("conjonctions", None), ("conjonctions_coordination", "conjonctions"), ("conjonctions_subordination", "conjonctions"),
   ("conjonctions_subordination_cause", "conjonctions_subordination"), ("conjonctions_subordination_but", "conjonctions_subordination"),
   ("conjonctions_subordination_comparaison", "conjonctions_subordination"), ("conjonctions_subordination_concession", "conjonctions_subordination"),
   ("conjonctions_subordination_condition", "conjonctions_subordination"), ("conjonctions_subordination_conséquence", "conjonctions_subordination"),
   ("conjonctions_subordination_temps", "conjonctions_subordination"), ("conjonctions_subordination_autres", "conjonctions_subordination"),
   ("locutions_conjonctives", "conjonctions")],
 "prépositions": [("prépositions", None), ("prépositions_spatiales", "prépositions"), ("prépositions_temporelles", "prépositions"),
   ("prépositions_autres", "prépositions"), ("locutions_prépositives", "prépositions")],
 "expressions": [("expressions", None), ("expressions_basiques", "expressions"), ("expressions_courantes", "expressions"),
   ("expressions_modales", "expressions"), ("incises", "expressions"), ("incises_introductives", "incises"),
   ("incises_milieu", "incises"), ("incises_conclusives", "incises")],
 "adverbes": [("adverbes", None)] + [(f"adverbes_{x}", "adverbes") for x in
   "affirmation comparaison corrélation doute fréquence intensité lieu manière modalité négation ordre possibilité quantité spécificatifs temps".split()]
   + [("adverbes_interrogatifs", "adverbes"), ("locutions_adverbiales", "adverbes"), ("pronoms_adverbiaux", "adverbes")],
}
AJOUTS = {"articles", "conjonctions_subordination_but", "conjonctions_subordination_autres", "prépositions_autres", "adverbes_interrogatifs"}
PARENT = {}
for fam, lst in ARBRE.items():
    for c, p in lst:
        if p and c not in PARENT: PARENT[c] = p   # pronoms_adverbiaux garde son parent « pronoms »
RENOMME = {"adjectifs_numéraux_cardinaux": "adjectifs_cardinaux", "prépositions_locutions": "locutions_prépositives",
           "adverbes_locutions": "locutions_adverbiales", "adverbes_liaison": None,
           "pronoms_personnels_compléments": "pronoms_personnels_compléments"}
LOCUTION = re.compile(r"[ ’']|-à-")  # locution = plusieurs mots
def ancetres(t):
    out = []
    while t in PARENT: t = PARENT[t]; out.append(t)
    return out

d = json.load(open(P))
FAM_PIECE = {"adjectifs": "adjectifs", "determinants": "adjectifs", "pronoms": "pronoms", "conjonctions": "conjonctions",
             "prepositions": "prépositions", "adverbes": "adverbes", "adjectifs_2": "adjectifs", "adverbes_2": "adverbes"}
for p in d["pieces"]:
    fam = FAM_PIECE.get(p["id"])
    for n in p["niches"]:
        if n.get("libre") or not fam: n["tags"] = [] if n.get("libre") else n.get("tags", []); continue
        tags = set()
        for t in n.get("sous_categories", []):
            t = RENOMME.get(t, t)
            if t: tags.add(t)
        if p["id"] in ("adjectifs", "adjectifs_2"): tags.add("adjectifs_qualificatifs")
        if p["id"] == "determinants" and n["fr"].startswith("un / une"): tags.add("adjectifs_cardinaux")
        # compléments communs aux deux emplois : me, te, nous, vous
        if p["id"] == "pronoms":
            if n["fr"] in ("me (complément)", "te (complément)", "nous (complément)", "vous (complément)"):
                tags |= {"pronoms_personnels_compléments_directs", "pronoms_personnels_compléments_indirects"}
            tags = {t for t in tags if t != "pronoms_personnels_compléments"} or tags
            if n["fr"] in ("quelque chose", "n'importe qui", "n'importe quoi", "l'un l'autre", "la plupart", "quelqu'un"):
                tags.add("locutions_pronominales")
        if p["id"] == "adverbes":
            if n["fr"] in ("peut-être", "probablement"): tags.add("adverbes_possibilité")
        base = re.sub(r"\s*\(.*?\)", "", n["fr"]).split(" / ")[0].replace(" ?", "").strip()
        if base in ("aujourd'hui", "plus… plus"): base = "x"
        if LOCUTION.search(base) and not base.startswith(("ne…", "le ", "la ", "l'", "les ", "un ", "du ")):
            loc = {"conjonctions": "locutions_conjonctives", "prépositions": "locutions_prépositives",
                   "adverbes": "locutions_adverbiales"}.get(fam)
            if loc: tags.add(loc)
        full = set(tags)
        for t in tags: full |= set(ancetres(t))
        if fam not in full: full.add(fam if fam != "adjectifs" else "adjectifs")
        full |= {t for t in n.get("tags", []) if t.startswith("expressions")}
        n["tags"] = sorted(full)
d["sous_categories"] = {"arbre": ARBRE, "ajouts": sorted(AJOUTS)}
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
# contrôle : chaque étiquette d'enfant a au moins une niche
from collections import Counter
c = Counter(t for p in d["pieces"] for n in p["niches"] for t in n.get("tags", []))
for fam, lst in ARBRE.items():
    print(fam, " ".join(f"{x}:{c.get(x,0)}" for x, _ in lst))
