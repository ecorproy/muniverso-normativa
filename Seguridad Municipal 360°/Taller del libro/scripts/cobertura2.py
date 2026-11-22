# Cobertura por tema: propio de cada viñeta de las capas (primer identificador) frente a lo citado en el texto del tema.
import re, json
BASE='/home/claude/repo/360/Seguridad Municipal 360°/'
libro=open('/home/claude/libro/docx/libro.md',encoding='utf-8').read().replace('\\','')
adm=open(BASE+'Capa de jurisprudencia administrativa de los 36 temas.md',encoding='utf-8').read()
con=open(BASE+'Capa de jurisprudencia constitucional de los 36 temas.md',encoding='utf-8').read()
tca=open(BASE+'Capa de jurisprudencia contencioso administrativa de los 36 temas.md',encoding='utf-8').read()
leg=open(BASE+'Cuerpo legal de los 36 temas.md',encoding='utf-8').read()
nv=lambda y,n: f'{int(y)}-{int(n)}'
RX_VOTO=re.compile(r'N\.°\s*(\d{4})-0*(\d{1,6})')
RX_DICT=re.compile(r'\b((?:C|OJ)-\d{1,3}-\d{4})\b')
RX_LEY=re.compile(r'Ley(?:es)? N\.°\s*(\d{1,5})')
def secciones(txt, ini=None, fin=None):
    if ini: txt=txt[txt.index(ini):]
    if fin and fin in txt: txt=txt[:txt.index(fin)]
    out={}; cur=None
    for ln in txt.split('\n'):
        m=re.match(r'\*\*(\d{1,2})\.\s',ln)
        if m:
            cur=sorted({int(x) for x in re.findall(r'(?:^\*\*|/\s*)(\d{1,2})\.',ln)})
            for c in cur: out.setdefault(c,[])
            continue
        if ln.startswith('#') or ln.startswith('**'): cur=None; continue
        if cur and ln.strip().startswith('-'):
            for c in cur: out[c].append(ln)
    return out
A=secciones(adm,'## Cuadrante I'); C=secciones(con,'## Votos por tema','## Límites de la competencia municipal')
T=secciones(tca,'## Votos por tema','## Laterales de otras jurisdicciones'); L=secciones(leg,'## Cuadrante I')
pars=[p for p in libro.split('\n') if p.strip()]
i5=[i for i,p in enumerate(pars) if p.startswith('**5. Los treinta y seis temas')][0]
i6=[i for i,p in enumerate(pars) if p.startswith('**6. Conclusión')][0]
tema={}; cur=None
for p in pars[i5:i6]:
    m=re.search(r'\(tema (\d{1,2})\)',p[:200])
    if re.match(r'\*\*Cuadrante|Leído en conjunto|El cuadrante|El recorrido deja|El (primer|segundo|tercer|cuarto) cuadrante',p): cur=None; continue
    if m: cur=int(m.group(1)); tema.setdefault(cur,[])
    if cur: tema[cur].append(p)
nombres={}
for m in re.finditer(r'\*\*(\d{1,2})\. ([^*]+)\*\*',leg): nombres[int(m.group(1))]=m.group(2).strip()
tot=dict(w=0,lc=0,la=0,pa=0,pb=0,pc=0,cg=0,vp=0,vc=0,ta=0,tc=0)
rows=[]
for n in range(1,37):
    txt=' '.join(tema.get(n,[])); w=len(txt.split())
    leyes=set()
    for ln in L.get(n,[]):
        leyes|=set(RX_LEY.findall(ln))
        if re.search(r'\bCM\b',ln): leyes.add('7794')
    lt=set(RX_LEY.findall(txt))
    pa=set(); pb=set(); cg=0
    for ln in A.get(n,[]):
        m=RX_DICT.search(ln)
        if 'CGR' in ln[:14]: cg+=1; continue
        if m: (pa if ln.lstrip('- ').startswith('A') else pb).add(m.group(1))
    dt=set(RX_DICT.findall(txt))
    vp=set()
    for ln in C.get(n,[]):
        if ln.lstrip('- ').startswith('Ver '): continue
        m=RX_VOTO.search(ln)
        if m: vp.add(nv(*m.groups()))
    vt={nv(y,x) for y,x in RX_VOTO.findall(txt)}
    tc=set()
    for ln in T.get(n,[]):
        m=re.search(r'N\.°\s*(\d{1,5})-(\d{4})',ln)
        if m: tc.add(f'{int(m.group(1))}-{m.group(2)}')
    tt={f'{int(a)}-{b}' for a,b in re.findall(r'Tribunal Contencioso Administrativo[^)]{0,60}?resoluci[oó]n N\.°\s*(\d{1,5})-(\d{4})',txt)}
    r=dict(n=n,nombre=nombres.get(n,''),w=w,lc=len(leyes&lt),la=len(leyes),pc=len((pa|pb)&dt),pa=len(pa),pb=len(pb),cg=cg,vc=len(vp&vt),vp=len(vp),tc=len(tc&tt),ta=len(tc),
           leyes_sin=sorted(leyes-lt,key=int))
    rows.append(r)
    for k in tot: tot[k]+=r[k]
    print(f"| {n} | {r['nombre'][:34]} | {w} | {r['lc']}/{r['la']} | {r['pc']}/{r['pa']+r['pb']} (A {r['pa']}) | {cg} | {r['vc']}/{r['vp']} | {r['tc']}/{r['ta']} |")
print('TOTALES',tot)
json.dump(rows,open('/home/claude/libro/cobertura2.json','w'),ensure_ascii=False,indent=1)
alltca=set(re.findall(r'N\.°\s*(\d{1,5}-\d{4})',tca[tca.index('## Votos por tema'):tca.index('## Laterales de otras jurisdicciones')]))
print('resoluciones TCA distintas en la capa (por tema y organización):',len(alltca))
for q,(a,b) in {'I':(1,9),'II':(10,18),'III':(19,27),'IV':(28,36)}.items():
    s=[r for r in rows if a<=r['n']<=b]
    print(q,'palabras',sum(r['w'] for r in s),'| leyes',sum(r['lc'] for r in s),'/',sum(r['la'] for r in s),'| PGR',sum(r['pc'] for r in s),'/',sum(r['pa']+r['pb'] for r in s),'| CGR',sum(r['cg'] for r in s),'| votos',sum(r['vc'] for r in s),'/',sum(r['vp'] for r in s),'| TCA',sum(r['tc'] for r in s),'/',sum(r['ta'] for r in s))
