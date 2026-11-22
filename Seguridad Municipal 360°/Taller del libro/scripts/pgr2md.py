# pgr2md.py PEGADO.txt CÓDIGO "consultante" "institución": convierte un pronunciamiento de la Procuraduría pegado desde
# SINALEVI al formato del repositorio y lo deja en /home/claude/libro/fuentes/dictamenes/Dictamen CÓDIGO.md
import re, sys
src = open(sys.argv[1], encoding='utf-8', errors='replace').read()
cod, cons, inst = sys.argv[2], sys.argv[3], sys.argv[4]
m = re.search(r'(Dictamen|Opinión Jurídica)\s*:\s*(\d+)\s*-\s*del\s*(\d{2}/\d{2}/\d{4})', src)
tipo = 'Dictamen de la Procuraduría General de la República' if m.group(1) == 'Dictamen' else 'Opinión jurídica de la Procuraduría General de la República'
i = m.start(); j = src.find('© 2026 Procuraduría'); j = j if j > 0 else len(src)
body = re.sub(r'\n{3,}', '\n\n', re.sub(r'(?m)^[ \t\u00a0]+', '', src[i:j])).strip('\n')
head = f'''---
numero: "{cod}"
tipo: "{tipo}"
fecha: "{m.group(3)}"
consultante: "{cons}"
institucion: "{inst}"
materia: "Servicios municipales"
temas: "Agua potable y acueductos municipales"
enlace: ""
descargado: "2026-11-22"
fuente: "Texto de SINALEVI aportado por Edward Cortés García el 22 de noviembre de 2026"
---
# Dictamen {cod}

'''
out = f'/home/claude/libro/fuentes/dictamenes/Dictamen {cod}.md'
open(out, 'w', encoding='utf-8').write(head + body + '\n')
print(cod, '|', m.group(1), m.group(3), '|', len(body), 'car. ->', out)
