# Pièce 1 — Noms (palais mental 3D italien)
# Colonnes : fr | it | prononciation | zipf_fr | zipf_it | mot_cle | scene | decryptage | formes | lien(n -> n+1)
import json, os

R = r"""
la chose|la cosa|KO-za|5.9|6.2|Cosaque|Un Cosaque danse en jonglant avec une chose mystérieuse emballée d'un point d'interrogation.|cosa ≈ Cosaque ; le paquet « ? » = une chose|pl. le cose|Le Cosaque lance son paquet « ? » qui frappe une grande horloge et la fait sonner.
le temps|il tempo|TÈM-po|6.0|5.6|tempo|Une horloge géante bat le tempo comme un métronome de chef d'orchestre.|ressemble au français « tempo » (musique)|pl. i tempi ; aussi « la météo » : che tempo fa ?|Le balancier de l'horloge bat si fort qu'il assomme un bonhomme qui passait.
l'homme|l'uomo|OUO-mo|6.0|5.7|« Oh ! Momo »|Un homme moustachu s'écrie « Oh ! » en voyant le singe Momo lui grimper sur les épaules.|uomo ≈ « oh, Mo » ; le bonhomme = l'homme|pl. irrégulier gli uomini|Momo arrache à l'homme son cœur battant et le gave de vitamines.
la vie|la vita|VI-ta|5.9|5.9|vitamine|Une bougie de vie avale des comprimés de vitamines et sa flamme double de taille.|vita = vie (latin), d'où « vitamine »|pl. le vite|La flamme de vie grandit jusqu'à devenir un soleil levant ; George crie « non ! ».
le jour|il giorno|DJOR-no|5.9|5.8|« George, non ! »|Le soleil se lève en pleine chambre et George crie « non ! » en se cachant sous la couette.|gior-no ≈ « George, non »|pl. i giorni ; buongiorno = bonjour|George balance son réveil qui fait volte-face et compte « 1 fois, 2 fois ».
la fois|la volta|VOL-ta|5.8|5.7|volte-face|Un compteur « ×1, ×2, ×3 » fait volte-face à chaque fois qu'on l'appelle.|volta ≈ volte-face (tour)|una volta = une fois, due volte = deux fois|Le compteur tournoyant atterrit dans la main de Manon.
la main|la mano|MA-no|5.9|5.6|Manon|Manon tend une main géante gantée de blanc qui serre toutes les autres mains.|ma-no ≈ Manon ; latin manus (manuel)|féminin en -o ! pl. irrégulier le mani|La main de Manon enfile un calendrier sur un gros anneau.
l'an / l'année|l'anno|AN-no|5.9|5.8|anneau|Les 12 pages d'un calendrier sont enfilées sur un gros anneau doré qui tourne.|anno ≈ anneau (le cycle) ; attention : ano ≠ anno|pl. gli anni ; quanti anni hai ? = quel âge as-tu ?|L'anneau roule et s'emboîte autour d'un globe terrestre comme un anneau de Saturne.
le monde|il mondo|MON-do|5.9|5.5|mondovision|Un globe terrestre est retransmis en mondovision sur mille écrans.|ressemble : mondo = monde|tutto il mondo = tout le monde (le monde entier)|Du globe sort une femme qui distribue des cartes à jouer.
la femme|la donna|DON-na|5.9|5.5|donne (cartes)|Une femme élégante donne les cartes autour d'une table de poker.|donna ≈ « donne » ; cf. Madone (ma donna)|épouse = la moglie|Une carte lancée par la femme se plante dans un œil qui regarde par un kiosque.
l'œil|l'occhio|OK-kio|5.6|5.0|au kiosque|Un œil géant regarde par la vitrine d'un kiosque à journaux.|oc-chio ≈ « au kiosque » ; latin oculus (oculiste)|pl. gli occhi|L'œil cligne et fige un chronomètre « mémento ».
le moment|il momento|mo-MÈN-to|5.8|5.5|mémento|Un chronomètre figé porte une étiquette « mémento ».|ressemble : momento = moment|un momento ! = un instant !|Le chronomètre roule jusqu'à une porte qu'il défonce.
la porte|la porta|POR-ta|5.7|5.2|porte-à-faux|Une porte tient en porte-à-faux sur un seul gond, battante.|ressemble : porta = porte ; mise sur le -a final|pl. le porte|La porte claque sur une tête qui passe un test.
la tête|la testa|TÈS-ta|5.7|5.2|test|Une tête passe un test, crayon entre les dents, sous l'œil d'un examinateur.|testa ≈ test (ancien fr. « teste »)|pl. le teste|La tête donne un coup qui envoie un pot sur un col de montagne.
le coup|il colpo|KOL-po|5.7|4.9|col + pot|Un coup de poing envoie un pot de fleurs voler jusqu'au sommet d'un col.|col-po ≈ « col » + « pot »|colpo di fulmine = coup de foudre|Le pot retombe sur le crâne d'un père pas drôle en soutane.
le père|il padre|PA-dré|5.7|5.3|padre (« pas drôle »)|Un père en soutane de padre ne rit jamais : « pas drôle ».|padre = père (aussi le prêtre)|papà = papa|Le padre bénit une mère qui agite un drapeau de Madrid.
la mère|la madre|MA-dré|5.6|5.2|Madrid|Une mère agite un drapeau de Madrid en berçant son bébé.|madre ≈ Madrid ; ressemble à mère|mamma = maman|La mère pose son bébé dans une case au toit de paille.
la maison|la casa|KA-za|5.8|5.7|case|Une maison est une case au toit de paille, avec boîte aux lettres.|casa ≈ case, casanier|a casa = à la maison ; pl. le case|De la case s'envole une note de musique qui monte vers la lune.
la nuit|la notte|NOT-té|5.8|5.3|note|La lune écrit une note de musique sur le ciel de la nuit.|not-te ≈ « note » ; latin nox|buonanotte = bonne nuit|La note tombe dans le berceau d'un bambin.
l'enfant|il bambino|bam-BI-no|5.7|5.3|bambin|Un bambin joufflu tape sur un tambour.|ressemble : bambino ≈ bambin|f. la bambina ; aussi il figlio (fils, enfant de)|Le tambour du bambin rassemble une foule de gens gentils.
les gens|la gente|DJÈN-té|5.6|5.1|gentil|Une foule de gens tous gentils se tient par la main.|gente ≈ gentil ; singulier collectif en italien|la gente è… (verbe au singulier) ; variante : le persone|La foule crie un mot qui jaillit comme une parole en bulle.
le mot|la parola|pa-RO-la|5.7|5.4|parole|Un mot sort d'une bouche en bulle de BD : une parole.|parola = mot (et parole)|pl. le parole ; parolaccia = gros mot|La bulle se pose sur une place libre, un poste.
la place|il posto|POS-to|5.6|5.3|poste|Une place libre est marquée d'un poste de radio posé sur la chaise.|posto ≈ poste ; place (siège, endroit)|variante : la piazza (place publique)|La radio annonce un pays aisé et prospère.
le pays|il paese|pa-É-zé|5.6|5.2|pays aisé|Un pays aisé : carte couverte de lingots.|pa-e-se ≈ « pays aisé »|aussi « village » ; pl. i paesi|D'un lingot sort une horloge en or.
l'heure|l'ora|O-ra|5.7|5.4|or|Une horloge en or brille au poignet.|ora ≈ or ; aussi « maintenant »|che ore sono ? = quelle heure est-il ?|L'horloge en or tombe dans un aquarium.
l'eau|l'acqua|AK-koua|5.6|5.1|aquarium|Un aquarium déborde d'eau sur le carrelage.|acqua ≈ aqua(rium)|acqua minerale|Un ami nage dans l'aquarium et salue.
l'ami|l'amico|a-MI-ko|5.6|5.1|ami + co|Un ami à mi-côte tend la main.|ressemble : amico = ami|pl. gli amici ; f. l'amica|L'ami gonfle ses joues et souffle un air d'opéra.
l'air|l'aria|A-ria|5.6|4.9|aria (opéra)|Un ventilateur souffle et une cantatrice chante une aria.|aria = air (et air d'opéra)|all'aria aperta = en plein air|La cantatrice se décale sur le côté, vers une latte de parquet.
le côté|il lato|LA-to|5.6|4.9|latéral|Un côté (flanc d'un cube) est poussé latéralement.|lato ≈ latéral|da un lato… dall'altro = d'un côté… de l'autre|Le cube glisse contre un professeur qui a raison, rage au nez.
la raison|la ragione|ra-DJO-né|5.6|4.9|rage au nez|Un professeur a raison, la rage au nez, en pointant le tableau.|ra-gio-ne ≈ « rage au nez »|avere ragione = avoir raison|Le professeur tape le tableau qui se brise sur un ouvrier au lavoir.
le travail|il lavoro|la-VO-ro|5.6|5.3|lavoir|Un ouvrier travaille à frotter du linge au lavoir.|la-vo-ro ≈ « lavoir » ; lavorare = travailler|pl. i lavori (travaux)|L'ouvrier brode un nom sur le linge.
le nom|il nome|NO-mé|5.6|5.0|nommé|Un badge « Je m'appelle… » est nommé à haute voix.|ressemble : nome = nom|come ti chiami ? (pas nome) = comment tu t'appelles ?|Le badge parle avec une voix qui fait bouger vos chaises.
la voix|la voce|VO-tché|5.5|5.0|vos chaises|Une voix puissante sort d'un micro et fait trembler vos chaises.|vo-ce ≈ « vos chaises » ; cf. vocal|ad alta voce = à voix haute|Les chaises se cassent : c'est un cas.
le cas|il caso|KA-zo|5.5|5.2|casse|Un dossier « cas n°1 » casse en deux.|ressemble : caso = cas|per caso = par hasard ; in ogni caso = en tout cas|Le dossier tombe dans les mains d'un monsieur qui fait signe au rez-de-chaussée.
le monsieur|il signore|si-GNO-ré|5.5|5.1|signe au rez|Un monsieur en chapeau fait signe au rez-de-chaussée.|si-gno-re ≈ « signe au rez »|devant un nom : il signor Rossi|Le monsieur tend une demande collée sur son dos.
la question|la domanda|do-MAN-da|5.6|5.1|dos + mandat|Un point d'interrogation géant porté sur le dos avec un mandat.|domanda = question (faux ami partiel de « demande »)|fare una domanda = poser une question|Le point d'interrogation pique une faucheuse : la mort.
la mort|la morte|MOR-té|5.6|5.0|mort|La faucheuse brandit sa faux.|ressemble : morte = mort|attention : morto = mort (adjectif)|La faucheuse rejoint un champ de bataille de guerre.
la guerre|la guerra|GOUÈR-ra|5.6|5.0|guerre|Un champ de bataille avec deux armées.|ressemble : guerra = guerre (r roulé)|pl. le guerre|Un éclair tombe du ciel : « Dis, oh ! » crie un dieu barbu.
le dieu|il dio|DI-o|5.5|5.3|« Dis, oh ! »|Un dieu barbu sur un nuage crie « Dis, oh ! ».|dio ≈ « dis, oh » ; latin deus|pl. irrégulier gli dei ; Dio mio !|Le dieu lance un rat qui gâte la robe d'une fille.
la fille|la ragazza|ra-GAT-tsa|5.6|5.0|rat gâte ça|Un rat gâte la robe d'une jeune fille.|ra-gaz-za ≈ « rat gâte ça »|fille (enfant de) = la figlia|La fille appelle son filleul à l'aide.
le fils|il figlio|FI-lio|5.4|4.9|filleul|Un fils et son parrain : le filleul.|fi-glio ≈ filleul (gli = « lli »)|pl. i figli (aussi « enfants »)|Le filleul raconte une story sur un livre de contes.
l'histoire|la storia|STO-ria|5.5|5.1|story|Un livre de contes : une story.|storia ≈ story ; histoire (récit et passé)|pl. le storie|Une ampoule (idée) jaillit du livre.
l'idée|l'idea|i-DÈ-a|5.5|5.0|idée|Une ampoule s'allume au-dessus d'une tête.|ressemble : idea = idée|non ne ho idea = je n'en ai aucune idée|L'ampoule éclaire une ville où court un guépard.
la ville|la città|tchit-TA|5.5|5.1|Cheetah|Un guépard (cheetah) court dans les rues de la ville.|cit-tà ≈ « Cheetah » ; cité|invariable : le città|Le guépard renverse une vitrine de soldes.
l'argent|i soldi|SOL-di|5.5|5.0|soldes|Une vitrine de soldes déborde de billets.|soldi ≈ soldes ; argent (métal) = l'argento|toujours au pluriel ; variante : il denaro|Les billets recouvrent un corps de culturiste.
le corps|il corpo|KOR-po|5.5|4.8|corporel|Un corps de culturiste prend la pose.|ressemble : corpo = corps|pl. i corpi|Le culturiste exhibe un cœur qui court sur des jambes de coureur.
le cœur|il cuore|KOUO-ré|5.5|5.0|coureur|Un cœur rouge court avec des jambes de coureur.|cuo-re ≈ « coureur » ; latin cor|pl. i cuori|Le cœur franchit une ligne d'arrivée « FINE ».
la fin|la fine|FI-né|5.5|5.0|fine|Un ruban de fin de course marqué « FINE ».|ressemble : fine = fin (aussi fin du film)|alla fine = à la fin|Derrière la ligne, un coureur a besoin d'un bisou et reçoit un gnon.
le besoin|il bisogno|bi-ZO-gno|5.4|4.8|bisou, gnon|Quelqu'un a besoin d'un bisou et reçoit un gnon.|bi-so-gno ≈ « bisou, gnon »|avere bisogno di = avoir besoin de|Le gnon fait trébucher un pied sur un piédestal.
le pied|il piede|PIÈ-dé|5.4|4.7|piédestal|Un pied géant posé sur un piédestal.|ressemble : piede = pied|a piedi = à pied|Le pied écrase de la terre qui jaillit.
la terre|la terra|TÈR-ra|5.5|5.0|terre|Une motte de terre brune.|ressemble : terra = terre|per terra = par terre|De la motte pousse une boussole qui indique le sens.
le sens|il senso|SÈN-so|5.5|5.0|sensé|Une boussole indique le sens.|ressemble : senso = sens|senso unico = sens unique|La boussole se transforme en mannequin de mode.
la façon|il modo|MO-do|5.5|5.2|mode|Un mannequin de mode défile d'une certaine façon.|modo = manière (cf. mode = manière)|in questo modo = de cette façon|Le mannequin rejoint une photo de famille.
la famille|la famiglia|fa-MI-glia|5.5|5.0|famille|Une photo de famille sur une cheminée.|ressemble : famiglia ; gli = « lli »|pl. le famiglie|Tous les membres lèvent les yeux en un regard qui se garde dans le dos.
le regard|lo sguardo|ZGOUAR-do|5.4|4.5|« s'garde, dos ! »|Un regard en jumelles se garde dans le dos.|sguardo ≈ (re)garde ; s + gu|guardare = regarder|Les jumelles fixent un point.
le point|il punto|POUN-to|5.5|5.0|ponctuel|Un gros point noir ponctuel.|ressemble : punto = point|punto di vista = point de vue|Le point devient un poing au bout d'un bras chaud.
le bras|il braccio|BRAT-tcho|5.4|4.6|bras chaud|Un bras chaud fume.|brac-cio ≈ « bras chaud »|pl. irrégulier le braccia (f.)|Le bras pointe une estrade dans la rue.
la rue|la strada|STRA-da|5.5|5.1|estrade|Une estrade au milieu de la rue.|strada ≈ estrade (latin strata)|variante : la via (rue nommée)|Sur l'estrade, une machine à quatre roues : la voiture.
la voiture|la macchina|MAK-ki-na|5.4|5.0|machine|Une voiture-machine fumante.|macchina ≈ machine|variante : l'auto (f.)|La voiture recule dans une chambre où une caméra filme.
la chambre|la camera|KA-mé-ra|5.4|4.8|caméra|Une caméra filme une chambre.|camera ≈ caméra — faux ami : camera = chambre|camera da letto = chambre à coucher|La caméra filme un fantôme : la peur.
la peur|la paura|pa-OU-ra|5.4|4.9|pas hourra|Un fantôme fait peur : pas hourra !|pa-u-ra ≈ « pas hourra »|avere paura = avoir peur|Le fantôme part à la soirée : ce sera la fête.
le soir|la sera|SÉ-ra|5.4|4.9|ce sera|Ce soir, ce sera la fête : coucher de soleil.|sera ≈ « ce sera »|buonasera = bonsoir|Le soleil se couche et se relève : mattina.
le matin|la mattina|mat-TI-na|5.4|4.8|matin|Un réveil sonne au matin.|ressemble : mattina = matin|di mattina = le matin|Le réveil saute sur une mésange.
le mois|il mese|MÉ-zé|5.3|4.8|mes aises|Un calendrier mensuel où l'on est à mes aises.|me-se ≈ « mes aises »|pl. i mesi|Le calendrier révèle sept jours : la semaine.
la semaine|la settimana|set-ti-MA-na|5.4|4.8|sept + Ti Mana|Sept jours (sette) portés par Ti Mana.|setti-mana ≈ sette = sept|pl. le settimane|Ti Mana compte les minutes.
la minute|il minuto|mi-NOU-to|5.4|4.8|minute|Un sablier d'une minute.|ressemble : minuto|masculin ! un minuto|Le sablier se couche dans un lit et boit du lait tôt.
le lit|il letto|LÈT-to|5.4|4.7|lait tôt|On boit du lait tôt au lit.|let-to ≈ « lait tôt »|pl. i letti|Le verre de lait roule sur la table et on t'a volé l'eau.
la table|il tavolo|TA-vo-lo|5.4|4.6|t'as volé l'eau|À table : « T'as volé l'eau ! »|ta-vo-lo ≈ « t'as volé l'eau »|masculin ! ; tavola (table mise)|La carafe vide frappe un livre de libraire.
le livre|il libro|LI-bro|5.4|4.8|libraire|Un livre en librairie.|ressemble : libro ≈ libraire|pl. i libri|Le livre tombe à la mer à marée haute.
la mer|il mare|MA-ré|5.4|4.9|marée|La mer à marée haute.|mare ≈ marée|masculin ! ; al mare|La vague éteint un feu de fou aux cocos.
le feu|il fuoco|FOUO-ko|5.4|4.6|fou aux cocos|Un fou fait du feu avec des cocos.|fuo-co ≈ « fou… co »|fuochi d'artificio = feux d'artifice|Le feu illumine une louche pleine de lumière.
la lumière|la luce|LOU-tché|5.4|4.7|louche|Une louche verse de la lumière.|lu-ce ≈ « louche » ; cf. lucide|accendere la luce = allumer|La louche verse du sang gai.
le sang|il sangue|SAN-goué|5.4|4.5|sang gai|Du sang gai qui danse.|san-gue ≈ « sang gai »|sanguinare = saigner|Le sang éclabousse un frère fraternel.
le frère|il fratello|fra-TÈL-lo|5.3|4.7|fraternel|Deux frères fraternels s'embrassent.|fratello ≈ fraternel|pl. i fratelli|Le frère attrape une sauterelle : sa sœur.
la sœur|la sorella|so-RÈL-la|5.3|4.6|sauterelle|Une sauterelle avec un nœud : la sœur.|so-rel-la ≈ « sauterelle »|pl. le sorelle|La sauterelle saute sur un garçon qui gâte ça aussi.
le garçon|il ragazzo|ra-GAT-tso|5.4|4.8|rat gâte ça|Un garçon dont le rat gâte la casquette.|ragazzo = garçon (cf. ragazza)|garçon de café = il cameriere|Le garçon partage une part de gâteau.
la part|la parte|PAR-té|5.4|5.3|part|Une part de gâteau.|ressemble : parte = part, partie|da parte di = de la part de|La part est vendue dans une affaire.
l'affaire|l'affare|af-FA-ré|5.4|4.6|affaire|Une mallette d'affaire.|ressemble : affare (masc.)|gli affari = les affaires ; variante : la faccenda|La mallette s'ouvre sur l'ordre d'un or dîné.
l'ordre|l'ordine|OR-di-né|5.4|4.7|or dîné|Un ordre servi sur un plateau d'or au dîner.|or-di-ne ≈ « or dîné » ; ordinal|in ordine = en ordre|Le plateau porte le sceau de l'État.
l'état|lo stato|STA-to|5.4|5.0|statut|L'État : une statue de Marianne.|stato ≈ statut ; aussi participe « été »|Stati Uniti = États-Unis|La statue tombe au fond d'un puits.
le fond|il fondo|FON-do|5.4|4.6|fond|Le fond d'un puits.|ressemble : fondo = fond|in fondo = au fond|Au fond, un problème mathématique masculin.
le problème|il problema|pro-BLÈ-ma|5.4|5.1|problème|Une équation insoluble au tableau.|ressemble ; masculin en -a !|pl. i problemi|Le tableau est saisi par la police.
la police|la polizia|po-li-TSI-a|5.3|4.7|police|Une voiture de police.|ressemble : polizia (z = ts)|poliziotto = policier|La police amène un docteur.
le docteur|il dottore|dot-TO-ré|5.3|4.6|docteur|Un docteur au stéthoscope.|ressemble : dottore|dottoressa = docteure|Le docteur ausculte un roi qui chante ré.
le roi|il re|RÉ|5.3|4.7|ré (note)|Un roi qui chante la note ré.|re = roi (latin rex)|invariable : i re ; la regina = la reine|Le roi chante l'été de l'âge.
l'âge|l'età|é-TA|5.3|4.6|été|Le temps d'un été : l'âge.|e-tà ≈ « été » ; invariable|alla mia età = à mon âge|L'été arrive en lieu en courant comme un loup.
le lieu|il luogo|LOUO-go|5.3|4.7|loup, go !|Un loup (« go ! ») à un lieu-dit.|luo-go ≈ « loup, go » ; latin locus|aver luogo = avoir lieu|Le loup entre dans un bureau : « ouf, fichu ! ».
le bureau|l'ufficio|ouf-FI-tcho|5.3|4.6|ouf, fichu !|Un employé au bureau : « Ouf, fichu ! ».|uf-fi-cio ≈ « ouf, fichu » ; office|meuble bureau = la scrivania|L'employé file à l'école.
l'école|la scuola|SKOUO-la|5.3|4.7|scolaire|Une école avec cartables.|scuola ≈ scolaire|a scuola = à l'école|Un cartable vole par la fenêtre.
la fenêtre|la finestra|fi-NÈS-tra|5.3|4.5|fenêtre|Une fenêtre ouverte.|ressemble : finestra|pl. le finestre|Par la fenêtre, on voit le ciel tchèque.
le ciel|il cielo|TCHÈ-lo|5.3|4.6|tchèque l'eau|Le ciel bleu où un Tchèque arrose.|cie-lo ≈ « tchè-lo » ; latin caelum|pl. i cieli|Une carte vole dans le ciel.
le papier|la carta|KAR-ta|5.3|4.9|carte|Une feuille de papier en carte.|carta = papier (cf. carte)|carta igienica ; carta di credito|La carte se colle sur un visage qui vise.
le visage|il viso|VI-zo|5.3|4.5|vise|Un visage qui vise.|vi-so ≈ « vise »|variante : la faccia, il volto|Le visage fixe un mur.
le mur|il muro|MOU-ro|5.3|4.5|mur|Un mur de briques.|ressemble : muro ; mura (remparts)|pl. i muri ; le mura (enceinte)|Sur le mur, un cœur d'amour.
l'amour|l'amore|a-MO-ré|5.4|5.2|amour|Un cœur d'amour.|ressemble : amore|amore mio !|L'amour se déclare vérité.
la vérité|la verità|vé-ri-TA|5.3|4.8|vérité|Un miroir de vérité.|ressemble : verità (accent final)|invariable|Le miroir reflète un traîneau : le train.
le train|il treno|TRÈ-no|5.2|4.6|traîneau|Un train-traîneau.|tre-no ≈ « traîneau »|in treno = en train|Le train sonne un téléphone.
le téléphone|il telefono|té-LÈ-fo-no|5.3|4.9|téléphone|Un téléphone qui sonne.|ressemble ; accent sur LÈ|al telefono = au téléphone|Le téléphone est saisi par un chef au capot.
le chef|il capo|KA-po|5.3|4.9|capot|Un chef assis sur un capot.|capo ≈ capitaine ; tête|capo = chef ; cuisinier = lo chef|Le chef salue une signora.
madame|la signora|si-GNO-ra|5.4|4.8|signe au rat|Madame fait signe au rat.|si-gno-ra ≈ « signe au rat »|signorina = mademoiselle|Le rat de madame court jusqu'à l'atelier des verbes : « être ».
"""

rows = []
for i, line in enumerate([l for l in R.strip().split("\n") if l.strip()]):
    p = line.split("|")
    assert len(p) == 10, (i, len(p), line)
    fr, it, pr, zf, zi, mc, sc, de, fo, li = p
    rows.append(dict(n=i, fr=fr, cible=it, prononciation=pr, zipf_fr=float(zf), zipf_cible=float(zi),
                     zipf_source="estimé", mot_cle=mc, scene=sc, decryptage=de, formes=fo, lien=li,
                     categorie="noms", sous_categories=["noms"]))
assert len(rows) == 100, len(rows)
for a in ("fr", "cible"):
    vals = [r[a] for r in rows]
    d = {v for v in vals if vals.count(v) > 1}
    assert not d, (a, d)

data = {"langue": "italien", "code": "it-IT", "pieces": [
    {"id": "noms", "titre_fr": "Les noms", "titre_cible": "I nomi", "decor": "marché italien", "niches": rows}]}
os.makedirs("/home/claude/pm_italien", exist_ok=True)
json.dump(data, open("/home/claude/pm_italien/data_italien.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(rows))
