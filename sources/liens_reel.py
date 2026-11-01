"""Chaîne de liens n -> n+1 pour l'ordre mesuré (Zipf FR parlé)."""
import json
P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))
L = """
Le Cosaque lance son paquet « ? », qui s'enfile sur l'anneau doré du calendrier.
L'anneau du calendrier roule et percute un homme qui crie « Oh ! », le singe Momo sur les épaules.
Momo attrape le balancier d'une horloge-métronome et bat le tempo.
Le balancier rallume une bougie de vie, qui avale des vitamines.
La flamme de vie grandit jusqu'à devenir un soleil levant ; George crie « non ! ».
George se réfugie derrière une femme qui donne les cartes.
Chaque carte posée fait tourner le compteur « ×1, ×2 », qui fait volte-face.
Le compteur tournoyant réclame un bisou et reçoit un gnon.
Le gnon fait rouler quelqu'un jusqu'aux pieds d'un dieu barbu qui crie « Dis, oh ! ».
Le dieu lance un éclair sur un padre en soutane, toujours pas drôle.
Le padre bénit une fille dont un rat gâte la robe.
Le rat s'enfuit en grimpant sur un globe retransmis en mondovision.
Le globe roule jusqu'à la mi-côte, où un ami l'arrête du pied.
L'ami salue un monsieur qui fait signe au rez-de-chaussée.
Le monsieur tend un tambour à un bambin, qui tape dessus.
Le tambour réveille une mère qui agite un drapeau de Madrid.
Le drapeau accroche une horloge en or, qui tombe.
L'horloge en or est ramassée par une foule de gens gentils.
La foule porte tout son linge au lavoir, où un ouvrier frotte.
L'ouvrier éclabousse un garçon dont un rat gâte la casquette.
Le garçon court s'abriter dans une case au toit de paille.
Derrière la case, le soleil se couche : ce soir, ce sera la fête.
À la fête, chacun porte un badge où son nom est écrit.
Le badge brille et la lune écrit une note de musique dans la nuit.
La note tombe sur un tableau et y écrit une équation insoluble.
Pour se consoler de l'équation, on coupe une part de gâteau.
La part de gâteau est servie par une maman qui s'écrie « mamma mia ! ».
Le cri de la maman fait fuir un fantôme : pas hourra !
Le fantôme traverse une vitrine de soldes pleine de billets.
Les billets volent sur un professeur qui a raison, la rage au nez.
Le professeur souffle si fort qu'un ventilateur fait chanter une aria à la cantatrice.
La cantatrice saisit la main gantée de Manon.
La main de Manon arrache la faux de la Mort.
La Mort fige d'un coup de faux le chronomètre « mémento ».
Le chronomètre est offert à un filleul par son parrain.
Le filleul pose le chronomètre sur une tête qui passe un test.
La tête donne un coup qui envoie un pot sur un col.
Le pot retombe sur le capot d'une voiture-machine.
La voiture emboutit un point d'interrogation qui porte un mandat sur le dos.
Le point d'interrogation ouvre une mallette d'affaire.
Dans la mallette, un truc est emballé dans une robe de soirée.
Le truc s'allume comme une ampoule : une idée.
L'ampoule éclaire une photo de famille sur la cheminée.
La famille dessine un cœur d'amour sur la photo.
Le cœur d'amour pousse un trèfle à quatre feuilles qui fait fortune.
Le trèfle se glisse dans un sablier d'une minute.
Le sable s'échappe sur un mec qui appelle son canari : « Titi, oh ! ».
Le canari se pose devant un œil géant au kiosque.
L'œil cligne et deux frères fraternels apparaissent.
Les deux frères ouvrent un livre de story.
Du livre sort un papa qui porte son enfant sur les épaules.
L'enfant juché sur le papa fait basculer une porte en porte-à-faux.
La porte claque et éclabousse une flaque de sang gai qui danse.
Le sang tache le badge « TYPE » d'un type en casquette.
Le type compte sept jours sur ses doigts avec Ti Mana.
Ti Mana s'installe à ses aises devant le calendrier du mois.
Le calendrier s'envole au-dessus de la ville où court un guépard.
Le guépard fend un dossier « cas n°1 », qui casse en deux.
Le dossier tombe sur une chaise libre où trône un poste de radio.
La radio glisse latéralement sur le côté d'un cube.
Le cube heurte une voiture de police, sirène hurlante.
La sirène effraie un rat auquel madame fait signe.
Le rat de madame plonge dans un aquarium qui déborde.
L'eau de l'aquarium détrempe une motte de terre.
Dans la terre pousse une bulle de BD qui contient un mot.
La bulle se colle sur l'objectif d'une caméra qui filme la chambre.
La caméra filme un réveil qui sonne le matin.
Le réveil sonne le départ d'un train-traîneau.
Le traîneau colle une étiquette « genre » sur le front de René, qui est gêné.
René arrache l'étiquette et la colle sur le torse d'un culturiste.
Le culturiste défile comme un mannequin de mode.
Le mannequin marche jusqu'à l'endroit où un loup crie « go ! ».
Le loup poursuit un mari en habit de noces qui court tôt le matin.
Le mari porte un bébé qui hurle dans son berceau.
Les cris du bébé font tomber une arme posée sur une armure.
L'arme tire un gros point noir sur le mur.
Le point noir est examiné par un docteur au stéthoscope.
Le docteur ausculte une bobine de film qui défile dans un projecteur.
Le projecteur éblouit un appareil photo, qui crépite de flashs.
Un flash fait éclater le ruban d'arrivée « FINE ».
Après la ligne d'arrivée, les cartables filent vers l'école.
Un cartable atterrit sur le capot où le chef est assis.
Le chef allume un feu en frottant deux noix de coco comme un fou.
Le feu réchauffe le reste du repas dans une barquette du resto.
La barquette est lancée sur un champ de bataille de guerre.
Un chien traverse la bataille avec une canne dans la gueule.
Le chien dépose la canne sur le plateau de jeu d'un jockey.
Le jockey reçoit un plateau en or servi au dîner : un ordre.
Le plateau en or reflète tout, comme le miroir de vérité.
Le miroir tombe sur un pied géant posé sur un piédestal.
Le pied pousse une voile qui se gonfle d'envie de partir.
La voile fait chavirer un code civil qui rit tôt : « Dis, rit tôt ! ».
Le code civil rit si fort qu'un cœur saute sur ses jambes de coureur.
Le cœur coureur traverse un pays aisé couvert de lingots.
Un lingot sert de presse-livre dans la vitrine du libraire.
Du livre sort un génie qui devient le parent de Tore.
Le génie tend à Tore un plateau de service chargé d'une faveur.
La faveur déballée est un gyrophare qui tourne.
Le gyrophare éclaire un minuscule sablier qu'on tend à Timo.
Timo retourne le sablier et le temps file vers l'atelier des verbes, niche 00 : « être ».
""".strip().split("\n")
assert len(L) == 100, len(L)
for r, l in zip(d["pieces"][0]["niches"], L):
    r["lien"] = l
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print("ok")
