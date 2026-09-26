import re,html,json,collections,math
from wordfreq import zipf_frequency as Z
def clean(s,lang):
    s=html.unescape(re.sub(r'<[^>]+>','',s))
    s=re.sub(r'\[[^\]]*\]|\{[^}]*\}|\([^)]*\)','',s)
    s=s.strip().strip('.').strip()
    s=s.lower() if lang=='en' else s.replace('I','ı').replace('İ','i').lower()
    if lang=='en': s=re.sub(r'^(to|a|an|the)\s+','',s)
    s=re.sub(r'\s+',' ',s).strip()
    if not s or len(s)>30 or len(s.split())>3: return None
    if not re.fullmatch(r"[a-zçğıöşüâîû' -]+",s) or s.startswith('-') or s.endswith('-'): return None
    return s
BAD=re.compile(r"\b(someone|something|somebody|one's|oneself|equivalent|expressing|used|indicating|denoting|form of|plural|singular)\b")
# EN->TR (translation tables)
entr=collections.defaultdict(lambda: collections.defaultdict(float))
for line in open('wiktionary-dict/src/en-tr-enwiktionary.txt',encoding='utf-8'):
    m=re.match(r'^(.+?) \{([^}]+)\}.*?:: (.*)$',line.strip())
    if not m: continue
    en=m.group(1).strip().lower()
    if m.group(2) in ('prop',): continue
    for j,t in enumerate(re.split(r'[,;]',m.group(3))):
        if '[' in t: continue
        t=clean(t,'tr')
        if t: entr[en][t]+=1/(1+0.15*j)
# TR->EN (Turkish entries)
tren=collections.defaultdict(lambda: collections.defaultdict(float))
for line in open('Wiktionary-Dictionaries/Turkish-English Wiktionary dictionary.tsv',encoding='utf-8'):
    if '\t' not in line: continue
    hw,body=line.rstrip('\n').split('\t',1)
    heads=[clean(h,'tr') for h in hw.split('|')]
    heads=[h for h in heads if h]
    if not heads: continue
    lis=re.findall(r'<li>(.*?)</li>',body)
    for k,li in enumerate(lis):
        li=re.sub(r'<[^>]+>','',li); li=re.sub(r'\([^)]*\)','',html.unescape(li))
        if k>=5: break
        for p,e in enumerate(re.split(r'[,;]',li)):
            e=clean(e,'en')
            if e and not BAD.search(e):
                for h in heads[:1]: tren[h][e]+=1/(1+0.3*k)/(1+0.15*p)
# inverted
inv=collections.defaultdict(lambda: collections.defaultdict(float))
for t,d in tren.items():
    for e,w in d.items(): inv[e][t]+=w
entr_inv=collections.defaultdict(lambda: collections.defaultdict(float))
for e,d in entr.items():
    for t,w in d.items(): entr_inv[t][e]+=w
def rank(cands,lang,exclude=(),both=()):
    out=[]
    for t,d in cands.items():
        if t in exclude: continue
        f=Z(t,lang)
        if f<(2.5 if lang=='en' else 1.5) and len(cands)>1: continue
        out.append((t, d*(1.8 if t in both else 1)*(f+1)**0.8))
    out.sort(key=lambda x:-x[1])
    if not out: return []
    top=out[0][1]
    out=[x for x in out if x[1]>=0.2*top]
    return [[t, 100 if i==0 else max(30,round(100*math.sqrt(s/top)))] for i,(t,s) in enumerate(out[:8])]
def en2tr(e):
    c=collections.defaultdict(float)
    for t,w in entr.get(e,{}).items(): c[t]+=w
    for t,w in inv.get(e,{}).items(): c[t]+=0.6*w
    return rank(c,'tr',both=set(entr.get(e,{}))&set(inv.get(e,{})))
def tr2en(t,exclude):
    c=collections.defaultdict(float)
    for e,w in tren.get(t,{}).items(): c[e]+=w
    for e,w in entr_inv.get(t,{}).items(): c[e]+=0.6*w
    return rank(c,'en',exclude,both=set(tren.get(t,{}))&set(entr_inv.get(t,{})))
if __name__=='__main__':
    for e in 'house three cold run book reluctant home achieve available therefore meticulous friend eat get take'.split():
        r=en2tr(e); print(e, r, '| rev', tr2en(r[0][0],{e}) if r else '')
