# seg.py VOTO  -> estructura;  seg.py VOTO r1[:max] cIII[:max] pt[:max] /patrón/ancho ...
import re, sys, glob
v = sys.argv[1]
c = glob.glob(f'/home/claude/libro/fuentes/votos/Sentencia {v}.md') or glob.glob(f'/home/claude/repo/main/Jurisprudencia constitucional (Sala Constitucional)/**/Sentencia {v}.md', recursive=True)
r = open(c[0], encoding='utf-8').read()
cons = [(m.start(), m.group(1)) for m in re.finditer(r'(?m)^\W{0,6}([IVXL]{1,7})\)?\s*\.?\s*[-–—.]+\s*\S', r)]
res = [(m.start(), m.group(1)) for m in re.finditer(r'(?m)^\W{0,3}(\d{1,2})\s*\.\s*[-–—]', r)]
pt = [m.start() for m in re.finditer(r'(?im)^\W{0,6}por tanto\s*:?', r)]
ci = [m.start() for m in re.finditer(r'(?im)^\W{0,6}considerando\s*:?\s*$', r)]
def limpio(a, b): return re.sub(r'[ \t]+', ' ', re.sub(r'\n\s*\n+', '\n', r[a:b])).strip()
def fin(lista, i, tope): return lista[i+1][0] if i+1 < len(lista) else tope
tope_res = ci[0] if ci else (cons[0][0] if cons else len(r))
tope_con = pt[-1] if pt else len(r)
if len(sys.argv) == 2:
    print('largo', len(r), '| considerando @', ci, '| por tanto @', pt)
    print('resultandos:', [(n, p) for p, n in res])
    for k, (p, n) in enumerate(cons): print(f'  {n:>5} @{p:>6} ({fin(cons,k,tope_con)-p:>6}) {limpio(p, p+90)}')
for a in sys.argv[2:]:
    if a.startswith('/'):
        pat, _, an = a[1:].rpartition('/'); an = int(an or 300)
        for m in re.finditer(pat, r):
            donde = [n for p, n in cons if p <= m.start()]
            print(f'--- /{pat}/ @{m.start()} (cons. {donde[-1] if donde else "-"}):', limpio(max(0, m.start()-an), m.end()+an)); print()
        continue
    et, _, mx = a.partition(':'); mx = int(mx or 100000)
    if et == 'pt': s = limpio(pt[-1], len(r))
    elif et[0] == 'r':
        k = [i for i, (p, n) in enumerate(res) if n == et[1:] and p < tope_res][0]; s = limpio(res[k][0], fin(res, k, tope_res))
    else:
        ks = [i for i, (p, n) in enumerate(cons) if n == et[1:] and p >= (ci[0] if ci else 0)]
        k = ks[-1] if et.endswith('!') else ks[0]; s = limpio(cons[k][0], fin(cons, k, tope_con))
    print(f'=== {v} {et} ({len(s)}) ==='); print(s[:mx] if mx > 0 else s[mx:]); print()
