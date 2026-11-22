# arts.py LEY_NUM|CP art [art...]  -> texto literal de los artículos (segmentador de build.py). L=longitud máx.
import sys, re, os
os.environ['SRC'] = '/nonexistent'; os.environ['OUT'] = '/tmp'
code = open('/home/claude/scripts/build.py', encoding='utf-8').read()
code = re.sub(r'\nmain\(\)\s*$', '\n', code)
ns = {}; exec(compile(code, 'build.py', 'exec'), ns)
L = int(os.environ.get('L', '1200'))
n = sys.argv[1]
f = ns['F_CP'] if n == 'CP' else ns['f_ley'](n)
if not f: print('NO ESTÁ la ley', n); sys.exit()
raw = open(f, encoding='utf-8').read()
d = ns['meta'](f)
print('##', os.path.basename(f), '|', d.get('nombre', ''), '|', d.get('fecha_norma', '') or d.get('fecha', ''))
ms = list(ns['ART_RE'].finditer(raw))
for a in sys.argv[2:]:
    hit = [i for i, m in enumerate(ms) if (m.group(1) + (' ' + m.group(2) if m.group(2) else '')) == a]
    if not hit: print(f'  art {a}: NO HALLADO'); continue
    for i in hit[:2]:
        s = raw[ms[i].start(): ms[i + 1].start() if i + 1 < len(ms) else ms[i].start() + 4000]
        s = re.sub(r'\s+', ' ', s).strip()
        print(f'  art {a}: ' + s[:L] + ('…' if len(s) > L else ''))
