"""Étape 1 : nouvelle sélection et nouvel ordre des noms selon le Zipf FR parlé (estimé).
Retire les 10 noms au parlé le plus bas (≤ 5,0) et ajoute 10 noms typiques de l'oral (≥ 5,1)."""
import json
P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))
old = d["pieces"][0]["niches"]

RETIRES = ["le ciel", "la fenêtre", "le mur", "le roi", "le visage",
           "le bras", "le feu", "la lumière", "la mer", "le regard"]

AJOUTS = r"""
maman|la mamma|MAM-ma|4.9,5.7,5.7|4.9,5.5,5.5|maman|Une maman serre son enfant dans ses bras en chantant « mamma mia ».|ressemble : mamma ; m doublé|mamma mia ! ; la madre (registre neutre)
papa|il papà|pa-PA|4.9,5.7,5.7|4.8,5.4,5.5|papa|Un papa porte son enfant sur les épaules.|ressemble : papà, accent final ; ≠ il papa (le pape)|il padre (registre neutre)
le truc|la roba|RO-ba|4.6,5.5,5.4|4.5,5.2,5.2|robe|Un truc informe est emballé dans une robe de soirée.|ro-ba ≈ « robe »|che roba è ? = c'est quoi ce truc ? ; variante il coso
le mec|il tipo|TI-po|4.4,5.5,5.6|4.6,5.1,5.3|type|Un mec en casquette, très typé, montre son badge « TYPE ».|tipo ≈ type (même usage familier)|variante il tizio
le chéri|il tesoro|té-ZO-ro|4.4,5.3,5.4|4.7,5.0,5.2|trésor|Un coffre au trésor s'ouvre et dit « mon chéri ».|tesoro ≈ trésor (terme affectueux)|tesoro mio ! ; variante caro / cara
la chance|la fortuna|for-TOU-na|4.8,5.3,5.3|4.6,4.9,5.0|fortune|Un trèfle à quatre feuilles fait fortune.|fortuna ≈ fortune ; sens « chance »|che fortuna ! ; buona fortuna = bonne chance
le bébé|il bebè|bé-BÈ|4.6,5.2,5.3|4.0,4.5,4.7|bébé|Un bébé en couche hurle dans un berceau.|ressemble : bebè, accent final|variante il neonato (nouveau-né)
le mari|il marito|ma-RI-to|4.9,5.2,5.3|4.6,4.9,5.0|« mari, tôt ! »|Un mari en costume de mariage court tôt le matin.|ma-ri-to ≈ « mari tôt »|la moglie = la femme (épouse)
la fête|la festa|FÈS-ta|4.8,5.1,5.2|4.6,4.9,5.0|festival|Une fête : cotillons et ballons.|festa ≈ festival (latin festum)|fare festa = faire la fête
le café|il caffè|kaf-FÈ|4.8,5.1,5.1|4.5,4.8,4.8|café|Une tasse de café fumante.|ressemble : caffè, deux f et accent final|un caffè = un expresso ; il bar = le café (lieu)
"""

niches = [r for r in old if r["fr"] not in RETIRES]
assert len(niches) == 90
for line in [l for l in AJOUTS.strip().split("\n") if l.strip()]:
    fr, it, pr, zf, zi, mc, sc, de, fo = line.split("|")
    zf = [float(x) for x in zf.split(",")]; zi = [float(x) for x in zi.split(",")]
    niches.append(dict(fr=fr, cible=it, prononciation=pr, mot_cle=mc, scene=sc, decryptage=de, formes=fo,
                       zipf_fr=round(sum(zf)/3, 1), zipf_cible=round(sum(zi)/3, 1), zipf_source="estimé",
                       categorie="noms", sous_categories=["noms"], profil_usage="conv",
                       zipf={"fr": dict(zip(("ecrit", "parle", "series"), zf)),
                             "it": dict(zip(("ecrit", "parle", "series"), zi))},
                       n_ancien=999, lien=""))
for r in niches:
    r.setdefault("n_ancien", r.get("n", 999))
niches.sort(key=lambda r: (-r["zipf"]["fr"]["parle"], -r["zipf_fr"], r["n_ancien"]))
for i, r in enumerate(niches):
    r["n"] = i
    r["lien"] = ""
    r.pop("n_ancien", None)
assert len({r["cible"] for r in niches}) == 100
d["pieces"][0]["niches"] = niches
d["pieces"][0]["ordre"] = "Zipf FR parlé décroissant (estimé)"
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print(" | ".join(f'{r["n"]:02d} {r["fr"]}' for r in niches))
