import re,sys,glob
v=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 300
f=glob.glob(f'/home/claude/repo/main/Jurisprudencia constitucional (Sala Constitucional)/**/Sentencia {v}.md',recursive=True)[0]
x=re.sub(r'\s+',' ',open(f,encoding='utf-8').read())
for m in re.finditer(r' ((?:[IVXL]+)\.?-|Resultando:|RESULTANDO:|Considerando:|CONSIDERANDO:|Por tanto:?|POR TANTO:?)',x):
    print(m.start(), x[m.start():m.start()+n].strip()); print()
