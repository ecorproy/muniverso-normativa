"""Respuesta al dictamen crítico (A1-A7, A10): tesis visibles, antecedentes, casos difíciles,
cuadrantes, poder explicativo de la red, indicadores de las seis formas, niveles de resultado
y matiz del 20 % del artículo 55 de la Ley 5412."""
B = '/home/claude/libro'
R = '/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
import shutil, os


def rd(c):
    f = f'{B}/{c}/src/{c}.md'
    if not os.path.exists(f):
        os.makedirs(f'{B}/{c}/src', exist_ok=True)
        shutil.copy(f'{R}/{c}/src/{c}.md', f)
    return open(f, encoding='utf-8').read()


def wr(c, s):
    open(f'{B}/{c}/src/{c}.md', 'w', encoding='utf-8').write(s)


def rep(s, a, b):
    if b in s:
        return s
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)


def antes_de(s, ancla, texto):
    if texto[:60] in s:
        return s
    assert s.count(ancla) == 1, ancla
    return s.replace(ancla, texto + '\n\n' + ancla)


def despues_de_parrafo(s, inicio, texto):
    if texto[:60] in s:
        return s
    ps = s.split('\n\n')
    k = [i for i, p in enumerate(ps) if p.startswith(inicio)]
    assert len(k) == 1, inicio
    ps.insert(k[0] + 1, texto)
    return '\n\n'.join(ps)


# A1. Introducción: tesis visibles
s = rd('intro')
tesis = '''## Lo que este libro sostiene

Antes del viaje conviene decir adónde lleva. El libro reúne mucha legislación, jurisprudencia y criterios administrativos, pero no los reúne para repetirlos. Los usa para sostener siete tesis, que el lector puede comprobar en el lugar donde cada una se demuestra.

La primera es que lo local se define por la persona y no por el territorio ni por la oficina: es lo que importa de manera directa e inmediata a quien habita el cantón o se encuentra en él (capítulo 3).

La segunda es que las personas del cantón no son solo las vecinas residentes. El municipio lo forman los vecinos, pero los servicios locales tienen como destinatarias potenciales a todas las personas que están en el cantón, incluidas las que viven en sus calles (capítulo 3 y tema 8).

La tercera es que la competencia ajena no libera. Cuando la necesidad corresponde a otra institución, el deber municipal se convierte en coordinar, instar y llevar a la persona hasta ella (capítulo 2 y tema 30).

La cuarta es que la escasez no excusa. La falta de recursos no justifica dejar de prestar un servicio; lo exigible es prever (capítulo 4 y conclusión).

La quinta es que el servicio se cumple cuando llega. La evaluación por productos y servicios que exige la ley de empleo público se lee desde lo que recibe la persona, no desde la actividad de la oficina (capítulo 4).

La sexta es que las fallas de la acción municipal tienen formas reconocibles. Las seis formas en que muere una red, captura, corte, desgaste, envenenamiento, sustitución y acaparamiento, sirven para diagnosticar cualquier servicio (capítulo 1 y conclusión).

La séptima es que lo que hoy se mide no coincide con lo que es exigible. Cada tema compara el deber jurídico con los instrumentos que evalúan a las municipalidades, y el anexo A reúne esas treinta y seis brechas en una sola matriz.

Ninguna de esas tesis parte de cero. El capítulo 3 dice qué estaba ya dicho por la Sala Constitucional, la Procuraduría, la ley y la doctrina, y qué agrega este libro.'''
s = antes_de(s, '## El mapa del viaje', tesis)
wr('intro', s)

