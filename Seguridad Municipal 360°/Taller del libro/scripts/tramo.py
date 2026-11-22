# tramo.py ARCHIVO DESDE HASTA: imprime el tramo [DESDE, HASTA) del archivo, con espacios normalizados
import re, sys
raw = open(sys.argv[1], encoding='utf-8').read()
print(re.sub(r'\s+', ' ', raw[int(sys.argv[2]):int(sys.argv[3])]))
