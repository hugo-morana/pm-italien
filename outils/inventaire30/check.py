import pickle,collections,re,json
from wordfreq import zipf_frequency
import simplemma
P=pickle.load(open('inv.pkl','rb'))
I=P['items'];lib=P['lib'];lf=P['libform']
CL=r"(mi|ti|si|ci|vi|lo|la|li|le|gli|ne|glie(lo|la|li|le|ne)|me(lo|la|li|le|ne)|te(lo|la|li|le|ne)|se(lo|la|li|le|ne)|ce(lo|la|li|le|ne)|ve(lo|la|li|le|ne))+$"
def cands(lem,pos,forms):
    c={lem, lem.split()[0], lem.replace("´","'")}
    for f in forms:
        fl=f.lower().replace("´","'"); c.add(fl)
        c.add(simplemma.lemmatize(fl,lang='it'))
        if pos in('VERB','AUX'):
            b=re.sub(CL,'',fl)
            if b!=fl and b:
                c.add(b); c.add(b+'e'); c.add(simplemma.lemmatize(b,lang='it'))
                if b.endswith('r'): c.add(b+'e')
    return {x for x in c if x}
res={}
for (lem,pos),v in I.items():
    cs=cands(lem,pos,v['forms'])
    hit=[x for x in cs if x in lib or x in lf]
    best=lem.split()[0]
    if pos in('VERB','AUX'):
        sl=[simplemma.lemmatize(f.lower(),lang='it') for f in v['forms']]
        if zipf_frequency(best,'it')==0 and sl: best=max(sl,key=lambda s:zipf_frequency(s,'it'))
    res[(lem,pos)]=dict(v,cands=sorted(cs),hit=hit,lemma=best,z=zipf_frequency(best,'it'))
pickle.dump(res,open('items_checked.pkl','wb'))
miss=[(k,v) for k,v in res.items() if not v['hit'] and k[1]!='PROPN']
print('missing',len(miss),collections.Counter(k[1] for k,_ in miss))
miss.sort(key=lambda kv:-kv[1]['z'])
for k,v in miss[:40]: print(v['lemma'],k[1],v['n'],v['z'],list(v['forms'])[:3])
print(sum(1 for k,v in miss if v['z']>=3))
