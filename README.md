# Dar ed-Darja (branche pm-algerien)

Version **darija algérien** (parler d'Alger) du palais mental 3D : réplique complète du Palazzo dell'italiano (104 salles, 9 581 niches), avec les mêmes phrases d'exemple françaises.

- Chaque niche : mot en écriture arabe + translittération latine (arabizi : 3 = ع, 7 = ح, 9 = ق), prononciation, API, mot-clé sonore français, scène, phrase d'exemple darija et exemples supplémentaires.
- Sources de la traduction : `sources/darija/rNNN_darija.txt` et `rNNN_px.txt` (une paire par salle), guide de traduction `GUIDE_DARIJA.md`, construction de `data3d.json` avec `build_darija.py` (à partir du `data3d.json` italien) et adaptation de la page avec `patch_app.py`.
- Pas de fréquences darija (aucun corpus fiable) : les vues « fréquence DZ » sont masquées. Le darija est lu par la voix arabe de l'appareil ; les sons français sont ceux du palais italien.
- Progression séparée de l'italien (préfixe `pmdz:` en local, `dz_` dans Supabase).
- Relecture par un locuteur natif algérois à faire : les doutes et mots-clés faibles sont signalés dans les décryptages.

---

# Palazzo dell'italiano

Palais mental 3D pour apprendre le vocabulaire italien depuis le français (méthode des loci).

- **`index.html`** : le palais 3D (27 pièces sur deux étages, 2 298 niches). Visite guidée ou libre, fiche avec audio, tests, répétition espacée et courbe de compréhension. Il charge `data3d.json` et three.js r128 depuis jsDelivr.
- **`validation.html`** : les tableaux de validation de toutes les pièces (une ligne repliable par niche).
- **`data3d.json`** : les données du palais, dans l'ordre de la boucle.
- **`sources/`** : les données complètes (`data_italien.json`), les listes d'expressions (`listes/`), les étages 2 (`etages/`) et les scripts qui construisent les pièces et les pages.

## Organisation

Chaque pièce compte 100 niches réparties sur 10 surfaces (mur gauche, diagonales, fond, mur droit, sol, plafond). Les cadres suivent le code couleur MemoHugoDate : 0 blanc, 1 rouge, 2 orange, 3 jaune, 4 vert, 5 bleu, 6 violet, 7 marron, 8 rose, 9 gris. Dans chaque panneau, x0 est au-dessus de la grille 3×3, parcourue en serpentin.

Une niche contient le mot français, sa traduction italienne, la prononciation et l'API, un mot-clé sonore et sa scène, une phrase d'exemple, les fréquences Zipf (écrit, parlé, mixte, occurrences par 100 millions de mots) et le lien vers la niche suivante.

## Comptes et progression

Chaque personne peut se connecter avec son adresse e-mail (bouton **Compte**) : elle reçoit un code à 6 chiffres, sans mot de passe. Sa progression (répétition espacée, courbe de compréhension) est alors enregistrée en ligne et la suit sur tous ses appareils. Sans connexion, la progression reste dans le navigateur de l'appareil.

La connexion utilise [Supabase](https://supabase.com) (offre gratuite). Mise en place, une seule fois :

1. Crée un compte puis un projet sur supabase.com (région Europe).
2. **SQL Editor** → colle le contenu de `supabase/schema.sql` → *Run*. La table `progress` est créée, et chacun ne peut lire que ses propres lignes.
3. **Authentication → Emails → Magic Link** : dans le modèle, remplace le lien par le code, par exemple `<p>Ton code Palazzo : <strong>{{ .Token }}</strong></p>`.
4. **Project Settings → API** : copie l'URL du projet et la clé `anon public` dans `config.js`.

Dans la version publiée sur Claude, la progression va sur le compte Claude et ce réglage n'est pas utilisé.

## Fréquences

- Français : Lexique 3.83 (livres et films) et OpenSubtitles 2018.
- Italien : itWaC (écrit) et OpenSubtitles 2018 (parlé).
- Locutions et expressions : estimation à partir des mots qui les composent, comme wordfreq (signalée par ≈).

## Reconstruire

```
python3 sources/sous_categories.py      # étiquettes de sous-catégories
python3 sources/build_table.py          # page de validation
python3 sources/build_data3d.py         # data3d.json pour le palais
python3 sources/mots_phrase.py          # niches pour « Mots de la phrase » : a C_lieu, participes passés, villes et pays
```

Les scripts ont été écrits pour l'environnement de travail d'origine : les chemins absolus en tête de fichier sont à adapter.

## Hors-ligne

Sur GitHub Pages, `sw.js` (service worker) garde l'app sur l'appareil : `index.html`, `data3d.json`, `vendor/three.min.js`, la page de validation et les icônes. La page et les données passent d'abord par le réseau pour recevoir les mises à jour, puis par le cache. Les sons sont mis en cache au fil de l'écoute, ou d'un coup avec le bouton « Télécharger tous les sons » du plan. Les paquets sont versionnés (`?v=`) : seuls ceux qui changent sont retéléchargés. La progression reste sur l'appareil hors connexion et se resynchronise avec Supabase au retour du réseau.
