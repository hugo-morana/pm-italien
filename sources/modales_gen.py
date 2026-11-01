"""Génère expr_modales_N.txt (13 colonnes) à partir de modales_N.txt (texte|it|ex_fr|mot_fr|ex_it|mot_it).
Mot-clé, scène et lien : image du verbe (reprise des salles de verbes) + personnage du sujet. API et prononciation : lexique ci-dessous."""
import json, re, sys

# mot italien -> (API, prononciation à la française) ; accent tonique en MAJUSCULES
LEX = {
 "è": ("ɛ", "È"), "sono": ("ˈsono", "SO-no"), "sei": ("ˈsɛi", "SÈÏ"), "siamo": ("ˈsjamo", "SIA-mo"), "siete": ("ˈsjɛte", "SIÈ-té"),
 "era": ("ˈɛra", "È-ra"), "eri": ("ˈɛri", "È-ri"), "eravamo": ("eraˈvamo", "é-ra-VA-mo"), "eravate": ("eraˈvate", "é-ra-VA-té"), "erano": ("ˈɛrano", "È-ra-no"), "ero": ("ˈɛro", "È-ro"),
 "ho": ("ɔ", "O"), "hai": ("ˈai", "AÏ"), "ha": ("a", "A"), "abbiamo": ("abˈbjamo", "ab-BIA-mo"), "avete": ("aˈvete", "a-VÉ-té"), "hanno": ("ˈanno", "ANN-no"),
 "avevo": ("aˈvevo", "a-VÉ-vo"), "avevi": ("aˈvevi", "a-VÉ-vi"), "aveva": ("aˈveva", "a-VÉ-va"), "avevamo": ("aveˈvamo", "a-vé-VA-mo"), "avevate": ("aveˈvate", "a-vé-VA-té"), "avevano": ("aˈvevano", "a-VÉ-va-no"),
 "voglio": ("ˈvɔʎʎo", "VO-llio"), "vuoi": ("ˈvwɔi", "VOUOÏ"), "vuole": ("ˈvwɔle", "VOUO-lé"), "vogliamo": ("voʎˈʎamo", "vo-LLIA-mo"), "volete": ("voˈlete", "vo-LÉ-té"), "vogliono": ("ˈvɔʎʎono", "VO-llio-no"),
 "vorrei": ("vorˈrɛi", "vor-RÈÏ"), "vorresti": ("vorˈresti", "vor-RÈS-ti"), "vorrebbe": ("vorˈrebbe", "vor-RÈB-bé"), "vorremmo": ("vorˈremmo", "vor-RÈM-mo"), "vorreste": ("vorˈreste", "vor-RÈS-té"), "vorrebbero": ("vorˈrebbero", "vor-RÈB-bé-ro"),
 "posso": ("ˈpɔsso", "POS-so"), "puoi": ("ˈpwɔi", "POUOÏ"), "può": ("ˈpwɔ", "POUO"), "possiamo": ("posˈsjamo", "pos-SIA-mo"), "potete": ("poˈtete", "po-TÉ-té"), "possono": ("ˈpɔssono", "POS-so-no"),
 "potrei": ("poˈtrɛi", "po-TRÈÏ"), "potresti": ("poˈtresti", "po-TRÈS-ti"), "potrebbe": ("poˈtrebbe", "po-TRÈB-bé"), "potremmo": ("poˈtremmo", "po-TRÈM-mo"), "potreste": ("poˈtreste", "po-TRÈS-té"),
 "devo": ("ˈdevo", "DÉ-vo"), "devi": ("ˈdevi", "DÉ-vi"), "deve": ("ˈdeve", "DÉ-vé"), "dobbiamo": ("dobˈbjamo", "dob-BIA-mo"), "dovete": ("doˈvete", "do-VÉ-té"), "devono": ("ˈdevono", "DÉ-vo-no"),
 "dovrei": ("doˈvrɛi", "do-VRÈÏ"), "dovuto": ("doˈvuto", "do-VOU-to"), "potuto": ("poˈtuto", "po-TOU-to"), "avrei": ("aˈvrɛi", "a-VRÈÏ"), "avresti": ("aˈvresti", "a-VRÈS-ti"),
 "so": ("ˈsɔ", "SO"), "sai": ("ˈsai", "SAÏ"), "sa": ("ˈsa", "SA"), "sappiamo": ("sapˈpjamo", "sap-PIA-mo"), "sapete": ("saˈpete", "sa-PÉ-té"), "sanno": ("ˈsanno", "SANN-no"),
 "sapresti": ("saˈpresti", "sa-PRÈS-ti"), "saprebbe": ("saˈprebbe", "sa-PRÈB-bé"), "sapreste": ("saˈpreste", "sa-PRÈS-té"), "sapevo": ("saˈpevo", "sa-PÉ-vo"),
 "penso": ("ˈpɛnso", "PÈNN-so"), "pensi": ("ˈpɛnsi", "PÈNN-si"), "pensa": ("ˈpɛnsa", "PÈNN-sa"), "pensiamo": ("penˈsjamo", "pènn-SIA-mo"), "pensate": ("penˈsate", "pènn-SA-té"), "pensano": ("ˈpɛnsano", "PÈNN-sa-no"),
 "credo": ("ˈkredo", "KRÉ-do"), "credi": ("ˈkredi", "KRÉ-di"), "crede": ("ˈkrede", "KRÉ-dé"), "crediamo": ("kreˈdjamo", "kré-DIA-mo"), "credete": ("kreˈdete", "kré-DÉ-té"), "credono": ("ˈkredono", "KRÉ-do-no"),
 "conosco": ("koˈnosko", "ko-NOS-ko"), "conosci": ("koˈnoʃʃi", "ko-NOCH-chi"), "conosce": ("koˈnoʃʃe", "ko-NOCH-ché"), "conosciamo": ("konoʃˈʃamo", "ko-noch-CHA-mo"), "conoscete": ("konoʃˈʃete", "ko-noch-CHÉ-té"), "conoscono": ("koˈnoskono", "ko-NOS-ko-no"),
 "piace": ("ˈpjatʃe", "PIA-tché"), "piacciono": ("ˈpjattʃono", "PIAT-tcho-no"), "piacerebbe": ("pjatʃeˈrebbe", "pia-tché-RÈB-bé"), "piacerebbero": ("pjatʃeˈrebbero", "pia-tché-RÈB-bé-ro"),
 "amo": ("ˈamo", "A-mo"), "spero": ("ˈspɛro", "SPÈ-ro"), "preferisco": ("prefeˈrisko", "pré-fé-RIS-ko"), "dispiace": ("disˈpjatʃe", "dis-PIA-tché"),
 "bisogna": ("biˈzoɲɲa", "bi-ZO-gna"), "bisognerebbe": ("bizoɲɲeˈrebbe", "bi-zo-gné-RÈB-bé"), "bisogno": ("biˈzoɲɲo", "bi-ZO-gno"), "bisognato": ("bizoɲˈɲato", "bi-zo-GNA-to"),
 "sarebbe": ("saˈrebbe", "sa-RÈB-bé"), "stato": ("ˈstato", "STA-to"), "stata": ("ˈstata", "STA-ta"), "sto": ("ˈstɔ", "STO"), "stavo": ("ˈstavo", "STA-vo"), "per": ("per", "pèr"),
 "voglia": ("ˈvɔʎʎa", "VO-llia"), "c'è": ("tʃɛ", "TCHÈ"), "ci": ("tʃi", "tchi"), "c'era": ("ˈtʃɛra", "TCHÈ-ra"), "più": ("ˈpju", "PIOU"),
 "non": ("non", "nonn"), "che": ("ke", "ké"), "di": ("di", "di"), "a": ("a", "a"), "mi": ("mi", "mi"), "ti": ("ti", "ti"), "vi": ("vi", "vi"), "gli": ("ʎi", "lli"), "le": ("le", "lé"), "si": ("si", "si"), "se": ("se", "sé"),
 "lo": ("lo", "lo"), "ne": ("ne", "né"), "sì": ("ˈsi", "SI"), "no": ("ˈnɔ", "NO"), "volentieri": ("volenˈtjɛri", "vo-lènn-TIÈ-ri"), "ancora": ("anˈkora", "ann-KO-ra"),
 "cosa": ("ˈkɔza", "KO-za"), "ne": ("ne", "né"), "vero": ("ˈvero", "VÉ-ro"), "trovi": ("ˈtrɔvi", "TRO-vi"), "lei": ("ˈlɛi", "LÈÏ"), "loro": ("ˈloro", "LO-ro"), "noi": ("ˈnoi", "NOÏ"),
 "io": ("ˈio", "I-o"), "tu": ("ˈtu", "TOU"), "lui": ("ˈlui", "LOUI"), "voi": ("ˈvoi", "VOÏ"), "fosse": ("ˈfosse", "FOS-sé"),
}

