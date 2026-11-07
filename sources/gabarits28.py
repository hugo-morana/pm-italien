"""Affichage paramétrique des items (champs frd / itd, affichage seulement ; le son et la correction gardent fr / it).
- Tournures à trous : on retrouve, par alignement avec la forme d'origine (fro / ito : S V C…), les mots qui
  remplacent un trou, et on les affiche entre crochets : [qn] [qc] [qqpart] [v] [v inf] [n] [adj]…
- Déterminants et articles (tour des adjectifs) : le [n], il mio [n], beaucoup de [n]…"""
import json, re, difflib, sys
P = "/home/claude/pm_italien/pm3d/data3d.json"
D = json.load(open(P))
VAR = re.compile(r"^(?P<pre>[«(\"'’]*)(?P<v>(?:S|V|C)\d?(?:_[a-zàéèâ]+)?|C2ando)(?P<post>[^\wàéèâ]*)$")
VT = {"": "v", "inf": "v inf", "pp": "v pp", "sub": "v subj", "fut": "v fut", "cond": "v cond", "imper": "v imp", "ger": "v gér", "pass": "v passé"}
CT = {"adj": "adj", "date": "date", "heure": "heure", "mois": "mois", "âge": "âge", "nb": "nb", "prix": "prix", "langue": "langue",
      "nationalité": "nationalité", "moment": "moment", "temps": "moment"}
def tag(v, rep, L):
    b, _, suf = v.partition("_"); b = b.rstrip("0123456789")
    if v == "C2ando": return "v gér"
    if b == "S": return "qn" if L == "fr" else "qcn"
    if b == "V": return VT.get(suf, "v")
    if suf == "lieu": return "qqpart" if L == "fr" else "qualche parte"
    if suf == "qn": return "qn" if L == "fr" else "qcn"
    if suf in CT: return CT[suf]
    r = rep.lower()
    if re.sub(r"[^\w]", "", r) in ("italien", "litalien", "italiano", "litaliano"): return "langue"
    if re.sub(r"[^\w]", "", r) in ("paul", "paolo", "marco"): return "nom"
    if re.sub(r"[^\w]", "", r) in ("trois", "tre"): return "heure"
    if re.sub(r"[^\w]", "", r) in ("trente",): return "âge"
    if re.sub(r"[^\wà]", "", r) in ("beau", "belle", "beaux", "belles", "bello", "bella", "belli"): return "adj"
    if L == "fr":
        if re.search(r"\bqn\b", r): return "qn"
        if re.search(r"\bqc\b", r): return "qc"
        if "qqpart" in r or "quelque part" in r: return "qqpart"
    else:
        if re.search(r"\bqcn\b", r): return "qcn"
        if re.search(r"\bqcs\b", r): return "qcs"
        if "qualche parte" in r: return "qualche parte"
    return "n"
FAIRE = {"fr": r"faisais|faisait|faisions|faisiez|faisaient|faire|fais|fait|faisons|faites|font|fasse|fasses|fassions|fassiez|fassent|ferai|feras|fera|ferons|ferez|feront|ferais|ferait|ferions|feriez|feraient|faisant|faits?|faites",
         "it": r"facevo|facevi|faceva|facevamo|facevate|facevano|facessimo|facessero|facessi|facesse|fare|faccio|fai|fa|facciamo|fate|fanno|faccia|facciano|facciate|facessi|facesse|farò|farai|farà|faremo|farete|faranno|farei|faresti|farebbe|faremmo|fareste|farebbero|fatto|fatta|facendo"}
