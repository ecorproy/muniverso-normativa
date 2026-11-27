"""Correcciones autorizadas por el autor (27-11-2026) a los índices especializados:
dos entradas con unidades omitidas y catorce fuentes citadas sin entrada."""
import re,copy,unicodedata
from docx.oxml.ns import qn
from indices import lee,T,S
UNIDADES_FALTANTES={'Decreto Ejecutivo N.° 43952':'capítulo 4','Voto N.° 2003-011382':'capítulo 3'}
NUEVAS=[ # (índice, categoría, nombre, unidades)
 ('Índice de legislación','Leyes','Ley N.° 5525, Ley de Planificación Nacional (1974)',['capítulo 4']),
 ('Índice de legislación','Leyes','Ley N.° 8131, Ley de la Administración Financiera de la República y Presupuestos Públicos (2001)',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Sala Constitucional','Voto N.° 2021-017098',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Procuraduría General de la República','Dictamen C-016-2024',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Procuraduría General de la República','Dictamen C-078-2025',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Índice de Cumplimiento para la Mejora Pública (ICM) 2026 [Infografía metodológica]',['capítulo 4','conclusión']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Listado de buenas prácticas del Índice de Cumplimiento para la Mejora Pública 2026',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Ficha técnica: indicador de eficacia [Índice de Cumplimiento para la Mejora Pública]',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Ficha técnica: indicador de eficiencia [Índice de Cumplimiento para la Mejora Pública]',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Ficha técnica: indicador de estrategia y gestión de datos [Índice de Cumplimiento para la Mejora Pública]',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Ficha técnica: indicador de cultura y liderazgo [Índice de Cumplimiento para la Mejora Pública]',['capítulo 4']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Tabla de datos del Índice de Gestión de Servicios Municipales 2025',['tema 4','tema 10','tema 29','conclusión']),
 ('Índice de jurisprudencia y criterios administrativos','Contraloría General de la República','Fichas de indicadores del Índice de Gestión de Servicios Municipales 2025',['tema '+str(n) for n in (1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,32,33,34,35,36)]),
 ('Índice de obras y documentos citados',None,'Ortíz-Fernandez, J., Baldeón-Tovar, M., Medina-Pelaiza, L., Ortíz-Huamán, C., & Godiño-Poma, M. (2024). Gestión por procesos en las empresas. Una revisión sistémica. Gestionar: Revista de Empresa y Gobierno, 4(1), 7-22. https://doi.org/10.35622/j.rg.2024.01.001',['capítulo 4']),
]
def nz(s): return re.sub(r'[^a-z0-9 ]+','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def clave(cat,nombre):
    if cat=='Leyes': return (int(re.search(r'N\.° ([\d.]+)',nombre).group(1).replace('.','')),)
    if cat=='Sala Constitucional': return (nombre,)
    if cat=='Procuraduría General de la República':
        m=re.search(r'([A-Z]+)-(\d+)-(\d{4})',nombre); return (m.group(1),int(m.group(3)),int(m.group(2))) if m else (nombre,)
    return (nz(nombre),)
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
def pon_texto(p,txt):
    rs=p.findall(qn('w:r'))
    for r in rs[1:]: p.remove(r)
    t=rs[0].find(qn('w:t')); t.text=txt; t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
def corrige(body,unidades_de):
    """unidades_de: dict nombre-> lista de unidades (para las entradas con None)."""
    els=list(body); R=lee(els); log=[]
    for ind,cat,i,nombre,uni in R:
        for k,falta in UNIDADES_FALTANTES.items():
            if nombre.startswith(k) and falta not in uni:
                pon_texto(els[i],nombre+': '+compacta(uni+[falta])+'.'); log.append(f'{nombre}: se agrega {falta}')
    for ind,cat,nombre,uni in NUEVAS:
        uni=uni or unidades_de[nombre]
        els=list(body); R=lee(els)
        grupo=[(i,n) for (x,c,i,n,u) in R if x==ind and c==cat]
        k=clave(cat,nombre); ref=None
        for i,n in grupo:
            try: menor=clave(cat,n)<k
            except TypeError: menor=nz(n)<nz(nombre)
            if menor: ref=i
        nuevo=copy.deepcopy(els[grupo[0][0]]); pon_texto(nuevo,nombre+': '+compacta(uni)+'.')
        if ref is None: els[grupo[0][0]].addprevious(nuevo)
        else: els[ref].addnext(nuevo)
        log.append(f'Nueva entrada ({cat or ind}): {nombre}: {compacta(uni)}')
    return log
