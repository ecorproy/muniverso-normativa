# heads.py ARCHIVO [desde] [hasta]: encabezados de considerando (romanos) con posición, en todo el archivo
import re, sys
raw = open(sys.argv[1], encoding='utf-8').read()
a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
b = int(sys.argv[3]) if len(sys.argv) > 3 else len(raw)
for m in re.finditer(r'(?im)^\W{0,6}(resultando|considerando|por tanto)\s*:?\s*$', raw):
    print(f'{m.start():>7} ### {m.group(1).upper()}')
for m in re.finditer(r'(?m)^\W{0,6}([IVXL]{1,7})\)?\s*\.?\s*[-–—.]+\s*\S', raw):
    if a <= m.start() <= b:
        print(f'{m.start():>7} {m.group(1):>7} | ' + re.sub(r'\s+', ' ', raw[m.start():m.start()+int(sys.argv[4]) if len(sys.argv) > 4 else m.start()+120]))
