# Artículos de las leyes del inventario que nombran al gobierno municipal con otra palabra
# (municipio, gobierno local, alcalde/alcaldía, ayuntamiento, ente o corporación local) y no están en el inventario.
import re, glob
inv = open('/home/claude/repo/360/Seguridad Municipal 360°/Inventario de artículos que nombran a las municipalidades.md', encoding='utf-8').read()
normas = {}
for s in re.split(r'\n### ', inv)[1:]:
    head = s.split('\n', 1)[0]
    normas[head] = set(a.strip() for a in re.findall(r'\*\*Art\. ([^:*]+):\*\*', s))
ART = re.compile(r'(?im)^\W{0,6}(?:ART[IÍ]CULO|Art[ií]culo|Articulo)\s+(\d+)(?:\s*(bis|ter))?\s*[º°o]?\s*[\.\-—–:]')
TERM = {'municipio': r'municipio', 'gobierno local': r'gobiernos?\s+local', 'alcalde o alcaldía': r'\balcald', 'ayuntamiento': r'ayuntamiento', 'ente o corporación local': r'(?:entes?|corporaci[oó]n(?:es)?)\s+local'}
base = '/home/claude/repo/main/Leyes y decretos nacionales'
res = {k: [] for k in TERM}; todos = set(); rev = 0; con_mun_fuera = 0
for head, arts in normas.items():
    m = re.match(r'Ley N\.° (\d+)\.', head)
    if not m: continue
    n = m.group(1)
    fs = glob.glob(f'{base}/*/Ley {n}.md') + glob.glob(f'{base}/*/Ley {n}.md.md')
    if not fs: continue
    rev += 1
    raw = re.sub(r'(?s)^---.*?---', '', open(fs[0], encoding='utf-8').read(), count=1)
    ms = list(ART.finditer(raw)); seen = set()
    for i, mm in enumerate(ms):
        k = mm.group(1) + (' ' + mm.group(2).lower() if mm.group(2) else '')
        if k in seen: continue
        seen.add(k)
        txt = raw[mm.start():(ms[i+1].start() if i+1 < len(ms) else len(raw))]
        if k in arts: continue
        if re.search(r'municipal', txt, re.I): con_mun_fuera += 1; continue
        for name, rx in TERM.items():
            if re.search(rx, txt, re.I): res[name].append((n, k)); todos.add((n, k))
print('leyes revisadas:', rev)
print('artículos con «municipal…» que NO están en el inventario (control):', con_mun_fuera)
for name, v in res.items(): print(f'  {name}: {len(v)} artículos en {len(set(x[0] for x in v))} leyes', v[:10])
print('total sin repetir:', len(todos), 'artículos en', len(set(x[0] for x in todos)), 'leyes')
