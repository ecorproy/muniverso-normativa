# Convierte una ley pegada de SINALEVI en un archivo con encabezado, para el verificador.
# Uso: sinalevi2md.py PEGADO.txt dd/mm/aaaa [carpeta]
import re, sys, os
src, fecha = sys.argv[1], sys.argv[2]
dest = sys.argv[3] if len(sys.argv) > 3 else '/home/claude/libro/fuentes'
t = open(src, encoding='utf-8').read().replace('\r', '')
lines = [l for l in t.split('\n')]
nz = [l.strip() for l in lines if l.strip()]
m = re.match(r'Ley\s+(\d+)', nz[0]); num = m.group(1); nombre = nz[1]
ver = re.search(r'Versión de la Norma:\s*(.+)', t)
body = '\n'.join(lines)
body = re.sub(r'(?m)^\s*Ficha Art[íi]culo.*$', '', body)
body = re.sub(r'(?m)^-Usted está en la última versión de la norma-\s*$', '', body)
body = re.sub(r'(?m)^Versión de la Norma:.*$', '', body)
body = re.sub(r'(?m)^[ \t ]+', '', body)
body = re.sub(r'\n{3,}', '\n\n', body).strip()
fm = ['---', f'numero: "Ley {num}"', f'nombre: "{nombre}"', 'estado: "vigente"',
      f'version_sinalevi: "{ver.group(1).strip() if ver else ""}"', 'ente_emisor: "Asamblea Legislativa"',
      f'fecha_norma: "{fecha}"', 'descargado: "2026-11-22"',
      'fuente: "Texto de SINALEVI pegado por el autor el 22 de noviembre de 2026."', '---']
out = f'{dest}/Ley {num}.md'
open(out, 'w', encoding='utf-8').write('\n'.join(fm) + '\n' + body + '\n')
print(out, len(body), 'caracteres;', 'versión', ver.group(1).strip() if ver else '?')
