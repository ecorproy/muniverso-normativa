"""Word final60 -> final61: Estado de la Nación 2026 (cap. 4), ICSC 2025 y ICDS de MIDEPLAN."""
import re,sys,copy,unicodedata
from docx import Document
from docx.shared import Cm
from docx.text.paragraph import Paragraph
fi,fo=sys.argv[1:3]; d=Document(fi); L='/home/claude/libro/'; RP='/home/claude/recursos/png/'
def P(): return d.paragraphs
def bloques(f): return [b.strip() for b in open(f,encoding='utf-8').read().split('\n\n') if b.strip()]
def busca(f,ini):
    r=[b for b in bloques(f) if b.startswith(ini)]; assert len(r)==1,(f,ini,len(r)); return r[0]
def runs(p,t):
    for k,part in enumerate(re.split(r'\*([^*]+)\*',t)):
        if part: r=p.add_run(part); r.italic=True if k%2 else None
def rango(titulo,nivel):
    ps=P(); h=[i for i,p in enumerate(ps) if p.style.name==nivel and p.text.strip()==titulo]; assert len(h)==1,titulo
    def fin(p): return p.style.name=='Heading 1' or (nivel=='Heading 2' and p.style.name=='Heading 2' and p.paragraph_format.page_break_before)
    e=next((i for i in range(h[0]+1,len(ps)) if fin(ps[i])),len(ps)); return h[0],e
def par(ini,a,b):
    ps=P(); k=[i for i in range(a,b) if ps[i].text.startswith(ini)]; assert len(k)==1,(ini,len(k)); return ps[k[0]]
def nuevo_despues(p,texto,estilo='Body Text'):
    n=copy.deepcopy(p._p)
    for ch in list(n):
        if not ch.tag.endswith('}pPr'): n.remove(ch)
    p._p.addnext(n); q=Paragraph(n,p._parent); q.style=d.styles[estilo]
    pf=q.paragraph_format; pf.page_break_before=None
    runs(q,texto); return q
def reemplaza(p,texto):
    for r in list(p.runs): r._r.getparent().remove(r._r)
    runs(p,texto)
modelo=None  # las leyendas van ahora dentro de tablas flotantes
def imagen(after,png,alt,ancho=16):
    d.add_picture(png,width=Cm(ancho)); np_=P()[-1]._p; np_.getparent().remove(np_)
    if np_.pPr is not None: np_.remove(np_.pPr)
    if modelo._p.pPr is not None: np_.insert(0,copy.deepcopy(modelo._p.pPr))
    for dp in np_.xpath('.//wp:docPr'): dp.set('descr',alt); dp.set('title',alt)
    after._p.addnext(np_)
def clave(t): return unicodedata.normalize('NFD',t.lower()).encode('ascii','ignore').decode()
def ref(titulo,nivel,texto):
    a,b=rango(titulo,nivel); ps=P()
    h=[i for i in range(a,b) if ps[i].text=='Referencias' and ps[i].style.name.startswith('Heading')][0]
    refs=[]; i=h+1
    while i<b and not ps[i].style.name.startswith('Heading') and ps[i].text.strip(): refs.append(ps[i]); i+=1
    plano=re.sub(r'\*','',texto)
    if any(r.text==plano for r in refs): return
    pos=next((k for k,r in enumerate(refs) if clave(r.text)>clave(plano)),len(refs))
    if pos==0:
        nuevo_despues(ps[h],texto,'First Paragraph'); refs[0].style=d.styles['Body Text']
    else: nuevo_despues(refs[pos-1],texto,'Body Text')


import subprocess, difflib
REPO='/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos/'
def plano(t): return re.sub(r'\*','',t)
def parrafos(t): return [b.strip() for b in t.split('\n\n') if b.strip() and not b.startswith('#') and not b.startswith('[[')]
def viejo(c): return subprocess.run(['git','-C','/home/claude/repo/360','show','HEAD:Seguridad Municipal 360°/Taller del libro/Capítulos/'+c+'/out/'+c+'.md'],capture_output=True,text=True).stdout
def cuerpo_md(t): return t.split('\n## Referencias')[0]
def aplica(c,titulo,nivel):
    a_=parrafos(cuerpo_md(viejo(c))); b_=parrafos(cuerpo_md(open(L+c+'/chk_X/'+c+'.md',encoding='utf-8').read()))
    for tag,i1,i2,j1,j2 in reversed(difflib.SequenceMatcher(None,a_,b_,autojunk=False).get_opcodes()):
        if tag=='equal': continue
        a,b=rango(titulo,nivel); ps=P()
        def busca_w(md):
            k=[i for i in range(a,b) if ps[i].text.strip()==plano(md).strip()]
            assert len(k)==1,(c,md[:60],len(k)); return ps[k[0]]
        if tag=='replace' and i2-i1==j2-j1:
            for x,y in zip(a_[i1:i2],b_[j1:j2]): reemplaza(busca_w(x),y)
        elif tag=='insert':
            q=busca_w(a_[i1-1])
            for y in b_[j1:j2]: q=nuevo_despues(q,y)
        elif tag=='replace' and j2-j1>i2-i1:
            ws=[busca_w(x) for x in a_[i1:i2]]
            for w,y in zip(ws,b_[j1:j1+i2-i1]): reemplaza(w,y)
            q=ws[-1]
            for y in b_[j1+i2-i1:j2]: q=nuevo_despues(q,y)
        else: raise SystemExit((c,tag,i1,i2,j1,j2))
