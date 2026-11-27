import sys
from docx import Document
from PIL import Image
f=sys.argv[1]; png9=sys.argv[2]; png13=sys.argv[3]
d=Document(f); P=d.paragraphs
def cap(start):
    return next(i for i,p in enumerate(P) if p.style.name=='Image Caption' and p.text.startswith(start))
def cambia(i_cap, png):
    pimg=P[i_cap-1]
    rid=pimg._p.xpath('.//a:blip/@r:embed')[0]
    part=d.part.related_parts[rid]
    part._blob=open(png,'rb').read()
    w,h=Image.open(png).size
    for ext in pimg._p.xpath('.//wp:extent')+pimg._p.xpath('.//a:ext'):
        cx=int(ext.get('cx')); ext.set('cy',str(int(cx*h/w)))
cambia(cap('Figura 9.'),png9)
i13=cap('Figura 13.')
cambia(i13,png13)
def retit(p):
    t=p.text; nuevo=t.replace('Producto interno y servicio prestado.','Del servicio prestado al producto recibido.')
    assert nuevo!=t
    for r in p.runs[1:]: r.text=''
    # conservar formato del primer run con texto
    rs=[r for r in p.runs]
    full=''.join(r.text for r in rs)
    rs[0].text=nuevo if len(rs)==1 else rs[0].text
    if len(rs)>1:
        pass
    return
# leyenda e índice: reemplazo run a run
n=0
for p in d.paragraphs:
    for r in p.runs:
        if 'Producto interno y servicio prestado' in r.text:
            r.text=r.text.replace('Producto interno y servicio prestado','Del servicio prestado al producto recibido'); n+=1
print('leyendas cambiadas',n)
d.save(f)