PERS = {"je": ("Mon reflet (je)", "à mon reflet (je)"), "tu": ("Mon ami (tu)", "à mon ami (tu)"), "il": ("Un homme (il)", "à un homme (il)"),
        "elle": ("Une femme (elle)", "à une femme (elle)"), "on": ("La foule (on)", "à la foule (on)"), "nous": ("Notre duo (nous)", "à notre duo (nous)"),
        "vpol": ("Le majordome (vous de politesse)", "au majordome (vous de politesse)"), "vplu": ("La bande d'amis (vous)", "à la bande d'amis (vous)"),
        "ils": ("Le groupe d'hommes (ils)", "au groupe d'hommes (ils)"), "elles": ("Le groupe de femmes (elles)", "au groupe de femmes (elles)"),
        "S": ("Quelqu'un", "à quelqu'un"), "imp": ("Le grand panneau (impersonnel)", "au grand panneau (impersonnel)"), "q": ("Un point d'interrogation géant", "à un point d'interrogation géant")}

def personne(t):
    s = " " + t.replace("’", "'") + " "
    if re.search(r"\(pol\)", s): return "vpol"
    if re.search(r"\(plu", s): return "vplu"
    if re.search(r"Il (faut|faudrait|aurait fallu|y a|n'y a)|Faut-il|Faudrait-il|Y a-t-il", s): return "imp"
    for k, pat in [("je", r" (Je|J')|-je |^ Ai-je| J'"), ("tu", r" (Tu|T')|-tu "), ("ils", r" Ils |-ils "), ("elles", r" Elles |-elles "),
                   ("il", r" Il |-il "), ("elle", r" Elle |-elle "), ("on", r" On |-on "), ("nous", r" Nous |-nous "), ("vplu", r" Vous |-vous "), ("S", r" S ")]:
        if re.search(pat, s): return k
    return "q"

