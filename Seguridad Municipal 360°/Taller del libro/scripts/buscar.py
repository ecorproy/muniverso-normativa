# Busca patrones en un texto paginado (\f) y muestra fragmentos cortos con su página.
# Uso: python3 -I buscar.py ARCHIVO ANTES DESPUES MAXHITS PATRON [DESDE HASTA]
import sys, re
f, antes, desp, mx, pat = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
a = int(sys.argv[6]) if len(sys.argv) > 6 else 1
b = int(sys.argv[7]) if len(sys.argv) > 7 else 10**9
t = open(f, encoding='utf-8').read().split('\f')
rx = re.compile(pat, re.I)
n = 0
for i, p in enumerate(t, 1):
    if i < a or i > b: continue
    q = re.sub(r'\s+', ' ', p)
    last = -10**9
    for m in rx.finditer(q):
        if m.start() - last < antes + desp: continue
        last = m.start()
        s = max(0, m.start() - antes); e = min(len(q), m.end() + desp)
        print(f'[p.{i}] …{q[s:e]}…\n')
        n += 1
        if n >= mx: sys.exit()
