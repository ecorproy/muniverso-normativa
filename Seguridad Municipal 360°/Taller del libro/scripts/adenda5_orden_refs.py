import sys
from docx import Document
f=sys.argv[1]; d=Document(f); P=d.paragraphs
iq=next(i for i,p in enumerate(P) if p.text.startswith('Queda el orden de las palabras'))
def find(s): return next(p for i,p in enumerate(P) if i>iq and p.text.startswith(s))
l5525=find('Ley N.° 5525,'); l8131=find('Ley N.° 8131,')
find('Ley N.° 6227,')._p.addprevious(l5525._p)
find('Ley N.° 8422,')._p.addprevious(l8131._p)
d.save(f)
P=d.paragraphs
i=next(i for i,p in enumerate(P) if i>iq and p.text.startswith('Ley N.° 2,'))
for k in range(i,i+10): print(P[k].text[:40])
