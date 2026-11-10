# Audio des phrases d'exemple — état
- lots.json : 163 lots d'exemples (0-162, alternés FR/IT, du plus fréquent au plus rare) + 163/164 (mots sans voix).
- FAITS : 0-9, 11, 163, 164.  À FAIRE : 10, 12-162.
- Boucle : prompt.py k… → update_node (nœuds A-H) → run → télécharger raw/lotKKK.mp3 → transcribe connect_from = nœud TTS
  → get_flow_run_status (sortie sauvée en fichier) → ORDER=1 python3 x_extract.py <fichier> L:k … (même ordre que les sessions)
  → sync_lots.py → (cd aud_L && PREFIX=exf_/exi_ python3 cut_stt.py k) → merge_hp.py → apply_ex.py → publier ex_*.mp3.
