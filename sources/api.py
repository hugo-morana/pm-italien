"""Transcription API (italien standard, phonémique) de chaque mot cible."""
import json
P = "/home/claude/pm_italien/data_italien.json"
A = """ˈkɔsa ˈanno ˈwɔmo ˈtɛmpo ˈvita ˈdʒorno ˈdɔnna ˈvɔlta biˈzoɲɲo ˈdio
ˈpadre raˈɡattsa ˈmondo aˈmiko siɲˈɲore bamˈbino ˈmadre ˈora ˈdʒɛnte laˈvoro
raˈɡattso ˈkasa ˈsera ˈnome ˈnɔtte proˈblɛma ˈparte ˈmamma paˈura ˈsɔldi
raˈdʒone ˈarja ˈmano ˈmɔrte moˈmento ˈfiʎʎo ˈtɛsta ˈkolpo ˈmakkina doˈmanda
afˈfare ˈrɔba iˈdɛa faˈmiʎʎa aˈmore forˈtuna miˈnuto ˈtittsjo ˈɔkkjo fraˈtɛllo
ˈstɔrja paˈpa ˈpɔrta ˈsaŋɡwe ˈtipo settiˈmana ˈmese tʃitˈta ˈkazo ˈposto
ˈlato politˈtsia siɲˈɲora ˈakkwa ˈtɛrra paˈrɔla ˈkamera matˈtina ˈtrɛno ˈdʒɛnere
ˈkɔrpo ˈmɔdo ˈlwɔɡo maˈrito beˈbɛ ˈarma ˈpunto dotˈtore ˈfilm ˈfɔto
ˈfine ˈskwɔla ˈkapo ˈfwɔko ˈrɛsto ˈɡwɛrra ˈkane ˈdʒɔko ˈordine veriˈta
ˈpjɛde ˈvɔʎʎa diˈritto ˈkwɔre paˈese ˈlibro dʒeniˈtore faˈvore ˈdʒiro ˈattimo""".split()
assert len(A) == 100
d = json.load(open(P))
for r, a in zip(d["pieces"][0]["niches"], A):
    r["api"] = f"/{a}/"
d["api_note"] = "Italien standard (toscan), transcription phonémique ; ˈ précède la syllabe accentuée, consonne doublée = géminée. Dans le Nord, le s entre voyelles se prononce souvent [z] (casa [ˈkaza])."
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print("ok")
