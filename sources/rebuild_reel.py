"""Reconstruit la pièce Noms à partir des fréquences réelles.
Sélection : top 100 des lemmes NOM de Lexique 3 (freqlemfilms2), locutions et interjections exclues, synonymes fusionnés.
Ordre : Zipf FR parlé = moyenne Lexique films + OpenSubtitles 2018."""
import json, sys, copy
sys.argv = ["x"]
exec(open("/home/claude/pm_italien/freq_reelles.py").read().split("if __name__")[0])

P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))
old = {r["fr"]: r for r in d["pieces"][0]["niches"]}
v1 = {r["fr"]: r for r in json.load(open("/home/claude/pm_italien/data_italien_v1.json"))["pieces"][0]["niches"]}

# Part « nom » corrigée à la main pour les formes italiennes très ambiguës (le tagueur d'itWaC les classe mal)
SHARE_MANUEL = {"ora": 0.25, "porta": 0.45, "resto": 0.6, "voglia": 0.5, "gioco": 0.8, "diritto": 0.7, "giro": 0.8}
_share = share_it
share_it = lambda o: SHARE_MANUEL.get(o, _share(o))
globals()["share_it"] = share_it

# fr affiché | clés Lexique | lemme itWaC
CLES = {
 "l'an / l'année": (["an", "année"], "anno"), "le garçon / le gars": (["garçon", "gars"], "ragazzo"),
 "le travail / le boulot": (["travail", "boulot"], "lavoro"), "la part / la partie": (["part", "partie"], "parte"),
 "l'œil": (["oeil"], "occhio"), "le cœur": (["coeur"], "cuore"), "les gens": (["gens"], "gente"),
 "l'argent": (["argent"], "soldo"), "madame": (["madame"], "signora"), "maman": (["maman"], "mamma"),
 "papa": (["papa"], "papà"), "le dieu": (["dieu"], "dio"),
}
RENOMME = {"le garçon": "le garçon / le gars", "le travail": "le travail / le boulot", "la part": "la part / la partie"}
GARDES = ["la chose", "l'an / l'année", "l'homme", "le jour", "la femme", "le temps", "la vie", "le dieu", "la fois", "le père",
          "la fille", "le monde", "le besoin", "l'ami", "le monsieur", "l'enfant", "l'heure", "la mère", "la maison", "les gens",
          "le travail", "la nuit", "le soir", "le nom", "la peur", "le garçon", "maman", "le problème", "l'argent", "la main",
          "la part", "l'air", "le fils", "la tête", "le coup", "la raison", "la mort", "l'amour", "le moment", "la voiture",
          "l'œil", "la question", "l'affaire", "le frère", "l'idée", "la famille", "le truc", "la chance", "l'histoire", "la minute",
          "la porte", "le mec", "le mois", "madame", "l'eau", "le sang", "la place", "la ville", "la terre", "la semaine",
          "la chambre", "le côté", "le cas", "le mot", "la police", "le matin", "le mari", "papa", "le train", "le corps",
          "le cœur", "le docteur", "la façon", "le point", "la guerre", "l'ordre", "le pied", "la fin", "l'école", "le chef",
          "le pays", "le livre", "la vérité", "le bébé"]

N = r"""
le type|il tipo|TI-po|type|Un type en casquette, très typé, montre un badge « TYPE ».|tipo ≈ type (aussi « genre de »)|che tipo è ? ; un tipo strano|C'est un drôle de type.|È un tipo strano.|type
le film|il film|FILM|film|Une bobine de film déroule ses images dans un projecteur.|identique et invariable|i film|On regarde un film ce soir ?|Guardiamo un film stasera?|film
le feu|il fuoco|FOUO-ko|fou aux cocos|Un fou fait du feu en frottant deux noix de coco.|fuo-co ≈ « fou… co »|fuochi d'artificio = feux d'artifice|Au feu !|Al fuoco!|feu
le chien|il cane|KA-né|canne|Un chien court avec une canne dans la gueule.|ca-ne ≈ « canne » ; cf. canin|pl. i cani|Attention, le chien mord !|Attenzione, il cane morde!|chien
le genre|il genere|DJÈ-né-ré|gêne, René|Une étiquette « genre » colle au front de René et le gêne.|ge-ne-re ≈ « gêne René » ; cf. genre, général|in genere = en général|C'est pas mon genre.|Non è il mio genere.|genre
l'arme|l'arma|AR-ma|armure|Une arme est posée sur une armure de chevalier.|ressemble : arma (féminin)|pl. le armi|Lâche ton arme !|Butta l'arma!|arme
l'endroit|il luogo|LOUO-go|« loup, go ! »|Un loup crie « go ! » et marque son endroit d'un drapeau.|luo-go ≈ « loup, go » ; latin locus|aver luogo = avoir lieu ; variante il posto|C'est un endroit magnifique.|È un luogo bellissimo.|endroit
le reste|il resto|RÈS-to|resto|Le reste du repas part en barquette du resto.|resto = reste ; aussi la monnaie rendue|tieni il resto = garde la monnaie|Tu gardes le reste ?|Tieni il resto?|reste
l'envie|la voglia|VO-llia|voile|Une voile se gonfle d'envie de partir.|vo-glia ≈ « voile » ; gli = « lli »|avere voglia di = avoir envie de|J'ai envie d'une glace.|Ho voglia di un gelato.|envie
la photo|la foto|FO-to|photo|Un appareil photo crépite de flashs.|ressemble ; féminin invariable|le foto ; fare una foto|Tu peux prendre une photo ?|Puoi fare una foto?|photo
le droit|il diritto|di-RIT-to|« dis, rit tôt »|Un code civil ouvert rit tôt le matin : « Dis, rit tôt ! ».|di-rit-to ≈ « dis, rit tôt » ; dritto = tout droit|avere il diritto di = avoir le droit de|T'as pas le droit !|Non hai il diritto!|droit
le tour|il giro|DJI-ro|gyrophare|Un gyrophare fait des tours sur lui-même.|giro ≈ gyro(phare), girouette|fare un giro = faire un tour|On fait un tour ?|Facciamo un giro?|tour
le jeu|il gioco|DJO-ko|jockey|Un jockey joue à un jeu de plateau sur son cheval.|gio-co ≈ « jockey »|pl. i giochi|C'est qu'un jeu !|È solo un gioco!|jeu
l'instant|l'attimo|AT-ti-mo|« à Timo »|Un sablier minuscule est tendu à Timo.|at-ti-mo ≈ « à Timo »|un attimo ! = un instant ! ; variante l'istante|Un instant, j'arrive !|Un attimo, arrivo!|instant
le parent|il genitore|djé-ni-TO-ré|génie + géniteur|Un génie sort de sa lampe et devient le parent de Tore.|geni-tore ≈ génie, géniteur|surtout au pl. i genitori|Mes parents arrivent demain.|I miei genitori arrivano domani.|parent
le service|il favore|fa-VO-ré|faveur|Un plateau de service tend une faveur emballée.|favore = faveur ; rendre service = fare un favore|variante il servizio (service public, au restaurant)|Tu peux me rendre un service ?|Puoi farmi un favore?|service
"""
niches = []
for k in GARDES:
    r = copy.deepcopy(old.get(k) or v1[k])
    if k in RENOMME: r["fr"] = RENOMME[k]
    niches.append(r)
