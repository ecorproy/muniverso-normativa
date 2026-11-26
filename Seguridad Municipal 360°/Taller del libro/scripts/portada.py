# Uso: python3 -I portada.py entrada.docx salida.docx logo.png
import sys, docx
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
d=docx.Document(sys.argv[1]); first=d.element.body[0]
p=d.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Cm(3)
p.add_run().add_picture(sys.argv[3], width=Cm(14))
q=d.add_paragraph(); q.add_run().add_break(WD_BREAK.PAGE)
first.addprevious(p._p); first.addprevious(q._p)
d.save(sys.argv[2])
