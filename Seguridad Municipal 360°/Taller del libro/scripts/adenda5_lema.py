import sys
from docx import Document
from PIL import Image
f_in,f_out,N=sys.argv[1],sys.argv[2],sys.argv[3]
d=Document(f_in); P=d.paragraphs
def run1(start):
    p=next(p for p in P if p.text.startswith(start)); assert len(p.runs)==1; return p.runs[0]
r=run1('Queda el orden de las palabras')
old='La pregunta que ordena la evaluación es qué recibió la persona.'; assert old in r.text
r.text=r.text.replace(old,'La pregunta que ordena la evaluación es qué recibió la persona y quién se lo prestó.')
r=run1('Por eso la pregunta que ordena todo el libro')
r.text=('Por eso la pregunta que ordena todo el libro cabe en una línea: qué recibió la persona y quién se lo prestó. '
        'En los servicios colectivos, como el alumbrado, el mantenimiento de las calles o la prevención de desastres, quien recibe es una comunidad, un distrito o una población, y la respuesta sigue siendo válida. '
        'Si la respuesta nombra lo que llegó, a quién llegó, persona o comunidad, y a la persona servidora que lo prestó, la red está viva en ese punto. Si no nombra nada, falta una pesa.')
r=run1('Quedan también tareas que exceden a un libro')
old='convertir la pregunta de a quién se le prestó en indicadores'; assert old in r.text
r.text=r.text.replace(old,'convertir la pregunta de qué recibió la persona y quién se lo prestó en indicadores')
def cambia(cap,png):
    i=next(i for i,p in enumerate(P) if p.style.name=='Image Caption' and p.text.startswith(cap))
    pimg=P[i-1]; rid=pimg._p.xpath('.//a:blip/@r:embed'); assert len(rid)==1
    d.part.related_parts[rid[0]]._blob=open(png,'rb').read()
    w,h=Image.open(png).size
    for ext in pimg._p.xpath('.//wp:extent')+pimg._p.xpath('.//a:ext'):
        ext.set('cy',str(int(int(ext.get('cx'))*h/w)))
for cap,png in [('Figura 5.','flujo.png'),('Figura 9.','c4_proceso.png'),('Figura 10.','c4_flujo.png'),('Figura 13.','c4_contraste.png')]:
    cambia(cap,N+png)
assert not any('se le prestó' in p.text for p in P)
d.save(f_out); print('ok')