# A2 y A3. Capítulo 3: antecedentes y casos difíciles
s = rd('cap03')
a2 = '''## Lo que ya estaba dicho y lo que el libro agrega

Conviene separar lo heredado de lo propio. Que lo local es un concepto indeterminado lo dijo la Sala en 1997, cuando reconoció que el constituyente dejó en el artículo 169 "un concepto jurídico indeterminado" [[V:1997-006469:considerando IV]]. Que se precisa caso por caso lo dijeron esa misma sentencia y la Procuraduría, como se vio en el capítulo 2. Que la competencia municipal es originaria y genérica viene de la sentencia de 1999 [[V:1999-005445:considerando VI]]. Que el interés público es "la expresión de los intereses individuales coincidentes de los administrados" [[L:6227:art. 113]] lo dice la Ley General de la Administración Pública desde 1978. Que la seguridad debe centrarse en las personas, prevenir y adaptarse a cada contexto es la propuesta de la seguridad humana (Naciones Unidas, 2016, p. 6). Que el servidor público se evalúa por productos y servicios lo disponen la Ley de Salarios [[L:2166:art. 47]] y la Ley Marco de Empleo Público [[L:10159:art. 28]]. Y que una definición general de lo local para todas las municipalidades es una senda peligrosa lo advirtió Leiva Poveda (2016, p. 11).

Lo que este libro agrega es la manera de unir esas piezas. Primero, desplaza el punto de partida: lo local se reconoce mirando a la persona que necesita, y no al territorio o a la oficina. Segundo, extiende el alcance subjetivo a quien está en el cantón sin residir en él. Tercero, organiza el ámbito de lo local en treinta y seis temas y cuatro cuadrantes, con una forma única de examinarlos. Cuarto, convierte cada tema en una comparación entre lo exigible y lo que hoy se mide. Y quinto, ofrece una tipología de las fallas, las seis formas en que muere la red, para diagnosticar cualquier servicio. Ninguna de esas operaciones contradice a la Sala ni a la Procuraduría; las supone. La pregunta que queda es si la definición sirve para resolver algo que la fórmula anterior no resolvía.'''
a3 = '''## Tres casos difíciles y un límite

La fórmula de la Sala define el interés local como "todo aquel de naturaleza pública que importa al cantón de manera directa e inmediata" [[V:2006-017907:considerando III]]. La definición de este libro cambia el sujeto: lo que importa a las personas que habitan el cantón o se encuentran en él. La diferencia parece pequeña, pero se nota en tres casos.

El primero es la persona en situación de calle. Si lo que importa es el cantón entendido como comunidad de vecinos residentes, quien duerme en un parque y no tiene domicilio queda en el borde del concepto, como un dato del entorno. La definición por la persona lo pone en el centro, y la ley le da la razón: el Código dirige las ayudas temporales a los vecinos y vecinas del cantón, pero los albergues a "las personas que se encuentren en situación de abandono y situación de calle" [[L:7794:art. 71]]. El tema 8 desarrolla las consecuencias.

El segundo son las becas y las ayudas que exigen nacionalidad o residencia. La fórmula territorial no dice a quién puede excluir la municipalidad. La definición por la persona distingue dos cosas: quién es destinatario potencial del servicio, que es toda persona del cantón, y qué requisitos puede fijar la ley para una prestación concreta. Con esa distinción, la vecindad que exige el Código para las ayudas es un requisito legítimo, y la nacionalidad no lo es, porque la Sala la tiene por "una condición ilegítima de exclusión de la adjudicación de becas" [[VT:2003-007806:2024-029734:considerando III!]]. El tema 12 aplica esa regla a los reglamentos de San José, Cartago, Liberia y Matina.

El tercero es la competencia ajena. En el caso del río Tempisque, dos municipalidades alegaron que no otorgan concesiones mineras. La mayoría de la Sala respondió que "La falta de competencia concesional no extingue el deber local de tutela ambiental y de prevención" [[V:2026-014917:considerando XVIII]]; un magistrado salvó el voto porque "no hay una denuncia interpuesta por el recurrente ante las autoridades recurridas contra las que se estima el recurso" [[V:2026-014917:considerando XXVI]]. La definición de este libro coincide con la mayoría y explica por qué: si lo local se mide por lo que importa a la persona del cantón, el deber de vigilar el territorio no depende de que alguien lo pida, y cuando la competencia es de otro se convierte en coordinar e instar. El tema 30 recorre el caso.

La definición también tiene un límite, y conviene mostrarlo. El Sistema de Emergencias 9-1-1 preguntó si una municipalidad puede operar su propia línea de emergencias. La Procuraduría respondió que las municipalidades "no pueden operar líneas de atención de emergencias de manera independiente al Sistema 9-1-1" [[D:C-287-2024:conclusión]], porque "no se trata de un asunto de interés exclusivamente cantonal, sino de una competencia supralocal" [[D:C-287-2024:conclusión]]. La definición de este libro llega al mismo resultado: la emergencia importa a la persona del cantón, pero la ley la atribuyó a un sistema nacional, y al gobierno local le queda coordinar con él. La definición no amplía la competencia municipal más allá de la ley; ordena la mirada con que se ejerce.'''
s = antes_de(s, '## La persona en el centro', a2 + '\n\n' + a3)
# A4. Cuadrantes y nueve temas
s = despues_de_parrafo(s, 'Cada cuadrante tiene nueve temas, y los cuatro suman treinta y seis.',
    'La simetría de nueve temas por cuadrante no es un hallazgo; es una decisión de orden. Otras clasificaciones son posibles: por servicio, por población o por la institución nacional con que se coordina. La de este libro se escogió por tres razones. Cada cuadrante nace de un artículo de la Constitución, cada tema cabe en un solo cuadrante y el cruce entre temas lo resuelve la red del capítulo 1, no la clasificación. Si una investigación posterior identifica más temas en un cuadrante que en otro, la simetría cederá, y el modelo seguirá siendo el mismo.')
wr('cap03', s)

