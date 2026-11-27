import sys
from docx import Document
from PIL import Image
f=sys.argv[1]; pares=sys.argv[2:]
d=Document(f); P=d.paragraphs
for k in range(0,len(pares),2):
    cap,png=pares[k],pares[k+1]
    i=next(i for i,p in enumerate(P) if p.style.name=='Image Caption' and p.text.startswith(cap))
    pimg=P[i-1]; rid=pimg._p.xpath('.//a:blip/@r:embed'); assert len(rid)==1
    d.part.related_parts[rid[0]]._blob=open(png,'rb').read()
    w,h=Image.open(png).size
    for ext in pimg._p.xpath('.//wp:extent')+pimg._p.xpath('.//a:ext'):
        ext.set('cy',str(int(int(ext.get('cx'))*h/w)))
d.save(f); print('ok')
