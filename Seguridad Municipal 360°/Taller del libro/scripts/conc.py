import re,glob,sys
P='/home/claude/repo/main/Jurisprudencia administrativa (PGR)/'
ancho=int(sys.argv[1])
for n in sys.argv[2:]:
    fs=glob.glob(P+'**/*%s.md'%n,recursive=True)
    if not fs: print('NO',n); continue
    h=re.sub(r'\s+',' ',open(fs[0],encoding='utf-8').read())
    md={k:(re.search(k+r': "([^"]*)"',h).group(1) if re.search(k+r': "([^"]*)"',h) else '') for k in ['fecha','consultante','institucion','materia','temas']}
    print('=====',n,'|',md['fecha'],'|',md['institucion'],'|',md['materia'],'|',md['temas'])
    i=max(h.rfind('CONCLUSI'),h.rfind('Conclusi'))
    print(h[i:i+ancho] if i>0 else '[sin conclusiones] '+h[-ancho:]); print()
