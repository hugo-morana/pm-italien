# Une niche par forme (palais de vocabulaire italien pour francophone)

Le palais range des items (une « niche » = un item : mot italien `it` + traduction `fr`). Certaines niches
regroupent plusieurs FORMES d'un même mot : « mio (il mio) = mon (ma, mes) », « un (uno, una, un') = un / une »,
« il (lo, l') = le », « buono / buona = bon bonne », « tutti / tutte », « i miei C / le mie C = mes C »…
L'utilisateur veut travailler chaque forme indépendamment : UNE niche par forme (ma, mon, mes ; un, une…).
Il veut aussi que déterminants et articles soient traités comme des adjectifs : les doublons entre la salle
« determinants » et les tournures d'adjectifs (« i miei C / le mie C », « molti C / molte C »…) doivent être
fusionnés : une seule niche par forme au final.

## Entrées
- `sources.json` : les niches candidates (champs : key, it/fr affichés, ito/fro = forme d'origine avec trous
  S/V/C, pr = prononciation, api, mc = mot-clé mnémotechnique, sc = scène mnémotechnique, de = décryptage,
  fo = formes/notes, efr/eit = exemple FR/IT, efm/eim = mot du français/italien surligné dans l'exemple, k).
- `index.tsv` : toutes les niches courtes existantes (key, it d'origine, fr d'origine) pour repérer les doublons.

## Ce qu'il faut décider pour CHAQUE source
1. **skip** si les alternatives italiennes ne sont pas des formes d'un même mot mais des synonymes
   (« neanche / nemmeno / neppure », « tra (fra) », « sul serio / seriamente », « single / celibe »,
   « un sacco di C / tanti C »…) ou une simple note entre parenthèses. Ces niches ne bougent pas.
2. **split** si ce sont des formes (genre, nombre, élision, article contracté, possessif avec article…) :
   produire une niche par forme. Exemples attendus :
   - « il (lo, l') » → il = le ; lo = le (devant s+consonne, z, gn…) ; l' = le / la (devant voyelle)
   - « la (l') » → la = la (l' est déjà couvert par la forme l' ci-dessus : ne pas le recréer)
   - « un (uno, una, un') » → un = un ; uno = un (devant s+consonne, z…) ; una = une ; un' = une (devant voyelle)
   - « i (gli, le) » → i = les (masc.) ; gli = les (masc., devant voyelle, s+consonne, z…) ; le = les (fém.)
   - « mio (il mio) » → il mio = mon ; la mia = ma ; i miei = mes (masc.) ; le mie = mes (fém.)
     (idem tuo/tua/tuoi/tue = ton/ta/tes ; suo… = son/sa/ses ; nostro… = notre/nos ; vostro… = votre/vos ;
     il loro / la loro / i loro / le loro = leur / leurs)
   - « del (della, dello, dell') » → del, dello, della, dell' (du / de la / de l') ; « dei (degli, delle) » → dei, degli, delle (des)
   - « buono / buona » → buono = bon ; buona = bonne
   - « tutti / tutte » → tutti = tous ; tutte = toutes
   - « questo C / quello C » → questo = ce / cet ; quello = ce …-là (forme : quel, quello, quell') etc.
   Les formes sont écrites SANS trou ni mot de remplissage : « molti » = « beaucoup de (masc. pl.) »,
   pas « molti libri ». Précise entre parenthèses ce qui distingue deux formes qui ont la même traduction
   (« mes (masc.) » / « mes (fém.) », « le (devant s+consonne) »).
3. **Doublons** : si une forme existe déjà comme niche (voir index.tsv, même mot italien, même sens), ne crée
   pas de nouvelle niche : mets sa key dans `reuse` (elle sera gardée telle quelle). Si deux sources donnent la
   même forme (ex. « mio (il mio) » et « i miei C / le mie C » donnent toutes deux « i miei »), une seule niche
   finale, qui liste les deux sources dans `from`.

## Contenu de chaque nouvelle niche (tout en français sauf it/eit)
- it, fr ; pr (prononciation simplifiée, majuscules sur la syllabe accentuée, comme « MI-o ») ; api (« /ˈmia/ »)
- mc : mot-clé mnémotechnique français qui sonne comme le mot italien (court, entre « »)
- sc : une scène mnémotechnique concrète et visuelle (1 phrase) qui relie mc au sens ; DIFFÉRENTE pour chaque forme
- de : décryptage court (« mia ≈ « mi(enne) » ; féminin de mio »)
- fo : notes de forme utiles (« devant un nom féminin singulier : la mia casa ; sans article : mia madre »)
- efr / eit : un exemple court et naturel qui utilise CETTE forme ; efm / eim : le mot exact surligné (sous-chaîne de l'exemple)
- Reprends ce qui est bon dans la source (pr, api, mc, sc, exemple) pour la forme qu'elle illustrait.

## Sortie : `out.json`
```
{"skip": ["key", …],
 "items": [ {"from": ["determinants:4", "adjectifs:9"], "primary": "determinants:4",
             "it": "i miei", "fr": "mes (masc.)", "pr": …, "api": …, "mc": …, "sc": …, "de": …, "fo": …,
             "efr": …, "efm": …, "eit": …, "eim": …}, … ],
 "reuse": [ {"from": ["adjectifs_2:1"], "key": "adjectifs_6:40", "form": "sicura"}, … ],
 "delete": ["key", …] }
```
- `primary` : la source dont la progression passe à cette niche (une seule niche par source doit l'avoir : la
  forme la plus courante, souvent le masculin singulier).
- `delete` : toutes les sources splittées (elles disparaissent, remplacées par les items).
Vérifie le JSON par un petit script (chaque source est dans skip ou delete ; efm ⊂ efr ; eim ⊂ eit ; chaque
source supprimée a exactement un item `primary`).
