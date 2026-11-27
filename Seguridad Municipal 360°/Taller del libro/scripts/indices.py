import re, json, collections
L=open('/home/claude/docx/libro.md',encoding='utf-8').read().split('\n')
extra=open('/home/claude/art/conclusion/out/zz_referencias.md',encoding='utf-8').read().split('\n')
units=[]; cur=None; inref=False
for x in L:
    m=re.match(r'^# (\d)\. ',x); t=re.match(r'^## (\d+)\. ',x)
    if m: cur=('cap',int(m.group(1))); inref=False; continue
    if x.startswith('# Introducción'): cur=('intro',0); inref=False; continue
    if x.startswith('# Conclusión'): cur=('concl',0); inref=False; continue
    if t and not x.startswith('### '): cur=('tema',int(t.group(1))); inref=False; continue
    if x.startswith('### Referencias'): inref=True; continue
    if x.startswith('#'): inref=False; continue
    if inref and x.strip(): units.append((cur,x.strip()))
if not any(c==('concl',0) for c,_ in units):
    for x in extra:
        if x.strip() and not x.startswith('#'): units.append((('concl',0),x.strip()))
def key(ref):
    r=ref.replace('*','')
    if r.startswith('Constitución Política'): return ('L','0','Constitución Política de la República de Costa Rica (1949)')
    m=re.match(r'Ley N\.° ([\d.]+), (.+?)\. \((\d{4})\)',r)
    if m: return ('L','1%07d'%int(m.group(1).replace('.','')),f'Ley N.° {m.group(1)}, {m.group(2)} ({m.group(3)})')
    m=re.match(r'Decreto Ejecutivo N\.° ([^,]+), (.+?)\. \((\d{4})\)',r)
    if m: return ('L','2'+m.group(1),f'Decreto Ejecutivo N.° {m.group(1)}, {m.group(2)} ({m.group(3)})')
    m=re.match(r'(Sala Constitucional|Sala Primera|Tribunal [^.(]+|Procuraduría General de la República|Contraloría General de la República)[^*]*?\. \(([^)]*)\)\. (.+?)(?:\. Sistema| \(expediente|\. https|$)',r)
    if m:
        org=m.group(1); doc=m.group(3).strip().rstrip('.')
        num=re.search(r'(\d{4}-\d{6}|C-\d{3}-\d{4}|\d{3,6}-[A-Z0-9-]+|\d+-\d{4})',doc)
        return ('J',org,doc)
    m=re.match(r'((?:Municipalidad|Concejo Municipal de Distrito) de [^.]+)\. \((\d{4})[a-z]?[^)]*\)\. (.+?)(?:\. Sistema|\. La Gaceta|\. https|\.$|$)',r)
    if m: return ('L','3'+m.group(1)+m.group(3),f'{m.group(3)}, {m.group(1)} ({m.group(2)})')
    m=re.match(r'(Instituto [^.]+|Consejo Nacional de Producción)\. \((\d{4})[^)]*\)\. (Reglamento.+?)(?:\. Sistema|\. La Gaceta|\. https|\.$|$)',r)
    if m: return ('L','4'+m.group(1)+m.group(3),f'{m.group(3)}, {m.group(1)} ({m.group(2)})')
    return ('O','',r[:120])
idx=collections.OrderedDict(); otros=collections.Counter()
for u,ref in units:
    k=key(ref)
    if k[0]=='O': idx.setdefault(('O','',ref.replace('*','').split('. Sistema')[0]),set()).add(u); otros[k[2][:60]]+=1; continue
    idx.setdefault(k,set()).add(u)
def lugares(s):
    caps=sorted(n for t,n in s if t=='cap'); temas=sorted(n for t,n in s if t=='tema'); c=any(t=='concl' for t,_ in s)
    parts=['introducción'] if any(t=='intro' for t,_ in s) else []
    if caps: parts.append(('capítulo ' if len(caps)==1 else 'capítulos ')+', '.join(map(str,caps)))
    if temas: parts.append(('tema ' if len(temas)==1 else 'temas ')+', '.join(map(str,temas)))
    if c: parts.append('conclusión')
    return '; '.join(parts)
leg=sorted([k for k in idx if k[0]=='L'],key=lambda k:(k[1][:1],k[1]))
jur=[k for k in idx if k[0]=='J']
orgs=['Sala Constitucional','Sala Primera','Tribunal','Procuraduría General de la República','Contraloría General de la República']
def okey(k):
    o=next(i for i,x in enumerate(orgs) if k[1].startswith(x))
    d=k[2]; y=n=0
    m=re.search(r'(\d{4})-(\d{6})',d) or None
    if m: y,n=int(m.group(1)),int(m.group(2))
    else:
        m=re.search(r'C-(\d{3})-(\d{4})',d)
        if m: y,n=int(m.group(2)),int(m.group(1))
        else:
            m=re.search(r'(\d+)-(\d{4})',d)
            if m: y,n=int(m.group(2)),int(m.group(1))
    sub=k[1] if orgs[o]=='Tribunal' else ''
    return (o,sub,y,n,d)
jur=sorted(jur,key=okey)
out=['# Índice de legislación','','Cada norma remite a los capítulos y temas en cuyas referencias aparece.','']
sec=None
names={'0':'Constitución','1':'Leyes','2':'Decretos ejecutivos','3':'Reglamentos y políticas municipales','4':'Reglamentos de otras instituciones'}
for k in leg:
    if k[1][0]!=sec: sec=k[1][0]; out+=['',f'### {names[sec]}','']
    out.append(f'- {k[2]}: {lugares(idx[k])}.')
out+=['','# Índice de jurisprudencia y criterios administrativos','','Cada resolución, dictamen u oficio remite a los capítulos y temas en cuyas referencias aparece.','']
sec=None
for k in jur:
    o=next(x for x in orgs if k[1].startswith(x)); lab={'Tribunal':'Otros tribunales'}.get(o,o)
    if lab!=sec: sec=lab; out+=['',f'### {lab}','']
    d=re.sub(r', de las [\d:]+ horas','',k[2])
    if o=='Tribunal': d=k[1]+', '+d
    out.append(f'- {d}: {lugares(idx[k])}.')
ext=re.compile(r'^(España|Francia|Italia|Tribunal de Justicia de la Unión|Fearn|Huerta|Katz|Leaders|Long Lake)')
obras=sorted([k for k in idx if k[0]=='O' and not ext.match(k[2])],key=lambda k:k[2])
extr=sorted([k for k in idx if k[0]=='O' and ext.match(k[2])],key=lambda k:k[2])
out+=['','### Jurisprudencia extranjera','']+[f'- {k[2].rstrip(".")}: {lugares(idx[k])}.' for k in extr]
out+=['','# Índice de obras y documentos citados','','Doctrina, informes y documentos institucionales que no son normas ni resoluciones.','']+[f'- {k[2].rstrip(".")}: {lugares(idx[k])}.' for k in obras]
open('/home/claude/indices/indices.md','w',encoding='utf-8').write('\n'.join(out)+'\n')
print(len(units),len(leg),len(jur)); print('OTROS',len(otros)); 
for a,b in otros.most_common(40): print(b,a)
