import json, html, unicodedata
def _nq(t): return ''.join(c for c in unicodedata.normalize('NFD', (t or '').lower()) if not unicodedata.combining(c)).replace('’', "'")
d = json.load(open("/home/claude/pm_italien/data_italien.json"))
COL = ["#f4f1ea", "#d33b2c", "#e8862a", "#e6c229", "#3f9b4f", "#2a5db0", "#7b3fa0", "#7a4b2a", "#e48bb0", "#8a8a8a"]
NOMS = ["blanc", "rouge", "orange", "jaune", "vert", "bleu", "violet", "marron", "rose", "gris"]
SURF = ["mur gauche", "diagonale gauche", "mur du fond", "diagonale droite", "mur droit",
        "sol droit", "sol centre", "sol gauche", "plafond gauche", "plafond droit"]
e = html.escape

import re
def mark(phrase, mot):
    h = e(phrase)
    if not mot: return h
    m = e(mot)
    out, n = re.subn(r"(?<![A-Za-zÀ-ÖØ-öø-ÿŒœ])" + re.escape(m) + r"(?![A-Za-zÀ-ÖØ-öø-ÿŒœ])", f"<mark>{m}</mark>", h)
    return out if n else h.replace(m, f"<mark>{m}</mark>", 1)

def occ(z):
    x = 10 ** (z - 1); n = int(round(x, -int(__import__("math").floor(__import__("math").log10(x))) + 2))
    return f"{n:,}".replace(",", "\u202f")

def bar(z, ax=""):
    if z is None: return '<span class="na">—</span>'
    return f'<span class="bar"><i style="width:{(z-1)/6*100:.0f}%"></i></span><b>{ax}{z:.1f}</b><span class="occ">{occ(z)}</span>'

def zgrid(r):
    z=r["zipf"]; ax = "≈" if r.get("approx") else ""
    cells="".join(f'<span class="rl">{lab}</span><span>{bar(z["fr"].get(k), ax)}</span><span>{bar(z["it"].get(k), ax)}</span>'
                  for k,lab in (("ecrit","écrit"),("parle","parlé"),("global","mixte")))
    return f'<div class="zg"><span></span><span class="rh">FR · Zipf / occ.</span><span class="rh">IT · Zipf / occ.</span>{cells}</div>'

from collections import Counter
CNT = Counter(t for p_ in d["pieces"] for r_ in p_["niches"] for t in r_.get("tags", []))
SC = d.get("sous_categories", {"arbre": {}, "ajouts": []})
FAM = {"adjectifs": "adjectifs", "determinants": "adjectifs", "pronoms": "pronoms", "conjonctions": "conjonctions",
       "prepositions": "prépositions", "adverbes": "adverbes"}
def soustabs(p):
    fam = FAM.get(p["id"]) or p.get("famille")
    g = GROUPE.get(p["id"], p["id"])
    premier = next(q["id"] for q in d["pieces"] if GROUPE.get(q["id"], q["id"]) == g)
    if not fam or p["id"] != premier: return ""
    lst = SC["arbre"][fam]; par = dict(lst)
    def prof(t):
        k = 0
        while par.get(t) and par.get(t) in par and k < 5: t = par[t]; k += 1
        return k
    out = ['<button class="st on" type="button" data-tag="">toutes</button>']
    for tag, parent in lst:
        if parent is None: continue
        lab = tag
        for pre in (fam + "_", "pronoms_", "adjectifs_"):
            if lab.startswith(pre) and lab != pre[:-1]: lab = lab[len(pre):]; break
        lab = lab.replace("_", " ")
        n = CNT.get(tag, 0); aj = " aj" if tag in SC["ajouts"] else ""
        out.append(f'<button class="st d{prof(tag)}{aj}" type="button" data-tag="{e(tag)}" title="{e(tag)}{" (ajout)" if aj else ""}"{" disabled" if not n else ""}>{e(lab)}{"＋" if aj else ""} <small>{n}</small></button>')
    return '<nav class="stabs" aria-label="Sous-catégories">' + "".join(out) + "</nav>"

# Abréviations des onglets
ABREV = {"noms": "n", "verbes": "v", "adjectifs": "adj", "pronoms": "pro", "conjonctions": "conj",
         "prepositions": "prp", "adverbes": "adv",  "expressions": "expr"}
