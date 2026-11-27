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

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
# 1. autocitas
def aplica2(c,arch,titulo,nivel):
    import subprocess
    old=subprocess.run(['git','-C','/home/claude/repo/360','show','HEAD:Seguridad Municipal 360°/Taller del libro/Capítulos/'+c+'/out/'+arch],capture_output=True,text=True).stdout
    a_=parrafos(cuerpo_md(old)); b_=parrafos(cuerpo_md(open(L+c+'/chk_X/'+arch,encoding='utf-8').read()))
    a,b=rango(titulo,nivel); ps=P(); n=0
    for x,y in zip(a_,b_):
        if x==y: continue
        k=[i for i in range(a,b) if ps[i].text.strip()==plano(x).strip()]; assert len(k)==1,(c,x[:60],len(k))
        reemplaza(ps[k[0]],y); n+=1
    assert len(a_)==len(b_); print(c,n)
aplica2('cap02','all.md','2. Lo local en el artículo 169','Heading 1')
aplica2('cap04','cap04.md','4. La persona en el centro','Heading 1')
# 2. centrado por estilo
for nombre in ['Heading 1','Captioned Figure','Image Caption']:
    d.styles[nombre].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
for p in P():
    if p._p.findall('.//'+qn('w:drawing')): p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
# 3. índice de figuras: SEQ en cada leyenda y TOC por identificador
def campo(par_el, antes_run, instr, resultado):
    def r(): return OxmlElement('w:r')
    els=[]
    b=r(); fc=OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'),'begin'); b.append(fc); els.append(b)
    i=r(); it=OxmlElement('w:instrText'); it.set(qn('xml:space'),'preserve'); it.text=instr; i.append(it); els.append(i)
    sp=r(); fc=OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'),'separate'); sp.append(fc); els.append(sp)
    t=r(); tt=OxmlElement('w:t'); tt.text=resultado; t.append(tt); els.append(t)
    e=r(); fc=OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'),'end'); e.append(fc); els.append(e)
    for x in els: antes_run.addprevious(x)
n=0
for p in P():
    if p.style.name!='Image Caption' or 'SEQ Figura' in p._p.xml: continue
    m=re.match(r'Figura (\d+)\.',p.text); assert m,p.text[:40]
    r0=p.runs[0]; t=r0.text; assert t.startswith('Figura '+m.group(1)),t[:30]
    rest=t[len('Figura '+m.group(1)):]
    r0.text='Figura '
    nuevo=copy.deepcopy(r0._r); r0._r.addnext(nuevo)
    from docx.text.run import Run
    Run(nuevo,p).text=rest
    campo(p._p,nuevo,' SEQ Figura \\* ARABIC ',m.group(1)); n+=1
print('leyendas',n)
ok=0
for it in d.element.body.iter(qn('w:instrText')):
    if it.text and 'TOC' in it.text and 'Image Caption' in it.text:
        it.text=' TOC \\h \\z \\c "Figura" '; ok+=1
        beg=it.getparent().getprevious().find(qn('w:fldChar')); beg.set(qn('w:dirty'),'true')
assert ok==1
d.save(fo); print('listo')
