# Une niche par alternative « X / Y » (palais de vocabulaire italien pour francophone)

Le palais range des items (une « niche » = un mot ou une expression italienne `it` + sa traduction française `fr`).
Certaines niches regroupent plusieurs alternatives séparées par « / » :
- côté français : « chez / par / depuis » = da ; « joli / mignon » = carino ; « il appelait / il s'appelait (chiamare, imparfait) » = chiamava
- côté italien : « non plus » = « neanche / nemmeno / neppure » ; « Bon courage ! » = « Forza! / In bocca al lupo! »

L'utilisateur apprend le français → italien pour l'EXPRESSION (il part d'un mot français) et l'italien → français pour la
COMPRÉHENSION (il part d'un mot italien). Il ne veut plus apprendre « X / Y » d'un bloc : il veut UNE niche par
alternative, avec un seul mot (ou une seule expression) de chaque côté.

## Entrée
`srcN.json` : liste de niches. Champs : key, classe, fr, it, pr (prononciation simplifiée de l'italien, syllabe accentuée
en majuscules, ex. « MI-o »), api (« /ˈmio/ »), mc (mot-clé mnémotechnique français qui sonne comme l'italien), sc (scène
mnémotechnique), de (décryptage), fo (notes de forme), efr/eit (exemple FR/IT), efm/eim (mot surligné dans l'exemple,
sous-chaîne exacte de efr/eit), k (type : "" mot, "tpl" tournure à trous, "loc" locution, "col" collocation, "fig" expression figée).

## Règle de séparation
Pour chaque niche, découpe `fr` et `it` sur « / » (hors parenthèses) et produis une niche par alternative :
- FR multiple, IT unique (« chez / par / depuis » = da) → « chez = da », « par = da », « depuis = da ».
- IT multiple, FR unique (« non plus » = neanche / nemmeno / neppure) → « non plus = neanche », « non plus = nemmeno »…
- Les deux multiples → associe chaque alternative française à l'alternative italienne qui lui correspond vraiment
  (« Il aime qc. / Il adore qc. » ↔ « Gli piace qcs / Adora qcs ») ; s'il n'y a pas de correspondance terme à terme,
  fais une niche par alternative italienne (avec la traduction FR la plus juste) ET une par alternative française restante.
- Chaque nouvelle niche doit être une TRADUCTION CORRECTE et naturelle dans les deux sens. Corrige l'autre côté si besoin :
  « il s'appelait (chiamare, imparfait) » = « si chiamava », pas « chiamava » ; « prenons ! (prendere, impératif) » =
  « prendiamo! ». Garde les notes entre parenthèses utiles à CETTE alternative (« (chiamare, imparfait) », « (masc. pl.) »,
  « (Lei) ») et retire celles qui concernaient l'autre.
- Formes conjuguées : « que je demeure / que tu demeures (rimanere, subjonctif) » = rimanga → « que je demeure (rimanere,
  subjonctif) = (che io) rimanga » et « que tu demeures (rimanere, subjonctif) = (che tu) rimanga ».
- Tournures avec qn / qc / qqpart (FR) et qcn / qcs / da qualche parte (IT) : garde ces abréviations telles quelles.
- **skip** si le « / » n'est pas une alternative (fraction, « et/ou », date, sigle), ou si une alternative est un simple
  doublon orthographique de l'autre. Si une alternative est fausse ou trop rare, ne la garde pas (et note-le dans `note`).
- `primary` : l'alternative la plus courante (celle qui reçoit la progression déjà acquise sur la niche d'origine). Une
  seule par source.

## Contenu de chaque nouvelle niche (tout en français sauf it / eit)
- fr, it ; pr, api (de CET italien ; reprends ceux de la source s'il n'a pas changé)
- mc : mot-clé mnémotechnique qui sonne comme l'italien (reprends celui de la source si l'italien est le même)
- sc : UNE scène concrète et visuelle (1 phrase) qui relie le mc au sens de CETTE alternative française ; différente
  pour chaque niche (si l'italien est le même mais le sens français change, la scène doit montrer ce sens-là)
- de : décryptage court ; fo : notes de forme utiles (ou "")
- efr / eit : un exemple court et naturel qui emploie CETTE alternative des deux côtés ; efm / eim : le mot exact
  surligné (sous-chaîne exacte de efr / eit)
- Reprends tout ce qui est bon dans la source pour l'alternative qu'elle illustrait déjà.

## Sortie : `outN.json`
```
{"skip": ["key", …],
 "items": [ {"from": "verbes_3:61", "primary": true, "fr": …, "it": …, "pr": …, "api": …, "mc": …, "sc": …, "de": …,
             "fo": …, "efr": …, "efm": …, "eit": …, "eim": …, "note": ""}, … ] }
```
Chaque source est soit dans `skip`, soit présente dans `items` (au moins 2 items, exactement un `primary: true`).
Aucun `fr` ni `it` d'un item ne doit encore contenir « / » hors parenthèses.
Vérifie à la fin avec un petit script Python : sources toutes couvertes, un primary par source, efm ⊂ efr, eim ⊂ eit,
pas de « / » restant hors parenthèses, JSON valide.
