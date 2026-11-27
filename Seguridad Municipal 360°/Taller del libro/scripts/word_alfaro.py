"""Word final57 -> final58: pasajes de Alfaro Redondo (2009/2025) y actualización de índices."""
import re,sys,copy
from docx import Document
fi,fo=sys.argv[1:3]
d=Document(fi); ps=lambda: d.paragraphs
L='/home/claude/libro/'
def parrafos(f): return [b.strip() for b in open(f,encoding='utf-8').read().split('\n\n') if b.strip()]
def busca(f,inicio):
    r=[b for b in parrafos(f) if b.startswith(inicio)]; assert len(r)==1,(f,inicio,len(r)); return r[0]
def runs(p,t):
    for k,part in enumerate(re.split(r'\*([^*]+)\*',t)):
        if part: r=p.add_run(part); r.italic=True if k%2 else None
def rango(titulo,nivel='Heading 1'):
    P=ps(); h=[i for i,p in enumerate(P) if p.style.name==nivel and p.text.strip()==titulo]; assert len(h)==1,titulo
    e=next((i for i in range(h[0]+1,len(P)) if P[i].style.name in ('Heading 1',) or (nivel=='Heading 2' and P[i].style.name=='Heading 2' and P[i].paragraph_format.page_break_before)),len(P))
    return h[0],e
def par_en(ini,a,b):
    P=ps(); k=[i for i in range(a,b) if P[i].text.startswith(ini)]; assert len(k)==1,(ini,len(k)); return P[k[0]]
def inserta_despues(p,texto,estilo='Body Text'):
    new=copy.deepcopy(p._p)
    for ch in list(new):
        if ch.tag.endswith('}r') or ch.tag.endswith('}hyperlink'): new.remove(ch)
    p._p.addnext(new)
    from docx.text.paragraph import Paragraph
    q=Paragraph(new,p._parent); q.style=d.styles[estilo]; runs(q,texto); return q
def reemplaza(p,texto):
    for r in list(p.runs): r._r.getparent().remove(r._r)
    runs(p,texto)
REF_A="Alfaro Redondo, R. (2025). *El régimen municipal costarricense a inicios del siglo XXI* (Cuadernos para la Ciudadanía 8). Editorial Universidad de Costa Rica. (Trabajo original publicado en 2009)"
def ref_primera(a,b):
    P=ps(); h=[i for i in range(a,b) if P[i].text=='Referencias' and P[i].style.name.startswith('Heading')]; assert len(h)==1
    first=P[h[0]+1]; assert first.text>'Alfaro'
    q=inserta_despues(P[h[0]],REF_A,'First Paragraph'); first.style=d.styles['Body Text']
# capítulo 2
f=L+'cap02/chk_alf/all.md'
a,b=rango('2. Lo local en el artículo 169')
inserta_despues(par_en('Antes de ellas hubo un siglo',a,b),busca(f,'Ronald Alfaro Redondo pone'))
a,b=rango('2. Lo local en el artículo 169')
inserta_despues(par_en('Después de 1949 el legislador',a,b),busca(f,'Lo hizo a contracorriente'))
a,b=rango('2. Lo local en el artículo 169'); ref_primera(a,b)
# tema 15
f=L+'t15/chk_alf/t15.md'
a,b=rango('15. Participación','Heading 2')
inserta_despues(par_en('La consulta popular la organiza',a,b),busca(f,'Los plebiscitos revocatorios han sido'))
a,b=rango('15. Participación','Heading 2')
inserta_despues(par_en('Lo que la ley exige se puede contar',a,b),busca(f,'Las mediciones hechas fuera'))
a,b=rango('15. Participación','Heading 2'); ref_primera(a,b)
# conclusión
f=L+'conclusion/chk_alf/conclusion.md'
a,b=rango('Conclusión. Volver al núcleo')
reemplaza(par_en('La sexta es que',a,b),busca(f,'La sexta es que'))
reemplaza(par_en('Tampoco dice que todas',a,b),busca(f,'Tampoco dice que todas'))
ref_primera(a,b)
# índices
a,b=rango('Índice de obras y documentos citados')
P=ps()
for i in range(a,b):
    t=P[i].text
    if t.startswith('Cortés García, E. (2026)'): reemplaza(P[i],t.replace(': capítulos 2, 4.',': introducción; capítulos 2, 4.'))
    if t.startswith('Leiva Poveda, J. (2016)'): reemplaza(P[i],re.sub(r': (capítul)',r': introducción; \1',t,count=1))
P=ps(); conan=[i for i in range(a,b) if P[i].text.startswith('Conan Doyle')][0]
P[conan-1]  # párrafo descriptivo
q=inserta_despues(P[conan-1],'Alfaro Redondo, R. (2025). El régimen municipal costarricense a inicios del siglo XXI (Cuadernos para la Ciudadanía 8). Editorial Universidad de Costa Rica. (Trabajo original publicado en 2009): capítulo 2; tema 15; conclusión.','Compact')
a,b=rango('Índice de obras y documentos citados'); P=ps()
lei=[i for i in range(a,b) if P[i].text.startswith('Leiva Poveda')][0]
inserta_despues(P[lei],'Lora-Tamayo Vallvé, M. (Dir.). (2020). Manual de derecho local (4.ª ed.). Iustel: introducción.','Compact')
a,b=rango('Índice de legislación'); P=ps()
cm=[i for i in range(a,b) if P[i].text.startswith('Ley N.° 7794, Código Municipal (1998)')][0]
reemplaza(P[cm],P[cm].text.replace(': capítulos 1, 2, 3, 4;',': introducción; capítulos 1, 2, 3, 4;'))
d.save(fo); print('listo')