for line in [l for l in N.strip().split("\n") if l.strip()]:
    fr, it, pr, mc, sc, de, fo, efr, eit, key = line.split("|")
    niches.append(dict(fr=fr, cible=it, prononciation=pr, mot_cle=mc, scene=sc, decryptage=de, formes=fo,
                       exemple_fr=efr, exemple_cible=eit, categorie="noms", sous_categories=["noms"],
                       audio_mot=None, audio_phrase=None, lien=""))
    CLES[fr] = ([key], it.split(" ", 1)[1] if " " in it else it.split("'", 1)[1])
# le mec -> il tizio (il tipo va au « type »)
for r in niches:
    if r["fr"] == "le mec":
        r.update(cible="il tizio", prononciation="TIT-tsio", mot_cle="« Titi, oh ! »",
                 scene="Un mec en casquette appelle son canari : « Titi, oh ! ».", decryptage="ti-zio ≈ « Titi, oh »",
                 formes="f. la tizia ; tizio e caio = untel et untel", exemple_fr="C'est qui, ce mec ?", exemple_cible="Chi è quel tizio?")
    if r["fr"] == "le feu" and not r.get("audio_mot"): r.setdefault("audio_mot", None)
assert len(niches) == 100, len(niches)

def cles(r):
    if r["fr"] in CLES: return CLES[r["fr"]]
    lx = r["fr"].replace("l'", "").split(" ", 1)[-1].replace("œ", "oe")
    it = r["cible"].replace("l'", "").split(" ", 1)[-1]
    return [lx], it

for r in niches:
    lx, it = cles(r)
    fr_s, it_s = scores_fr(lx), scores_it(it)
    assert fr_s and it_s, (r["fr"], lx, it)
    r["lex"], r["lemme_it"] = lx, it
    r["zipf"] = {"fr": fr_s, "it": it_s}
    r["zipf_fr"], r["zipf_cible"] = fr_s["parle"], it_s["parle"]
    r["zipf_source"] = "mesuré"
    for k in ("profil_usage", "variantes"): r.pop(k, None)

niches.sort(key=lambda r: -r["zipf"]["fr"]["parle"])
for i, r in enumerate(niches):
    r["n"] = i; r["lien"] = ""
assert len({r["cible"] for r in niches}) == 100 and len({r["fr"] for r in niches}) == 100
d["pieces"][0]["niches"] = niches
d["pieces"][0]["ordre"] = "Zipf FR parlé (moyenne Lexique 3 films + OpenSubtitles 2018), décroissant"
d["zipf_methode"] = ("Zipf par lemme. FR : écrit = Lexique 3.83 livres ; films = Lexique 3.83 sous-titres de films ; "
    "sous-titres = OpenSubtitles 2018 (films et séries) ; parlé = moyenne films + sous-titres ; global = wordfreq. "
    "IT : écrit = itWaC (web) ; parlé = OpenSubtitles 2018 ; global = wordfreq. Formes homographes corrigées "
    "par la part « nom » (Lexique pour le FR, itWaC calibré pour l'IT, réglage manuel pour ora, porta, resto, voglia, gioco, diritto, giro).")
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
for r in niches:
    f, i = r["zipf"]["fr"], r["zipf"]["it"]
    print(f'{r["n"]:02d} {r["fr"]:24} parlé {f["parle"]:.2f} (films {f["films"]:.2f} / os {f["soustitres"]:.2f}) écrit {f["ecrit"]:.2f} | {r["cible"]:14} parlé {i["parle"]:.2f} écrit {i["ecrit"]:.2f}')
