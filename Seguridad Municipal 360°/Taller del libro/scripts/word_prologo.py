"""Inserta la página del prólogo (Título 1 «Prólogo», página vacía) antes de la introducción."""
import sys,copy
from docx import Document
fi,fo=sys.argv[1:3]
d=Document(fi)
intro=[p for p in d.paragraphs if p.style.name=='Heading 1' and p.text.startswith('Introducción')]
assert len(intro)==1
assert not any(p.style.name=='Heading 1' and p.text=='Prólogo' for p in d.paragraphs)
h=intro[0].insert_paragraph_before('Prólogo'); h.style=d.styles['Heading 1']
for _ in range(2):
    b=intro[0].insert_paragraph_before(''); b.style=d.styles['Body Text']
d.save(fo); print('ok')
