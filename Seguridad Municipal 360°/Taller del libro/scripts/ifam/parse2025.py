import re,csv,sys
raw=open('/tmp/ifam/idx2025.txt',encoding='utf-8').read()
pages=raw.split('\f')
def num(s):
    s=s.replace('₡','').replace(' ','').replace(' ','').replace('.','').replace(',','.')
    try: return float(s)
    except: return None
rows=[]
for i,pg in enumerate(pages,1):
    if 'DATOS CANTONALES' not in pg and 'DATOS' not in pg: continue
    hm=re.search(r'(\d\.\d\d(?:\.\d\d)?)\s+([A-ZÁÉÍÓÚÑ][^\n]*?)\s*(?:\n|$)',pg)
    if not re.search(r'Población:',pg): continue
    code=hm.group(1); name=hm.group(2).strip()
    def f(lbl):
        mm=re.search(lbl+r':\s*([^\n]+)',pg); return mm.group(1).strip() if mm else ''
    r=dict(pagina=i,codigo=code,nombre=name,
        poblacion=num(f('Población').split('hab')[0]),
        extension=f('Extensión territorial'),
        pres2024=num(f('Presupuesto total 2024')),
        pres2025=num(f('Presupuesto ordinario 2025')),
        plan=f('Plan regulador'),
        ley8114=num(f('Ley 8114')), inmuebles=num(f('Bienes inmuebles')),
        construccion=num(f('Permisos de construcción')), patentes=num(f('Patentes')),
        zmt=num(f(r'Zona Marítimo Terrestre \(ZMT\)')), otros=num(f('Otros Ingresos')),
        idh=f('Índice desarrollo humano'), competitividad=f('Posición índice competitividad'),
        progreso=f('Posición índice progreso social'), gestion=f(r'Posición índice gestión \(CGR\)'))
    rows.append(r)
w=csv.DictWriter(open('/home/claude/ifam/ifam2025.csv','w',encoding='utf-8',newline=''),fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows)
print(len(rows))
