"""Cierre de la conclusión: quiénes son las personas del cantón (cap. 3 y conclusión),
respuesta a Leiva, voto del Tempisque, vuelta a la pregunta de 2016, agenda con
destinatarios, y traslado del ICDS de la conclusión al tema 36."""
B = '/home/claude/libro'


def rd(c):
    return open(f'{B}/{c}/src/{c}.md', encoding='utf-8').read()


def wr(c, s):
    open(f'{B}/{c}/src/{c}.md', 'w', encoding='utf-8').write(s)


def rep(s, old, new):
    assert s.count(old) == 1, old[:70]
    return s.replace(old, new)


VIVEN = 'a las personas que viven en un cantón'
HABITAN = 'a las personas que habitan un cantón o se encuentran en él'

# capítulo 3
s = rd('cap03')
s = rep(s, 'importa de manera directa e inmediata ' + VIVEN + '.', 'importa de manera directa e inmediata ' + HABITAN + '.')
s = rep(s, 'Si lo local se define por lo que importa a las personas que viven en el cantón,',
        'Si lo local se define por lo que importa a las personas que habitan el cantón o se encuentran en él,')
ancla = 'se llama el estado civil" (Kant, 1797/1873, p. 163).'
nuevo = ('Las personas del cantón no son solo las que residen en él. El artículo 1 del Código define por la vecindad y la residencia al municipio, que es la comunidad política que elige y que la municipalidad convoca. La Constitución, en cambio, encarga al Gobierno Municipal los intereses y servicios locales "en cada cantón" [[CP:art. 169]], es decir, en un territorio, y la ley ya atiende a quien está en él sin residir. Desde 2021, el Código cuenta entre las atribuciones municipales la de "Crear los albergues necesarios para la atención de personas en situación de abandono y situación de calle" [[L:7794:art. 4, inciso j]]. El artículo 71 dirige las ayudas temporales a los "vecinos y vecinas del cantón" [[L:7794:art. 71]], y los albergues a "las personas que se encuentren en situación de abandono y situación de calle" [[L:7794:art. 71]]. '
         'Falta una definición legal de quién habita un cantón, y el reglamento de la Defensoría de los Habitantes ofrece una por analogía. Para sus efectos, habitantes son "Todas las personas físicas o jurídicas domiciliadas o que se encuentren, en forma permanente o transitoria, en el territorio nacional" [[DE:22266:art. 2]]. Llevada al cantón, esa noción alcanza al residente, a quien trabaja o estudia en él, a quien lo atraviesa y a quien vive en sus calles. El municipio lo forman los vecinos residentes; los servicios locales llegan a todo el que está en el cantón.')
if 'Las personas del cantón no son solo' not in s:
    s = rep(s, ancla, ancla + '\n\n' + nuevo)
wr('cap03', s)

# tema 36: recibe el ICDS que sale de la conclusión
s = rd('t36')
t36_ancla = [p for p in s.split('\n\n') if p.startswith('Un compendio permite, en cambio')][0]
t36_nuevo = ('El desarrollo no sigue al dinero en la misma proporción. En el índice cantonal de desarrollo sostenible de 2022, Belén ocupa el tercer puesto, con 94,68, y Alajuelita el vigesimoprimero, con 77,90, en una escala relativa que da 100 a Escazú y 0 a Talamanca (Ministerio de Planificación Nacional y Política Económica [MIDEPLAN], 2025, pp. 13 y 15). Con el presupuesto de 2024, en cambio, a cada habitante de Belén le correspondían trece veces más recursos que a cada habitante de Alajuelita, como se verá en la conclusión. El propio Ministerio recomienda usar ese índice como herramienta complementaria y evitar las comparaciones simplistas (MIDEPLAN, 2025, p. 48).')
if 'El desarrollo no sigue al dinero' not in s:
    s = rep(s, t36_ancla, t36_ancla + '\n\n' + t36_nuevo)
wr('t36', s)

# conclusión
s = rd('conclusion')
s = rep(s, 'todo interés y todo servicio de naturaleza pública que importa de manera directa e inmediata ' + VIVEN + '.',
        'todo interés y todo servicio de naturaleza pública que importa de manera directa e inmediata ' + HABITAN + '. '
        'Esas personas no son solo las residentes: el municipio lo forman los vecinos [[L:7794:art. 1]], pero la ley encarga a la municipalidad albergues para quienes viven en la calle [[L:7794:art. 4, inciso j]], y los servicios locales llegan a todo el que está en el cantón.')
