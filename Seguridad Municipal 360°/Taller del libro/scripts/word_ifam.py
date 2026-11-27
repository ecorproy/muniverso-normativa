"""Word final59 -> final60: Índice Municipal del IFAM (2024 y 2025) en temas 17, 32, 36 y conclusión."""
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
R24="Instituto de Fomento y Asesoría Municipal. (2024). *Índice Municipal de Costa Rica 2024*. https://drive.google.com/file/d/1StgLMG4K8U3vHaziSk1rOayGPFBxw6sn/view"
R25="Instituto de Fomento y Asesoría Municipal. (2025). *Índice Municipal de Costa Rica 2025*. https://drive.google.com/file/d/1JdJsvWDa0uZMg7WBLKVCjm5hgxM1zmIh/view"
# tema 17
f=L+'t17/chk_ifam/t17.md'; a,b=rango('17. Acceso digital','Heading 2')
nuevo_despues(par('La medición premia que la persona',a,b),busca(f,'Hay otra medición cuyo nombre'))
ref('17. Acceso digital','Heading 2',R24)
# tema 32
f=L+'t32/chk_ifam/t32.md'; a,b=rango('32. Vivienda','Heading 2')
q=nuevo_despues(par('Las fichas del índice muestran qué se pregunta del urbanismo',a,b),busca(f,'El estado de los planes puede verse'))
imagen(q,RP+'t32_grafico.png','Tema 32: estado del plan regulador según las fichas cantonales del IFAM 2025')
ref('32. Vivienda','Heading 2',R24); ref('32. Vivienda','Heading 2',R25)
# tema 36
f=L+'t36/chk_ifam/t36.md'; a,b=rango('36. Economía local y reparto de la riqueza','Heading 2')
p=par('Ninguna de las dos mediciones mira el reparto',a,b)
prev=P()[[i for i,x in enumerate(P()) if x._p is p._p][0]-1]
nuevo_despues(prev,busca(f,'Un compendio permite, en cambio'))
reemplaza(p,busca(f,'Ninguna de las dos mediciones mira el reparto dentro'))
ref('36. Economía local y reparto de la riqueza','Heading 2',R25)
# conclusión
f=L+'conclusion/chk_ifam/conclusion.md'; a,b=rango('Conclusión. Volver al núcleo','Heading 1')
p=par('Tampoco dice que todas',a,b); reemplaza(p,busca(f,'Tampoco dice que todas'))
imagen(p,RP+'conclusion_grafico.png','Conclusión: presupuesto municipal 2024 por habitante en los 84 cantones, según el IFAM',ancho=12)
ref('Conclusión. Volver al núcleo','Heading 1',R25)
# índice de obras
a,b=rango('Índice de obras y documentos citados','Heading 1'); ps=P()
kant=[i for i in range(a,b) if ps[i].text.startswith('Kant, I.')][0]
q=nuevo_despues(ps[kant-1],'Instituto de Fomento y Asesoría Municipal. (2024). Índice Municipal de Costa Rica 2024. https://drive.google.com/file/d/1StgLMG4K8U3vHaziSk1rOayGPFBxw6sn/view: temas 17, 32.','Compact')
nuevo_despues(q,'Instituto de Fomento y Asesoría Municipal. (2025). Índice Municipal de Costa Rica 2025. https://drive.google.com/file/d/1JdJsvWDa0uZMg7WBLKVCjm5hgxM1zmIh/view: temas 32, 36; conclusión.','Compact')
d.save(fo); print('listo')