VERBES = [("besoin", r"besoin"), ("envie", r"envie"), ("falloir", r"faut|faudr|fallu"), ("ilya", r"y a"), ("espérer", r"espère"), ("regretter", r"regrette"),
          ("préférer", r"préfère"), ("aimer", r"aim"), ("vouloir", r"veu|voul|voudr"), ("pouvoir", r"peu|pouv|pourr|puis|pu "), ("devoir", r"doi|dev|dû"),
          ("savoir", r"sai|sav|saur|sait"), ("penser", r"pens"), ("croire", r"croi|croy"), ("connaître", r"conna"), ("aller", r"vais|allais"),
          ("être", r"suis|est|es |es-|êtes|sommes|sont|étai|étiez|étions|été"), ("avoir", r"ai|as|a |a-|avons|avez|ont|avai|avi")]
def verbe(t):
    t = t.replace("Est-ce que ", "").replace("n'est-ce pas", "")
    for v, pat in VERBES:
        if re.search(pat, t.lower()): return v
    return "q"

# image de chaque verbe : (mot-clé, action) — reprend les salles de verbes et de noms
IMG = {"être": ("« est-ce rêve ? »", "flotte au-dessus d'un lit en se demandant « est-ce rêve ? »"),
       "avoir": ("avare", "serre contre soi un coffre d'avare"),
       "besoin": ("bisou, gnon", "a besoin d'un bisou et reçoit un gnon"),
       "envie": ("voile", "regarde une voile gonflée d'envie de partir"),
       "falloir": ("« bisou, gnon »", "lit le panneau « IL FAUT » qui réclame un bisou"),
       "ilya": ("« tché ! »", "montre du doigt ce qu'il y a : « tché ! »"),
       "espérer": ("espérer", "espère devant une étoile filante"),
       "regretter": ("déplaisir", "tend un vase cassé, le visage plein de déplaisir (mi dispiace)"),
       "préférer": ("préférer", "préfère la plus grosse de deux glaces"),
       "aimer": ("plaisir", "savoure un gâteau avec un soupir de plaisir (mi piace)"),
       "vouloir": ("« vole, lait ! »", "veut faire voler une bouteille de lait : « vole, lait ! »"),
       "pouvoir": ("« pote, hé ! »", "soulève une voiture comme un pote costaud : « pote, hé ! »"),
       "devoir": ("dos vert", "porte sa dette sur un dos vert"),
       "savoir": ("sapé", "parade en savant bien sapé qui sait tout"),
       "penser": ("Penseur", "prend la pose du Penseur de Rodin"),
       "croire": ("credo", "brandit un panneau « CREDO »"),
       "connaître": ("connaisseur", "goûte un vin en connaisseur"), "q": ("intonation", "fait monter la voix en fin de phrase"),
       "aller": ("stop", "attend au stop, sur le point de partir (sto per)")}

