import sys
B='/home/claude/libro/'
E={'cap02/src/all.md':[
 ("[[S1:2015-000164:considerando I]]. La Sala admitió que","[[S1:2015-000164:considerando I]]. La Sala Primera admitió que"),
 ("]]. La Sala rechazó ese argumento","]]. La Sala Primera rechazó ese argumento"),
 (", y la Sala ordenó devolver",", y la Sala Primera ordenó devolver"),
 ("que la Sala describió en 1999","que la Sala Constitucional describió en 1999"),
 ("pero es el criterio que la Sala admitió para que una ley la traslade.","pero es el criterio que la Sala Constitucional admitió para que una ley la traslade.")],
'cap03/src/cap03.md':[("que la Sala o el Tribunal consideraron correctas","que la Sala Constitucional, la Sala Primera o el Tribunal consideraron correctas")],
'cap04/src/cap04.md':[
 ("de los habitantes. La Sala lo dijo al describir","de los habitantes. La Sala Constitucional lo dijo al describir"),
 ("Ese mismo año la Sala aplicó","Ese mismo año la Sala Primera aplicó"),
 ("]]. La Sala distinguió dos formas","]]. La Sala Primera distinguió dos formas"),
 ("la línea de la Sala sobre el buen funcionamiento","la línea de la Sala Constitucional sobre el buen funcionamiento")],
't13/src/t13.md':[("recibir. La Sala lo fijó en un caso","recibir. La Sala Constitucional lo fijó en un caso")],
't16/src/t16.md':[("la justifique.\n\nLa Sala precisó","la justifique.\n\nLa Sala Constitucional precisó")],
't29/src/t29.md':[("Si la Sala midió","Si la Sala Constitucional midió"),("Si la Sala condenó sin esa ley","Si la Sala Constitucional condenó sin esa ley")]}
for f,L in E.items():
    t=open(B+f,encoding='utf-8').read()
    for a,b in L:
        assert t.count(a)==1,(f,a); t=t.replace(a,b)
    open(B+f,'w',encoding='utf-8').write(t); print('ok',f,len(L))
