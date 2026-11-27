# q.py ley NUM patrón  |  q.py pgr patrón [carpeta]  |  q.py art NUM ART
import sys,re,glob
R='/home/claude/repo/main'
def ley(n):
    fs=glob.glob(f'{R}/Leyes y decretos nacionales/*/Ley {n}.md')+glob.glob(f'{R}/Leyes y decretos nacionales/*/Ley {n}.md.md')+glob.glob(f'/home/claude/libro/fuentes/Ley {n}.md')
    return fs[0] if fs else None
def arts(t):
    parts=re.split(r'(?mi)^(?=\*\*\s*Art[íi]culo\s+\d+)',t)
    for p in parts:
        m=re.match(r'(?i)\**\s*Art[íi]culo\s+(\d+\s*(?:bis|ter)?)',p)
        yield (m.group(1) if m else '-'),p
mode=sys.argv[1]
if mode=='ley':
    f=ley(sys.argv[2]); print(f); t=open(f,encoding='utf-8').read()
    for a,p in arts(t):
        for m in re.finditer(sys.argv[3],p,re.I):
            s=re.sub(r'\s+',' ',p[max(0,m.start()-250):m.end()+300]); print(f'art {a}: …{s}…\n'); break
elif mode=='art':
    f=ley(sys.argv[2]); t=open(f,encoding='utf-8').read()
    for a,p in arts(t):
        if a.strip()==sys.argv[3]: print(re.sub(r'[ \t]+',' ',p[:int(sys.argv[4]) if len(sys.argv)>4 else 2500]))
elif mode=='pgr':
    carp=sys.argv[3] if len(sys.argv)>3 else '*'
    for f in sorted(glob.glob(f'{R}/Jurisprudencia administrativa (PGR)/{carp}/*.md')):
        t=open(f,encoding='utf-8').read()
        m=re.search(sys.argv[2],t,re.I)
        if m: print(f.split('/')[-1], '|', re.sub(r'\s+',' ',t[max(0,m.start()-150):m.end()+200]))
