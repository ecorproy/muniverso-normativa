import sys,re,hashlib,json
sys.path.insert(0,'/home/claude/division')
from docx import Document
from docx.oxml.ns import qn
from indices import lee
from lxml import etree
ORIG='/home/claude/Seguridad Municipal 360 (final76).docx'
TI='/home/claude/division/Seguridad Municipal 360° — Tomo I — Fundamentos, vida y dignidad.docx'
TII='/home/claude/division/Seguridad Municipal 360° — Tomo II — Protección especial, bienestar y entorno.docx'
def T(e): return ''.join(t.text or '' for t in e.iter(qn('w:t')))
def S(e):
    s=e.find(qn('w:pPr')+'/'+qn('w:pStyle')) if e.tag==qn('w:p') else None
    return s.get(qn('w:val')) if s is not None else ''
def imgs(d,els):
    out=[]
    for e in els:
        for b in e.iter(qn('a:blip')):
            out.append(hashlib.sha256(d.part.related_parts[b.get(qn('r:embed'))].blob).hexdigest()[:16])
    return out
def info(d,els):
    return dict(textos=[T(e) for e in els if e.tag in (qn('w:p'),qn('w:tbl'))],
                xml=[re.sub(r' w:id="\d+"','',re.sub(r'r:(embed|id)="[^"]+"','',etree.tostring(e).decode())) for e in els if e.tag in (qn('w:p'),qn('w:tbl'))],
                imgs=imgs(d,els),
                hl=[d.part.rels[h.get(qn('r:id'))].target_ref for e in els for h in e.iter(qn('w:hyperlink')) if h.get(qn('r:id'))],
                bm=[b.get(qn('w:name')) for e in els for b in e.iter(qn('w:bookmarkStart'))]+[e.get(qn('w:name')) for e in els if e.tag==qn('w:bookmarkStart')])
o=Document(ORIG); oe=list(o.element.body)
a=Document(TI); ae=list(a.element.body); b=Document(TII); be=list(b.element.body)
def rango(els,ini_txt,fin_pred):
    i=next(k for k,e in enumerate(els) if S(e)=='Heading1' and T(e)==ini_txt)
    # incluir marcador inmediatamente anterior
    while i>0 and els[i-1].tag==qn('w:bookmarkStart'): i-=1
    j=next(k for k,e in enumerate(els) if fin_pred(e))
    return els[i:j]
O=info(o,oe[5:6008])
A=info(a,rango(ae,'Prólogo',lambda e:T(e)=='Nota de continuidad'))
B=info(b,rango(be,'Cuadrante III. Protección especial',lambda e:S(e)=='Heading1' and T(e)=='Índice de legislación'))
res={}
res['textos_original']=len(O['textos']); res['textos_tomos']=len(A['textos'])+len(B['textos'])
res['texto_identico']=O['textos']==A['textos']+B['textos']
res['xml_identico']=O['xml']==A['xml']+B['xml']
if not res['xml_identico']:
    dif=[k for k,(x,y) in enumerate(zip(O['xml'],A['xml']+B['xml'])) if x!=y]; res['xml_dif']=dif[:5]
    if dif: k=dif[0]; res['ej']=(O['xml'][k][:300],(A['xml']+B['xml'])[k][:300])
res['imagenes_original']=len(O['imgs']); res['imagenes_tomos']=len(A['imgs'])+len(B['imgs']); res['imagenes_identicas']=O['imgs']==A['imgs']+B['imgs']
res['hipervinculos']=(len(O['hl']),len(A['hl'])+len(B['hl']),O['hl']==A['hl']+B['hl'])
res['marcadores']=(len(O['bm']),len(A['bm'])+len(B['bm']),sorted(O['bm'])==sorted(A['bm']+B['bm']))
res['palabras']=(sum(len(t.split()) for t in O['textos']),sum(len(t.split()) for t in A['textos']+B['textos']))
res['caracteres']=(sum(len(t) for t in O['textos']),sum(len(t) for t in A['textos']+B['textos']))
# portada
res['logo_I']=imgs(a,ae[:1])==imgs(o,oe[:1]); res['logo_II']=imgs(b,be[:1])==imgs(o,oe[:1])
# índices: unión de relaciones
def rel(els):
    R={}
    for ind,cat,i,nombre,uni in lee(els): R[(ind,nombre)]=set(uni or [])
    return R
Ro=rel(list(Document('/tmp/final76_indices_corregidos.docx').element.body))
def rel_tomo(els):
    R={}
    for e in els:
        tx=T(e)
        if S(e)!='Compact': continue
        m=re.match(r'(.*?): ((?:introducción|capítulos?|temas?|conclusión|anexos)[^.]*?)(?:\. Véase también Tomo (?:I|II): (.*))?\.$',tx)
        if m: R[m.group(1)]=(m.group(2),m.group(3))
    return R
from indices import unidades
Ra,Rb=rel_tomo(ae),rel_tomo(be)
mal=[]
for (ind,nombre),us in Ro.items():
    tot=set()
    for R in (Ra,Rb):
        if nombre in R:
            x,y=R[nombre]; tot|=set(unidades(x))|set(unidades(y or ''))
    if tot!=us: mal.append((nombre[:60],sorted(us^tot)))
res['indices_entradas_original']=len(Ro); res['indices_relaciones_original']=sum(len(v) for v in Ro.values())
res['indices_entradas_TI']=len(Ra); res['indices_entradas_TII']=len(Rb)
res['indices_compartidas_TI']=sum(1 for v in Ra.values() if v[1]); res['indices_compartidas_TII']=sum(1 for v in Rb.values() if v[1])
res['indices_relaciones_no_conservadas']=mal[:10]; res['n_mal']=len(mal)
print(json.dumps(res,ensure_ascii=False,indent=1))
json.dump(res,open('auditoria.json','w'),ensure_ascii=False,indent=1)
