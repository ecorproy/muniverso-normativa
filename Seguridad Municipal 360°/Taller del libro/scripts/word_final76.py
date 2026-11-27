"""final76: sin huecos por figuras. Parte de final75.
1) Las 17 figuras numeradas dejan de ser tablas flotantes (tblpPr) y quedan en el flujo.
2) Aplica las operaciones de huecos_ops.json, una por figura (clave = rId de la imagen):
   - escala s: reduce la figura;
   - despues k: la mueve detrás de los k párrafos de texto que la siguen;
   - antes k: la mueve delante de los k párrafos de texto que la preceden."""
import json,sys,os
from docx import Document
from docx.oxml.ns import qn
SRC='/home/claude/Seguridad Municipal 360 (final75).docx'
OUT=sys.argv[1] if len(sys.argv)>1 else '/home/claude/Seguridad Municipal 360 (final76).docx'
OPS=json.load(open('/home/claude/adenda_scripts/huecos_ops.json')) if os.path.exists('/home/claude/adenda_scripts/huecos_ops.json') else {}
d=Document(SRC); body=d.element.body
def clave(e):
    b=e.find('.//'+qn('a:blip')); return b.get(qn('r:embed')) if b is not None else None
for t in body.findall(qn('w:tbl')):
    pr=t.find(qn('w:tblPr')); fp=pr.find(qn('w:tblpPr')) if pr is not None else None
    if fp is not None and t.find('.//'+qn('wp:extent')) is not None:
        pr.remove(fp); ov=pr.find(qn('w:tblOverlap'))
        if ov is not None: pr.remove(ov)
# todas las figuras flotantes («arriba de la página») pasan a estar en el flujo
def a_inline(e):
    a=e.find('.//'+qn('wp:anchor'))
    if a is None: return
    il=a.makeelement(qn('wp:inline'),{'distT':'0','distB':'0','distL':'0','distR':'0'})
    for t in ('wp:extent','wp:effectExtent','wp:docPr','wp:cNvGraphicFramePr','a:graphic'):
        c=a.find(qn(t))
        if c is not None: il.append(c)
    a.getparent().replace(a,il)
    pp=e.find(qn('w:pPr'))
    if pp is None: pp=e.makeelement(qn('w:pPr'),{}); e.insert(0,pp)
    if pp.find(qn('w:jc')) is None: pp.append(pp.makeelement(qn('w:jc'),{qn('w:val'):'center'}))
    sp=pp.find(qn('w:spacing'))
    if sp is not None: pp.remove(sp)
    pp.append(pp.makeelement(qn('w:spacing'),{qn('w:before'):'60',qn('w:after'):'120'}))
for e in list(body):
    if e.tag==qn('w:p') and e.find('.//'+qn('wp:anchor')) is not None: a_inline(e)
def es_texto(e):
    if e.tag!=qn('w:p') or e.find('.//'+qn('wp:extent')) is not None: return False
    s=e.find(qn('w:pPr')+'/'+qn('w:pStyle')); s=s.get(qn('w:val')) if s is not None else ''
    return s in ('BodyText','FirstParagraph','Compact','BlockText')
figs={clave(e):e for e in body if e.find('.//'+qn('wp:extent')) is not None and clave(e)}
for k,op in OPS.items():
    e=figs[k]
    if 'escala' in op:
        s=op['escala']
        for x in e.iter(qn('wp:extent')):
            x.set('cx',str(int(int(x.get('cx'))*s))); x.set('cy',str(int(int(x.get('cy'))*s)))
        for x in e.iter(qn('a:ext')):
            if x.get('cx'): x.set('cx',str(int(int(x.get('cx'))*s))); x.set('cy',str(int(int(x.get('cy'))*s)))
    grupo=[e]
    n=e.getnext()
    if e.tag==qn('w:p') and n is not None and n.tag==qn('w:p'):
        st=n.find(qn('w:pPr')+'/'+qn('w:pStyle'))
        if st is not None and st.get(qn('w:val')) in ('ImageCaption','Caption'): grupo.append(n)
    if op.get('junto') and grupo[-1].getnext() is not None: grupo.append(grupo[-1].getnext())
    if op.get('estilo_figura'):
        pp=e.find(qn('w:pPr')); st=pp.find(qn('w:pStyle')); st.set(qn('w:val'),'CaptionedFigure')
        if pp.find(qn('w:jc')) is None: pp.append(pp.makeelement(qn('w:jc'),{qn('w:val'):'center'}))
    if op.get('mov',0)>0:
        ref=grupo[-1]
        for _ in range(op['mov']):
            n=ref.getnext()
            if n is None or not es_texto(n): break
            ref=n
        if ref is not grupo[-1]:
            for g in reversed(grupo): ref.addnext(g)
    if op.get('mov',0)<0:
        ref=e
        for _ in range(-op['mov']):
            n=ref.getprevious()
            if n is None or not es_texto(n): break
            ref=n
        if ref is not e:
            for g in grupo: ref.addprevious(g)
d.save(OUT); print('ok',OUT,len(OPS),'operaciones')
