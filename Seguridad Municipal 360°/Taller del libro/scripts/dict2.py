# dict2.py LARGO_CONSULTA LARGO_CONCLUSION DICTAMEN...: consulta y conclusión, compactas
import re, sys, glob
R = '/home/claude/repo/main/Jurisprudencia administrativa (PGR)'
a, b = int(sys.argv[1]), int(sys.argv[2])
for d in sys.argv[3:]:
    fs = glob.glob(f'{R}/*/Dictamen {d}.md')
    if not fs: print(f'##### {d}: NO ESTÁ'); continue
    t = open(fs[0], encoding='utf-8').read()
    g = lambda k: (re.search(r'(?m)^' + k + r':\s*"([^"]*)"', t) or [None, ''])[1]
    flat = re.sub(r'\s+', ' ', re.sub(r'(?s)^---.*?---', '', t, count=1))
    i = flat.find('Estimad')
    ms = [m.start() for m in re.finditer(r'(?i)\bCONCLUSI[OÓ]N(?:ES)?\b', flat)]
    print(f'##### {d} | {g("fecha")} | {g("institucion")} | {len(t.split())} pal.')
    print('CONSULTA:', flat[i:i + a]); print('CONCLUSIÓN:', flat[ms[-1]:ms[-1] + b] if ms else flat[-b:]); print()
