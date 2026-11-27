"""Word final61 -> final62: corrección del congreso de 2016 en la introducción."""
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


f=L+'intro/src/intro.md'; T='Introducción. El camino'
a,b=rango(T,'Heading 1')
p=par('Todo empezó en octubre',a,b); reemplaza(p,busca(f,'Todo empezó en octubre'))
q=nuevo_despues(p,busca(f,'El congreso tenía un objetivo'))
a,b=rango(T,'Heading 1'); p=par('Recuerdo perfectamente a varias',a,b); reemplaza(p,busca(f,'El panel de expertos'))
ref(T,'Heading 1','Municipalidad de San José. (2016, 21 de octubre). *V Congreso Jurídico Municipal “Dr. Mauro Murillo Arias”*. https://munimsj.wordpress.com/2016/10/21/v-congreso-juridico-municipal-dr-mauro-murillo-arias/')
t='Municipalidad de San José. (2016, 21 de octubre). V Congreso Jurídico Municipal “Dr. Mauro Murillo Arias”. https://munimsj.wordpress.com/2016/10/21/v-congreso-juridico-municipal-dr-mauro-murillo-arias/: introducción.'
ps=P(); a,b=rango('Índice de obras y documentos citados','Heading 1')
ent=[ps[i] for i in range(a,b) if ps[i].style.name=='Compact']
prev=[e for e in ent if clave(e.text)<clave(t)][-1]; nuevo_despues(prev,t,'Compact')
d.save(fo); print('listo')
