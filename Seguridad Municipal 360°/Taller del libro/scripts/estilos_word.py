"""Normaliza los estilos de Word del libro (final55 -> final56)."""
import sys, copy, re
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

src, dst = sys.argv[1], sys.argv[2]
d = Document(src)
st = d.styles

def sty(sid):
    return st.element.find(f'.//{qn("w:style")}[@{qn("w:styleId")}="{sid}"]')

def setp(el, tag, attrs=None, remove=False):
    pPr = el.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); el.insert(0, pPr)
    old = pPr.find(qn(tag))
    if old is not None: pPr.remove(old)
    if not remove:
        e = OxmlElement(tag)
        for k, v in (attrs or {}).items(): e.set(qn(k), v)
        pPr.append(e)

def setr(el, tag, attrs=None, remove=False):
    rPr = el.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr'); el.append(rPr)
    old = rPr.find(qn(tag))
    if old is not None: rPr.remove(old)
    if not remove:
        e = OxmlElement(tag)
        for k, v in (attrs or {}).items(): e.set(qn(k), v)
        rPr.append(e)

# 1. Nombres integrados: Word los muestra como Título, Subtítulo, Título 1..9
for n in range(1, 10):
    s = sty(f'Heading{n}')
    s.find(qn('w:name')).set(qn('w:val'), f'heading {n}')

# 2. Título 2 sin salto de página en el estilo (el salto pasa a los temas)
setp(sty('Heading2'), 'w:pageBreakBefore', remove=True)

# 3. Títulos 4 y 5 con el mismo diseño que 1 a 3
for sid, sz, ital in (('Heading4', '24', False), ('Heading5', '22', True)):
    s = sty(sid)
    setp(s, 'w:spacing', {'w:before': '240', 'w:after': '120'})
    setr(s, 'w:b', {}); setr(s, 'w:bCs', {})
    setr(s, 'w:i', {} if ital else None, remove=not ital)
    setr(s, 'w:iCs', remove=True)
    setr(s, 'w:sz', {'w:val': sz}); setr(s, 'w:szCs', {'w:val': sz})

# 4. Subtítulo sin la negrita heredada de Título
setr(sty('Subtitle'), 'w:b', {'w:val': '0'}); setr(sty('Subtitle'), 'w:bCs', {'w:val': '0'})

# 5. Subtítulo 2
s2 = st.add_style('Subtítulo 2', WD_STYLE_TYPE.PARAGRAPH)
s2.base_style = st['Subtitle']; s2.next_paragraph_style = st['Body Text']; s2.quick_style = True
e2 = s2.element
setp(e2, 'w:jc', {'w:val': 'left'}); setp(e2, 'w:spacing', {'w:before': '0', 'w:after': '240'})
setr(e2, 'w:i', {}); setr(e2, 'w:color', {'w:val': '44505F'})
setr(e2, 'w:sz', {'w:val': '26'}); setr(e2, 'w:szCs', {'w:val': '26'})

H1, H2, H3 = st['Heading 1'], st['Heading 2'], st['Heading 3']
ps = d.paragraphs

# 6. Autor -> Subtítulo
for p in ps:
    if p.style.name == 'Author': p.style = st['Subtitle']

# 7. Temas: salto de página directo
for p in ps:
    if p.style.name == 'heading 2' or p.style == H2:
        p.paragraph_format.page_break_before = True

# 8. Secciones de capítulos y conclusión: Título 3 -> Título 2 (sin salto)
cap = False; cambios = 0
for p in ps:
    if p.style == H1:
        t = p.text.strip()
        cap = bool(re.match(r'^[1-4]\. ', t)) or t.startswith('Conclusión')
        continue
    if cap and p.style == H3:
        p.style = H2; p.paragraph_format.page_break_before = False; cambios += 1

# 9. Línea «Temas X a Y.» bajo cada cuadrante
rangos = {'Cuadrante I.': 'Temas 1 a 9.', 'Cuadrante II.': 'Temas 10 a 18.',
          'Cuadrante III.': 'Temas 19 a 27.', 'Cuadrante IV.': 'Temas 28 a 36.'}
puestas = 0
for p in ps:
    if p.style == H1:
        for k, v in rangos.items():
            if p.text.startswith(k + ' '):
                nuevo = copy.deepcopy(p._p)
                for ch in list(nuevo):
                    if ch.tag != qn('w:pPr'): nuevo.remove(ch)
                pPr = nuevo.find(qn('w:pPr'))
                for ch in list(pPr): pPr.remove(ch)
                p._p.addnext(nuevo)
                from docx.text.paragraph import Paragraph
                q = Paragraph(nuevo, p._parent); q.style = s2; q.add_run(v); puestas += 1
d.save(dst)
print('secciones subidas a Título 2:', cambios, '| líneas de cuadrante:', puestas)
