"""Étape 2 : chaîne de liens n -> n+1 pour l'ordre « parlé »."""
import json
P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))
L = """
George balance son réveil, qui s'enfile sur l'anneau doré du calendrier.
L'anneau roule et heurte le compteur « ×1, ×2 », qui fait volte-face.
Le compteur tournoyant percute le chronomètre « mémento » et le fige.
Le chronomètre roule jusqu'à une case et sonne à sa porte.
De la case sort un padre en soutane, pas drôle du tout.
Le padre bénit un bambin qui tape sur son tambour.
Le bambin tape si fort que l'horloge en or tombe de son poignet.
L'horloge en or atterrit sur une chaise libre où trône un poste de radio.
La radio joue et un ami accourt de la mi-côte.
L'ami lève les bras au ciel et un dieu barbu lui crie « Dis, oh ! ».
Le dieu laisse tomber un drapeau de Madrid dans les bras d'une mère.
La mère agite le drapeau et une foule de gens gentils la suit.
La foule pousse un aquarium, qui déborde.
L'eau éclabousse une fille dont un rat gâte la robe.
La fille appelle à l'aide un monsieur qui fait signe au rez-de-chaussée.
Le monsieur fonce dans une vitrine de soldes pleine de billets.
Avec les billets, un Cosaque achète une chose emballée d'un « ? ».
Le Cosaque donne un coup au paquet, qui envoie un pot sur un col.
Le pot dévale du col jusque dans la ville où court un guépard.
Le guépard bondit dans la photo de famille posée sur la cheminée.
La famille sort de la photo et monte sur une estrade en pleine rue.
Sur l'estrade, quelqu'un réclame un bisou et reçoit un gnon.
Le gnon renverse un sablier d'une minute.
Le sable qui coule écrit une équation insoluble au tableau.
L'équation fait fuir un rat auquel madame fait signe.
Madame tend son rat à une maman qui s'écrie « mamma mia ! ».
La maman passe son enfant au papa, qui le hisse sur ses épaules.
Perché là-haut, l'enfant règle le tempo d'une horloge-métronome.
Le balancier assomme un homme qui crie « Oh ! » sous le singe Momo.
Momo arrache la faux des mains de la Mort.
La Mort tend un cadeau à son filleul.
Le filleul grimpe sur un pied géant posé sur un piédestal.
Le pied écrase l'accélérateur d'une voiture-machine.
La voiture recule dans une chambre filmée par une caméra.
La caméra filme le coucher de soleil : ce soir, ce sera la fête.
Le soleil couché se relève et un réveil sonne le matin.
Le réveil sonne sept coups, un pour chaque jour porté par Ti Mana.
Ti Mana boit son lait tôt, au lit.
Le verre de lait roule jusqu'à la table : « T'as volé l'eau ! ».
La carafe vide tombe sur un livre de libraire.
Le livre est ouvert par un garçon dont un rat gâte la casquette.
Le rat mord le garçon, qui court chez le docteur.
Le docteur décroche un téléphone qui sonne sans arrêt.
Le téléphone vibre sur le capot où le chef est assis.
Le chef avale des vitamines et sa bougie de vie double de taille.
La flamme de vie se pose dans la main gantée de Manon.
La main de Manon fait tourner le globe, retransmis en mondovision.
Du globe sort une femme qui donne les cartes.
La femme annonce un mot qui jaillit en bulle de BD.
La bulle se pose sur le calendrier du mois où je suis à mes aises.
Deux frères fraternels se disputent la page du calendrier.
Le frère attrape une sauterelle à nœud : sa sœur.
La sauterelle saute sur le bureau d'un employé : « Ouf, fichu ! ».
L'employé lance son cartable vers la porte de l'école.
À l'école, on distribue à chacun une carte de papier.
Le papier sert à emballer un truc dans une robe de soirée.
Le truc est ramassé par un mec qui porte le badge « TYPE ».
Le mec chante une note qui monte jusqu'à la lune.
La lune éclaire un pays aisé couvert de lingots.
Un lingot glisse sur le côté d'un cube et le pousse.
Le cube heurte un professeur qui a raison, la rage au nez.
Le professeur brise le tableau sur un ouvrier au lavoir.
L'ouvrier brode un nom sur le linge qu'il lave.
Le badge nommé se colle au dos du point d'interrogation à mandat.
Le point d'interrogation fait sursauter un fantôme : pas hourra !
Le fantôme tombe dans une flaque de sang gai qui danse.
Le sang se répand en forme de cœur d'amour.
Le cœur d'amour monte dans un train-traîneau.
Le traîneau défonce une porte en porte-à-faux.
La porte claque sur une tête qui passe un test.
La tête fend un dossier « cas n°1 », qui casse en deux.
Du dossier tombe un livre de story.
Une ampoule jaillit des pages du livre.
L'ampoule éclaire le ruban d'arrivée « FINE ».
Derrière la ligne, une boussole indique le sens.
La boussole se déplie en mannequin de mode.
Le mannequin pose un gros point noir sur le sol.
Le point noir est un sabot posé par la police.
La police confisque un trèfle à quatre feuilles qui fait fortune.
Le trèfle ouvre un coffre au trésor qui murmure « mon chéri ».
L'éclat du trésor aveugle un œil géant au kiosque.
L'œil cligne, un ventilateur souffle et une cantatrice chante une aria.
L'aria déclenche une guerre entre deux armées.
Sur le champ de bataille, on se dispute une part de gâteau.
La part de gâteau est vendue dans une mallette d'affaire.
La mallette s'ouvre sur un plateau en or servi au dîner : un ordre.
Le plateau porte le sceau de l'État, une statue de Marianne.
La statue tombe au fond d'un puits.
Au fond du puits, un mari en habit de noces court, tôt le matin.
Le mari porte un bébé qui hurle.
Le bébé hurle si fort que sa voix fait trembler vos chaises.
Les chaises tombent sur un culturiste, qui les repousse.
Le culturiste exhibe un cœur qui court sur des jambes de coureur.
Le cœur coureur s'enfonce dans une motte de terre.
La motte de terre fleurit en un seul été.
L'été arrive au lieu-dit en courant comme un loup.
Le loup se voit dans le miroir de vérité.
Le miroir se brise en cotillons de fête.
Les cotillons tombent dans une tasse de café fumante.
La vapeur du café monte vers l'atelier des verbes, à la niche 00 : « être ».
""".strip().split("\n")
assert len(L) == 100, len(L)
for r, l in zip(d["pieces"][0]["niches"], L):
    r["lien"] = l
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print("ok")
