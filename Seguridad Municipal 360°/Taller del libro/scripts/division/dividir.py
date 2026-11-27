"""Divide Seguridad Municipal 360° (final76) en dos tomos, sobre copias del DOCX original."""
import sys,re,copy,shutil
sys.path.insert(0,'/home/claude/division')
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from indices import lee
ORIG='/home/claude/Seguridad Municipal 360 (final76).docx'
QR='/home/claude/division/qr_leoncortescr.png'
OUTS={'I':'/home/claude/division/Seguridad Municipal 360° — Tomo I — Fundamentos, vida y dignidad.docx',
      'II':'/home/claude/division/Seguridad Municipal 360° — Tomo II — Protección especial, bienestar y entorno.docx'}
SUB={'I':'Tomo I. Fundamentos, vida y dignidad','II':'Tomo II. Protección especial, bienestar y entorno'}
def T(e): return ''.join(t.text or '' for t in e.iter(qn('w:t')))
def S(e):
    s=e.find(qn('w:pPr')+'/'+qn('w:pStyle')) if e.tag==qn('w:p') else None
    return s.get(qn('w:val')) if s is not None else ''
def tomo_de(u):
    if u in ('introducción',) or u.startswith('capítulo'): return 'I'
    if u.startswith('tema'): return 'I' if int(u.split()[1])<=18 else 'II'
    return 'II'
ORD=lambda et: (0,0) if et=='introducción' else (1,int(et.split()[1])) if et.startswith('cap') else (2,int(et.split()[1])) if et.startswith('tema') else (3,0) if et=='conclusión' else (4,0)
def compacta(us):
    us=sorted(set(us),key=ORD); caps=[u.split()[1] for u in us if u.startswith('cap')]; tem=[u.split()[1] for u in us if u.startswith('tema')]
    out=[]
    if 'introducción' in us: out.append('introducción')
    if caps: out.append(('capítulo ' if len(caps)==1 else 'capítulos ')+', '.join(caps))
    if tem: out.append(('tema ' if len(tem)==1 else 'temas ')+', '.join(tem))
    if 'conclusión' in us: out.append('conclusión')
    if 'anexos' in us: out.append('anexos')
    return '; '.join(out)

