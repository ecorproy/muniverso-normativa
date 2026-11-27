import json,re,sys,os
sys.path.insert(0,'/home/claude/division')
from collections import defaultdict,OrderedDict
from docx import Document
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
from empareja import carga,empareja
from unidades_docx import mapa,T
DOCX='/home/claude/Seguridad Municipal 360 (final76).docx'
D,U,R=carga(DOCX); par,usado=empareja(D,U,R)
refs=D['referencias']; A=[a for a in D['apariciones'] if not a['fuente'].startswith('RECURSO')]
ET=D['etiquetas']
def tomo_de(et):
    if et in ('introducción','prólogo') or et.startswith('capítulo'): return 'I'
    if et.startswith('tema'): return 'I' if int(et.split()[1])<=18 else 'II'
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
NAT={'CP':'Constitución','L':'Ley','DE':'Decreto ejecutivo','RM':'Reglamento o política municipal','V':'Sentencia (Sala Constitucional)',
 'S1':'Sentencia (Sala Primera)','T':'Resolución (Tribunal Contencioso Administrativo)','J':'Resolución (otros tribunales)','O':'Oficio, informe o resolución (CGR)','M':'Doctrina o documento'}
def naturaleza(f):
    k=f.split(':')[0]
    if k=='D': return 'Opinión jurídica (PGR)' if f.split(':')[1].startswith('OJ') else 'Dictamen (PGR)'
    if k=='M' and re.search(r'v\.|Tribunal|Conseil|Corte|Sentencia|Supreme|Audiencia',refs.get(f,'')): return 'Jurisprudencia extranjera'
    return NAT.get(k,k)
def autoridad(f):
    k=f.split(':')[0]; r=refs.get(f,'')
    fijo={'CP':'Asamblea Nacional Constituyente','L':'Asamblea Legislativa','DE':'Poder Ejecutivo','V':'Sala Constitucional','S1':'Sala Primera','D':'Procuraduría General de la República','O':'Contraloría General de la República'}
    if k in fijo: return fijo[k]
    m=re.match(r'([^().]+?)(?:\.)? \(',r)
    return (m.group(1) if m else r.split('.')[0])[:120]
def fecha(r):
    m=re.search(r'\((\d{4}[a-z]?|s\. f\.)',r); return m.group(1) if m else ''
def url(r):
    m=re.findall(r'https?://\S+',r); return ' '.join(x.rstrip('.') for x in m)
