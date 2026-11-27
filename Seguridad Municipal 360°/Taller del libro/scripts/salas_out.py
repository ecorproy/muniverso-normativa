import sys,os
R=sys.argv[1]
P={'cap02':[(". La Sala admitió que la infraestructura",". La Sala Primera admitió que la infraestructura"),(". La Sala rechazó ese argumento",". La Sala Primera rechazó ese argumento"),(", y la Sala ordenó devolver",", y la Sala Primera ordenó devolver"),("que la Sala describió en 1999","que la Sala Constitucional describió en 1999"),("criterio que la Sala admitió para que una ley la traslade","criterio que la Sala Constitucional admitió para que una ley la traslade")],
'cap03':[("que la Sala o el Tribunal consideraron correctas","que la Sala Constitucional, la Sala Primera o el Tribunal consideraron correctas")],
'cap04':[("de los habitantes. La Sala lo dijo al describir","de los habitantes. La Sala Constitucional lo dijo al describir"),("Ese mismo año la Sala aplicó","Ese mismo año la Sala Primera aplicó"),(". La Sala distinguió dos formas",". La Sala Primera distinguió dos formas"),("la línea de la Sala sobre el buen funcionamiento","la línea de la Sala Constitucional sobre el buen funcionamiento")],
't13':[("recibir. La Sala lo fijó en un caso","recibir. La Sala Constitucional lo fijó en un caso")],
't16':[("La Sala precisó el contenido de esa garantía","La Sala Constitucional precisó el contenido de esa garantía")],
't29':[("Si la Sala midió","Si la Sala Constitucional midió"),("Si la Sala condenó sin esa ley","Si la Sala Constitucional condenó sin esa ley")]}
for c,L in P.items():
    d=f'{R}/{c}/out'
    for f in sorted(os.listdir(d)):
        if not f.endswith('.md') or f.startswith('zz'): continue
        p=f'{d}/{f}'; t=open(p,encoding='utf-8').read(); n=[t.count(a) for a,b in L]
        if sum(n)==0: continue
        for a,b in L: t=t.replace(a,b)
        open(p,'w',encoding='utf-8').write(t); print(c,f,n)
