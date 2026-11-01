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
```

Les scripts ont été écrits pour l'environnement de travail d'origine : les chemins absolus en tête de fichier sont à adapter.