# Pièces regroupées sous un même onglet
GROUPE = {"adjectifs": "adjectifs", "determinants": "adjectifs",
          **{f"basiques_{i}": "expressions" for i in range(1, 6)},
          "courantes_1": "expressions", **{f"modales_{i}": "expressions" for i in range(1, 7)}, "incises_1": "expressions", "incises_2": "expressions", "incises_3": "expressions", "incises_4": "expressions"}
GROUPE.update({f"{b}_{k}": b for b in ("noms", "verbes", "adjectifs", "adverbes") for k in range(2, 10)})
TITRE_GROUPE = {"adjectifs": "Les adjectifs", "expressions": "Les expressions"}

def sauts(p):
    g = GROUPE.get(p["id"], p["id"])
    ps = [q for q in d["pieces"] if GROUPE.get(q["id"], q["id"]) == g]
    if len(ps) < 2 or ps[0] is not p: return ""
    b = "".join(f'<button class="st saut" type="button" data-cible="p-{q["id"]}">{e(q["titre_fr"].replace("Les ", "").replace("adjectifs ", ""))}</button>' for q in ps)
    return f'<nav class="stabs" aria-label="Pièces de cet onglet">{b}</nav>'


def nxt(p, r):
    for x in p["niches"][r["n"] + 1:]:
        if not x.get("libre"): return f'{x["n"]:02d}'
    return "pièce suiv."

def piece_html(p):
  sections = []
  for t in range(10):
    cards = []
    for r in p["niches"][t*10:(t+1)*10]:
        if r.get("libre"):
            cards.append(f'<div class="niche libre" style="--frame:{COL[t]}"><div class="row"><span class="num">{r["n"]:02d}</span><span class="fr">libre</span></div></div>')
            continue
        zp = r.get("zipf_fr")
        cards.append(f'''<details class="niche" style="--frame:{COL[t]}" data-tags="{e(" ".join(r.get("tags", [])))}" data-q="{e(_nq(" | ".join([r["fr"], r.get("texte_source") or "", r["cible"], r.get("mot_cle") or ""])))}">
<summary class="row"><span class="num">{r["n"]:02d}</span><span class="fr">{e(r["fr"])}</span><span class="rit" lang="it">{e(r["cible"])}</span><span class="rz" title="Zipf parlé français (score grossier)">{(("≈" if r.get("approx") else "") + f"{zp:.1f}") if isinstance(zp,(int,float)) else "—"}</span><span class="ro" title="Occurrences par 100 millions de mots, parlé français (score fin)">{f"{oc:,}".replace(",", "\u202f") if isinstance(oc:=((r.get("occ100M") or {}).get("fr") or {}).get("parle"),(int,float)) else "—"}</span><span class="chev" aria-hidden="true">›</span></summary>
<div class="fiche">
<p class="it"><button class="say" type="button" aria-label="Écouter le mot" data-say="{e(r["cible"])}" data-src="{e(r["audio_mot"] or "")}">🔊</button>{e(r["cible"])}</p>
<p class="phon"><span class="ipa" lang="it-fonipa">{e(r["api"])}</span><span class="pr">{e(r["prononciation"])}</span></p>
<div class="ex"><button class="say" type="button" aria-label="Écouter la phrase" data-say="{e(r["exemple_cible"])}" data-src="{e(r["audio_phrase"] or "")}">🔊</button><div><p class="exit">{mark(r["exemple_cible"], r.get("exemple_cible_mot"))}</p><p class="exfr">{mark(r["exemple_fr"], r.get("exemple_fr_mot"))}</p></div></div>
{zgrid(r)}
<dl>
<div><dt>Mot-clé</dt><dd class="mc">{e(r["mot_cle"])}</dd></div>
<div><dt>Scène</dt><dd>{e(r["scene"])}</dd></div>
<div><dt>Décryptage</dt><dd class="muted">{e(r["decryptage"])} · <em>{e(r["formes"])}</em></dd></div>
<div class="lien"><dt>⟶ {nxt(p, r)}</dt><dd>{e(r["lien"])}</dd></div>
</dl></div></details>''')
    sections.append(f'''<section><h2><span class="cart" style="--frame:{COL[t]}">{t}x</span> {SURF[t]} <small>cadre {NOMS[t]}{(" · " + e(p["blocs"][t])) if p.get("blocs") and p["blocs"][t] else ""}</small></h2>
<div class="list">{"".join(cards)}</div></section>''')
  return f'''<div class="piece" id="p-{p["id"]}" data-piece="{p["id"]}" data-group="p-{GROUPE.get(p["id"], p["id"])}"><div class="ens"><h1>{e(p["titre_cible"])} · <span>{e(p["titre_fr"].lower())}</span></h1><p class="sub">Pièce {d["pieces"].index(p)+1} · {e(p.get("decor",""))} · {len(p["niches"])} niches · ordre : {e(p.get("ordre",""))}</p>{sauts(p)}{soustabs(p)}<div class="ctl"><button class="st" type="button" data-all="1">Tout déplier</button><button class="st" type="button" data-all="0">Tout replier</button></div></div>{"".join(sections)}</div>'''

