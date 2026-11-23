# hbloques.py SALIDA_DEL_VERIFICADOR.md H1 H2 ...: compara el resumen de cada bloque esperado con el «h» que dan los acuses
# del documento (h = primeros 8 hexadecimales del sha256 del texto del bloque). Sirve para ubicar un párrafo alterado.
import sys, hashlib
t = open(sys.argv[1], encoding='utf-8').read()
blocks = [b.strip('\n') for b in t.split('\n\n') if b.strip()]
hs = sys.argv[2:]
for i, b in enumerate(blocks):
    s = b.lstrip('#').lstrip(' ')
    d = hashlib.sha256(s.encode()).hexdigest()[:8]
    e = hs[i] if i < len(hs) else '-'
    print(i, 'OK ' if d == e else 'XX ', d, e, repr(s[:50]))
