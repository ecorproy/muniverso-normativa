# ver.py ANCHO MAX VOTO PATRÓN [PATRÓN...]  : hasta MAX coincidencias de cada patrón con su contexto y posición (votos de la Sala, subcarpetas incluidas)
import re, sys, glob
R = '/home/claude/repo/main/Jurisprudencia constitucional (Sala Constitucional)/Municipal'
LOC = '/home/claude/libro/fuentes/votos'
w = int(sys.argv[1]); mx = int(sys.argv[2]); v = sys.argv[3]; pats = sys.argv[4:]
fs = glob.glob(f'{LOC}/Sentencia {v}.md') + glob.glob(f'{R}/Sentencia {v}.md') + glob.glob(f'{R}/*/Sentencia {v}.md')
if not fs: print('NO ESTÁ', v); sys.exit()
raw = open(fs[0], encoding='utf-8').read()
heads = [(m.start(), m.group(1)) for m in re.finditer(r'(?m)^\W{0,6}([IVXL]{1,7})\)?\s*\.?\s*[-–—.]+\s*\S', raw)]
pt = [m.start() for m in re.finditer(r'(?im)^\W{0,6}por tanto\s*:?', raw)]
print(f'##### {v} ({len(raw)} car.; por tanto en {pt[-1] if pt else "?"})')
for p in pats:
    ms = list(re.finditer(p, raw, re.I))
    print(f'  [{p}] {len(ms)} coincidencia(s)')
    for m in ms[:mx]:
        lab = [h for pos, h in heads if pos <= m.start()]
        zona = 'POR TANTO' if pt and m.start() >= pt[-1] else (lab[-1] if lab else 'antes del I')
        print(f'    @{m.start()} {zona}: …' + re.sub(r'\s+', ' ', raw[max(0, m.start() - w):m.end() + w]) + '…')
