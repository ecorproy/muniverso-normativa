import re
from docx.oxml.ns import qn
def T(e): return ''.join(t.text or '' for t in e.iter(qn('w:t')))
def S(e):
    s=e.find(qn('w:pPr')+'/'+qn('w:pStyle')) if e.tag==qn('w:p') else None
    return s.get(qn('w:val')) if s is not None else ''
def mapa(els):
    """unidad de cada elemento del cuerpo"""
    u='preliminares'; out=[]
    for e in els:
        st,t=S(e),T(e)
        if st=='Heading1':
            if t.startswith('Prólogo'): u='prólogo'
            elif t.startswith('Introducción'): u='introducción'
            elif re.match(r'\d\. ',t): u='capítulo '+t[0]
            elif t.startswith('Cuadrante'): u=t
            elif t.startswith('Conclusión'): u='conclusión'
            elif t=='Anexos': u='anexos'
            elif t.startswith('Índice'): u=t
        elif st=='Heading2' and re.match(r'(\d+)\. ',t) and (u.startswith('Cuadrante') or u.startswith('tema')):
            u='tema '+re.match(r'(\d+)',t).group(1)
        out.append(u)
    return out
