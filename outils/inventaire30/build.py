import json,re
from wordfreq import zipf_frequency as zf
O={o['lemma']:o for o in json.load(open('todo.json'))}
EX=json.load(open('exclus.json'))
for l,why in [] if any(e['lemma']=='conquista' for e in EX) else [('conquista','forme du verbe conquistare (déjà présent)'),('accorto','participe de accorgersi (déjà présent)')]:
    o=O[l]; EX.append(dict(lemma=l,classe=o['pos'],forms=', '.join(o['forms']),ex=o['eit'],raison=why))
json.dump(EX,open('exclus.json','w'),ensure_ascii=False)
POS2F={'NOUN':'N','VERB':'V','ADJ':'A','ADV':'D','PRON':'P','DET':'A','SCONJ':'C'}
FAM={'N':'noms','V':'verbes','A':'adjectifs','D':'adverbes','P':'pronoms','C':'conjonctions'}
SALLE={'noms':'Les noms','verbes':'Les verbes','adjectifs':'Les adjectifs','adverbes':'Les adverbes','pronoms':'Les pronoms','conjonctions':'Les conjonctions'}
CL={'N':'nom','V':'verbe','A':'adjectif','D':'adverbe','P':'pronom','C':'conjonction'}
out=[];bad=[]
for f in ['c1.txt','c2.txt','c3.txt']:
    for line in open(f):
        line=line.rstrip('\n')
        if not line.strip(): continue
        p=line.split('|'); assert len(p)==12,(f,line)
        lem,it,fr,pr,mc,sc,efm,th,fam,eit,efr,eim=p
        lem={'a vicenda':'vicenda','per iscritto':'iscritto','alla perfezione':'perfezione','in borghese':'borghese','scorgere':'scortare'}.get(lem,lem)
        o=O[lem]
        fam=fam or POS2F[o['pos']]
        new=bool(eit)
        eit=eit or o['eit']; efr=efr or o['efr']
        if not eim:
            fl=sorted(o['forms'],key=len,reverse=True)
            eim=next((x for x in fl if x in eit),None)
        if not eim or eim not in eit: bad.append(('eim',lem,eit,eim))
        if efm not in efr: bad.append(('efm',lem,efr,efm))
        head=re.sub(r"^(il|lo|la|l'|i|gli|le|un|una)\s*","",it)
        w=head.split()[-1] if ' ' in head and fam!='D' else head
        z_it=round(zf(head,'it'),2) if ' ' not in head else round(zf(head.split()[-1],'it'),2)
        frh=re.sub(r"\s*[,;(].*","",fr); frh=re.sub(r"^(le|la|les|l'|un|une)\s*","",frh)
        z_fr=round(zf(frh,'fr'),2)
        out.append(dict(lemma=lem,it=it,fr=fr,pr=pr,mc=mc,sc=sc,efm=efm,th=th,fam=FAM[fam],classe=CL[fam],eit=eit,efr=efr,eim=eim,
            newex=new,src=o['src'],n=o['n'],z=z_it,zfr=z_fr,salle=SALLE[FAM[fam]],note='nouvel exemple rédigé' if new else 'exemple repris de '+o['src']))
print(len(out),'bad',len(bad))
for b in bad: print(b)
missing=set(O)-{o['lemma'] for o in out}-{'conquista','accorto'}
print('non traités',missing)
json.dump(out,open('missing_final.json','w'),ensure_ascii=False,indent=0)
