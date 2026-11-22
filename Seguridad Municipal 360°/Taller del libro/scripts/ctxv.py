# ctxv.py ANCHO VOTO PATRÓN [PATRÓN...]  (varios grupos separados por «--»): contexto de cada patrón con el considerando en que cae
import re, sys, glob
R = '/home/claude/repo/main/Jurisprudencia constitucional (Sala Constitucional)/Municipal'
w = int(sys.argv[1]); args = sys.argv[2:]
groups = []; cur = []
for a in args:
    if a == '--':
        groups.append(cur); cur = []
    else: cur.append(a)
groups.append(cur)
for g in groups:
    v, pats = g[0], g[1:]
    fs = glob.glob(f'{R}/Sentencia {v}.md') + glob.glob(f'{R}/*/Sentencia {v}.md')
    if not fs: print(f'##### {v}: NO ESTÁ'); continue
    raw = open(fs[0], encoding='utf-8').read()
    heads = [(m.start(), m.group(1)) for m in re.finditer(r'(?m)^\W{0,6}([IVXL]{1,7})\)?\s*\.?\s*[-–—.]+\s*\S', raw)]
    pt = [m.start() for m in re.finditer(r'(?im)^\W{0,6}por tanto\s*:?', raw)]
    print(f'##### {v} ({len(raw.split())} pal.; por tanto en {pt[-1] if pt else "?"})')
    for p in pats:
        ms = list(re.finditer(p, raw, re.I))
        if not ms: print(f'  [{p}] SIN COINCIDENCIA'); continue
        m = ms[0]
        lab = [h for pos, h in heads if pos <= m.start()]
        zona = 'POR TANTO' if pt and m.start() >= pt[-1] else (lab[-1] if lab else 'antes del I')
        print(f'  [{p}] {len(ms)} vez/veces; cons. {zona}: …' + re.sub(r'\s+', ' ', raw[max(0, m.start() - w):m.end() + w]) + '…')
