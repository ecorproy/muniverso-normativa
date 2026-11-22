# Mide cuántos artículos de las normas del inventario dicen «municipio(s)» sin decir «municipal…»,
# que es el término con que parece haberse armado el inventario.
import re, glob, os, sys
inv = open('/home/claude/repo/360/Seguridad Municipal 360°/Inventario de artículos que nombran a las municipalidades.md', encoding='utf-8').read()
secs = re.split(r'\n### ', inv)[1:]
normas = {}
for s in secs:
    m = re.match(r'(Ley|Decreto Ejecutivo|Constitución[^\n]*|[^\n.]+?) N\.° (\d+)\.', s)
    head = s.split('\n', 1)[0]
    arts = re.findall(r'\*\*Art\. ([^:*]+):\*\*', s)
    normas[head] = arts
print('normas en el inventario:', len(normas), '| artículos:', sum(len(v) for v in normas.values()))
ART = re.compile(r'(?im)^\W{0,6}(?:ART[IÍ]CULO|Art[ií]culo|Articulo)\s+(\d+)(?:\s*(bis|ter))?\s*[º°o]?\s*[\.\-—–:]')
base = '/home/claude/repo/main/Leyes y decretos nacionales'
tot_extra = 0; ej = []; leyes_con = 0; revisadas = 0
for head, arts in normas.items():
    m = re.match(r'Ley N\.° (\d+)\.', head)
    if not m: continue
    n = m.group(1)
    fs = glob.glob(f'{base}/*/Ley {n}.md') + glob.glob(f'{base}/*/Ley {n}.md.md')
    if not fs: continue
    revisadas += 1
    raw = open(fs[0], encoding='utf-8').read()
    raw = re.sub(r'(?s)^---.*?---', '', raw, count=1)
    ms = list(ART.finditer(raw)); seen = set(); extra = []
    for i, mm in enumerate(ms):
        end = ms[i+1].start() if i+1 < len(ms) else len(raw)
        k = mm.group(1) + (' ' + mm.group(2).lower() if mm.group(2) else '')
        if k in seen: continue
        seen.add(k)
        txt = raw[mm.start():end]
        if re.search(r'municipio', txt, re.I) and not re.search(r'municipal', txt, re.I) and k not in arts:
            extra.append(k)
    if extra:
        leyes_con += 1; tot_extra += len(extra)
        if len(ej) < 14: ej.append((n, head[:55], extra[:8]))
print('leyes del inventario revisadas contra su texto:', revisadas)
print('artículos que dicen «municipio(s)» sin «municipal…» y no están en el inventario:', tot_extra, 'en', leyes_con, 'leyes')
for e in ej: print('  ', e)
