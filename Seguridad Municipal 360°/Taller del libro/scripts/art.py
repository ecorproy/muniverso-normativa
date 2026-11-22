# Imprime artículos de una ley del repositorio: art.py <archivo> <máx. caracteres> <art> [<art> ...]
import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
mx = int(sys.argv[2])
ART = re.compile(r'(?im)^\W{0,6}(?:ART[IÍ]CULO|Art[ií]culo|Articulo)\s+(\d+)(?:\s*(bis|ter))?\s*[º°o]?\s*[\.\-—–:]')
ms = list(ART.finditer(t))
for want in sys.argv[3:]:
    hit = False
    for i, m in enumerate(ms):
        k = m.group(1) + (' ' + m.group(2).lower() if m.group(2) else '')
        if k == want:
            end = ms[i+1].start() if i+1 < len(ms) else len(t)
            s = re.sub(r'\s+', ' ', t[m.start():end]).strip()
            print(f'[{want}] ' + s[:mx] + (' …' if len(s) > mx else '')); hit = True; break
    if not hit: print(f'[{want}] NO HALLADO')