def quita_ref(titulo,nivel,ini):
    a,b=rango(titulo,nivel); ps=P()
    k=[i for i in range(a,b) if ps[i].text.startswith(ini)]; assert len(k)==1
    e=ps[k[0]]._p; e.getparent().remove(e)

from docx.shared import Pt
from docx.oxml.ns import qn
import unicodedata
def bloques_md(t):
    out=[]
    for b in t.split('\n\n'):
        b=b.strip()
        if not b or b.startswith('[[') or b.startswith('<?') or b.startswith('# '): continue
        out.append(b)
    return out
def nuevo_md(q,b):
    if b.startswith('## '): return nuevo_despues(q,b[3:],'Heading 2')
    if b.startswith('### '): return nuevo_despues(q,b[4:],'Heading 3')
    return nuevo_despues(q,b)
def aplica3(c,titulo,nivel):
    a_=bloques_md(cuerpo_md(viejo(c))); b_=bloques_md(cuerpo_md(open(L+c+'/chk_X/'+c+'.md',encoding='utf-8').read()))
    n=0
    for tag,i1,i2,j1,j2 in reversed(difflib.SequenceMatcher(None,a_,b_,autojunk=False).get_opcodes()):
        if tag=='equal': continue
        a,b=rango(titulo,nivel); ps=P()
        def busca_w(md):
            t=plano(md[3:] if md.startswith('## ') else md).strip()
            k=[i for i in range(a,b) if ps[i].text.strip()==t]
            assert len(k)==1,(c,md[:60],len(k)); return ps[k[0]]
        if tag=='replace' and i2-i1==j2-j1:
            for x,y in zip(a_[i1:i2],b_[j1:j2]): reemplaza(busca_w(x),y); n+=1
        elif tag in ('insert','replace'):
            ws=[busca_w(x) for x in a_[i1:i2]]
            for w,y in zip(ws,b_[j1:j1+(i2-i1)]): reemplaza(w,y); n+=1
            q=ws[-1] if ws else busca_w(a_[i1-1])
            for y in b_[j1+(i2-i1):j2]: q=nuevo_md(q,y); n+=1
        else: raise SystemExit((c,tag))
    print(c,'cambios',n)
def refs_en_orden(c,titulo,nivel):
    zz=[x.strip() for x in open(L+c+'/chk_X/zz_referencias.md',encoding='utf-8').read().split('\n\n') if x.strip() and not x.startswith('#')]
    n=0
    for k,z in enumerate(zz):
        a,b=rango(titulo,nivel); ps=P()
        h=[i for i in range(a,b) if ps[i].text=='Referencias' and ps[i].style.name.startswith('Heading')][0]
        lista=[ps[i] for i in range(h+1,b) if ps[i].text.strip()]
        if any(p.text.startswith(plano(z)[:70]) for p in lista): continue
        prev=None
        for j in range(k-1,-1,-1):
            m=[p for p in lista if p.text.startswith(plano(zz[j])[:70])]
            if m: prev=m[0]; break
        if prev is None:
            nuevo_despues(ps[h],z,'First Paragraph'); lista[0].style=d.styles['Body Text']
        else: nuevo_despues(prev,z,'Body Text')
        n+=1
    print(c,'refs',n)
for c,t,nv in [('cap01','1. La red','Heading 1'),('cap03','3. El concepto','Heading 1'),('cap04','4. La persona en el centro','Heading 1'),('conclusion','Conclusión. Volver al núcleo','Heading 1'),('t01','1. Salud física','Heading 2')]:
    aplica3(c,t,nv); refs_en_orden(c,t,nv)