ent_de=defaultdict(list)
for ind,cat,i,nombre,uni,best,sc in par: ent_de[best].append((ind,cat,nombre,uni))
wb=Workbook(); H=Font(name='Arial',bold=True,color='FFFFFF'); F=Font(name='Arial',size=10); FILL=PatternFill('solid',fgColor='2C4A6E')
def hoja(ws,cab,filas,anchos):
    ws.append(cab)
    for c in ws[1]: c.font=H; c.fill=FILL; c.alignment=Alignment(wrap_text=True,vertical='top')
    for f in filas: ws.append(f)
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font=F; c.alignment=Alignment(wrap_text=True,vertical='top')
    for i,w in enumerate(anchos,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions
# --- Fuentes
porf=defaultdict(list)
for a in A: porf[a['fuente']].append(a)
fil=[]
orden=sorted(U,key=lambda f:(f.split(':')[0],f))
for n,f in enumerate(orden,2):
    ap=porf[f]; us=U[f]; t1=[u for u in us if tomo_de(u)=='I']; t2=[u for u in us if tomo_de(u)=='II']
    formas=list(OrderedDict.fromkeys(re.sub(r', (?:art|cons|considerando|p|pp|apartado|conclusión|conclusiones|por tanto|resultando|inciso)\b.*\)$',')',a['forma']) for a in ap))[:6]
    locs=list(OrderedDict.fromkeys(a['loc'] for a in ap if a['loc']))
    ents=ent_de.get(f,[])
    estado='Pendiente de comprobación' if not ents else ('Incidencia previa' if any(set(e[3])!=us for e in ents) else ('Compartida entre tomos' if t1 and t2 else 'Conservada'))
    fil.append([f,naturaleza(f),autoridad(f),f.split(':',1)[1] if ':' in f else f,fecha(refs.get(f,'')),refs.get(f,''),' | '.join(formas),'; '.join(locs)[:3000],
                compacta(us),compacta(t1),compacta(t2),f'=IF(AND(J{n}<>"",K{n}<>""),"Sí","No")',f"=COUNTIF(Apariciones!A:A,A{n})",url(refs.get(f,'')),estado,' / '.join(e[2] for e in ents)])
ws=wb.active; ws.title='Fuentes'
hoja(ws,['Identificador','Naturaleza','Autoridad o autor','Identificación','Fecha','Cita completa (referencia)','Citas abreviadas (formas en el texto)','Localizadores','Ubicaciones','Tomo I','Tomo II','Compartida','Apariciones','URL','Estado','Entrada en los índices del original'],fil,[18,22,28,18,9,60,40,40,30,26,26,11,11,30,20,45])
# --- Apariciones
ws=wb.create_sheet('Apariciones')
hoja(ws,['Identificador','Unidad','Tomo','Localizador','Forma en el texto','Cita textual'],[[a['fuente'],ET[a['unidad']],a['tomo'],a['loc'],a['forma'],'Sí' if a['textual'] else 'No'] for a in A],[18,14,7,30,70,10])
# --- Citas textuales
ct=[]
for u in ET:
    p=f'/home/claude/libro/{u}/chk_X/zz_citas.json'
    if not os.path.exists(p): p=f'/home/claude/libro/{u}/out/zz_citas.json'
    if os.path.exists(p):
        for c in json.load(open(p)): ct.append([ET[u],tomo_de(ET[u]),c['fuente'],c['palabras'],c['estado'],c['cita']])
ws=wb.create_sheet('Citas textuales'); hoja(ws,['Unidad','Tomo','Fuente y localizador','Palabras','Cotejo','Inicio de la cita'],ct,[14,7,40,10,10,70])
# --- Índices
fi=[[ind,cat or '',nombre,compacta(uni),compacta([u for u in uni if tomo_de(u)=='I']),compacta([u for u in uni if tomo_de(u)=='II']),best,'Sí' if set(uni)==U.get(best,set()) else 'No'] for ind,cat,i,nombre,uni,best,sc in par]
ws=wb.create_sheet('Índices'); hoja(ws,['Índice','Categoría','Entrada','Unidades (original)','Tomo I','Tomo II','Fuente en la matriz','Coincide con las apariciones'],fi,[28,28,60,40,30,30,20,14])
# --- Remisiones entre tomos
els=list(Document(DOCX).element.body); M=mapa(els)
pat=re.compile(r'\b(temas?|cap[íi]tulos?|anexos?|figuras?) ((?:\d+|[AB])(?:(?:, | y | o |-| a )(?:\d+|[AB]))*)',re.I)
rem=[]
for e,u in zip(els,M):
    if not (u.startswith('tema') or u.startswith('capítulo') or u in ('introducción','conclusión','anexos')): continue
    t=T(e); tu=tomo_de(u)
    for m in pat.finditer(t):
        tipo=m.group(1).lower(); ns=re.findall(r'\d+|[AB]',m.group(2))
        dest=[]
        for x in ns:
            if tipo.startswith('tema'): dest.append(('tema '+x, tomo_de('tema '+x)))
            elif tipo.startswith('cap'): dest.append(('capítulo '+x,'I'))
            elif tipo.startswith('anexo'): dest.append(('anexo '+x,'II'))
            else: dest.append(('figura '+x,'II' if x=='16' else 'I'))
        otros=[d for d,tt in dest if tt!=tu]
        if otros: rem.append([u,tu,m.group(0),', '.join(otros),'II' if tu=='I' else 'I',t[max(0,m.start()-80):m.end()+40]])
ws=wb.create_sheet('Remisiones entre tomos'); hoja(ws,['Unidad de origen','Tomo de origen','Remisión','Destino en el otro tomo','Tomo de destino','Contexto'],rem,[14,8,22,26,9,90])
# --- Siglas
sig=[]
B_SIG=['CP','CM','LGAP','LJC','CC','CT','CGR','PGR','IGSM','TCA','ICN','IFAM','CCSS']
for u in ET:
    p=f'/home/claude/libro/{u}/chk_X/'
    f=[x for x in os.listdir(p) if x.endswith('.md') and not x.startswith('zz') and x not in ('unido.md','unido_esperado.md')] if os.path.isdir(p) else []
    if not f: continue
    txt=open(p+f[0],encoding='utf-8').read()
    for s in B_SIG:
        ms=[m.start() for m in re.finditer(r'(?<![\w\[])'+s+r'\b',txt)]
        if not ms: continue
        md=re.search(r'[\[(]'+s+r'[\]),. ]',txt); dd=md.start() if md else -1
        ok=dd>=0 and dd<=ms[0]+1
        antes=txt[:ms[0]]; en_cita=antes.count('"')%2==1
        obs='Definida en la propia unidad antes del primer uso' if ok else ('Primer uso dentro de una cita textual (sigla de la fuente)' if en_cita else 'Uso sin definición previa en la unidad')
        sig.append([ET[u],tomo_de(ET[u]),s,len(ms),'Sí' if ok else 'No',obs])
ws=wb.create_sheet('Siglas por unidad'); hoja(ws,['Unidad','Tomo','Sigla','Usos','Definida antes del primer uso','Observación'],sig,[14,7,9,8,14,50])
# --- Resumen
ws=wb.create_sheet('Resumen',0)
ws.append(['Matriz maestra de trazabilidad jurídica y documental — Seguridad Municipal 360°']); ws['A1'].font=Font(name='Arial',bold=True,size=13)
ws.append(['Manuscrito: Seguridad Municipal 360° (final76).docx. Unidades del Tomo I: introducción, capítulos 1 a 4 y temas 1 a 18. Unidades del Tomo II: temas 19 a 36, conclusión y anexos.'])
ws.append([])
filas=[('Fuentes únicas','=COUNTA(Fuentes!A:A)-1'),('Fuentes con presencia en el Tomo I','=COUNTIF(Fuentes!J:J,"?*")'),('Fuentes con presencia en el Tomo II','=COUNTIF(Fuentes!K:K,"?*")'),
 ('Fuentes compartidas entre tomos','=COUNTIF(Fuentes!L:L,"Sí")'),('Apariciones (citas en el texto)','=COUNTA(Apariciones!A:A)-1'),('Apariciones en el Tomo I','=COUNTIF(Apariciones!C:C,"I")'),
 ('Apariciones en el Tomo II','=COUNTIF(Apariciones!C:C,"II")'),('Citas textuales','=COUNTA(\'Citas textuales\'!A:A)-1'),('Entradas de los índices del original','=COUNTA(Índices!A:A)-1'),
 ('Entradas que no coinciden con las apariciones','=COUNTIF(Índices!H:H,"No")'),('Fuentes sin entrada propia en los índices','=COUNTIF(Fuentes!O:O,"Pendiente de comprobación")'),
 ('Remisiones hacia el otro tomo','=COUNTA(\'Remisiones entre tomos\'!A:A)-1'),('Siglas usadas sin definición previa en su unidad','=COUNTIF(\'Siglas por unidad\'!E:E,"No")')]
for a,b in filas: ws.append([a,b])
for row in ws.iter_rows(min_row=2):
    for c in row: c.font=Font(name='Arial',size=10,bold=c.font.bold)
ws.column_dimensions['A'].width=55; ws.column_dimensions['B'].width=14
OUT='/home/claude/division/Matriz maestra de trazabilidad jurídica y documental de Seguridad Municipal 360°.xlsx'
wb.save(OUT); print(OUT, len(fil),len(A),len(ct),len(fi),len(rem),len(sig))
