# esperado.py SALIDA_DEL_VERIFICADOR.md SHA256 BYTES
# Convierte el texto expandido por build_libro.py a la forma de la exportación en markdown (corchetes escapados)
# y lo compara con el sha256 y el tamaño del blob del documento.
import sys, hashlib
t = open(sys.argv[1], encoding='utf-8').read()
e = t.replace('[', '\\[').replace(']', '\\]')
b = e.encode('utf-8'); h = hashlib.sha256(b).hexdigest()
open(sys.argv[1].replace('.md', '') + '_esperado.md', 'wb').write(b)
print('bytes esperados:', len(b), '| bytes documento:', sys.argv[3], '| diferencia:', len(b) - int(sys.argv[3]))
print('sha256 esperado :', h); print('sha256 documento:', sys.argv[2]); print('IDÉNTICO' if h == sys.argv[2] else 'DISTINTO')
