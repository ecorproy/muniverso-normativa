"""Lee los índices especializados del DOCX: devuelve [(indice, categoria, elem_idx, nombre, unidades)]."""
import re
from docx.oxml.ns import qn
def T(e): return ''.join(t.text or '' for t in e.iter(qn('w:t')))
def S(e):
    s=e.find(qn('w:pPr')+'/'+qn('w:pStyle')) if e.tag==qn('w:p') else None
    return s.get(qn('w:val')) if s is not None else ''
UNI=re.compile(r':((?: (?:introducción|capítulos? [\d, ]+|temas? [\d, ]+|conclusión|anexos?);?)+)\.$')
def unidades(s):
    out=[]
    for parte in s.split(';'):
        parte=parte.strip()
        m=re.match(r'(capítulos?|temas?) (.*)',parte)
        if m:
            base='capítulo' if m.group(1).startswith('cap') else 'tema'
            out+= [f'{base} {int(n)}' for n in re.findall(r'\d+',m.group(2))]
        elif parte: out.append({'anexo':'anexos'}.get(parte,parte))
    return out
def lee(els):
    res=[]; ind=cat=None
    for i,e in enumerate(els):
        st=S(e); t=T(e)
        if st=='Heading1': ind=t if t.startswith('Índice de') and t!='Índice de figuras' else None; cat=None; continue
        if ind is None: continue
        if st=='Heading3': cat=t; continue
        if st=='Compact':
            m=UNI.search(t)
            if not m: res.append((ind,cat,i,t,None)); continue
            res.append((ind,cat,i,t[:m.start()],unidades(m.group(1))))
    return res
