import copy,re
from docx import Document
from docx.text.paragraph import Paragraph
from docx.text.run import Run
f='/home/claude/Seguridad Municipal 360 (final54).docx'; d=Document(f)
L='/home/claude/libro/'
REF=[x for x in open(L+'t04/chk5/zz_referencias.md',encoding='utf-8').read().split('\n\n') if 'Tabla de datos del Índice' in x][0]
def chap(ini):
    ps=d.paragraphs; hs=[k for k,p in enumerate(ps) if p.style.name in ('Heading 1','Heading 2') and p.text.startswith(ini)]; assert len(hs)==1,(ini,len(hs)); h=hs[0]
    e=next((k for k in range(h+1,len(ps)) if ps[k].style.name in ('Heading 1','Heading 2')),len(ps)); return ps,h,e
def ref_par(model,md):
    q=copy.deepcopy(model._p); np=Paragraph(q,model._parent); runs=np.runs; r0=runs[0]
    for r in runs[1:]: r._r.getparent().remove(r._r)
    first=True
    for s in re.split(r'(\*[^*]+\*)',md):
        if not s: continue
        it=s.startswith('*'); s=s.strip('*')
        if first: r0.text=s; r0.italic=True if it else None; first=False
        else:
            nr=copy.deepcopy(r0._r); r0._r.getparent().append(nr); rr=Run(nr,np); rr.text=s; rr.italic=True if it else None
    return q
def tema(ini,cap,anchor,start):
    nuevo=[x for x in open(L+f'{cap}/chk5/{cap}.md',encoding='utf-8').read().split('\n\n') if x.startswith(start)][0]
    ps,h,e=chap(ini)
    k=[i for i in range(h,e) if ps[i].text.startswith(anchor)]; assert len(k)==1 and len(ps[k[0]].runs)==1,(ini,anchor,len(k))
    q=copy.deepcopy(ps[k[0]]._p); ps[k[0]]._p.addnext(q); Paragraph(q,ps[k[0]]._parent).runs[0].text=nuevo
    ps,h,e=chap(ini)
    k=[i for i in range(h,e) if ps[i].text.startswith(('Contraloría General de la República. (2025). [Fichas','Contraloría General de la República. (2025). Fichas'))]; assert len(k)==1,(ini,'fichas')
    model=next(ps[i] for i in range(k[0],e) if any(r.italic for r in ps[i].runs))
    ps[k[0]]._p.addnext(ref_par(model,REF))
tema('4. Integridad personal','t04','La seguridad y la vigilancia en la comunidad es uno de los diez','La tabla de datos que acompaña')
tema('10. Igualdad','t10','La comparación entre la definición y las variables','Las respuestas de 2025')
tema('29. Residuos','t29','La Contraloría evalúa la gestión de este servicio','La tabla de datos que acompaña')
# conclusión
c=open(L+'conclusion/chk5/conclusion.md',encoding='utf-8').read().split('\n\n')
nuevo=[x for x in c if x.startswith('La sexta es que lo que hoy se mide')][0]
ps,h,e=chap('Conclusión')
k=[i for i in range(h,e) if ps[i].text.startswith('La sexta es que lo que hoy se mide')]; assert len(k)==1 and len(ps[k[0]].runs)==1
ps[k[0]].runs[0].text=nuevo
k=[i for i in range(h,e) if ps[i].text.startswith('Constitución Política de la República de Costa Rica. (1949)')]; assert len(k)==1
model=next(ps[i] for i in range(h,e) if ps[i].text.startswith('Contraloría General de la República. (2026a)'))
ps[k[0]]._p.addnext(ref_par(model,REF))
d.save(f); print('ok')
