# Imprime páginas de un texto extraído con pdftotext (separadas por \f).
# Uso: python3 -I pp.py ARCHIVO DESDE HASTA [maxchars_por_pagina]
import sys, re
f, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 100000
t = open(f, encoding='utf-8').read().split('\f')
for i in range(a, min(b, len(t)) + 1):
    p = t[i-1]
    p = re.sub(r'[ \t]+', ' ', p)
    p = re.sub(r'\n\s*\n+', '\n', p).strip()
    print(f'===== p. {i} de {len(t)} =====')
    print(p[:mx])
