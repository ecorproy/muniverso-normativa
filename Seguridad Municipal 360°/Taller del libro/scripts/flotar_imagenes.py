"""Imágenes flotantes al comienzo de la página donde caen, con ajuste «arriba y abajo»:
el texto llena el resto de la página y no quedan huecos. Las figuras con leyenda van
en una tabla flotante de una celda, para que la leyenda no se separe de su imagen."""
import sys, copy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
fi, fo = sys.argv[1:3]
d = Document(fi)
WPNS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ANCHO = 9406  # 16,59 cm en twips

def anchoriza(inline, rh):
    a = parse_xml(f'<wp:anchor xmlns:wp="{WPNS}" distT="0" distB="114300" distL="0" distR="0" simplePos="0" relativeHeight="{rh}" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="0"><wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="margin"><wp:align>center</wp:align></wp:positionH><wp:positionV relativeFrom="margin"><wp:align>top</wp:align></wp:positionV></wp:anchor>')
    ext = inline.find(qn('wp:extent')); eff = inline.find(qn('wp:effectExtent'))
    a.append(copy.deepcopy(ext))
    a.append(copy.deepcopy(eff) if eff is not None else parse_xml(f'<wp:effectExtent xmlns:wp="{WPNS}" l="0" t="0" r="0" b="0"/>'))
    a.append(parse_xml(f'<wp:wrapTopAndBottom xmlns:wp="{WPNS}"/>'))
    for tag in ['wp:docPr', 'wp:cNvGraphicFramePr']:
        e = inline.find(qn(tag))
        if e is not None: a.append(copy.deepcopy(e))
    a.append(copy.deepcopy(inline.find(qn('a:graphic'))))
    inline.getparent().replace(inline, a)

def tabla_flotante(paras):
    t = parse_xml(f'<w:tbl xmlns:w="{W}"><w:tblPr><w:tblpPr w:leftFromText="0" w:rightFromText="0" w:topFromText="0" w:bottomFromText="227" w:vertAnchor="margin" w:horzAnchor="margin" w:tblpXSpec="center" w:tblpYSpec="top"/><w:tblOverlap w:val="never"/><w:tblW w:w="{ANCHO}" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar><w:tblLook w:val="0000"/></w:tblPr><w:tblGrid><w:gridCol w:w="{ANCHO}"/></w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w="{ANCHO}" w:type="dxa"/></w:tcPr></w:tc></w:tr></w:tbl>')
    paras[0].addprevious(t)
    tc = t.find('.//' + qn('w:tc'))
    for p in paras:
        tc.append(p)
    return t

ps = d.paragraphs
rh = 251660000
flot = tabla = 0
cuerpo = d.element.body
for i, p in enumerate(ps):
    if p.style.name != 'Captioned Figure' or p._p.getparent() is not cuerpo: continue
    inl = p._p.findall('.//' + qn('wp:inline'))
    if not inl: continue
    prev = ps[i-1].style.name if i > 0 else ''
    if prev in ('Heading 1', 'Heading 2', 'Title'):   # imagen de apertura: se queda en línea
        continue
    nxt = ps[i+1] if i + 1 < len(ps) else None
    if nxt is not None and nxt.style.name == 'Image Caption':
        tabla_flotante([p._p, nxt._p]); tabla += 1
    else:
        for x in inl:
            rh += 2; anchoriza(x, rh)
        # el párrafo que sostiene el ancla no ocupa alto
        pPr = p._p.get_or_add_pPr()
        sp = pPr.find(qn('w:spacing'))
        if sp is None: sp = OxmlElement('w:spacing'); pPr.append(sp)
        sp.set(qn('w:before'), '0'); sp.set(qn('w:after'), '0'); sp.set(qn('w:line'), '20'); sp.set(qn('w:lineRule'), 'exact')
        flot += 1
d.styles['Captioned Figure'].paragraph_format.keep_with_next = False
d.save(fo)
print('flotantes', flot, 'tablas', tabla)
