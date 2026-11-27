import shutil, re, sys, unicodedata
R='/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
L='/home/claude/libro'
NUEVAS=('Programa Estado de la Nación. (2026)','Observatorio de la Violencia. (2026)','Ministerio de Planificación Nacional y Política Económica. (2025)','Decreto Ejecutivo N.° 22266')
def clave(r):
    r=re.sub(r'[*_]','',r); r=unicodedata.normalize('NFD',r)
    return ''.join(ch for ch in r if unicodedata.category(ch)!='Mn').lower()
for c in sys.argv[1:]:
    o=f'{R}/{c}/out'; u=open(f'{o}/unido.md',encoding='utf-8').read()
    viejo=open(f'{o}/{c}.md',encoding='utf-8').read()
    body,sep,refs=u.partition('\n## Referencias\n')
    nuevo=open(f'{L}/{c}/chk_X/{c}.md',encoding='utf-8').read()
    if body.rstrip()!=viejo.rstrip():
        bl=body.split('\n'); vl=viejo.split('\n')
        extra=[x for x in bl[:6] if x not in vl and x.strip()]
        assert len(extra)==1 and '\n'.join(x for x in bl if x!=extra[0]).replace('\n\n\n','\n\n').rstrip()==viejo.rstrip(), c
        k=bl.index(extra[0]); nl=nuevo.split('\n'); nuevo='\n'.join(nl[:k]+[extra[0],'']+nl[k:])
    lista=[x for x in refs.strip().split('\n\n') if x.strip()]
    zz=[x for x in open(f'{L}/{c}/chk_X/zz_referencias.md',encoding='utf-8').read().split('\n\n') if x.startswith(NUEVAS)]
    zzall=open(f'{L}/{c}/chk_X/zz_referencias.md',encoding='utf-8').read()
    lista=[x for x in lista if not (x.startswith(NUEVAS) and x[:60] not in zzall)]
    for z in zz:
        if not any(x.startswith(z[:60]) for x in lista):
            pos=next((i for i,x in enumerate(lista) if clave(x)>clave(z)),len(lista))
            lista.insert(pos,z.strip())
    open(f'{o}/unido.md','w',encoding='utf-8').write(nuevo.rstrip()+'\n\n## Referencias\n\n'+'\n\n'.join(lista)+'\n')
    for f in [f'{c}.md','zz_citas.json','zz_informe.txt','zz_referencias.md']:
        shutil.copy(f'{L}/{c}/chk_X/{f}',f'{o}/{f}')
    shutil.copy(f'{L}/{c}/src/{c}.md',f'{R}/{c}/src/{c}.md')
    print(c,'ok',len(zz))
