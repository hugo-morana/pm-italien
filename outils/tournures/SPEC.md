# Réécriture des tournures à trous (palais de vocabulaire italien)

Chaque item est une tournure française (`fr`) et sa traduction italienne (`it`) qui contiennent des
variables de trou : S, S2 (sujet), V, V2 (verbe conjugué), V_inf, V_sub, V_pp, V_cond, V_fut, V_imper,
V_ger, V_pass, C, C2 (complément), C_lieu, C_qn, C_adj, C_date, C_heure, C_mois, C_âge, C_nb, C_prix,
C_langue, C_nationalité, C_moment, C_temps, C2ando (erreur de saisie)… Les phrases d'exemple
`efr` / `eit` montrent un emploi réel : sers-t'en pour comprendre ce que chaque trou représente
(une personne ? une chose ? une proposition entière ?).

But : remplacer chaque variable par un équivalent lisible, comme dans un dictionnaire, pour que la
tournure se lise ET se prononce en entier (elle sera lue à voix haute par une voix de synthèse,
après développement des abréviations).

## Remplacements

Français (abréviations à écrire telles quelles) :
- sujet S → `qn` ; S2 → `qn d'autre`
- complément C/C2 → `qc` si c'est une chose, `qn` si c'est une personne (d'après le sens et l'exemple :
  « dire C à C2 » → « dire qc à qn », « aider C à V_inf C2 » → « aider qn à faire qc »)
- lieu (C_lieu, ou C qui est clairement un lieu) → `qqpart` (adapter la préposition : « aller à C_lieu » → « aller qqpart »)
- C_qn → `qn`
- verbe : toujours le verbe **faire**, à la forme demandée et **accordé avec son sujet** :
  V (présent) : « qn fait », « je fais », « nous faisons », « ils font » ; V_inf → faire ;
  V_sub → fasse/fassions… ; V_pp → fait ; V_cond → ferait/ferions… ; V_fut → fera… ;
  V_imper → fais/faites ; V_ger → en faisant ; V_pass → a fait (passé composé) ;
  V2 → faire aussi (même accord). Si le contexte rend « faire » absurde, garde « faire » quand même.
- « S V C » qui représente une proposition entière → `qn fait qc`
- trous rares : C_adj → `beau` (accordé) ; C_date → `le 3 mai` ; C_heure → `trois heures` ;
  C_mois → `mai` ; C_âge → `trente ans` ; C_nb → `dix` ; C_prix → `dix euros` ; C_langue → `l'italien` ;
  C_nationalité → `italien` ; C_moment / C_temps → `lundi` ou `longtemps` selon le sens.

Italien (abréviations de dictionnaire) :
- sujet S → `qcn` (qualcuno) ; S2 → `qcn altro`
- complément chose → `qcs` (qualcosa) ; personne → `qcn`
- lieu → `da qualche parte` (adapter : « andare a C_lieu » → « andare da qualche parte ») ; C_qn → `qcn`
- verbe : toujours **fare**, accordé : V → fa / faccio / facciamo / fanno… (sujet implicite : déduis la
  personne du français ou de la forme du verbe voisin) ; V_inf → fare ; V_sub → faccia/facciamo… ;
  V_pp → fatto ; V_cond → farebbe… ; V_fut → farà… ; V_imper → fai/fate ; V_ger → facendo ; V_pass → ha fatto
- trous rares : C_adj → `bello` (accordé) ; date → `il 3 maggio` ; heure → `le tre` ; mois → `maggio` ;
  âge → `trent'anni` ; nb → `dieci` ; prix → `dieci euro` ; langue → `l'italiano` ; nationalité → `italiano` ;
  moment/temps → `lunedì` ou `molto tempo`.

## Règles
- Ne change RIEN d'autre : mêmes mots, même ponctuation, mêmes alternatives séparées par « / », mêmes
  parenthèses d'explication (ex. « (politesse) »). Seuls les trous changent, plus les retouches
  grammaticales strictement nécessaires autour (élision, préposition, accord).
- Supprime les doublons absurdes de trous : « On veut V_inf C C. » → « On veut faire qc. »
- Le résultat ne doit plus contenir aucune variable (S, V, C, V_inf, C2…) ni « C2ando ».
- Corrige la ponctuation mal espacée (« S V C , OK? » → « qn fait qc, OK ? »), espace fine avant ? ! ; : en français comme d'habitude (espace simple).
- Une tournure qui n'a qu'un trou garde sa forme courte : « depuis C_moment » → « depuis lundi » ;
  « plein de C » → « plein de qc ».

## Sortie
Un fichier JSON : liste d'objets `{"key": …, "fr": …, "it": …}` (même ordre, même `key`, TOUS les items).
Vérifie à la fin avec un petit script que le nombre d'items est identique et qu'aucune variable ne reste
(regex : `(?<![\w’'])(?:S|V|C)\d?(?:_[a-zàéèâ]+)?(?![\w’'])`).
