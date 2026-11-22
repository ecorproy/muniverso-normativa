# pas.py FILE REGEX [REGEX...]  -> pasajes alrededor de cada coincidencia, con considerando
import re,sys,os
N=int(os.environ.get('N','260')); K=int(os.environ.get('K','2'))
f=sys.argv[1]; pats=sys.argv[2:]
raw=open(f,encoding='utf-8').read()
# reparar tildes separadas ("planificaci ó n") solo para mostrar
def fix(t):
    t=re.sub(r'(?<=\w) ([áéíóúñüÁÉÍÓÚÑÜ]) (?=\w)',r'\1',t)
    t=re.sub(r'(?<=\w) ([áéíóú])(?=[\s,.;:)])',r'\1',t)
    return t
heads=[(m.start(),m.group(1)) for m in re.finditer(r'(?m)^\W{0,6}([IVXL]{1,7})\)?\s*\.?\s*[-–—.]+\s*\S',raw)]
body=raw.find('Texto de la resoluci')
print(f'## {os.path.basename(f)}')
for p in pats:
    ms=[m for m in re.finditer(p,raw,re.I|re.S)]
    ms2=[m for m in ms if m.start()>=body] or ms
    print(f'-- /{p}/ {len(ms)} coincidencias ({len(ms2)} en el cuerpo)')
    for m in ms2[:K]:
        h=[x for x in heads if x[0]<=m.start()]
        cons=h[-1][1] if h else '?'
        s=raw[max(0,m.start()-N):m.end()+N]
        print(f'   [cons {cons}] …'+fix(re.sub(r'\s+',' ',s))+'…')