s = rep(s, 'y solo después si una ley especial la obliga.',
        'y solo después si una ley especial la obliga. Así se atiende la advertencia de Leiva Poveda, para quien buscar una definición general de lo local para todas las municipalidades era imposible y peligroso (Leiva Poveda, 2016, p. 11). La definición del libro no reparte materias: reúne criterios y deja el mapa abierto.')
# MIDEPLAN sale de la conclusión
s = rep(s, ' La distancia en el dinero no se traslada entera a la medición del desarrollo. En el índice cantonal de desarrollo sostenible de 2022, Belén ocupa el tercer puesto, con 94,68, y Alajuelita el vigesimoprimero, con 77,90, en una escala relativa que da 100 a Escazú y 0 a Talamanca (Ministerio de Planificación Nacional y Política Económica [MIDEPLAN], 2025, pp. 13 y 15). El propio Ministerio recomienda usar ese índice como herramienta complementaria y evitar las comparaciones simplistas (MIDEPLAN, 2025, p. 48).', '')
# Tempisque en la tercera regularidad
s = rep(s, '"no ha permanecido ajena a la situación ni ha adoptado una postura pasiva frente al riesgo advertido" [[V:2026-000643:considerando IV]].',
        '"no ha permanecido ajena a la situación ni ha adoptado una postura pasiva frente al riesgo advertido" [[V:2026-000643:considerando IV]]. '
        'Ese mismo año, en el caso del río Tempisque, la Sala llevó la regla más lejos y condenó a dos municipalidades que no otorgan concesiones mineras, porque "La falta de competencia concesional no extingue el deber local de tutela ambiental y de prevención" [[V:2026-014917:considerando XVIII]]. Su conclusión resume esta regularidad: "la autonomía municipal no es excusa para la pasividad local" [[V:2026-014917:considerando XXV]].')
# déficit estructural en la quinta
s = rep(s, 'Una municipalidad que organiza sus servicios por departamentos estancos atiende pedazos de una persona que llega entera.',
        'Una municipalidad que organiza sus servicios por departamentos estancos atiende pedazos de una persona que llega entera. La Sala le puso nombre a ese defecto en el caso del Tempisque: la omisión reprochable puede consistir en que "la suma de actuaciones parciales no alcanza el estándar exigible" [[V:2026-014917:considerando XXII]].')
# agenda con destinatarios
viejo = s[s.index('Quedan también tareas que exceden a un libro.'):s.index('La imagen final es la del principio.')]
nuevo_ag = ('Quedan también tareas que exceden a un libro, y cada una tiene destinatario. A la municipalidad le toca medir: convertir la pregunta de qué recibió la persona y quién se lo prestó en indicadores que el cantón pueda llevar año tras año, y a la Contraloría, incorporar esa pregunta a los índices con que ya evalúa la gestión. Al Concejo le toca decidir. Le corresponde "Fijar la política y las prioridades de desarrollo del municipio" [[L:7794:art. 13]], y la ley le pide adoptarlas "asegurando el respeto, protección, garantía y promoción de los derechos humanos reconocidos en la Constitución, leyes y convenios internacionales ratificados" [[L:7794:art. 13]]. Para adoptar este enfoque, una política municipal puede apoyarse en las competencias que ya existen, leídas juntas. A la persona titular de la alcaldía, como administradora general, le toca vigilar "la organización, el funcionamiento, la coordinación y el fiel cumplimiento de los acuerdos municipales" [[L:7794:art. 17, inciso a]], que es donde la política se vuelve servicio. Al legislador le queda precisar por ley lo que hoy se precisa caso por caso, porque la Sala advirtió desde 1997 que "la única forma de definir o de distinguir lo local de lo que no lo es, es por medio de un texto legal" [[V:1997-006469:considerando IV]]. Y a quienes estudian el derecho municipal les toca seguir investigando, tema por tema y cantón por cantón, para nombrar los grados que faltan.\n\n'
            'En 2016, en San José, pregunté si el viejo artículo 62 del Código Municipal servía para definir lo local. No servía para definirlo, porque era una norma sobre bienes y contratos. Pero apuntaba en la dirección correcta: al final de esa norma de patrimonio aparecían personas con su necesidad a la vista, y este libro terminó poniéndolas en el núcleo de la célula. Hoy esa misma norma, convertida en el artículo 71, nombra también a las personas en situación de calle, que no siempre son vecinas residentes y que, sin embargo, son del cantón.\n\n')
s = s.replace(viejo, nuevo_ag)
s = rep(s, 'La imagen final es la del principio.', 'La imagen final es la del primer capítulo.')
wr('conclusion', s)
print('ok')
