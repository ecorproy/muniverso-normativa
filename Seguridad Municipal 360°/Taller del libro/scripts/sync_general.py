"""Sincroniza src, out y unido de los capítulos indicados con su construcción chk_X.
El unido conserva sus referencias (con URL) y agrega las que falten en el orden de zz_referencias."""
import sys, shutil, os
R='/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos/'
L='/home/claude/libro/'
for c in sys.argv[1:]:
    arch='all.md' if c=='cap02' else c+'.md'
    os.makedirs(R+c+'/out',exist_ok=True); os.makedirs(R+c+'/src',exist_ok=True)
    nuevo=open(L+c+'/chk_X/'+arch,encoding='utf-8').read().split('\n## Referencias')[0].rstrip()
    zz=[x.strip() for x in open(L+c+'/chk_X/zz_referencias.md',encoding='utf-8').read().split('\n\n') if x.strip() and not x.startswith('#')]
    lista=[]
    if os.path.exists(R+c+'/out/unido.md'):
        u=open(R+c+'/out/unido.md',encoding='utf-8').read()
        body,_,refs=u.partition('\n## Referencias\n')
        lista=[x.strip() for x in refs.strip().split('\n\n') if x.strip()]
        nl=nuevo.split('\n'); bl=body.split('\n')
        extra=[x for x in bl[:6] if x.strip() and x not in nl and not x.startswith('#')]
        if extra: nuevo='\n'.join(nl[:2]+[extra[0],'']+nl[2:])
    for k,z in enumerate(zz):
        if any(x.startswith(z[:70]) for x in lista): continue
        prev=[zz[j] for j in range(k-1,-1,-1) if any(x.startswith(zz[j][:70]) for x in lista)]
        pos=0 if not prev else [i for i,x in enumerate(lista) if x.startswith(prev[0][:70])][0]+1
        lista.insert(pos,z)
    open(R+c+'/out/unido.md','w',encoding='utf-8').write(nuevo+'\n\n## Referencias\n\n'+'\n\n'.join(lista)+'\n')
    for f in [arch,'zz_citas.json','zz_informe.txt','zz_referencias.md']: shutil.copy(L+c+'/chk_X/'+f,R+c+'/out/'+f)
    shutil.copy(L+c+'/src/'+arch,R+c+'/src/'+arch)
    print(c,'ok')
