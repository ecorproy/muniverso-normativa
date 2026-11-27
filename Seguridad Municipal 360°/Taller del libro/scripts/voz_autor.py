"""Voz del autor (cap. 3): convención para distinguir lo propio de lo ajeno y contraste con otras construcciones doctrinales."""
f='/home/claude/libro/cap03/src/cap03.md'; s=open(f,encoding='utf-8').read()
a='La cuarta se presenta como propuesta, y es buena parte del aporte del libro.'
b=a+' Para que la voz del autor no se confunda con la de sus fuentes, cada tema abre con su tesis, introducida con la fórmula *Este libro sostiene*, y las lecturas y propuestas propias se reconocen por esa misma voz: el libro sostiene, el libro propone. Lo que dicen la Sala, la Procuraduría, el legislador o un autor va siempre con su nombre y su cita.'
if b not in s:
    assert s.count(a)==1; s=s.replace(a,b)
sec='''## La definición frente a otras construcciones

La definición de este libro no es la primera respuesta a la pregunta de qué es lo local, y su novedad solo se aprecia frente a las anteriores. Hay cinco con las que conviene medirla.

La primera es la de Eduardo Ortiz Ortiz, que leyó por separado las dos palabras del artículo 169. Los servicios son la actividad municipal dirigida a satisfacer una necesidad de la colectividad, y los intereses, cualesquiera otros fines de igual alcance que se logran por medios distintos del servicio público (Ortiz Ortiz, 1987, como se citó en Leiva Poveda, 2016, p. 3). Su criterio es el objeto: qué clase de actividad es. Este libro conserva la distinción y cambia el punto de mira: no pregunta primero qué clase de actividad es, sino a quién le importa y si le llega.

La segunda es la de Ernesto Jinesta Lobo, para quien las municipalidades son entes territoriales de fin general, a los que corresponde cualquier interés o servicio que tenga la connotación de local (Jinesta Lobo, 2002, como se citó en Leiva Poveda, 2016, pp. 3-4). Su criterio es la naturaleza del ente. Explica por qué la competencia es genérica, pero no dice cuándo se cumple. Este libro agrega esa medida: la competencia se cumple cuando el servicio llega a la persona.

La tercera es la de Jorge Leiva Poveda, que rechazó una definición general para todas las municipalidades y propuso tratar lo local como concepto jurídico indeterminado, con su núcleo, su halo y su zona negativa (Leiva Poveda, 2016, pp. 9-11). Su criterio es la técnica de determinación. Este libro la adopta entera y se separa de ella en un punto: sí propone una definición, pero hecha de criterios y no de materias, de modo que no fija en el tiempo los ámbitos de acción ni toma como modelo a una municipalidad determinada.

La cuarta es la de la Sala Constitucional, que definió el interés local como lo que importa al cantón de manera directa e inmediata [[V:2006-017907:considerando III]]. Su criterio es la intensidad del interés. Este libro conserva la intensidad y cambia el sujeto: lo que importa es a las personas que habitan el cantón o se encuentran en él. La sección siguiente muestra qué cambia con ello.

La quinta es la lectura histórica de Ronald Alfaro Redondo, según la cual las instituciones autónomas creadas después de 1949 dejaron a las municipalidades con funciones residuales (Alfaro Redondo, 2009/2025, p. 10). Su criterio es la distribución efectiva de funciones. Este libro parte del mismo diagnóstico, pero lee lo local como una reserva constitucional y no como un residuo: lo que la ley no ha trasladado sigue siendo deber municipal.

Ninguna de esas construcciones mide el cumplimiento por lo que recibe la persona, ni ordena el ámbito de lo local en temas examinados con una misma pregunta. Ese es el aporte que este libro reclama frente a la doctrina costarricense. La comparación con el derecho local de otros países excede este libro.'''
anc='## Tres casos difíciles y un límite'
if '## La definición frente a otras construcciones' not in s:
    assert s.count(anc)==1; s=s.replace(anc,sec+'\n\n'+anc)
open(f,'w',encoding='utf-8').write(s); print('ok')
