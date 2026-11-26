# ctx.py tNN "frag1" "frag2"...: muestra la oración previa, la que contiene y la siguiente (con macros)
import re,sys,glob,os
R='/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
n=sys.argv[1]; d=f'/home/claude/art/{n}/src' if os.path.isdir(f'/home/claude/art/{n}/src') else f'{R}/{n}/src'
t=open(glob.glob(f'{d}/*.md')[0],encoding='utf-8').read()
for f in sys.argv[2:]:
    i=t.find(f)
    if i<0: print('NO:',f); continue
    a=max(t.rfind('. ',0,max(0,t.rfind('. ',0,i))),t.rfind('\n',0,i)); b=t.find('. ',i+len(f)); b=t.find('. ',b+2) if b>0 else -1
    print('»',t[a+1:(b if b>0 else i+500)+1].strip()[:900]); print('---')
