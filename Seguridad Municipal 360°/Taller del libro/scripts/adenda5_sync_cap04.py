import sys,re
from docx import Document
f_in,f_out,comp=sys.argv[1],sys.argv[2],sys.argv[3]
C=[re.sub(r'\s+',' ',x).strip() for x in open(comp,encoding='utf-8').read().split('\n\n')]
d=Document(f_in); P=d.paragraphs
for ini in ['De ese mismo deber sale el índice de este libro','La frontera la trazó la Sala Constitucional','En una municipalidad estas reglas tienen un límite']:
    c=[x for x in C if x.startswith(ini)]; assert len(c)==1,ini; c=c[0]
    assert '*' not in c and '[[' not in c, ini
    w=[p for p in P if p.text.startswith(ini)]; assert len(w)==1,ini; w=w[0]
    assert len(w.runs)==1, (ini,len(w.runs))
    w.runs[0].text=c
d.save(f_out); print('ok')
