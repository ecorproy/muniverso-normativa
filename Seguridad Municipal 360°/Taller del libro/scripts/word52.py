import copy,re
from docx import Document
from docx.text.paragraph import Paragraph
f='/home/claude/Seguridad Municipal 360 (final52).docx'; d=Document(f)
L='/home/claude/libro/'
def P(): return d.paragraphs
def chap(ini):
    ps=P(); h=next(k for k,p in enumerate(ps) if p.style.name=='Heading 1' and p.text.startswith(ini))
    e=next((k for k in range(h+1,len(ps)) if ps[k].style.name=='Heading 1'),len(ps)); return h,e
def settext(p,a,b):
    assert len(p.runs)==1 and p.text.count(a)==1; p.runs[0].text=p.runs[0].text.replace(a,b)
def ref_par(model,md):
    q=copy.deepcopy(model._p); np=Paragraph(q,model._parent)
    parts=re.split(r'(\*[^*]+\*)',md); runs=np.runs
    r0=runs[0]
    for r in runs[1:]: r._r.getparent().remove(r._r)
    r0.text=''; r0.italic=None
    first=True
    for s in parts:
        if not s: continue
        it=s.startswith('*'); s=s.strip('*')
        if first: r0.text=s; r0.italic=True if it else None; first=False
        else:
            nr=copy.deepcopy(r0._r); r0._r.getparent().append(nr)
            from docx.text.run import Run
            rr=Run(nr,np); rr.text=s; rr.italic=True if it else None
    return q
refs4=[x for x in open(L+'cap04/chk3/zz_referencias.md',encoding='utf-8').read().split('\n\n') if 'Mejora Pública' in x]
# capítulo 3
h,e=chap('3. El concepto'); ps=P()
k=[i for i in range(h,e) if 'Servicios Municipales 2025 de la Contraloría.' in ps[i].text]; assert len(k)==1
settext(ps[k[0]],'Servicios Municipales 2025 de la Contraloría.','Servicios Municipales 2025 de la Contraloría, y la medición del cumplimiento de sus disposiciones, del Índice de Cumplimiento para la Mejora Pública 2026.')
# capítulo 4: párrafo
nuevo=[x for x in open(L+'cap04/chk3/cap04.md',encoding='utf-8').read().split('\n\n') if x.startswith('La Contraloría General de la República mide')][0]
h,e=chap('4. La persona'); ps=P()
k=[i for i in range(h,e) if ps[i].text.startswith('La cadena necesita quien la arme')]; assert len(k)==1
q=copy.deepcopy(ps[k[0]]._p); ps[k[0]]._p.addnext(q); Paragraph(q,ps[k[0]]._parent).runs[0].text=nuevo
assert len(Paragraph(q,ps[k[0]]._parent).runs)==1
# capítulo 4: referencias, después de la Constitución
h,e=chap('4. La persona'); ps=P()
k=[i for i in range(h,e) if ps[i].text.startswith('Constitución Política de la República de Costa Rica. (1949)')]; assert len(k)==1
model=next(ps[i] for i in range(h,e) if ps[i].text.startswith('Ley N.° ') and any(r.italic for r in ps[i].runs))
ancla=ps[k[0]]._p
for md in refs4:
    q=ref_par(model,md); ancla.addnext(q); ancla=q
# conclusión
h,e=chap('Conclusión'); ps=P()
k=[i for i in range(h,e) if 'un reglamento, un equipo, una partida.' in ps[i].text]; assert len(k)==1
settext(ps[k[0]],'un reglamento, un equipo, una partida.','un reglamento, un equipo, una partida. El Índice de Cumplimiento para la Mejora Pública de la Contraloría mide otra cosa: con qué eficacia y en qué plazo atiende la institución las disposiciones del órgano contralor (Contraloría General de la República [CGR], Índice de Cumplimiento para la Mejora Pública (ICM) 2026, 2026a, p. 1). Cumplir una disposición puede mejorar un servicio, pero el índice registra el cumplimiento.')
h,e=chap('Conclusión'); ps=P()
k=[i for i in range(h,e) if ps[i].text.startswith('Constitución Política de la República de Costa Rica. (1949)')]; assert len(k)==1
model=next(ps[i] for i in range(h,e) if ps[i].text.startswith('Ley N.° ') and any(r.italic for r in ps[i].runs))
ps[k[0]]._p.addnext(ref_par(model,refs4[4]))
d.save(f)
# comprobación
d=Document(f)
for ini in ('4. La persona','Conclusión'):
    ps=d.paragraphs; h=next(k for k,p in enumerate(ps) if p.style.name=='Heading 1' and p.text.startswith(ini))
    for p in ps[h:]:
        if 'Mejora Pública' in p.text and p.text.startswith('Contraloría'): print(ini,'|',[(r.italic,r.text[:25]) for r in p.runs])
        if p.text.startswith('Ley N.° ') : break
