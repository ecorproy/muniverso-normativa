"""Word final60 -> final61: Estado de la Nación 2026 (cap. 4), ICSC 2025 y ICDS de MIDEPLAN."""
import re,sys,copy,unicodedata
from docx import Document
from docx.shared import Cm
from docx.text.paragraph import Paragraph
fi,fo=sys.argv[1:3]; d=Document(fi); L='/home/claude/libro/'; RP='/home/claude/recursos/png/'
def P(): return d.paragraphs
def bloques(f): return [b.strip() for b in open(f,encoding='utf-8').read().split('\n\n') if b.strip()]
def busca(f,ini):
    r=[b for b in bloques(f) if b.startswith(ini)]; assert len(r)==1,(f,ini,len(r)); return r[0]
def runs(p,t):
    for k,part in enumerate(re.split(r'\*([^*]+)\*',t)):
        if part: r=p.add_run(part); r.italic=True if k%2 else None
def rango(titulo,nivel):
    ps=P(); h=[i for i,p in enumerate(ps) if p.style.name==nivel and p.text.strip()==titulo]; assert len(h)==1,titulo
    def fin(p): return p.style.name=='Heading 1' or (nivel=='Heading 2' and p.style.name=='Heading 2' and p.paragraph_format.page_break_before)
    e=next((i for i in range(h[0]+1,len(ps)) if fin(ps[i])),len(ps)); return h[0],e
def par(ini,a,b):
    ps=P(); k=[i for i in range(a,b) if ps[i].text.startswith(ini)]; assert len(k)==1,(ini,len(k)); return ps[k[0]]
def nuevo_despues(p,texto,estilo='Body Text'):
    n=copy.deepcopy(p._p)
    for ch in list(n):
        if not ch.tag.endswith('}pPr'): n.remove(ch)
    p._p.addnext(n); q=Paragraph(n,p._parent); q.style=d.styles[estilo]
    pf=q.paragraph_format; pf.page_break_before=None
    runs(q,texto); return q
def reemplaza(p,texto):
    for r in list(p.runs): r._r.getparent().remove(r._r)
    runs(p,texto)
modelo=P()[[i for i,p in enumerate(P()) if p.style.name=='Image Caption' and p.text.startswith('Figura 1.')][0]-1]
def imagen(after,png,alt,ancho=16):
    d.add_picture(png,width=Cm(ancho)); np_=P()[-1]._p; np_.getparent().remove(np_)
    if np_.pPr is not None: np_.remove(np_.pPr)
    if modelo._p.pPr is not None: np_.insert(0,copy.deepcopy(modelo._p.pPr))
    for dp in np_.xpath('.//wp:docPr'): dp.set('descr',alt); dp.set('title',alt)
    after._p.addnext(np_)
def clave(t): return unicodedata.normalize('NFD',t.lower()).encode('ascii','ignore').decode()
def ref(titulo,nivel,texto):
    a,b=rango(titulo,nivel); ps=P()
    h=[i for i in range(a,b) if ps[i].text=='Referencias' and ps[i].style.name.startswith('Heading')][0]
    refs=[]; i=h+1
    while i<b and not ps[i].style.name.startswith('Heading') and ps[i].text.strip(): refs.append(ps[i]); i+=1
    plano=re.sub(r'\*','',texto)
    if any(r.text==plano for r in refs): return
    pos=next((k for k,r in enumerate(refs) if clave(r.text)>clave(plano)),len(refs))
    if pos==0:
        nuevo_despues(ps[h],texto,'First Paragraph'); refs[0].style=d.styles['Body Text']
    else: nuevo_despues(refs[pos-1],texto,'Body Text')


