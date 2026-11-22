# nexus2md.py PEGADO.txt "resultado" "contra quién": convierte un voto pegado desde NexusPJ al formato del repositorio
# y lo deja en /home/claude/libro/fuentes/votos/Sentencia AAAA-NNNNNN.md (solo el «Texto de la resolución»).
import re, sys
MES = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'setiembre':9,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
src = open(sys.argv[1], encoding='utf-8', errors='replace').read()
res = sys.argv[2] if len(sys.argv) > 2 else ''
contra = sys.argv[3] if len(sys.argv) > 3 else ''
m = re.search(r'Resolución Nº\s*(\d+)\s*-\s*(\d{4})', src); num = f'{m.group(2)}-{int(m.group(1)):06d}'
m = re.search(r'Fecha de la Resolución:\s*(\d{1,2}) de (\w+) del (\d{4}) a las (\d{1,2}):(\d{2})', src)
fecha = f'{int(m.group(1)):02d}/{MES[m.group(2).lower()]:02d}/{m.group(3)}'; hora = f'{int(m.group(4)):02d}:{m.group(5)}'
exp = re.search(r'Expediente:\s*(\S+)', src).group(1)
red = re.search(r'Redactado por:\s*([^\n]+)', src).group(1).strip()
_c = re.search(r'Clase de asunto:\s*([^\n]+)', src); cla = _c.group(1).strip() if _c else 'Recurso de amparo'
i = src.index('Texto de la resolución') + len('Texto de la resolución')
ends = [src.find(x, i) for x in ('Documento Firmado Digitalmente', '-- Código verificador --', 'Teléfonos: 2549', 'Clasificación elaborada por', 'Es copia fiel del original')]
j = min(e for e in ends if e > 0)
body = re.sub(r'\n{3,}', '\n\n', re.sub(r'(?m)^[ \t\u00a0]+', '', src[i:j])).strip('\n')
head = f'''---
numero: "{num}"
nombre: "Sentencia {num} de la Sala Constitucional — {contra}"
ente_emisor: "Sala Constitucional"
tipo: "Sentencia de la Sala Constitucional"
fecha: "{fecha}"
hora: "{hora}"
expediente: "{exp}"
clase: "{cla}"
resultado: "{res}"
redactor: "{red}"
materia: "Municipal (Seguridad Municipal 360°)"
enlace: ""
descargado: "2026-11-22"
fuente: "Texto de NexusPJ aportado por Edward Cortés García el 22 de noviembre de 2026 (tomado de Nexus.PJ ese día)"
---
# Sentencia {num} de la Sala Constitucional

'''
out = f'/home/claude/libro/fuentes/votos/Sentencia {num}.md'
open(out, 'w', encoding='utf-8').write(head + body + '\n')
print(num, '|', fecha, hora, '|', exp, '|', red, '|', cla, '|', len(body), 'car. |', len(body.split()), 'palabras ->', out)
