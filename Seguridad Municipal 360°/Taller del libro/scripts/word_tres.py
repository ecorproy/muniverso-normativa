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

RPEN="Programa Estado de la Nación. (2026). Armonía con la naturaleza. En *Informe Estado de la Nación 2026* (cap. 4, pp. 185-278). Programa Estado de la Nación."
ROV="Observatorio de la Violencia. (2026). *Índice Cantonal de Seguridad Ciudadana 2025: resumen metodológico y resultados*."
RMI="Ministerio de Planificación Nacional y Política Económica. (2025). *Índice cantonal de desarrollo sostenible – Agenda 2030: 2020-2022*. https://biblioteca.mideplan.go.cr"
def inserta(c,titulo,nivel,ancla,inicios,refs):
    f=L+c+'/chk_X/'+c+'.md'; a,b=rango(titulo,nivel); q=par(ancla,a,b)
    for ini in inicios: q=nuevo_despues(q,busca(f,ini))
    for r in refs: ref(titulo,nivel,r)
inserta('t04','4. Integridad personal y de bienes','Heading 2','El índice mide, entonces,',['Otro índice mide el resultado','Ese índice no evalúa'],[ROV])
inserta('t06','6. Emergencias y desastres','Heading 2','Fuera del índice hay dos verificaciones.',['Tampoco el índice cantonal'],[RMI,RPEN])
inserta('t26','26. Violencia doméstica','Heading 2','El índice de gestión de la Contraloría no mide',['El dato existe en otra medición.'],[ROV])
inserta('t28','28. Agua y saneamiento','Heading 2','El acueducto municipal tiene, además,',['Otra medida llega desde la regulación.'],[RPEN])
inserta('t29','29. Residuos y limpieza','Heading 2','La tabla de datos que acompaña el índice de 2025 baja',['Una medición independiente mira','El hallazgo más severo es otro.'],[RPEN])
inserta('t30','30. Ambiente y arbolado','Heading 2','A las dos municipalidades les ordenó',['El Informe Estado de la Nación de 2026 destacó'],[RPEN])
inserta('t30','30. Ambiente y arbolado','Heading 2','Donde hay un área protegida creada por el Poder Ejecutivo,',['La Zona Protectora Cerros de Escazú muestra','El estudio da también la geografía'],[])
f=L+'conclusion/chk_X/conclusion.md'; a,b=rango('Conclusión. Volver al núcleo','Heading 1')
reemplaza(par('Tampoco dice que todas',a,b),busca(f,'Tampoco dice que todas'))
ref('Conclusión. Volver al núcleo','Heading 1',RMI)
a,b=rango('Índice de obras y documentos citados','Heading 1'); ps=P()
ent=[ps[i] for i in range(a,b) if ps[i].style.name=='Compact']
for t in ['Ministerio de Planificación Nacional y Política Económica. (2025). Índice cantonal de desarrollo sostenible – Agenda 2030: 2020-2022. https://biblioteca.mideplan.go.cr: temas 6; conclusión.',
          'Observatorio de la Violencia. (2026). Índice Cantonal de Seguridad Ciudadana 2025: resumen metodológico y resultados: temas 4, 26.',
          'Programa Estado de la Nación. (2026). Armonía con la naturaleza. En Informe Estado de la Nación 2026 (cap. 4, pp. 185-278). Programa Estado de la Nación: temas 6, 28, 29, 30.']:
    ps=P(); a,b=rango('Índice de obras y documentos citados','Heading 1')
    ent=[ps[i] for i in range(a,b) if ps[i].style.name=='Compact']
    prev=[e for e in ent if clave(e.text)<clave(t)][-1]; nuevo_despues(prev,t,'Compact')
d.save(fo); print('listo')
