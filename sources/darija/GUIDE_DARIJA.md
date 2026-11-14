# Guide : traduire une salle du palais italien en darija algérien

Tu remplis une ou plusieurs salles du palais mental « Dar ed-Darja ». C'est une réplique du palais italien de l'utilisateur : chaque niche garde le libellé français et la **même phrase d'exemple française**. Tu fournis la traduction en **darija algérien** tel qu'un Algérien natif d'Alger (parler du centre) le dit réellement à l'oral.

Dossier de travail : `/home/claude/src`. Ne modifie que tes propres fichiers `rooms/rNNN_darija.txt` et `rooms/rNNN_px.txt`.

## Entrées (lecture seule)
- `in/rNNN_in.txt` : une ligne par niche : `idx | libellé FR | référence italienne | phrase FR | segment FR surligné | type | sous-catégories`. L'italien sert seulement à comprendre le sens visé (homographes, registre, nuance). « (libre) » = niche vide, à ignorer.
- `in/rNNN_pxin.txt` : les phrases FR des exemples supplémentaires, par niche, dans l'ordre.
- Modèles terminés, à imiter (format, ton, qualité) : `rooms/r000_darija.txt`, `rooms/r000_px.txt` (noms) et `rooms/r001_darija.txt`, `rooms/r001_px.txt` (verbes). **Lis-en au moins 30 lignes avant de commencer.**

## Sortie 1 : `rooms/rNNN_darija.txt`
Une ligne par niche non vide, 11 champs séparés par ` | ` (un 12ᵉ facultatif) ; lignes commençant par `#` = commentaires :

`idx | cible arabe | translittération | prononciation | formes / variantes | phrase arabe | phrase latine | segment surligné (arabe) | mot-clé | scène | décryptage | [libellé FR corrigé]`

1. **cible arabe** : le mot ou l'expression darija en écriture arabe, telle que les Algériens l'écrivent (ڨ pour le g de ڨال, تاع, راني, واش, بزّاف, شدّة sur les géminées). Verbes : 3ᵉ pers. masc. sing. du passé (كلا, خدم), le présent va dans « formes ». Expressions / tournures à trous : la tournure darija (garde qn / qc si utile : « عندو ما يدير »).
2. **translittération** : arabizi algérien : 3 = ع, 7 = ح, 9 = ق, 2 = ء, kh = خ, gh = غ, ch = ش, dh = ذ/ظ/ض, j = ج, ou = و long, e = schwa ; article l- / el- / assimilé (ech-chems, d-dar). Pas de ` | ` dedans.
3. **prononciation** : approximation à la française, syllabe accentuée en MAJUSCULES (« el-OUAQT », « KHAL-la »).
4. **formes / variantes** : pluriel, féminin, présent des verbes, variante courante ou soutenue, note d'usage courte. Utilise « ; » comme séparateur.
5. **phrase arabe** : traduction naturelle, orale et algérienne de la phrase FR (pas d'arabe classique, pas de marocain ni de moyen-oriental). Les emprunts au français s'écrivent en arabe si c'est l'usage (لابان, الطوموبيل). Garde les noms propres. Si la tournure naturelle n'emploie pas le mot cible, préfère la phrase naturelle et explique-le dans le décryptage.
6. **phrase latine** : la même phrase en arabizi.
7. **segment surligné** : un morceau **copié exactement** de la phrase arabe (le mot ou la forme qui porte le sens de la niche). Il DOIT apparaître tel quel dans le champ 6. Laisse vide seulement si la phrase naturelle ne contient vraiment pas le mot.
8. **mot-clé** : un mot ou groupe de mots **français** qui sonne comme le mot darija (surtout sa syllabe accentuée). Évite les mots-clés qui sont déjà la traduction. Si rien ne convient, prends le moins mauvais et ajoute « (mot-clé faible) » dans le décryptage.
9. **scène** : une phrase au présent, concrète, exagérée, où le MOT-CLÉ (en majuscules) agit physiquement sur l'image du SENS français (en majuscules aussi). Ambiance algérienne quand c'est naturel (Casbah, Bab El Oued, Sahara, couleurs vert-blanc-rouge, thé à la menthe, makrouts…), sans en mettre partout.
10. **décryptage** : « son ≈ mot-clé ; image = sens », plus toute remarque utile (phrase française qui se dit autrement, faux ami, mot d'origine française/espagnole/turque…).
11. **libellé FR corrigé** (facultatif, 12ᵉ champ) : à donner **quand le libellé FR mentionne l'italien** (ex. « été (essere / stare, participe) », « les ans (anno, pluriel) », « oublier (familier) » s'il est inexact pour le darija). Réécris-le en français sans mot italien, en gardant la distinction utile (« été (participe) »). Sinon n'ajoute pas de 12ᵉ champ.

Interdits : le caractère `|` dans un champ ; une ligne coupée en deux ; inventer des mots darija. En cas de doute entre deux usages régionaux, prends celui d'Alger et cite l'autre en variante.

## Sortie 2 : `rooms/rNNN_px.txt`
Pour chaque ligne de `in/rNNN_pxin.txt`, dans le **même ordre** et le même nombre par niche : `idx | phrase arabe | phrase latine`. Traduction naturelle de la phrase FR (le mot de la niche n'a pas à y être si ce n'est pas naturel). Si la salle n'a aucun exemple supplémentaire, crée quand même le fichier (vide ou avec une ligne `#`).

## Cas particuliers
- **Formes verbales** (salles `formes_*`) : l'italien a une niche par forme conjuguée italienne. Donne la forme darija correspondant au sens de la phrase FR (participe, conditionnel, impératif…), et réécris le libellé FR sans l'italien. Les doublons de formes darija sont acceptables, mais varie le mot-clé et la scène.
- **Tournures à trous** (type `tpl`) : donne la tournure darija (avec qn / qc) en cible, et la phrase complète en exemple.
- **Doublons** : si deux niches françaises ont la même traduction darija (ex. vouloir / aimer = حبّ), c'est accepté ; signale-le dans le décryptage.
- **Villes et pays** : nom tel qu'on le dit en Algérie (روما, باريس, فرانسا, الدزاير pour Alger / l'Algérie).
- **Patrons syntaxiques** : la structure darija correspondante, avec qn / qc translittérés si besoin.

## Vérification (obligatoire)
Après chaque salle : `cd /home/claude/src && python3 build_darija.py --check NNN` (NNN = numéro sans zéros, ex. `--check 7`). Corrige jusqu'à « OK ». Puis relis 10 lignes au hasard en te demandant : « un Algérois de 30 ans dirait-il exactement ça ? ».

Travaille salle par salle et écris chaque fichier par morceaux si besoin (Write puis Edit/append via Bash `cat >>`), pour ne pas perdre le travail. Ne publie rien, ne touche pas à `site/` ni à `build_darija.py`.

Dans ton rapport final : salles faites (avec « OK » du contrôle), et une courte liste des choix à faire valider (mots-clés faibles, phrases adaptées, doutes de darija).