import subprocess, difflib
REPO='/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos/'
def plano(t): return re.sub(r'\*','',t)
def parrafos(t): return [b.strip() for b in t.split('\n\n') if b.strip() and not b.startswith('#') and not b.startswith('[[')]
def viejo(c): return subprocess.run(['git','-C','/home/claude/repo/360','show','HEAD:Seguridad Municipal 360°/Taller del libro/Capítulos/'+c+'/out/'+c+'.md'],capture_output=True,text=True).stdout
def cuerpo_md(t): return t.split('\n## Referencias')[0]
def aplica(c,titulo,nivel):
    a_=parrafos(cuerpo_md(viejo(c))); b_=parrafos(cuerpo_md(open(L+c+'/chk_X/'+c+'.md',encoding='utf-8').read()))
    for tag,i1,i2,j1,j2 in reversed(difflib.SequenceMatcher(None,a_,b_,autojunk=False).get_opcodes()):
        if tag=='equal': continue
        a,b=rango(titulo,nivel); ps=P()
        def busca_w(md):
            k=[i for i in range(a,b) if ps[i].text.strip()==plano(md).strip()]
            assert len(k)==1,(c,md[:60],len(k)); return ps[k[0]]
        if tag=='replace' and i2-i1==j2-j1:
            for x,y in zip(a_[i1:i2],b_[j1:j2]): reemplaza(busca_w(x),y)
        elif tag=='insert':
            q=busca_w(a_[i1-1])
            for y in b_[j1:j2]: q=nuevo_despues(q,y)
        elif tag=='replace' and j2-j1>i2-i1:
            ws=[busca_w(x) for x in a_[i1:i2]]
            for w,y in zip(ws,b_[j1:j1+i2-i1]): reemplaza(w,y)
            q=ws[-1]
            for y in b_[j1+i2-i1:j2]: q=nuevo_despues(q,y)
        else: raise SystemExit((c,tag,i1,i2,j1,j2))
def quita_ref(titulo,nivel,ini):
    a,b=rango(titulo,nivel); ps=P()
    k=[i for i in range(a,b) if ps[i].text.startswith(ini)]; assert len(k)==1
    e=ps[k[0]]._p; e.getparent().remove(e)

aplica('cap03','3. El concepto','Heading 1')
aplica('t36','36. Economía local y reparto de la riqueza','Heading 2')
aplica('conclusion','Conclusión. Volver al núcleo','Heading 1')
RDE="Decreto Ejecutivo N.° 22266, *Reglamento del Defensor de los Habitantes de la República*. (1993). Poder Ejecutivo de la República de Costa Rica. Sistema Costarricense de Información Jurídica. https://sinalevi.go.cr/ResultadosNormativa/Informacion?param1=11785&param2=12656&param3=3&param4=68288"
RMI="Ministerio de Planificación Nacional y Política Económica. (2025). *Índice cantonal de desarrollo sostenible – Agenda 2030: 2020-2022*. https://biblioteca.mideplan.go.cr"
ref('3. El concepto','Heading 1',RDE)
ref('36. Economía local y reparto de la riqueza','Heading 2',RMI)
quita_ref('Conclusión. Volver al núcleo','Heading 1','Ministerio de Planificación Nacional')
# imagen de síntesis del capítulo 3
W='{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr'
A='{http://schemas.openxmlformats.org/drawingml/2006/main}blip'
REL='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed'
hecho=0
for dp in d.element.body.iter(W):
    if dp.get('descr')=='Lo esencial: qué es lo local':
        inl=dp.getparent()
        rid=[b.get(REL) for b in inl.iter(A)][0]
        d.part.related_parts[rid]._blob=open(RP+'cap03_sintesis.png','rb').read(); hecho+=1
assert hecho==1
# índices
ps=P()
for p in ps:
    if p.style.name=='Compact' and p.text.startswith('Ministerio de Planificación Nacional y Política Económica. (2025)'):
        reemplaza(p,p.text.replace(': temas 6; conclusión.',': temas 6, 36.'))
p26=[p for p in P() if p.style.name=='Compact' and p.text.startswith('Decreto Ejecutivo N.° 26831')][0]
q=nuevo_despues(p26,'Decreto Ejecutivo N.° 22266, Reglamento del Defensor de los Habitantes de la República (1993): capítulo 3.','Compact')
p26._p.addprevious(q._p)
d.save(fo); print('listo')