def loose(span, vars_, L, verbs=True):
    """Remplacement par motifs quand l'alignement mot à mot n'est pas possible."""
    vs = [v for v in vars_ if v.startswith("V") or v == "C2ando"]
    def vf(m):
        t = tag(vs.pop(0), "", L) if vs else "v"; return "[" + t + "]"
    if L == "fr":
        span = re.sub(r"\ba fait\b", lambda m: "[v passé]" if any(v.endswith("_pass") for v in vars_) else m.group(0), span)
        span = re.sub(r"\ben faisant\b", "en [v gér]", span)
    else:
        span = re.sub(r"\bha fatto\b", lambda m: "[v passé]" if any(v.endswith("_pass") for v in vars_) else m.group(0), span)
    if vs and verbs: span = re.sub(r"(?<![\w\[])(?:" + FAIRE[L] + r")(?![\w\]])", vf, span)
    sx = {v.partition("_")[2] for v in vars_ if v.startswith("C")}
    RARE = [("âge", r"trente ans|trent'anni"), ("heure", r"trois heures|le tre"), ("date", r"le 3 mai|il 3 maggio"), ("mois", r"\bmai\b|\bmaggio\b"),
            ("nb", r"\bdix\b|\bdieci\b"), ("prix", r"dix euros|dieci euro"), ("langue", r"l'italien|l'italiano|\bitalien\b|\bitaliano\b"),
            ("moment", r"\blundi\b|\blunedì\b|\blongtemps\b|\bmolto tempo\b"), ("adj", r"\b(?:beau|belle|beaux|belles|bello|bella|belli)\b")]
    for t, rx in RARE:
        if any(CT.get(x) == t for x in sx) or (t in ("adj", "langue", "heure", "âge", "date") and sx): span = re.sub(rx, "[" + t + "]", span)
    if L == "fr":
        span = re.sub(r"\bqqpart\b|\bquelque part\b", "[qqpart]", span); span = re.sub(r"(?<!\[)\bqn\b", "[qn]", span); span = re.sub(r"(?<!\[)\bqc\b", "[qc]", span)
    else:
        span = re.sub(r"\b(da )?qualche parte\b", lambda m: (m.group(1) or "") + "[qualche parte]", span); span = re.sub(r"(?<!\[)\bqcn\b", "[qcn]", span); span = re.sub(r"(?<!\[)\bqcs\b", "[qcs]", span)
    return span
def merge(toks, L):
    o = []
    for t in toks:
        if o and o[-1] in (("qn",) if L == "fr" else ("qcn",)) and re.match(r"^(d'autre|altro)\b", t): o[-1] += " " + t
        else: o.append(t)
    return o
def tpl(orig, cur, L):
    a, b = orig.split(), merge(cur.split(), L); out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal": out += b[j1:j2]; continue
        va = [VAR.match(t) for t in a[i1:i2]]; vars_ = [m.group("v") for m in va if m]
        if not vars_: out += b[j1:j2]; continue
        def compat(m, t1):
            if not m: return True
            c = re.sub(r"^[«(\"'’]*|[^\wàéèâùûôîçœ']*$", "", t1).lower(); v = m.group("v")
            if not c: return False
            if v.startswith("S"): return c.split(" ")[0] in ("qn", "qcn")
            if v.startswith("V") or v == "C2ando": return re.fullmatch(FAIRE[L], c) is not None
            return re.fullmatch(FAIRE[L], c) is None
        if i2 - i1 == j2 - j1 and all(compat(m, t1) for m, t1 in zip(va, b[j1:j2])):
            for t0, t1, m in zip(a[i1:i2], b[j1:j2], va):
                if not m: out.append(t1); continue
                if " " in t1: w, rest = t1.split(" ", 1); out.append("[" + w + "] " + rest); continue
                core = re.sub(r"^[«(\"'’]*|[^\wàéèâùûôîçœ']*$", "", t1)
                pre = t1[:t1.index(core)] if core and core in t1 else m.group("pre"); post = t1[len(pre) + len(core):] if core else m.group("post")
                out.append(pre + "[" + tag(m.group("v"), t1, L) + "]" + post)
        else: out.append(loose(" ".join(b[j1:j2]), vars_, L))
    res = " ".join(x for x in out if x)
    allv = [m.group("v") for m in (VAR.match(t) for t in a) if m]
    res = loose(res, allv, L, verbs=False).replace("[âge] ans", "[âge]")
    if allv:   # « faire » de remplissage resté en clair : après le sujet, ou à l'infinitif devant le complément
        res = re.sub(r"(\[(?:qn|qcn)\](?: d'autre| altro)?(?: n[eo]n?)?) (" + FAIRE[L] + r")\b", r"\1 [v]", res)
        res = re.sub(r"(?<![\w\[])(faire|fare) (\[(?:qc|qcs|qn|qcn)\])", r"[v inf] \2", res)
        res = re.sub(r"(?<![\w\[])facendo (\[(?:qcs|qcn)\])", r"[v gér] \1", res)
        res = re.sub(r"(?<![\w\[])(fait|fa) (\[(?:qcn|qn)\])", r"[v] \2", res)
    return res
DET_IT = set("il lo l' la i gli le un uno una un' del dello della dell' dei degli delle questo questa questi queste quest' quello quel quell' quella quei quegli quelle molto molta molti molte poco poca pochi poche troppo troppa troppi troppe tanto tanta tanti tante altro altra altri altre ogni alcuni qualche parecchi certi certe diversi diverse vari quale quanto quanta".split())
POSS = re.compile(r"^(il|la|i|le) (mio|tuo|suo|nostro|vostro|loro|mia|tua|sua|nostra|vostra|miei|tuoi|suoi|nostri|vostri|mie|tue|sue|nostre|vostre)$|^(tutti i|tutti gli|tutte le)$")
def addn(alt, t="n"):
    alt = alt.strip()
    if "…" in alt: return alt.replace("…", "[" + t + "]")
    return alt + ("[" + t + "]" if alt.endswith(("'", "’")) else " [" + t + "]")