# A5. Capítulo 1: la red anticipó el déficit estructural
s = rd('cap01')
s = despues_de_parrafo(s, 'La primera es el corte.',
    'El corte tiene también una forma menos visible: varias instituciones actúan, cada una en su tramo, y nadie mira el conjunto. En 2026 la Sala Constitucional le puso nombre a esa forma sin usar la imagen de la red. Ante un río con inspecciones, expedientes y traslados de varias autoridades, concluyó que no había inacción sino "un déficit estructural de tutela efectiva" [[V:2026-014917:considerando XXII]], porque "la suma de actuaciones parciales no alcanza el estándar exigible para un caso de esta naturaleza" [[V:2026-014917:considerando XXII]]. Es la señal que se propaga por la red herida y no alcanza al vecino. El modelo de este libro permite anticipar dónde ocurre: en los pasos de una institución a otra y de una oficina a otra, que el capítulo 4 examina como los relevos de un proceso.')
wr('cap01', s)

# A6. Conclusión: un indicador por cada forma de muerte de la red
s = rd('conclusion')
ind = {
    'La captura pregunta quién recibe sin dar.': ' Se mide, por ejemplo, por la proporción de contrataciones adjudicadas a los mismos oferentes y por las obras pagadas que no se concluyen.',
    'El corte pregunta dónde se cae el expediente.': ' Se mide por los traslados entre oficinas o instituciones que no reciben respuesta y por los días que pasa un expediente entre una y otra.',
    'El desgaste pregunta qué no se está renovando.': ' Se mide por la antigüedad de la flotilla y del equipo frente a su vida útil, y por los mantenimientos programados que no se hicieron.',
    'El envenenamiento pregunta qué mala práctica se volvió costumbre.': ' Se mide por los reclamos cerrados con un acuse de recibo y por las verificaciones que no incluyen una visita al lugar.',
    'La sustitución pregunta qué hace otro por la municipalidad.': ' Se mide por los servicios del cantón que presta otra institución sin convenio y por las órdenes judiciales que obligaron a actuar.',
    'El acaparamiento pregunta qué información o qué recurso queda retenido en un punto.': ' Se mide por las sesiones no transmitidas, las actas publicadas fuera de plazo y los datos que la municipalidad produce y no publica.',
}
ps = s.split('\n\n')
for k, v in ind.items():
    j = [i for i, p in enumerate(ps) if p.startswith(k)]
    assert len(j) == 1, k
    if v.strip()[:40] not in ps[j[0]]:
        ps[j[0]] = ps[j[0]] + v
s = '\n\n'.join(ps)
s = rep(s, 'Las seis preguntas tienen una séptima detrás:', 'Los indicadores son una propuesta; el anexo A los completa tema por tema. Las seis preguntas tienen una séptima detrás:')
wr('conclusion', s)

# A7. Capítulo 4: tres niveles de resultado
s = rd('cap04')
s = despues_de_parrafo(s, 'El artículo 28 tiene la misma inversión.',
    'Conviene distinguir tres niveles, para no pedirle a una persona lo que solo puede dar una institución. El primero es la meta individual, que la ley evalúa con indicadores de los productos y servicios asignados a cada persona servidora [[L:10159:art. 28]]. El segundo es el resultado de la dependencia: que el servicio llegue completo, lo que depende de varias personas, del presupuesto y de otras oficinas. El tercero es el impacto en la población: que el cantón esté mejor, lo que depende además de factores que ninguna municipalidad controla. Un resultado institucional no puede imputarse sin más a una persona. La Administración responde por los daños de su funcionamiento [[L:6227:art. 190]], y la persona servidora responde personalmente solo cuando actúa con dolo o culpa grave [[L:6227:art. 199]]. La meta individual mide la porción que a cada quien se le asignó y se le dieron medios para cumplir; el resultado y el impacto se miden en la dependencia y en el cantón.')
wr('cap04', s)

# A10. Tema 1: el convenio como prueba idónea, no única
s = rd('t01')
s = rep(s, 'La municipalidad que quiera demostrar que cumple necesita el acuerdo con el Ministerio por escrito, y el Código Municipal le da el instrumento:',
    'La municipalidad que quiera demostrar que cumple debe poder acreditar esa determinación conjunta de necesidades. El instrumento más idóneo es un convenio escrito con el Ministerio, que el Código Municipal autoriza:')
s = rep(s, 'Sin ese convenio, la municipalidad gasta en salud ambiental pero no puede probar que lo hace en los términos del artículo 55, y la Contraloría no tiene contra qué medirla.',
    'No es el único posible: la determinación conjunta puede constar también en un plan o en un acta firmados con la autoridad de salud. Sin algún documento de ese tipo, la municipalidad gasta en salud ambiental pero no puede probar que lo hace en los términos del artículo 55, y la Contraloría no tiene contra qué medirla. Qué partidas pueden computarse para alcanzar el porcentaje es una pregunta que la ley deja a la determinación conjunta con el Ministerio y al control de la Contraloría [[L:5412:art. 55]].')
wr('t01', s)
print('ok')

# corrección posterior aplicada a mano en t01: «y el convenio, o el documento que acredite la determinación conjunta, es lo que permite responder la pregunta con datos.»
