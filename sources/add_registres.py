"""Scores Zipf par registre (écrit / parlé / séries), FR et IT.
Faute d'accès aux corpus, estimation : score global ± décalage selon le profil d'usage du mot.
Profils : adresse/conversation, littéraire, abstrait, drame/série, quotidien. Décalages (écrit, parlé, séries)."""
import json
P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))

PROFILS = {
    "conv":   (-0.3, +0.3, +0.4),
    "litt":   (+0.3, -0.4, -0.1),
    "abstr":  (+0.3, -0.2, -0.2),
    "drame":  (-0.1, 0.0, +0.4),
    "quot":   (-0.1, +0.2, +0.2),
    "interj": (-0.3, +0.4, +0.5),
}
TAG = {}
for p, mots in {
    "conv":  "le monsieur|madame|le docteur|le téléphone|l'ami|le chef|l'argent|le problème|la minute|la fois|le besoin|le moment|la place",
    "litt":  "le regard|la lumière|la voix|le ciel|le corps|la mer|la terre|la fenêtre|le mur|le bras|le visage|l'œil|la main|la tête|la porte|la nuit|le cœur|le monde|la vie|le temps|l'air|le feu|la guerre|le roi|l'homme|la femme",
    "abstr": "l'état|l'ordre|le cas|la question|la raison|le point|la part|l'affaire|le sens|la façon|le lieu|le fond|l'histoire|l'idée|le côté|le pays|l'âge|la vérité|le mot|le nom|le travail|la fin|la chose",
    "drame": "la mort|le sang|la police|la peur|l'amour|le coup",
    "quot":  "la maison|la voiture|l'école|le train|le lit|la table|le matin|le soir|la semaine|le mois|l'heure|l'eau|la famille|le frère|la sœur|le père|la mère|l'enfant|la fille|le garçon|le fils|les gens|la ville|la rue|la chambre|le jour|l'an / l'année|le bureau|le livre|le papier|le pied",
    "interj":"le dieu",
}.items():
    for m in mots.split("|"):
        TAG[m] = p

def reg(z, prof):
    e, pa, s = PROFILS[prof]
    c = lambda x: round(min(7.5, max(1.0, z + x)), 1)
    return {"ecrit": c(e), "parle": c(pa), "series": c(s)}

manq = []
for r in d["pieces"][0]["niches"]:
    prof = TAG.get(r["fr"])
    if not prof:
        manq.append(r["fr"]); continue
    r["profil_usage"] = prof
    r["zipf"] = {"fr": reg(r["zipf_fr"], prof), "it": reg(r["zipf_cible"], prof)}
assert not manq, manq
d["zipf_methode"] = ("Estimation : score global estimé ± décalage selon le profil d'usage du mot "
                     "(écrit ≈ livres et presse, parlé ≈ conversation, séries ≈ sous-titres TV). "
                     "À remplacer par les corpus : FR Lexique 3 (freqlivres / freqfilms), "
                     "IT SUBTLEX-IT, KIParla, itWaC.")
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print("ok")