def construir(t):
    d=Document(ORIG); body=d.element.body
    from corrige_indices import corrige
    global LOG; LOG=corrige(body,{})
    els=list(body); sect=els[-1]
    idx=lee(els); ent={i:(nombre,uni) for ind,cat,i,nombre,uni in idx}
    # ---------- piezas del original
    portada=els[0:4]; toc=els[4]
    contenido=els[5:3231] if t=='I' else els[3231:6008]
    indices=els[6008:-1]
    # ---------- helpers para párrafos nuevos (se crean al final del cuerpo y luego se mueven)
    def par(texto='',estilo=None,centrado=False,salto=False,cursiva=False):
        p=d.add_paragraph(style=estilo)
        if salto: p.paragraph_format.page_break_before=True
        if centrado: p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        if texto:
            r=p.add_run(texto); r.italic=cursiva or None
        return p._p
    nuevos=[]
    # ---------- portada (logo) con identificación del tomo
    logo,brk,titulo,autor=portada
    tomo_port=par(SUB[t],'Subtitle',True)
    # ---------- portadilla: título, autor, tomo, QR
    tomo_port2=par(SUB[t],'Subtitle',True)
    pq=d.add_paragraph(); pq.alignment=WD_ALIGN_PARAGRAPH.CENTER; pq.paragraph_format.space_before=Cm(6)
    pq.add_run().add_picture(QR,width=Cm(3.2)); pq=pq._p
    pu=par('leoncortescr.com',None,True)
    # ---------- índice general sintético de la obra
    gen=[par('Índice general de la obra','TOCHeading',salto=True)]
    def linea(txt,negrita=False,sang=0):
        p=d.add_paragraph(style='Compact'); r=p.add_run(txt); r.bold=negrita or None
        if sang: p.paragraph_format.left_indent=Cm(sang)
        gen.append(p._p)
    temas={}
    for e in els:
        m=re.match(r'(\d+)\. (.+)',T(e))
        if S(e)=='Heading2' and m: temas[int(m.group(1))]=m.group(2)
    linea('Tomo I. Fundamentos, vida y dignidad',True)
    linea('Prólogo',sang=0.6); linea('Introducción. El camino',sang=0.6)
    for c in ['1. La red','2. Lo local en el artículo 169','3. El concepto','4. La persona en el centro']: linea('Capítulo '+c,sang=0.6)
    for cuad,a,b in [('Cuadrante I. Vida',1,9),('Cuadrante II. Dignidad',10,18)]:
        linea(cuad+': '+'; '.join(f'{n}. {temas[n]}' for n in range(a,b+1))+'.',sang=0.6)
    linea('Índices de legislación, de jurisprudencia y criterios administrativos, de obras y documentos citados y de figuras del Tomo I',sang=0.6)
    linea('Tomo II. Protección especial, bienestar y entorno',True)
    for cuad,a,b in [('Cuadrante III. Protección especial',19,27),('Cuadrante IV. Bienestar y entorno',28,36)]:
        linea(cuad+': '+'; '.join(f'{n}. {temas[n]}' for n in range(a,b+1))+'.',sang=0.6)
    linea('Conclusión. Volver al núcleo',sang=0.6)
    linea('Anexo A. Lo exigible, lo que hoy se mide y la brecha',sang=0.6)
    linea('Anexo B. Cómo aplicar el modelo en una municipalidad',sang=0.6)
    linea('Índices de legislación, de jurisprudencia y criterios administrativos, de obras y documentos citados y de figuras del Tomo II',sang=0.6)
    # ---------- índice detallado del tomo (campo TOC de Word)
    toc=copy.deepcopy(toc)
    for tt in toc.iter(qn('w:t')):
        if tt.text=='Índice': tt.text='Índice del Tomo '+t
    tp=toc.find('.//'+qn('w:p')); pp=tp.find(qn('w:pPr'))
    pb=pp.makeelement(qn('w:pageBreakBefore'),{}); pp.insert(1,pb)
    # ---------- notas de continuidad
    if t=='I':
        nota=[par('Nota de continuidad','TOCHeading',salto=True),
              par('Este tomo termina con el tema 18. La obra sigue en el Tomo II, que contiene el Cuadrante III, Protección especial (temas 19 a 27), el Cuadrante IV, Bienestar y entorno (temas 28 a 36), la conclusión, Volver al núcleo, y los anexos A y B. La numeración de los temas y de las figuras continúa de un tomo a otro, de modo que las remisiones a los temas 19 a 36, a la conclusión, a los anexos y a la figura 16 se encuentran en el Tomo II.','BodyText')]
    else:
        nota=[par('Nota de continuidad','TOCHeading',salto=True),
              par('Este tomo continúa el Tomo I, que contiene la introducción, los capítulos 1 a 4, el Cuadrante I, Vida (temas 1 a 9), y el Cuadrante II, Dignidad (temas 10 a 18). Los capítulos 1 a 4 exponen los fundamentos que los temas de este tomo aplican. La numeración de los temas y de las figuras continúa de un tomo a otro, de modo que las remisiones a la introducción, a los capítulos 1 a 4, a los temas 1 a 18 y a las figuras 1 a 15 se encuentran en el Tomo I.','BodyText')]
    otro='II' if t=='I' else 'I'
    # ---------- índices especializados por tomo
    nuevos_ind=[]; cat_buf=[]; intro_ind={'Índice de legislación':'Cada norma remite a los capítulos y temas de este tomo en cuyas referencias aparece; cuando también aparece en el otro tomo, la entrada lo indica.',
        'Índice de jurisprudencia y criterios administrativos':'Cada resolución, dictamen u oficio remite a los capítulos y temas de este tomo en cuyas referencias aparece; cuando también aparece en el otro tomo, la entrada lo indica.',
        'Índice de obras y documentos citados':'Doctrina, informes y documentos institucionales que no son normas ni resoluciones. Cada entrada remite a las unidades de este tomo; cuando la obra también se cita en el otro tomo, la entrada lo indica.'}
    i0=6008; pend_cat=None; actual=None; conserva=[]
    figs_tomo=[]
    for k,e in enumerate(indices):
        i=i0+k; st=S(e); tx=T(e)
        if e.tag in (qn('w:bookmarkStart'),qn('w:bookmarkEnd')): conserva.append(e); continue
        if st=='Heading1':
            actual=tx; pend_cat=None
            conserva.append(e); continue
        if actual in intro_ind and st=='FirstParagraph':
            for r in e.findall(qn('w:r'))[1:]: e.remove(r)
            e.find(qn('w:r')).find(qn('w:t')).text=intro_ind[actual]; conserva.append(e); continue
        if st=='Heading3': pend_cat=e; continue
        if actual=='Índice de figuras':
            n=int(re.match(r'Figura (\d+)',tx).group(1)); tf='II' if n==16 else 'I'
            if tf==t: conserva.append(e)
            continue
        if i in ent:
            nombre,uni=ent[i]
            aqui=[u for u in uni if tomo_de(u)==t]; alla=[u for u in uni if tomo_de(u)!=t]
            if not aqui: continue
            suf=':'+''.join(tx[len(nombre):].split(':',1)[1:]) if False else tx[len(nombre):]
            # recorta el sufijo original («: unidades.») desde el final de las corridas
            quitar=len(suf); runs=e.findall('.//'+qn('w:r'))
            for r in reversed(runs):
                if quitar<=0: break
                tt=r.find(qn('w:t'))
                if tt is None or not tt.text: continue
                if len(tt.text)<=quitar: quitar-=len(tt.text); tt.text=''
                else: tt.text=tt.text[:-quitar]; quitar=0
            nuevo=': '+compacta(aqui)+(f'. Véase también Tomo {otro}: '+compacta(alla) if alla else '')+'.'
            r=e.makeelement(qn('w:r'),{}); tt=r.makeelement(qn('w:t'),{qn('xml:space') if False else '{http://www.w3.org/XML/1998/namespace}space':'preserve'}); tt.text=nuevo; r.append(tt); e.append(r)
            if pend_cat is not None: conserva.append(pend_cat); pend_cat=None
            conserva.append(e); continue
        conserva.append(e)
    if t=='I':
        conserva.append(par('Véase también Tomo II: figura 16.','Normal'))
    else:
        conserva.append(par('Véase también Tomo I: figuras 1 a 15.','Normal'))
    # ---------- arma el cuerpo
    for e in list(body): body.remove(e)
    orden=[logo,tomo_port,brk,titulo,autor,tomo_port2,pq,pu]+gen+[toc]
    if t=='II': orden+=nota
    orden+=contenido
    if t=='I': orden+=nota
    orden+=conserva+[sect]
    for e in orden: body.append(e)
    # ---------- marcadores sin pareja
    ini={b.get(qn('w:id')):b for b in body.iter(qn('w:bookmarkStart'))}
    fin={b.get(qn('w:id')):b for b in body.iter(qn('w:bookmarkEnd'))}
    quit=0
    for k,b in list(ini.items()):
        if k not in fin: b.getparent().remove(b); quit+=1
    for k,b in list(fin.items()):
        if k not in ini: b.getparent().remove(b); quit+=1
    # ---------- relaciones de imagen e hipervínculo sin uso
    xml=body.xml if hasattr(body,'xml') else ''
    from lxml import etree
    s=etree.tostring(body).decode()
    usados=set(re.findall(r'r:(?:embed|id|link)="([^"]+)"',s))
    borr=0
    for rid,rel in list(d.part.rels.items()):
        if (rel.reltype.endswith('/image') or rel.reltype.endswith('/hyperlink')) and rid not in usados:
            del d.part.rels[rid]; borr+=1
    d.save(OUTS[t]); print('Tomo',t,'elementos',len(body),'marcadores huérfanos quitados',quit,'relaciones sin uso quitadas',borr)
for t in ('I','II'): construir(t)
print('\n'.join(LOG))