def temps(t):
    l = t.lower()
    if re.search(r"aurai[st]? (pu|dû|fallu)", l): return "conditionnel passé"
    if re.search(r"rais\b|rait\b|rions\b|riez\b|raient\b|faudrait", l): return "conditionnel"
    if re.search(r"étai|étiez|étions|avai|aviez|avions|allais", l): return "imparfait"
    if "vpp" in l or "vop" in l or "été" in l or "a dû" in l: return "passé composé"
    return "présent"

DECOR = {"conditionnel": "dans un nuage de rêve (conditionnel)", "conditionnel passé": "dans un nuage de rêve jauni (conditionnel passé)",
         "imparfait": "sur une vieille photo sépia (imparfait)", "passé composé": "figé dans un flash photo (passé composé)", "présent": ""}

def ipa_pron(it):
    main = re.sub(r"\(.*?\)", " ", it.split(" / ")[0])
    ws = [w for w in re.findall(r"[a-zàèéìòùA-ZÈ']+", main.replace("…", " ")) if w]
    ip, pr, miss = [], [], []
    for w in ws:
        k = w.lower()
        if k not in LEX: miss.append(w); continue
        ip.append(LEX[k][0]); pr.append(LEX[k][1])
    return " ".join(ip), " ".join(pr), miss

def ligne(t, it, efr, mfr, eit, mit, nxt):
    p, v, tp = personne(t), verbe(t), temps(t)
    neg = bool(re.search(r"\bn[e']|\bpas\b|plus\b", t.replace("n'est-ce", ""))) and not t.startswith("Oui")
    q = "?" in t
    mc, act = IMG[v]
    sc = f"{PERS[p][0]} {act}"
    if DECOR[tp]: sc += ", " + DECOR[tp]
    sc += (", puis secoue la tête : non." if neg else ".")
    if q and p != "q": sc += " Un point d'interrogation flotte au-dessus."
    pron_note = {"vpol": "vous de politesse = Lei + 3ᵉ personne", "vplu": "vous pluriel = voi", "on": "on = noi (ou si impersonnel)",
                 "imp": "tournure impersonnelle", "S": "S = sujet", "q": "question par l'intonation"}.get(p, "")
    de = f"{it} — " + ("intonation" if v == "q" else f"{v}, {tp}") + (f" ; {pron_note}" if pron_note else "") + (" ; sujet omis en italien" if p in ("je", "tu", "il", "elle", "nous", "vplu", "ils", "elles", "on") else "")
    reg = "poli" if p == "vpol" or "Pourriez" in t or "Voudriez" in t else "neutre"
    ip, pr, miss = ipa_pron(it)
    if nxt:
        li = f"{PERS[p][0]} passe le relais {PERS[personne(nxt)][1]}, qui {IMG[verbe(nxt)][1]}."
    else:
        li = None
    return [t, it, pr or "—", ip or "—", mc, sc, de, reg, efr, mfr, eit, mit, li], miss

if __name__ == "__main__":
    k = int(sys.argv[1]); dernier_lien = sys.argv[2] if len(sys.argv) > 2 else ""
    L = [l.split("|") for l in open(f"/home/claude/pm_italien/modales_{k}.txt", encoding="utf-8").read().strip().split("\n")]
    assert all(len(x) == 6 for x in L), [x for x in L if len(x) != 6]
    out, manque = [], set()
    for i, x in enumerate(L):
        nxt = L[i + 1][0] if i + 1 < len(L) else None
        row, miss = ligne(*x, nxt); manque |= set(miss)
        if row[12] is None: row[12] = dernier_lien or f"{PERS[personne(x[0])][0]} pousse la porte de la salle suivante des expressions modales."
        out.append("|".join(row))
    if manque: print("MOTS ABSENTS DU LEXIQUE :", sorted(manque)); sys.exit(1)
    open(f"/home/claude/pm_italien/expr_modales_{k}.txt", "w").write("\n".join(out) + "\n")
    print("ok", len(out))