def det_it(s, t="n"):
    m = re.match(r"^(.*?)\s*(\([^()]*\))?$", s); return " / ".join(addn(a, t) for a in m.group(1).split(" / ")) + (" " + m.group(2) if m.group(2) else "")
def cl_fr(s):   # pronom complément : « le [v] (COD) », « lui [v] (COI, masc.) / leur [v] »
    alts = []
    for a in s.split(" / "):
        m = re.match(r"^(.*?)\s*(\([^()]*\))?$", a.strip()); alts.append(addn(m.group(1), "v") + (" " + m.group(2) if m.group(2) else ""))
    return " / ".join(alts)
CLIT = set("mi ti ci vi si lo la li le gli ne".split())
def det_fr(s):
    if s.startswith("combien (de) ?"): return "combien de [n] ?" + s[len("combien (de) ?"):]
    m = re.match(r"^(.*?)\s*(\?)?\s*(\(([^()]*)\))?$", s); main, q, rest = m.group(1), m.group(2), m.group(4)
    suf = ""
    if rest:
        p = [x.strip() for x in rest.split(",")]
        if re.match(r"^(…|livre)-(ci|là)$", p[0]): suf = p[0].split("-")[1]; p = p[1:]
        rest = ", ".join(p)
    alts = [addn(a) for a in main.split(" / ")]
    if suf: alts = [a if a.endswith(("-ci", "-là")) else a + "-" + suf for a in alts]
    return " / ".join(alts) + (" ?" if q else "") + (f" ({rest})" if rest else "")
nt = nd = 0; ex = []
for r in D["rooms"]:
    for n, x in enumerate(r["niches"]):
        if not x: continue
        x.pop("frd", None); x.pop("itd", None)
        for L in ("fr", "it"):   # points de suspension perdus (« neC pas » pour « ne… pas »)
            if re.search(r"[a-zàèéìòù]C(\b| )", x[L]) and x[L] != "la série TV": x[L] = re.sub(r"(?<=[a-zàèéìòù])C(?=\b| |$)", "…", x[L])
        if x["fr"] == "combiene ? (quanto, féminin)": x["fr"] = "combien (de) ? (quanto, féminin)"
        fd, id_ = x["fr"], x["it"]
        if x.get("fro") or x.get("ito"): fd, id_ = tpl(x.get("fro", x["fr"]), x["fr"], "fr"), tpl(x.get("ito", x["it"]), x["it"], "it")
        else:
            fd, id_ = loose(fd, [], "fr"), loose(id_, [], "it")
            fd = re.sub(r"(\[qn\](?: d'autre)?) (" + FAIRE["fr"] + r")\b", r"\1 [v]", fd); id_ = re.sub(r"(\[qcn\](?: altro)?) (" + FAIRE["it"] + r")\b", r"\1 [v]", id_)
        if r["fam"] == "adjectifs" and not x.get("k"):
            w = re.sub(r"\(.*?\)", "", x["it"]).strip()
            if w in DET_IT or POSS.match(w): fd, id_ = det_fr(x["fr"]), det_it(x["it"]); nd += 1
        if r["fam"] == "pronoms" and not x.get("k") and re.sub(r"\(.*?\)", "", x["it"]).strip() in CLIT: fd, id_ = cl_fr(x["fr"]), det_it(x["it"], "v"); nd += 1
        if x["it"] == "questo o quell'oggetto": id_ = "questo o quell'[n]"
        NEG = {"ne… pas": "ne [v] pas", "ne… plus": "ne [v] plus", "nessuno… più": None}
        if r["id"].startswith("adverbes") and x["fr"] in ("ne… pas", "ne… plus"): fd = x["fr"].replace("…", " [v]")
        if r["id"].startswith("adverbes") and x["it"] == "non… più": id_ = "non [v] più"
        if fd != x["fr"]: x["frd"] = fd
        if id_ != x["it"]: x["itd"] = id_
        if fd != x["fr"] or id_ != x["it"]: nt += 1; ex.append(f"{r['id']}:{n}\t{x['fr']}  →  {fd}\t||\t{x['it']}  →  {id_}")
json.dump(ex, open("/tmp/claude-0/-home-claude/de24b488-0b6e-5354-ba2e-0b5ce6b23f8d/scratchpad/gab_ex.json", "w"), ensure_ascii=False, indent=0)
if "--write" in sys.argv: json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("items paramétrés", nt, "dont déterminants", nd)
