# Compara, por tema, lo disponible en las capas del repositorio con lo que el texto actual del libro cita.
import re, json, sys
BASE='/home/claude/repo/360/Seguridad Municipal 360°/'
libro=open('/home/claude/libro/docx/libro.md',encoding='utf-8').read().replace('\\','')
adm=open(BASE+'Capa de jurisprudencia administrativa de los 36 temas.md',encoding='utf-8').read()
con=open(BASE+'Capa de jurisprudencia constitucional de los 36 temas.md',encoding='utf-8').read()
tca=open(BASE+'Capa de jurisprudencia contencioso administrativa de los 36 temas.md',encoding='utf-8').read()
leg=open(BASE+'Cuerpo legal de los 36 temas.md',encoding='utf-8').read()

def nv(y,n): return f'{int(y)}-{int(n)}'
RX_VOTO=re.compile(r'(?:voto|votos)?\s*N\.°\s*(\d{4})-0*(\d{1,6})')
RX_DICT=re.compile(r'\b((?:C|OJ|PGR-C|PGR-OJ)-\d{1,3}-\d{4})\b')
RX_LEY=re.compile(r'Ley(?:es)? N\.°\s*(\d{1,5})')
RX_TCA=re.compile(r'resoluci[oó]n N\.°\s*(\d{1,5})-(\d{4})')

def secciones(txt, ini=None, fin=None):
    if ini: txt=txt[txt.index(ini):]
    if fin and fin in txt: txt=txt[:txt.index(fin)]
    out={}; cur=None
    for ln in txt.split('\n'):
        m=re.match(r'\*\*(\d{1,2})\.\s',ln)
        m2=re.match(r'\*\*(\d{1,2})\.\s.*?/\s*(\d{1,2})\.',ln)
        if m:
            cur=[int(m.group(1))]
            if m2: cur.append(int(m2.group(2)))
            for c in cur: out.setdefault(c,[])
            continue
        if ln.startswith('#') or (ln.startswith('**') and not m): cur=None; continue
        if cur and ln.strip():
            for c in cur: out[c].append(ln)
    return out

A=secciones(adm,'## Cuadrante I')
C=secciones(con,'## Votos por tema','## Límites de la competencia municipal')
T=secciones(tca,'## Votos por tema','## Efecto sobre el 360')
L=secciones(leg,'## Cuadrante I')

# libro: párrafos de la sección 5 por tema
pars=[p for p in libro.split('\n') if p.strip()]
i5=[i for i,p in enumerate(pars) if p.startswith('**5. Los treinta y seis temas')][0]
i6=[i for i,p in enumerate(pars) if p.startswith('**6. Conclusión')][0]
tema={}; cur=None
for p in pars[i5:i6]:
    m=re.search(r'\(tema (\d{1,2})\)',p[:200])
    if p.startswith('**Cuadrante') or p.startswith('Leído en conjunto') or p.startswith('El cuadrante') or p.startswith('El recorrido deja') or p.startswith('El primer cuadrante') or p.startswith('El segundo cuadrante') or p.startswith('El tercer cuadrante') or p.startswith('El cuarto cuadrante'):
        cur=None; continue
    if m: cur=int(m.group(1)); tema.setdefault(cur,[])
    if cur: tema[cur].append(p)

todo_votos={nv(y,n) for y,n in RX_VOTO.findall(libro)}
todo_dict=set(RX_DICT.findall(libro))
todo_ley=set(RX_LEY.findall(libro))
todo_tca={f'{int(n)}-{y}' for n,y in RX_TCA.findall(libro) if 'Tribunal Contencioso' in libro}
print('LIBRO, totales distintos: leyes',len(todo_ley),'| dictámenes',len(todo_dict),'| votos Sala',len(todo_votos))
tcas_libro=set()
for m in re.finditer(r'Tribunal Contencioso Administrativo[^)]{0,60}?resoluci[oó]n N\.°\s*(\d{1,5})-(\d{4})',libro): tcas_libro.add(f'{int(m.group(1))}-{m.group(2)}')
print('LIBRO, resoluciones TCA distintas:',len(tcas_libro),sorted(tcas_libro))
cap_votos=set(); cap_dict=set()
for k,v in C.items():
    for ln in v: cap_votos|={nv(y,n) for y,n in RX_VOTO.findall(ln)}
