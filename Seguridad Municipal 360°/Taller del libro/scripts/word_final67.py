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
modelo=None  # las leyendas van ahora dentro de tablas flotantes
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

from docx.shared import Pt
from docx.oxml.ns import qn
import unicodedata
def bloques_md(t):
    out=[]
    for b in t.split('\n\n'):
        b=b.strip()
        if not b or b.startswith('[[') or b.startswith('<?') or b.startswith('# '): continue
        out.append(b)
    return out
def nuevo_md(q,b):
    if b.startswith('## '): return nuevo_despues(q,b[3:],'Heading 2')
    if b.startswith('### '): return nuevo_despues(q,b[4:],'Heading 3')
    return nuevo_despues(q,b)
def aplica3(c,titulo,nivel):
    a_=bloques_md(cuerpo_md(viejo(c))); b_=bloques_md(cuerpo_md(open(L+c+'/chk_X/'+c+'.md',encoding='utf-8').read()))
    n=0
    for tag,i1,i2,j1,j2 in reversed(difflib.SequenceMatcher(None,a_,b_,autojunk=False).get_opcodes()):
        if tag=='equal': continue
        a,b=rango(titulo,nivel); ps=P()
        def busca_w(md):
            t=plano(md[3:] if md.startswith('## ') else md).strip()
            k=[i for i in range(a,b) if ps[i].text.strip()==t]
            assert len(k)==1,(c,md[:60],len(k)); return ps[k[0]]
        if tag=='replace' and i2-i1==j2-j1:
            for x,y in zip(a_[i1:i2],b_[j1:j2]): reemplaza(busca_w(x),y); n+=1
        elif tag in ('insert','replace'):
            ws=[busca_w(x) for x in a_[i1:i2]]
            for w,y in zip(ws,b_[j1:j1+(i2-i1)]): reemplaza(w,y); n+=1
            q=ws[-1] if ws else busca_w(a_[i1-1])
            for y in b_[j1+(i2-i1):j2]: q=nuevo_md(q,y); n+=1
        else: raise SystemExit((c,tag))
    print(c,'cambios',n)
def refs_en_orden(c,titulo,nivel):
    zz=[x.strip() for x in open(L+c+'/chk_X/zz_referencias.md',encoding='utf-8').read().split('\n\n') if x.strip() and not x.startswith('#')]
    n=0
    for k,z in enumerate(zz):
        a,b=rango(titulo,nivel); ps=P()
        h=[i for i in range(a,b) if ps[i].text=='Referencias' and ps[i].style.name.startswith('Heading')][0]
        lista=[ps[i] for i in range(h+1,b) if ps[i].text.strip()]
        if any(p.text.startswith(plano(z)[:70]) for p in lista): continue
        prev=None
        for j in range(k-1,-1,-1):
            m=[p for p in lista if p.text.startswith(plano(zz[j])[:70])]
            if m: prev=m[0]; break
        if prev is None:
            nuevo_despues(ps[h],z,'First Paragraph'); lista[0].style=d.styles['Body Text']
        else: nuevo_despues(prev,z,'Body Text')
        n+=1
    print(c,'refs',n)
from docx.text.paragraph import Paragraph

aplica3('cap03','3. El concepto','Heading 1')
import glob
n=0
for i in range(1,37):
    c=f't{i:02d}'
    titulo=open(L+c+'/chk_X/'+c+'.md',encoding='utf-8').read().split('\n',1)[0][2:].strip()
    tesis=[x for x in open(L+c+'/chk_X/'+c+'.md',encoding='utf-8').read().split('\n\n') if x.startswith('*Tesis del tema.*')][0]
    a,b=rango(titulo,'Heading 2'); ps=P()
    if any(ps[k].text.startswith('Tesis del tema.') for k in range(a,b)): continue
    h=[k for k in range(a,b) if ps[k].text=='El caso' and ps[k].style.name.startswith('Heading')][0]
    modelo_p=ps[h+1]
    nuevo=copy.deepcopy(modelo_p._p)
    for ch in list(nuevo):
        if not ch.tag.endswith('}pPr'): nuevo.remove(ch)
    ps[h]._p.addprevious(nuevo)
    q=Paragraph(nuevo,ps[h]._parent); q.style=d.styles['Body Text']; runs(q,tesis); n+=1
print('tesis',n)
d.save(fo); print('listo')
