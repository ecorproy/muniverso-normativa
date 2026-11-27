import re,collections,statistics as st,csv
t=re.sub(r'\s+',' ',open('/tmp/ifam/idx2024_ocr.txt').read())
rows=[]
for m in re.finditer(r'índice final obtenido por (.{0,80}?) bajo el modelo',t,re.I):
    w=t[m.start():m.start()+700]
    name=re.sub(r'^(el cantón de|la intendencia de|el concejo municipal de distrito de|el distrito de|el Concejo Municipal de Distrito de)\s*','',m.group(1).strip(),flags=re.I)
    sc=re.search(r'es de (\d(?:[.,]\d)?) en una escala',w)
    lv=re.search(r'madurez es considerado ([a-zA-Záéíóú]+(?:\s?-\s?[a-zA-Záéíóú]+)?)',w)
    w2=w[w.find('madurez'):]
    low=re.search(r'(?:el|los) (?:valor(?:es)? )?más bajos? (?:lo comparten |se muestran? )?(?:en )?(?:la |las )?dimensi(?:ón|ones) ([A-ZÁÉÍÓÚ][^.(]{2,80})',w2)
    rows.append(dict(nombre=name, indice=float(sc.group(1).replace(',','.')) if sc else None,
        nivel=lv.group(1).replace(' ','').lower() if lv else '', bajo=(low.group(1) if low else '').strip()))
w=csv.DictWriter(open('smart2024.csv','w',encoding='utf-8',newline=''),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), sum(1 for r in rows if r['indice'] is None))
sc=[r['indice'] for r in rows if r['indice'] is not None]
print('min',min(sc),'max',max(sc),'media',round(st.mean(sc),2),'mediana',st.median(sc), 'n',len(sc))
print(collections.Counter(r['nivel'] for r in rows))
def dims(s): return [d for d in ('Planeamiento Urbano','Competitividad','Ambiente','Gobernanza','Desarrollo Humano') if d in s]
c=collections.Counter(); nb=0
for r in rows:
    d=dims(r['bajo'])
    if d: nb+=1
    for x in d: c[x]+=1
print('bajo',c,nb)
print('pu como más baja (sola o compartida)', sum(1 for r in rows if 'Planeamiento Urbano' in dims(r['bajo'])))
print(sorted([(r['indice'],r['nombre']) for r in rows if r['indice'] is not None])[:3], sorted([(r['indice'],r['nombre']) for r in rows if r['indice'] is not None])[-3:])
print([r for r in rows if not dims(r['bajo'])][:6])
