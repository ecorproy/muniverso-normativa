# dver.py ANCHO MAX DICTAMEN PATRÓN [PATRÓN...] : coincidencias de cada patrón con su contexto en un dictamen de la PGR
import re, sys, glob
R = '/home/claude/repo/main/Jurisprudencia administrativa (PGR)'
w = int(sys.argv[1]); mx = int(sys.argv[2]); d = sys.argv[3]; pats = sys.argv[4:]
fs = glob.glob(f'{R}/*/Dictamen {d}.md')
if not fs: print('NO ESTÁ', d); sys.exit()
t = open(fs[0], encoding='utf-8').read()
flat = re.sub(r'\s+', ' ', re.sub(r'(?s)^---.*?---', '', t, count=1))
print(f'##### {d} ({len(flat)} car.)')
for p in pats:
    ms = list(re.finditer(p, flat, re.I))
    print(f'  [{p}] {len(ms)} coincidencia(s)')
    for m in ms[:mx]:
        print(f'    @{m.start()}: …' + flat[max(0, m.start() - w):m.end() + w] + '…')
