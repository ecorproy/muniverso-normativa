# espejo.py PLANTILLA SALIDA SHA256 BYTES BANCO.md [BANCO2.md ...]
# Arma el espejo local de una pestaña: la prosa viene de la plantilla y cada cita textual marcada {{Q:inicio}}
# se toma del banco ya cotejado. Compara tamaño y sha256 con los del blob exportado del documento.
import re, sys, hashlib
tpl, out, sha, nbytes = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
quotes = []
for b in sys.argv[5:]:
    for line in open(b, encoding='utf-8'):
        m = re.match(r'^"(.+)" (?:\[\[|\()', line)
        if m and m.group(1) not in quotes:
            quotes.append(m.group(1))
t = open(tpl, encoding='utf-8').read()
bad = []
def rep(m):
    pre = m.group(1)
    c = [q for q in quotes if q.startswith(pre)]
    if len(c) != 1:
        bad.append((pre, len(c))); return m.group(0)
    return c[0]
t2 = re.sub(r'\{\{Q:(.+?)\}\}', rep, t)
if bad: print('MARCAS SIN RESOLVER:', bad); sys.exit(1)
b = t2.encode('utf-8')
open(out, 'wb').write(b)
h = hashlib.sha256(b).hexdigest()
print('marcas:', len(re.findall(r'\{\{Q:', t)), '| bytes espejo:', len(b), '| bytes documento:', nbytes, '| diferencia:', len(b) - nbytes)
print('sha256 espejo   :', h); print('sha256 documento:', sha); print('IDÉNTICO' if h == sha else 'DISTINTO')