for k,v in A.items():
    for ln in v: cap_dict|=set(RX_DICT.findall(ln))
print('CAPAS: dictámenes distintos por tema',len(cap_dict),'| votos distintos en "Votos por tema"',len(cap_votos))
print('  dictámenes de las capas citados en el libro:',len(cap_dict&todo_dict),'| votos de las capas citados en el libro:',len(cap_votos&todo_votos))
print('  dictámenes citados en el libro que no están en la capa por tema:',sorted(todo_dict-cap_dict))
allcon_votos={nv(y,n) for y,n in RX_VOTO.findall(con)}
print('  votos mencionados en toda la capa constitucional:',len(allcon_votos),'| de ellos citados en el libro:',len(allcon_votos&todo_votos))
rows=[]
print()
print('tema | palabras | leyes cuerpo legal / citadas en el tema | PGR capa (A+B) / citados tema | CGR capa | votos capa propios+ver / citados tema | TCA capa / citados tema')
for n in range(1,37):
    txt=' '.join(tema.get(n,[]))
    w=len(txt.split())
    leyes_cap=set()
    for ln in L.get(n,[]):
        leyes_cap|=set(RX_LEY.findall(ln))
        if re.search(r'\bCM\b',ln): leyes_cap.add('7794')
        if re.search(r'\bLGAP\b',ln): leyes_cap.add('6227')
    leyes_t=set(RX_LEY.findall(txt))
    d_cap=set(); cgr=0
    for ln in A.get(n,[]):
        d_cap|=set(RX_DICT.findall(ln))
        if 'CGR' in ln[:12]: cgr+=1
    d_t=set(RX_DICT.findall(txt))
    v_prop=set(); v_ver=set()
    for ln in C.get(n,[]):
        vs={nv(y,x) for y,x in RX_VOTO.findall(ln)}
        if ln.lstrip('- ').startswith('Ver '): v_ver|=vs
        else:
            m=RX_VOTO.search(ln)
            if m: v_prop.add(nv(*m.groups()))
    v_t={nv(y,x) for y,x in RX_VOTO.findall(txt)}
    t_cap=set()
    for ln in T.get(n,[]):
        for m in re.finditer(r'N\.°\s*(\d{1,5})-(\d{4})',ln): t_cap.add(f'{int(m.group(1))}-{m.group(2)}')
    t_t=set()
    for m in re.finditer(r'Tribunal Contencioso Administrativo[^)]{0,60}?resoluci[oó]n N\.°\s*(\d{1,5})-(\d{4})',txt): t_t.add(f'{int(m.group(1))}-{m.group(2)}')
    rows.append(dict(tema=n,palabras=w,leyes_cap=len(leyes_cap),leyes_cit=len(leyes_t),leyes_falt=sorted(leyes_cap-leyes_t,key=int),pgr_cap=len(d_cap),pgr_cit=len(d_t),pgr_cit_de_capa=len(d_cap&d_t),cgr_cap=cgr,votos_prop=len(v_prop),votos_ver=len(v_ver-v_prop),votos_cit=len(v_t),votos_prop_cit=len(v_prop&v_t),tca_cap=len(t_cap),tca_cit=len(t_t)))
    r=rows[-1]
    print(f"{n:2d} | {w:4d} | {r['leyes_cap']:2d}/{r['leyes_cit']:2d} | {r['pgr_cap']:2d}/{r['pgr_cit']:2d} | {cgr} | {r['votos_prop']:2d}+{r['votos_ver']:2d}/{r['votos_cit']:2d} (propios citados {r['votos_prop_cit']}) | {r['tca_cap']}/{r['tca_cit']}")
json.dump(rows,open('/home/claude/libro/cobertura.json','w'),ensure_ascii=False,indent=1)
S=lambda k: sum(r[k] for r in rows)
print('\nSUMAS por tema (con repeticiones entre temas): leyes capa',S('leyes_cap'),'citadas',S('leyes_cit'),'| PGR capa',S('pgr_cap'),'citados',S('pgr_cit'),'| CGR capa',S('cgr_cap'),'| votos propios',S('votos_prop'),'citados',S('votos_prop_cit'),'| TCA capa',S('tca_cap'),'citados',S('tca_cit'))
