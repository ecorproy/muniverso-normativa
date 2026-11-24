# donde.py ARCHIVO /patrón/ [ancho]: artículo en que cae cada aparición del patrón
import re, sys
t = re.sub(r'[ \t]+', ' ', open(sys.argv[1], encoding='utf-8').read())
pat = sys.argv[2].strip('/'); w = int(sys.argv[3]) if len(sys.argv) > 3 else 200
arts = [(m.start(), m.group(1)) for m in re.finditer(r'(?im)^\W*art[íi]culo\s+(\d+[\w ]{0,6}?)\s*[\.\-–:°º]', t)]
for m in re.finditer(pat, t, re.I):
    a = [n for p, n in arts if p <= m.start()]
    print(f'art. {a[-1] if a else "-"} @{m.start()}:', re.sub(r'\s+', ' ', t[max(0, m.start()-w):m.end()+w])); print()
