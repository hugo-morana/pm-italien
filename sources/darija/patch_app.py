"""Adapte index.html du palais italien au darija algérien."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf8").read()
n0 = len(h)

def sub(old, new, count=None, regex=False):
    global h
    if regex:
        h2, k = re.subn(old, new, h)
    else:
        k = h.count(old); h2 = h.replace(old, new)
    assert k > 0, ("absent", old)
    if count is not None:
        assert k == count, (old, k)
    h = h2

# --- titre / marque
sub("Palazzo dell'italiano", "Dar ed-Darja")
# --- voix : arabe (ar-DZ de préférence), lecture du texte en écriture arabe
sub('vs = all.filter(v => /^it/i.test(v.lang))', 'vs = all.filter(v => /^ar/i.test(v.lang))')
sub('voice = vs.find(v => /it-IT/i.test(v.lang) && v.localService) || vs[0] || null',
    'voice = vs.find(v => /ar-DZ/i.test(v.lang)) || vs.find(v => /ar-(MA|TN|LY)/i.test(v.lang)) || vs.find(v => v.localService) || vs[0] || null')
sub('u.lang = lang === "fr" ? "fr-FR" : "it-IT"', 'u.lang = lang === "fr" ? "fr-FR" : (v.lang || "ar-DZ")', 2)
sub('"Aucune voix italienne sur cet appareil"', '"Aucune voix arabe sur cet appareil"')
sub('? "fr-FR" : "it-IT";', '? "fr-FR" : "ar-DZ";')
# --- écriture arabe : sens de lecture, police
sub('lang="it"', 'lang="ar" dir="rtl"')
sub('lang="it-fonipa"', 'lang="ar-fonipa"')
css = """
[lang="ar"]{font-family:"Noto Naskh Arabic","Geeza Pro","Arabic Typesetting","Segoe UI","Tahoma",sans-serif;unicode-bidi:isolate}
.big-it span[lang="ar"]{font-size:1.25em}
.dz-lt{display:block;direction:ltr;font-family:var(--mono,'IBM Plex Mono',monospace);font-size:.62em;letter-spacing:.02em;opacity:.8;margin-top:2px}
.dz-elt{direction:ltr;font-size:13px;margin:2px 0 0;opacity:.85;font-family:var(--mono,'IBM Plex Mono',monospace)}
"""
sub("</style>", css + "</style>", count=None)
# mot en grand : arabe + translittération dessous
sub('<span>${escP(dI(x))}</span></div>',
    '<span lang="ar" dir="rtl">${escP(dI(x))}${x.lt ? `<span class="dz-lt" lang="fr">${esc(x.lt)}</span>` : ""}</span></div>', 1)
# phrase d'exemple : translittération sous l'arabe
sub('<p class="exit" lang="ar" dir="rtl">${mark(x.eit, x.eim)}</p>',
    '<p class="exit" lang="ar" dir="rtl">${mark(x.eit, x.eim)}</p>${x.elt ? `<p class="dz-elt">${esc(x.elt)}</p>` : ""}', 1)
sub('<p class="exit" lang="ar" dir="rtl">${esc(e[1])}</p>',
    '<p class="exit" lang="ar" dir="rtl">${esc(e[1])}</p>${e[4] ? `<p class="dz-elt">${esc(e[4])}</p>` : ""}', 1)
sub('<p class="exit" lang="ar" dir="rtl">${mark(shown.eit, shown.eim)}</p>',
    '<p class="exit" lang="ar" dir="rtl">${mark(shown.eit, shown.eim)}</p>${shown.elt ? `<p class="dz-elt">${esc(shown.elt)}</p>` : ""}', 1)
# --- correction : la translittération latine est acceptée (on tape rarement l'arabe)
sub('altsOf(rawIt(x)).concat(altsOf(x.it))', 'altsOf(rawIt(x)).concat(altsOf(x.it), altsOf(x.lt || ""))')
sub('altsOf(rawIt(shown)).concat(altsOf(shown.it))', 'altsOf(rawIt(shown)).concat(altsOf(shown.it), altsOf(shown.lt || ""))')
# norm : on garde les chiffres de l'arabizi (3, 7, 9) et on retire l'article el- / l-
sub(r'replace(/\b(il|lo|la|i|gli|le|l|un|una|uno|le|les|de|du|des)\b/g, " ")',
    r'replace(/\b(el|l|le|la|les|un|une|de|du|des)\b/g, " ")')
# recherche : la translittération compte aussi
sub('q: nrm(x.fr + " | " + x.it + " | " + x.mc)', 'q: nrm(x.fr + " | " + x.it + " | " + (x.lt || "") + " | " + x.mc)')
# --- libellés
for a, b in [("en français ou en italien", "en français, en darija (arabe ou latin)"),
             ("en italien et en français", "en darija et en français"),
             ("Traduis en italien", "Traduis en darija"),
             ("par fréquence en italien", "par fréquence en darija"),
             ("par fréquence italienne", "par fréquence darija"),
             ("(en italien pour FR → IT", "(en darija pour FR → DZ"),
             ("du français vers l'italien", "du français vers le darija"),
             ("de l'italien parlé courant", "du darija parlé courant")]:
    sub(a, b)
sub(r"\bIT → FR\b", "DZ → FR", regex=True)
sub(r"\bFR → IT\b", "FR → DZ", regex=True)
sub(r'(Mot|Exemple|Compréhension|fréq\.|Fréquence|fréquence) IT\b', r"\1 DZ", regex=True)
sub(r'"IT"', '"DZ"', regex=True) if '"IT"' in h else None
# --- pas encore de fréquences darija : on masque les palais et ordres « fréquence DZ »
sub('<button class="pill" type="button" data-palais="freqit">', '<button class="pill" type="button" data-palais="freqit" hidden>')
sub('<button class="pill" type="button" data-liborder="freqit" aria-pressed="false">', '<button class="pill" type="button" data-liborder="freqit" aria-pressed="false" hidden>')
sub('<button class="pill" type="button" data-approach="freqit">', '<button class="pill" type="button" data-approach="freqit" hidden>')
sub('const PAL = ["classe", "freq", "freqit", "theme", "lisa"]', 'const PAL = ["classe", "freq", "theme", "lisa"]')
open(dst, "w", encoding="utf8").write(h)
print("ok", n0, "->", len(h))
h = open(dst, encoding="utf8").read()
for a, b in [("de l'italien", "du darija"), ("l'italien", "le darija"), ("italien parlé", "darija parlé"),
             ("conversation italienne", "conversation en darija"), ("phrase italienne", "phrase en darija"), ("forme italienne", "forme darija")]:
    h = h.replace(a, b)
open(dst, "w", encoding="utf8").write(h)
h = open(dst, encoding="utf8").read()
h = h.replace("la fréquence italienne", "la fréquence darija").replace("conversation en italien", "conversation en darija")
open(dst, "w", encoding="utf8").write(h)
h = open(dst, encoding="utf8").read()
old = "  NL = layout.xmax.length;"
assert old in h
h = h.replace(old, "  NL = layout.xmax.length; for (let i = 0; i < NL; i++) if (layout.xmax[i] == null) layout.xmax[i] = 6.5;", 1)
open(dst, "w", encoding="utf8").write(h)
