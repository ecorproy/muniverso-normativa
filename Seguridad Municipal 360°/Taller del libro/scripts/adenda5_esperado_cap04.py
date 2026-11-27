import sys
base='/home/claude/libro/cap04/'
c=open(base+'chk/cap04.md',encoding='utf-8').read()
c=c.replace('(Sala Constitucional, voto N.° 2025-008201, considerando IV)','(Sala Constitucional, voto N.° 2025-008201, de las 13:00 horas del 17 de marzo de 2025, considerando IV)')
assert 'de las 13:00 horas del 17 de marzo de 2025' in c
rout=open(base+'out/zz_referencias.md',encoding='utf-8').read().split('\n\n')
rchk=open(base+'chk/zz_referencias.md',encoding='utf-8').read().split('\n\n')
v=[x for x in rout if 'Voto N.° 2025-008201' in x][0]
prev=rout[rout.index(v)-1]; assert prev in rchk
rchk.insert(rchk.index(prev)+1,v)
r='\n\n'.join(rchk)
l=c.split('\n',1)
u=l[0]+'\n\nNov 26, 2026 · @Edward Cortés García\n'+l[1]+'\n'+r
open(base+'nuevo_unido.md','w',encoding='utf-8').write(u)
# comprobar contra la salida publicada: lo que no cambió debe seguir idéntico
print(len(u))
