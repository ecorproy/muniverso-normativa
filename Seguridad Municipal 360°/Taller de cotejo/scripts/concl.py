import re,sys,glob,os
L=int(os.environ.get('L','1300'))
R='/home/claude/repo/main/Jurisprudencia administrativa (PGR)'
for d in sys.argv[1:]:
    fs=glob.glob(f'{R}/*/Dictamen {d}.md')
    if not fs: print(f'## {d}: NO ESTÁ'); continue
    t=open(fs[0],encoding='utf-8').read()
    g=lambda k:(re.search(r'(?m)^'+k+r':\s*"([^"]*)"',t) or [None,''])[1]
    i=[m.start() for m in re.finditer(r'(?i)\n[^\n]{0,25}conclusi[oó]n',t)]
    s=t[i[-1]:] if i else t[-L:]
    print(f'## {d} | {g("fecha")} | {g("institucion")}\n'+re.sub(r'\s+',' ',s)[:L]+'\n')