# introducción: sección nueva antes de «El mapa del viaje»
INTRO=open('/home/claude/libro/intro/src/intro.md',encoding='utf-8').read()
sec=INTRO[INTRO.index('## Lo que este libro sostiene'):INTRO.index('## El mapa del viaje')].strip()
a,b=rango('Introducción. El camino','Heading 1'); ps=P()
im=[i for i in range(a,b) if ps[i].text=='El mapa del viaje'][0]
from docx.text.paragraph import Paragraph
q=ps[im-1]
if 'Lo que este libro sostiene' not in [p.text for p in ps[a:b]]:
    for blq in [x.strip() for x in sec.split('\n\n') if x.strip()]:
        q=nuevo_md(q,blq)
# anexos
AX=open(L+'anexos/chk_X/anexos.md',encoding='utf-8').read()
ps=P(); ii=[k for k,p in enumerate(ps) if p.text=='Índice de legislación' and p.style.name=='Heading 1'][0]
ancla=ps[ii-1]
h1=nuevo_despues(ancla,'Anexos','Heading 1'); h1.paragraph_format.page_break_before=True
q=h1
lineas=AX.split('\n## Referencias')[0]
for blq in [x.strip() for x in lineas.split('\n\n') if x.strip() and not x.startswith('# ')]:
    if blq.startswith('|'):
        filas=[ [c.strip() for c in l.strip().strip('|').split('|')] for l in blq.split('\n') if not set(l.replace('|','').strip())<=set('-')]
        t=d.add_table(rows=len(filas),cols=4); t.style=d.styles['Table']
        for i,f in enumerate(filas):
            for j,txt in enumerate(f):
                cell=t.cell(i,j); par=cell.paragraphs[0]; par.style=d.styles['Compact']
                r=par.add_run(txt); r.font.size=Pt(8.5); r.bold=True if i==0 else None
                from docx.enum.text import WD_ALIGN_PARAGRAPH; par.alignment=WD_ALIGN_PARAGRAPH.LEFT
        trPr=t.rows[0]._tr.get_or_add_trPr(); from docx.oxml import OxmlElement
        th=OxmlElement('w:tblHeader'); th.set(qn('w:val'),'true'); trPr.append(th)
        q._p.addnext(t._tbl)
        # párrafo vacío de anclaje tras la tabla
        from copy import deepcopy
        vacio=OxmlElement('w:p'); t._tbl.addnext(vacio); q=Paragraph(vacio,q._parent); q.style=d.styles['Body Text']
        continue
    if blq.startswith('Fuente: elaboración propia'):
        q=nuevo_despues(q,blq,'Compact'); continue
    q=nuevo_md(q,blq)
# referencias de los anexos
zz=[x.strip() for x in open(L+'anexos/chk_X/zz_referencias.md',encoding='utf-8').read().split('\n\n') if x.strip() and not x.startswith('#')]
q=nuevo_despues(q,'Referencias','Heading 2')
for k,z in enumerate(zz): q=nuevo_despues(q,z,'First Paragraph' if k==0 else 'Body Text')
# índices
ORD=['introducción','capítulos','temas','conclusión','anexos']
def suma(texto,clase,num=None):
    base,sep,suf=texto.rpartition(': ')
    suf=suf.rstrip('.')
    g={}
    for parte in [x.strip() for x in suf.split(';')]:
        if parte.startswith('capítulo'): g['capítulos']=sorted({int(n) for n in re.findall(r'\d+',parte)})
        elif parte.startswith('tema'): g['temas']=sorted({int(n) for n in re.findall(r'\d+',parte)})
        else: g[parte]=True
    if num is not None:
        g[clase]=sorted(set(g.get(clase,[]))|{num})
    else: g[clase]=True
    out=[]
    for k in ORD:
        if k not in g: continue
        if k in ('capítulos','temas'):
            ns=g[k]; nombre=(k if len(ns)>1 else k[:-1]); out.append(nombre+' '+', '.join(map(str,ns)))
        else: out.append(k)
    return base+': '+'; '.join(out)+'.'
def indice(ini,clase,num=None):
    k=[p for p in P() if p.style.name=='Compact' and p.text.startswith(ini)]
    assert len(k)==1,ini
    reemplaza(k[0],suma(k[0].text,clase,num))
indice('Ley N.° 10159','anexos'); indice('Ley N.° 7794','anexos')
indice('Voto N.° 2026-014917','capítulos',1); indice('Voto N.° 2026-014917','capítulos',3)
indice('Voto N.° 2024-029734','capítulos',3); indice('Naciones Unidas, Dependencia','capítulos',3)
d.save(fo); print('listo')
