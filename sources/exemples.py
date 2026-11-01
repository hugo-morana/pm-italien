"""Phrases d'exemple à l'oral (mot employé comme nom) + champs audio."""
import json
P = "/home/claude/pm_italien/data_italien.json"
d = json.load(open(P))
E = """
le jour|Un jour, je t'emmène à Rome.|Un giorno ti porto a Roma.
l'an / l'année|L'année prochaine, on part en Italie.|L'anno prossimo andiamo in Italia.
la fois|Je te l'ai dit cent fois !|Te l'ho detto cento volte!
le moment|C'est pas le moment, là.|Non è il momento, adesso.
la maison|Je rentre à la maison.|Torno a casa.
le père|Mon père m'appelle tous les soirs.|Mio padre mi chiama ogni sera.
l'enfant|L'enfant dort enfin.|Il bambino finalmente dorme.
l'heure|T'as l'heure, s'il te plaît ?|Hai l'ora, per favore?
la place|Il reste une place à côté de moi.|C'è ancora un posto accanto a me.
l'ami|C'est mon meilleur ami.|È il mio migliore amico.
le dieu|Mon Dieu, quelle chaleur !|Dio mio, che caldo!
la mère|Ta mère a appelé.|Ha chiamato tua madre.
les gens|Les gens sont sympas ici.|La gente è simpatica qui.
l'eau|Tu veux de l'eau ?|Vuoi dell'acqua?
la fille|C'est une fille super gentille.|È una ragazza gentilissima.
le monsieur|Le monsieur, là-bas, vous attend.|Il signore laggiù la aspetta.
l'argent|J'ai plus d'argent sur moi.|Non ho più soldi con me.
la chose|C'est la chose la plus drôle de la soirée.|È la cosa più divertente della serata.
le coup|Il a pris un coup sur la tête.|Ha preso un colpo in testa.
la ville|J'adore cette ville.|Adoro questa città.
la famille|Toute la famille est là.|C'è tutta la famiglia.
la rue|Il habite dans ma rue.|Abita nella mia strada.
le besoin|J'ai besoin d'un café.|Ho bisogno di un caffè.
la minute|Attends une minute !|Aspetta un minuto!
le problème|Pas de problème !|Nessun problema!
madame|Bonjour madame, vous désirez ?|Buongiorno signora, desidera?
maman|Maman, j'ai faim !|Mamma, ho fame!
papa|Papa arrive dans dix minutes.|Papà arriva fra dieci minuti.
le temps|J'ai pas le temps, désolé.|Non ho tempo, scusa.
l'homme|Cet homme, je le connais.|Quell'uomo lo conosco.
la mort|Elle a peur de la mort.|Ha paura della morte.
le fils|Son fils a dix ans.|Suo figlio ha dieci anni.
le pied|J'ai mal au pied.|Mi fa male il piede.
la voiture|On prend la voiture ?|Prendiamo la macchina?
la chambre|Ta chambre est en bazar !|La tua camera è in disordine!
le soir|Le soir, je suis crevé.|La sera sono stanco morto.
le matin|Le matin, je bois un café.|La mattina bevo un caffè.
la semaine|On se voit la semaine prochaine.|Ci vediamo la settimana prossima.
le lit|Je vais au lit.|Vado a letto.
la table|À table, c'est prêt !|A tavola, è pronto!
le livre|Tu m'as rendu mon livre ?|Mi hai restituito il libro?
le garçon|C'est un garçon très drôle.|È un ragazzo molto simpatico.
le docteur|Il faut appeler le docteur.|Bisogna chiamare il dottore.
le téléphone|Ton téléphone sonne !|Ti suona il telefono!
le chef|Le chef est de mauvaise humeur.|Il capo è di cattivo umore.
la vie|C'est la vie !|È la vita!
la main|Lave-toi les mains !|Lavati le mani!
le monde|Le monde est petit !|Il mondo è piccolo!
la femme|Cette femme est incroyable.|Quella donna è incredibile.
le mot|J'ai pas compris un mot.|Non ho capito una parola.
le mois|Le mois prochain, je déménage.|Il mese prossimo trasloco.
le frère|Mon frère est en retard, comme d'hab.|Mio fratello è in ritardo, come al solito.
la sœur|Je te présente ma sœur.|Ti presento mia sorella.
le bureau|Je suis encore au bureau.|Sono ancora in ufficio.
l'école|Les enfants sont à l'école.|I bambini sono a scuola.
le papier|T'as un bout de papier ?|Hai un pezzo di carta?
le truc|C'est quoi, ce truc ?|Che roba è questa?
le mec|Ce mec est trop marrant.|Questo tipo è troppo divertente.
la nuit|Bonne nuit, à demain !|Buonanotte, a domani!
le pays|C'est un beau pays.|È un bel paese.
le côté|Mets-toi de ce côté.|Mettiti da questo lato.
la raison|T'as raison !|Hai ragione!
le travail|J'ai trop de travail.|Ho troppo lavoro.
le nom|C'est quoi ton nom ?|Qual è il tuo nome?
la question|J'ai une question.|Ho una domanda.
la peur|J'ai peur du noir.|Ho paura del buio.
le sang|Il y a du sang sur ta chemise !|C'è del sangue sulla tua camicia!
l'amour|C'est l'amour de ma vie.|È l'amore della mia vita.
le train|Mon train part à huit heures.|Il mio treno parte alle otto.
la porte|Ferme la porte, s'il te plaît.|Chiudi la porta, per favore.
la tête|J'ai mal à la tête.|Ho mal di testa.
le cas|Dans ce cas, on y va.|In questo caso, andiamo.
l'histoire|Raconte-moi une histoire.|Raccontami una storia.
l'idée|Bonne idée !|Buona idea!
la fin|À la fin, il a dit oui.|Alla fine ha detto di sì.
le sens|Ça n'a aucun sens.|Non ha nessun senso.
la façon|De toute façon, c'est trop tard.|In ogni modo, è troppo tardi.
le point|On fait le point demain.|Facciamo il punto domani.
la police|Appelle la police !|Chiama la polizia!
la chance|T'as de la chance !|Che fortuna!
le chéri|Tu viens, mon chéri ?|Vieni, tesoro?
l'œil|J'ai un truc dans l'œil.|Ho qualcosa nell'occhio.
l'air|T'as l'air fatigué.|Hai l'aria stanca.
la guerre|Mon grand-père a fait la guerre.|Mio nonno ha fatto la guerra.
la part|Tu veux ma part ?|Vuoi la mia parte?
l'affaire|C'est une bonne affaire !|È un buon affare!
l'ordre|Range ta chambre, c'est un ordre !|Metti in ordine la camera, è un ordine!
l'état|T'as vu dans quel état il est ?|Hai visto in che stato è?
le fond|Au fond, t'as raison.|In fondo, hai ragione.
le mari|Son mari est italien.|Suo marito è italiano.
le bébé|Le bébé pleure.|Il bebè piange.
la voix|T'as une belle voix.|Hai una bella voce.
le corps|J'ai mal partout, dans tout le corps.|Mi fa male tutto il corpo.
le cœur|Ça me brise le cœur.|Mi spezza il cuore.
la terre|Le téléphone est tombé par terre.|Il telefono è caduto per terra.
l'âge|À ton âge, j'étais pareil.|Alla tua età ero uguale.
le lieu|La fête a lieu samedi.|La festa ha luogo sabato.
la vérité|Dis-moi la vérité.|Dimmi la verità.
la fête|On fait une fête samedi.|Facciamo una festa sabato.
le café|Un café, s'il vous plaît.|Un caffè, per favore.
"""
rows = [l.split("|") for l in E.strip().split("\n")]
assert len(rows) == 100
for r, (fr, efr, eit) in zip(d["pieces"][0]["niches"], rows):
    assert r["fr"] == fr, (r["fr"], fr)
    r["exemple_fr"], r["exemple_cible"] = efr, eit
    b = f'audio/noms_{r["n"]:02d}'
    r["audio_mot"] = None      # remplacé par f"{b}_mot.mp3" quand le fichier est fourni
    r["audio_phrase"] = None   # remplacé par f"{b}_phrase.mp3"
d["audio"] = {"tts": "speechSynthesis it-IT (voix de l'appareil)",
              "fichiers": "audio/noms_NN_mot.mp3 et audio/noms_NN_phrase.mp3, prioritaires sur la synthèse"}
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print("ok")
