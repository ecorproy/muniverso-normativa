# nexus2md_otros.py PEGADO.txt tca|s1 "resultado" "partes": convierte una resolución del Tribunal Contencioso (tca)
# o de la Sala Primera (s1) pegada desde NexusPJ. Deja el archivo en /home/claude/libro/fuentes/tca o /sala1.
import re, sys
MES = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'setiembre':9,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
src = open(sys.argv[1], encoding='utf-8', errors='replace').read()
tipo, res, partes = sys.argv[2], sys.argv[3], sys.argv[4]
m = re.search(r'Resolución Nº\s*(\d+)\s*-\s*(\d{4})', src); num = f'{m.group(2)}-{int(m.group(1)):06d}'
m = re.search(r'Fecha de la Resolución:\s*(\d{1,2}) de (\w+) del (\d{4}) a las (\d{1,2}):(\d{2})', src)
fecha = f'{m.group(3)}-{MES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}'; hora = f'{int(m.group(4)):02d}:{m.group(5)}'
exp = re.search(r'Expediente:\s*(\S+)', src).group(1)
red = re.search(r'Redactado por:\s*([^\n]+)', src).group(1).strip()
i = src.index('Texto de la resolución') + len('Texto de la resolución')
ends = [src.find(x, i) for x in ('- Código Verificador -', 'Clasificación elaborada por', 'Es copia fiel del original')]
j = min(e for e in ends if e > 0)
body = re.sub(r'\n{3,}', '\n\n', re.sub(r'(?m)^[ \t\u00a0]+', '', src[i:j])).strip('\n')
if tipo == 'tca':
    sec = re.search(r'Tribunal Contencioso Administrativo Sección (\w+)', src).group(1)
    ente = f'Tribunal Contencioso Administrativo, Sección {sec}'; out = f'/home/claude/libro/fuentes/tca/Sentencia TCA {sec} {num}.md'
else:
    ente = 'Sala Primera de la Corte Suprema de Justicia'; out = f'/home/claude/libro/fuentes/sala1/Sentencia Sala Primera {num}.md'
head = f'''---
numero: "{num}"
nombre: "{ente}, N.° {int(num.split("-")[1])}-{num.split("-")[0]} — {partes}"
ente_emisor: "{ente}"
tipo: "Sentencia"
fecha: "{fecha}"
hora: "{hora}"
expediente: "{exp}"
clase: "Proceso de conocimiento"
resultado: "{res}"
redactor: "{red}"
materia: "Municipal (Seguridad Municipal 360°)"
enlace: ""
descargado: "2026-11-22"
fuente: "Texto de NexusPJ aportado por Edward Cortés García el 22 de noviembre de 2026"
---
# {ente}, N.° {int(num.split("-")[1])}-{num.split("-")[0]}

'''
open(out, 'w', encoding='utf-8').write(head + body + '\n')
print(num, fecha, hora, exp, red, len(body), '->', out)
