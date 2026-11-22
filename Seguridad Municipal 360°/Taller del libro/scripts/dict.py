# dict.py DICTAMEN [n frases] [largo conclusión]: consulta, frases con «lo local» y conclusión
import re, sys, glob
R = '/home/claude/repo/main/Jurisprudencia administrativa (PGR)'
d = sys.argv[1]; nf = int(sys.argv[2]) if len(sys.argv) > 2 else 6; lc = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
pat = sys.argv[4] if len(sys.argv) > 4 else r'lo\s+[“"«\']?\s*local\s*[”"»\']?(?!\w)'
f = (glob.glob(f'{R}/*/Dictamen {d}.md') + glob.glob(f'{R}/*/Opinión Jurídica {d}.md') + glob.glob(f'{R}/*/*{d}.md'))[0]
t = open(f, encoding='utf-8').read()
g = lambda k: (re.search(r'(?m)^' + k + r':\s*"([^"]*)"', t) or [None, ''])[1]
body = re.sub(r'(?s)^---.*?---', '', t, count=1)
flat = re.sub(r'\s+', ' ', body)
print(f'##### {d} | {g("fecha")} | {g("institucion")} | {g("consultante")} | {len(t.split())} palabras')
i = flat.find('Estimad'); print('CONSULTA:', flat[i:i + 1100]); print()
seen = 0
for m in re.finditer(r'[^.]*' + pat + r'[^.]*\.', flat, re.I):
    s = m.group(0).strip()
    if len(s) > 60:
        print('·', s[:560]); seen += 1
        if seen >= nf: break
ms = [m.start() for m in re.finditer(r'(?i)\bCONCLUSI[OÓ]N(?:ES)?\b', flat)]
print(); print('CONCLUSIÓN:', flat[ms[-1]:ms[-1] + lc] if ms else flat[-lc:])