_vus, _tabs = set(), []
for p in d["pieces"]:
    g = GROUPE.get(p["id"], p["id"])
    if g in _vus: continue
    _vus.add(g)
    lab = TITRE_GROUPE.get(g, p["titre_fr"])
    ab = ABREV.get(g, g)
    _tabs.append(f'<a class="tab" href="#p-{g}" data-tab="{g}" title="{e(lab)}" aria-label="{e(lab)}">{e(ab)}</a>')
tabs = "".join(_tabs)
pieces = "".join(piece_html(p) for p in d["pieces"])

page = f'''<title>Palais d'italien</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+SC:wght@600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@500&family=Noto+Sans:wght@400&display=swap">
<style>
/* Mise en page : enseigne de palazzo, puis 10 panneaux (dizaines) de fiches en grille fluide */
:root {{
  --bg:#f3ede3; --card:#fffaf2; --fg:#2b2320; --muted:#6f625a; --accent:#9c3d22; --line:#dccfbe; --hl:#f3d7c2;
  --display:"Cormorant SC", Georgia, serif; --body:"Source Serif 4", Georgia, serif; --mono:"IBM Plex Mono", ui-monospace, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#1d1916; --card:#27211d; --fg:#efe6da; --muted:#b3a395; --accent:#e08a63; --line:#3d342d; --hl:#5a3424; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#1d1916; --card:#27211d; --fg:#efe6da; --muted:#b3a395; --accent:#e08a63; --line:#3d342d; --hl:#5a3424; color-scheme:dark }}
body {{ background:var(--bg); color:var(--fg); font:15px/1.5 var(--body);
  padding-left:max(16px, env(safe-area-inset-left,0px)); padding-right:max(16px, env(safe-area-inset-right,0px)); padding-block:24px 48px }}
.wrap {{ max-width:1180px; margin:0 auto; display:flex; flex-direction:column; gap:32px }}
.ens {{ border:1px solid var(--line); border-radius:4px; padding:20px; text-align:center; background:var(--card) }}
.ens h1 {{ font:600 clamp(28px,6vw,44px)/1.1 var(--display); margin:0; letter-spacing:.04em; text-wrap:balance }}
.ens h1 span {{ color:var(--accent) }}
.ens p {{ margin:8px auto 0; max-width:62ch; color:var(--muted) }}
h2 {{ font:600 22px/1.2 var(--display); display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin:0 0 12px }}
h2 small {{ font:500 11px var(--mono); color:var(--muted); letter-spacing:.06em; text-transform:uppercase }}
.cart {{ font:500 14px var(--mono); border:3px solid var(--frame); padding:2px 8px; border-radius:3px }}
.list {{ display:flex; flex-direction:column; gap:4px }}
.niche {{ background:var(--card); border:1px solid var(--line); border-left:5px solid var(--frame); border-radius:3px; min-width:0 }}
.niche.libre {{ opacity:.55; border-style:dashed; border-left-style:solid }}
.row {{ display:flex; gap:12px; align-items:baseline; padding:9px 12px; min-height:24px; list-style:none; cursor:pointer }}
.niche.libre .row {{ cursor:default; padding-block:5px }}
.row::-webkit-details-marker {{ display:none }}
.row:hover {{ background:var(--bg) }}
.row:focus-visible {{ outline:2px solid var(--accent); outline-offset:-2px }}
.row .fr {{ flex:1 1 40%; min-width:0; overflow-wrap:anywhere }}
.rit {{ flex:1 1 40%; min-width:0; font:600 17px/1.2 var(--display); color:var(--accent); letter-spacing:.02em; overflow-wrap:anywhere }}
.rz {{ flex:none; font:500 11px var(--mono); color:var(--muted); font-variant-numeric:tabular-nums; width:3.5em; text-align:right }}
.ro {{ flex:none; font:500 11px var(--mono); color:var(--fg); font-variant-numeric:tabular-nums; width:8.5em; text-align:right }}
.chev {{ flex:none; color:var(--muted); transition:transform .15s; font-size:18px; line-height:1 }}
details[open] > .row .chev {{ transform:rotate(90deg) }}
details[open] > .row {{ border-bottom:1px solid var(--line) }}
.fiche {{ padding:10px 14px 14px; max-width:640px }}
@media (max-width:520px) {{ .row {{ flex-wrap:wrap; gap:2px 10px }} .rit {{ flex-basis:100%; order:5; padding-left:30px }} .row .fr {{ flex:1 1 0 }} .rz {{ width:auto }} .ro {{ width:auto }} }}
.ctl {{ display:flex; gap:6px; justify-content:center; margin-top:10px }}
.num {{ font:500 13px var(--mono); color:var(--muted); font-variant-numeric:tabular-nums }}
.fr {{ font-weight:600 }}
.it {{ font:600 24px/1.2 var(--display); color:var(--accent); margin:4px 0 8px; letter-spacing:.02em }}
.pr {{ font:500 11px var(--mono); color:var(--muted); letter-spacing:.05em; vertical-align:middle }}
dl {{ margin:0; display:flex; flex-direction:column; gap:6px }}
dl div {{ display:grid; grid-template-columns:78px 1fr; gap:8px }}
.zg {{ display:grid; grid-template-columns:56px 1fr 1fr; gap:2px 8px; align-items:center; padding:6px 0; border-block:1px solid var(--line) }}
.zg .rl, .zg .rh {{ font:500 10px var(--mono); text-transform:uppercase; letter-spacing:.06em; color:var(--muted) }}
dt {{ font:500 10px/1.9 var(--mono); text-transform:uppercase; letter-spacing:.06em; color:var(--muted) }}
dd {{ margin:0; min-width:0 }}
.mc {{ font-style:italic }}
.muted {{ color:var(--muted); font-size:13px }}
.lien {{ border-top:1px dashed var(--line); padding-top:6px }}
.lien dt {{ color:var(--accent) }}
.bar {{ display:inline-block; width:40px; height:6px; background:var(--line); border-radius:3px; margin-right:5px; vertical-align:middle }}
.bar i {{ display:block; height:100%; background:var(--accent); border-radius:3px }}
.say {{ font-size:15px; line-height:1; border:1px solid var(--line); background:var(--bg); color:var(--fg); border-radius:50%; width:32px; height:32px; flex:none; cursor:pointer; margin-right:8px; vertical-align:middle }}
.say:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px }}
.say.on {{ border-color:var(--accent); background:var(--card) }}
.ex {{ display:flex; align-items:flex-start; gap:0; margin:0 0 8px }}
.ex p {{ margin:0 }}
.phon {{ display:flex; gap:12px; align-items:baseline; flex-wrap:wrap; margin:-4px 0 8px 40px }}
.ipa {{ font:400 16px/1.3 "Noto Sans", "Gentium Plus", "Doulos SIL", "Lucida Sans Unicode", system-ui, sans-serif; letter-spacing:.02em }}
mark {{ background:var(--hl); color:inherit; padding:0 2px; border-radius:2px; box-shadow:inset 0 -2px 0 var(--accent) }}
.exfr mark {{ font-style:normal; font-weight:600 }}
.exit {{ font-weight:600 }}
.exfr {{ color:var(--muted); font-size:13px; font-style:italic }}
.novoice .say {{ display:none }}
#voix {{ font:500 11px var(--mono); color:var(--muted); margin-top:8px }}
.occ {{ display:block; font:500 10px var(--mono); color:var(--muted); font-variant-numeric:tabular-nums; padding-left:45px }}
.top {{ display:flex; flex-direction:column; gap:8px }}
.top p {{ margin:0; color:var(--muted); max-width:75ch }}
.kick {{ font:500 11px var(--mono); letter-spacing:.12em; text-transform:uppercase }}
.ti {{ font:600 clamp(32px,7vw,52px)/1 var(--display); margin:0; letter-spacing:.03em }}
.tabs {{ display:flex; gap:6px; overflow-x:auto; padding:8px 0 4px; scrollbar-width:thin }}
.tab {{ flex:none; font:500 12px var(--mono); padding:7px 12px; border:1px solid var(--line); border-radius:999px; color:var(--fg); text-decoration:none; background:var(--card) }}
.tab[aria-current="true"] {{ background:var(--accent); color:var(--card); border-color:var(--accent) }}
.tab:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px }}
.piece {{ display:flex; flex-direction:column; gap:32px }}
.piece[hidden] {{ display:none }}
.ens .sub {{ font:500 11px var(--mono); letter-spacing:.04em }}
.stabs {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center; margin-top:14px }}
.st {{ font:500 11px var(--mono); padding:5px 10px; border:1px solid var(--line); border-radius:999px; background:var(--bg); color:var(--fg); cursor:pointer }}
.st small {{ color:var(--muted); font-size:10px }}
.st.d1 {{ border-style:dashed }}
.st.d2 {{ border-style:dotted; font-size:10px }}
.st.saut {{ border-color:var(--accent); color:var(--accent) }}
.st.aj {{ font-style:italic }}
.st.on {{ background:var(--accent); color:var(--card); border-color:var(--accent) }}
.st.on small {{ color:var(--card) }}
.st:disabled {{ opacity:.4; cursor:default }}
.st:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px }}
#filtre {{ position:sticky; top:env(safe-area-inset-top,0px); z-index:5; background:var(--accent); color:var(--card); font:500 12px var(--mono); padding:8px 12px; border-radius:4px; display:flex; gap:10px; align-items:center; justify-content:space-between }}
#filtre button {{ font:inherit; background:var(--card); color:var(--fg); border:0; border-radius:999px; padding:4px 10px; cursor:pointer }}
.niche[hidden], section[hidden], #filtre[hidden] {{ display:none }}
.rech input {{ width:100%; box-sizing:border-box; font:16px var(--body); padding:10px 14px; border:1px solid var(--line); border-radius:999px; background:var(--card); color:var(--fg) }}
.rech input:focus-visible {{ outline:2px solid var(--accent); outline-offset:1px }}
.na {{ color:var(--muted); font:500 11px var(--mono) }}
dd b {{ font:500 11px var(--mono); font-variant-numeric:tabular-nums }}
</style>
<div class="wrap">
<header class="top"><p class="kick">Palazzo della lingua italiana</p><h1 class="ti">Palais d'italien</h1>
<p>Tableaux de validation avant construction 3D : une pièce par classe de mots, 100 niches par pièce, mot-clé sonore, scène et lien vers la niche suivante. Scores Zipf (1 à 7) mesurés par lemme. Écrit : Lexique 3 livres (FR), itWaC (IT). Parlé : sous-titres de films et séries, Lexique 3 + OpenSubtitles 2018 (FR), OpenSubtitles 2018 (IT). Mixte : wordfreq, qui mêle web, livres, presse, sous-titres et réseaux sociaux. Sous chaque Zipf : nombre d'occurrences par 100 millions de mots. L'ordre suit le score parlé français. Transcription API de l'italien standard : ˈ précède la syllabe accentuée, une consonne doublée se prononce longue ; dans le Nord, le s entre voyelles sonne souvent [z]. Mots-outils italiens : pas de corpus écrit étiqueté disponible, la colonne écrit reste vide (—). Locutions (bien sûr, parce que…) : score estimé à partir des mots qui les composent, comme wordfreq, signalé par ≈. 🔊 lit le mot ou la phrase avec la voix italienne de l'appareil, ou avec ton mp3 s'il est fourni.</p><p id="voix">Recherche d'une voix italienne…</p>
<nav class="tabs" aria-label="Pièces">{tabs}</nav>
<div class="rech"><input id="q" type="search" placeholder="Rechercher un mot, en français ou en italien…" aria-label="Rechercher" autocomplete="off" spellcheck="false"></div></header>
<div id="filtre" hidden><span id="filtre-txt"></span><button type="button" id="filtre-off">Retirer le filtre</button></div>
{pieces}
</div>
<script>
(function(){{
  var ps = document.querySelectorAll('.piece'), ts = document.querySelectorAll('.tab');
  function montre(){{
    var h = (location.hash || '').slice(1), ok = false;
    ps.forEach(function(p){{ if(p.dataset.group === h) ok = true; }});
    if(!ok) h = ps[0].dataset.group;
    ps.forEach(function(p){{ p.hidden = p.dataset.group !== h; }});
    ts.forEach(function(t){{ t.setAttribute('aria-current', t.getAttribute('href') === '#' + h ? 'true' : 'false'); }});
  }}
  var q = '', qi = document.getElementById('q'), tag = '', fb = document.getElementById('filtre'), ft = document.getElementById('filtre-txt');
  function applique(){{
    var h = (location.hash || '').slice(1), n = 0;
    document.querySelectorAll('.st').forEach(function(b){{ b.classList.toggle('on', b.dataset.tag === tag); }});
    ps.forEach(function(p){{
      var vis = 0;
      p.querySelectorAll('section').forEach(function(sec){{
        var k = 0;
        sec.querySelectorAll('.niche').forEach(function(c){{
          var ok = (!tag || (' ' + c.dataset.tags + ' ').indexOf(' ' + tag + ' ') >= 0) && (!q || (c.dataset.q || '').indexOf(q) >= 0);
          c.hidden = !ok; if(ok) k++;
        }});
        sec.hidden = !!(tag || q) && !k; vis += k;
      }});
      if(q){{ p.hidden = !vis; n += vis; }} else if(tag){{ p.hidden = !vis && p.dataset.group !== h; n += vis; }}
    }});
    fb.hidden = !tag && !q;
    if(tag || q) ft.textContent = (q ? 'Recherche « ' + qi.value.trim() + ' »' : '') + (q && tag ? ' · ' : '') + (tag ? 'Sous-catégorie : ' + tag : '') + ' · ' + n + ' niche' + (n > 1 ? 's' : '') + ', toutes pièces confondues';
  }}
  document.addEventListener('click', function(ev){{
    var b = ev.target.closest('.st'); if(!b || b.disabled) return;
    if(b.dataset.cible){{ document.getElementById(b.dataset.cible).scrollIntoView({{block:'start'}}); return; }}
    if(b.dataset.all){{ b.closest('.piece').querySelectorAll('details.niche').forEach(function(x){{ if(!x.hidden) x.open = b.dataset.all === '1'; }}); return; }}
    tag = b.dataset.tag; if(!tag) montre(); applique();
    if(tag) fb.scrollIntoView({{block:'start'}});
  }});
  document.getElementById('filtre-off').addEventListener('click', function(){{ tag = ''; q = ''; qi.value = ''; montre(); applique(); }});
  function nq(t){{ return t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/’/g, "'").trim(); }}
  var tmr = null;
  qi.addEventListener('input', function(){{ clearTimeout(tmr); tmr = setTimeout(function(){{
    var v = nq(qi.value); q = v.length >= 2 ? v : '';
    if(!q) montre(); applique();
  }}, 150); }});
  window.addEventListener('hashchange', function(){{ tag = ''; q = ''; qi.value = ''; montre(); applique(); window.scrollTo(0, 0); }});
  montre();
}})();
(function(){{
  var syn = window.speechSynthesis, voix = null, info = document.getElementById('voix');
  function choisir(){{
    if(!syn) return;
    var vs = syn.getVoices().filter(function(v){{ return /^it(-|_|$)/i.test(v.lang); }});
    voix = vs.find(function(v){{ return /it-IT/i.test(v.lang) && v.localService; }}) || vs[0] || null;
    info.textContent = voix ? 'Voix : ' + voix.name : 'Aucune voix italienne sur cet appareil : ajoute-la dans les réglages de synthèse vocale, ou fournis les mp3.';
  }}
  if(syn){{ choisir(); syn.onvoiceschanged = choisir; }} else {{ info.textContent = 'Synthèse vocale indisponible dans ce navigateur.'; }}
  var cur = null;
  document.addEventListener('click', function(ev){{
    var b = ev.target.closest('.say'); if(!b) return;
    if(cur){{ cur.classList.remove('on'); }}
    if(syn) syn.cancel();
    cur = b; b.classList.add('on');
    var fin = function(){{ b.classList.remove('on'); }};
    if(b.dataset.src){{ var a = new Audio(b.dataset.src); a.onended = fin; a.play().catch(fin); return; }}
    if(!syn){{ fin(); return; }}
    var u = new SpeechSynthesisUtterance(b.dataset.say);
    u.lang = 'it-IT'; if(voix) u.voice = voix; u.rate = 0.9; u.onend = fin; u.onerror = fin;
    syn.speak(u);
  }});
}})();
</script>'''
open("/home/claude/pm_italien/validation_noms.html", "w").write(page)
print("ok")
