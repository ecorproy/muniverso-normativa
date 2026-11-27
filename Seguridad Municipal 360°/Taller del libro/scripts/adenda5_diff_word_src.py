import sys,re
from docx import Document
doc,comp,ini_t,fin_t=sys.argv[1:5]
C=[re.sub(r'\s+',' ',x).strip() for x in open(comp,encoding='utf-8').read().split('\n\n')]
C=[re.sub(r'^> ','',x) for x in C if x and not x.startswith('#')]
P=[p.text.strip() for p in Document(doc).paragraphs]
i=next(k for k,p in enumerate(P) if p.startswith(ini_t))
j=next(k for k in range(i+1,len(P)) if P[k]==fin_t)
W=[p for p in P[i:j] if p and not p.startswith('Figura ')]
cs=set(C)
malos=[w for w in W if w not in cs and len(w)>60]
print('párrafos Word',len(W),'distintos (largos)',len(malos))
for w in malos: print('  ·',w[:110])
