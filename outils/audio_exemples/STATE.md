# Audio des phrases d'exemple — état
- lots.json : 163 lots (0-162) + 163/164 (mots sans voix). pair = fr, impair = it (vérifier via prompt.py).
- FAITS : 0-54 sauf 55 ; 57 ; 163-177. Quota épuisé le 08/11 14h45 (783 000). Nœuds G2 (C,D,G,H) déjà chargés avec 56,58,59,61 ; E avec 55.
- Quota ElevenLabs épuisé le 08/11 (663 000, reste 967). Reprendre quand Hugo recharge.
- Nœuds TTS (langue FIXÉE, ne passer que `prompt`) : FR = A RdFjwrYMzsSpHKDrUB0U, B ZGWLhv6YrDCz8EPw4Z0v, C ylgPgRce8XSIgSuQzWzp,
  D 4SkVzSB5ngnFR8AzS8uU ; IT = E KbSS24qGwhvFEPSVXkNZ, F p3hz4yqnek9VHnXoBIDE, G 1EZRyPmrpIlRFhhQHO5r, H fXc7CQUx2pgKKWlwbZV8.
- Boucle (max 5 TTS simultanés) : prompt.py k ; update_node(prompt) ; run (generations_count 1) ; quand fini :
  transcribe connect_from = nœud TTS ; get_flow_run_status(sessions TTS + transcriptions) ; `python3 harvest.py last`
  (télécharge, découpe, normalise -18 LUFS) ; puis apply_ex.py et publier.
- Niveau : loud.py (-18 LUFS, crête -1,5 dBFS) ; normenc.py (clips enc/) ; normpacks.py (paquets des mots, cache seg_cache/).
- fix_after_norm.json : correction efr verbes:94 à appliquer sur data3d après normpacks.
- 08/11 : voix Anki remplacées (lots 165-177, non_hp.json : 1 201 FR + 271 IT + 92 « autres exemples ») → paquets w29_*. Nœuds E et H passés en FR.
- 08/11 14h : 149 exemples FR mal formés « X » · Y corrigés (préfixe retiré dans data3d et lots.json) ; souvent la phrase n'illustre pas le mot (à signaler / revoir).
- Attente TTS : utiliser Bash run_in_background `sleep 100` plutôt que poller le statut TTS seul (sortie énorme).

## 08/11 — lots 60–117 générés (Hugo Pro, -18 LUFS), publiés v111
- 46 lots d'exemples restants (116, 118–162). queue.json : taken = lots faits uniquement.
- Correction : ", Un Buco Nero." → "Un buco nero." (data3d + lots.json).

## 08/11 soir — lots 116–155 générés (sauf 152, 154), publiés v113
- Quota épuisé (1 143 000). Restent 9 lots : 152, 154, 156, 157, 158, 159, 160, 161, 162.
- Prompts déjà prêts dans les nœuds : A=156, B=158, E=159, F=161 ; C=152, D=154, H=157 (échec quota, relancer tels quels).

## 08/11 18h30 — TERMINÉ : tous les lots d'exemples (0–162) en Hugo Pro, publiés v115
- 9126/9126 niches avec audio d'exemple FR+IT, -18 LUFS.
