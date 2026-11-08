# Audio des phrases d'exemple — état
- lots.json : 163 lots (0-162) + 163/164 (mots sans voix). pair = fr, impair = it (vérifier via prompt.py).
- FAITS : 0-35 sauf 36 ; 37 ; 163-177.  À FAIRE : 36, 38-162 (next.py choisit). Quota épuisé le 08/11 à 11h40 (723 000).
- Quota ElevenLabs épuisé le 08/11 (663 000, reste 967). Reprendre quand Hugo recharge.
- Nœuds TTS (langue FIXÉE, ne passer que `prompt`) : FR = A RdFjwrYMzsSpHKDrUB0U, B ZGWLhv6YrDCz8EPw4Z0v, C ylgPgRce8XSIgSuQzWzp,
  D 4SkVzSB5ngnFR8AzS8uU ; IT = E KbSS24qGwhvFEPSVXkNZ, F p3hz4yqnek9VHnXoBIDE, G 1EZRyPmrpIlRFhhQHO5r, H fXc7CQUx2pgKKWlwbZV8.
- Boucle (max 5 TTS simultanés) : prompt.py k ; update_node(prompt) ; run (generations_count 1) ; quand fini :
  transcribe connect_from = nœud TTS ; get_flow_run_status(sessions TTS + transcriptions) ; `python3 harvest.py last`
  (télécharge, découpe, normalise -18 LUFS) ; puis apply_ex.py et publier.
- Niveau : loud.py (-18 LUFS, crête -1,5 dBFS) ; normenc.py (clips enc/) ; normpacks.py (paquets des mots, cache seg_cache/).
- fix_after_norm.json : correction efr verbes:94 à appliquer sur data3d après normpacks.
- 08/11 : voix Anki remplacées (lots 165-177, non_hp.json : 1 201 FR + 271 IT + 92 « autres exemples ») → paquets w29_*. Nœuds E et H passés en FR.
