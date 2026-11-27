"""Inserta la introducción (src/intro.md) antes del capítulo 1."""
import copy,sys,re
from docx import Document
from docx.shared import Cm
src,f_in,f_out=sys.argv[1:4]
d=Document(f_in); R='/home/claude/recursos/png/'
P=d.paragraphs
modelo=P[[i for i,p in enumerate(P) if p.style.name=='Image Caption' and p.text.startswith('Figura 1.')][0]-1]
ancla=[p for p in P if p.style.name=='Heading 1' and p.text=='1. La red'][0]
ALT={'intro_mapa':'Introducción: mapa del viaje, seis estaciones de la red a la persona',
     'intro_rutas':'Introducción: cinco rutas de lectura según quien lee'}
def runs(p,t):
    for k,part in enumerate(re.split(r'\*([^*]+)\*',t)):
        if part: r=p.add_run(part); r.italic = True if k%2 else None
def par(style,t):
    p=ancla.insert_paragraph_before(); p.style=d.styles[style]; runs(p,t); return p
def imagen(nombre):
    d.add_picture(R+nombre+'.png',width=Cm(16))
    np_=d.paragraphs[-1]._p; np_.getparent().remove(np_)
    ppr=modelo._p.pPr
    if np_.pPr is not None: np_.remove(np_.pPr)
    if ppr is not None: np_.insert(0,copy.deepcopy(ppr))
    for dp in np_.xpath('.//wp:docPr'): dp.set('descr',ALT[nombre]); dp.set('title',ALT[nombre])
    ancla._p.addprevious(np_)
prev=None; n=0
for bl in [b.strip() for b in open(src,encoding='utf-8').read().split('\n\n') if b.strip()]:
    if bl.startswith('# '): par('Heading 1',bl[2:]); prev='h'
    elif bl.startswith('## '): par('Heading 2',bl[3:]); prev='h'
    elif bl.startswith('> '): par('Block Text',bl[2:]); prev='q'
    elif bl.startswith('[[RECURSO:'): imagen(bl[10:-2]); n+=1; prev='i'
    else: par('First Paragraph' if prev=='h' else 'Body Text',bl); prev='p'
d.save(f_out); print('recursos',n)
