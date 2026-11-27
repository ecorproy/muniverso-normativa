B='/home/claude/libro/'
def ins_after(f,start,nuevo):
    t=open(B+f,encoding='utf-8').read().split('\n\n'); i=[k for k,x in enumerate(t) if x.startswith(start)]; assert len(i)==1,(f,start)
    t.insert(i[0]+1,nuevo); open(B+f,'w',encoding='utf-8').write('\n\n'.join(t))
def rep(f,a,b):
    t=open(B+f,encoding='utf-8').read(); assert t.count(a)==1,(f,a); open(B+f,'w',encoding='utf-8').write(t.replace(a,b))
D='[[O:IGSMD:hoja de distritos]]'; M='[[O:IGSMD:hoja de municipalidades]]'
# Tema 29
ins_after('t29/src/t29.md','La Contraloría evalúa la gestión de este servicio',
 'La tabla de datos que acompaña el índice de 2025 baja la pregunta al distrito. Para la recolección de residuos ordinarios, registra la cobertura según las unidades residenciales atendidas y por atender: de los 491 distritos, 233 tienen cobertura total, 87 parcial y en 171 la administración no cuenta con la información '+D+'. '
 'La respuesta cambia con el desarrollo del distrito, según la clasificación del índice de desarrollo social de 2023 que la misma tabla incorpora. En los 123 distritos de mayor desarrollo, la cobertura es total en 99 y falta la información en 10; en los 58 de desarrollo muy bajo, es total en 4 y falta la información en 40 '+D+'. '
 'Donde menos se sabe si el camión pasa es donde más importa saberlo. En el aseo de vías la falta es mayor: la administración no cuenta con la información de cobertura en 352 de los 491 distritos '+D+'. '
 'Y solo 20 de las 84 municipalidades tienen identificada a la población vulnerable para la recolección con alguna de las cuatro variables que pregunta el índice '+M+'.')
# Tema 10
ins_after('t10/src/t10.md','La comparación entre la definición y las variables es reveladora',
 'Las respuestas de 2025 muestran cuánto falta aun con esas cuatro variables. En la recolección de residuos, 64 de las 84 municipalidades no tienen identificada a la población vulnerable con ninguna de ellas '+M+'. '
 'Y la cobertura del servicio se conoce peor donde el desarrollo social es más bajo: la administración no cuenta con el dato de cobertura de la recolección en 40 de los 58 distritos de desarrollo muy bajo, y le falta solo en 10 de los 123 de mayor desarrollo '+D+'. '
 'La desigualdad empieza por no saber a quién no se le está sirviendo.')
# Tema 4
ins_after('t04/src/t04.md','La seguridad y la vigilancia en la comunidad es uno de los diez servicios',
 'La tabla de datos que acompaña el índice de 2025 contesta la pregunta de los distritos. De las 84 municipalidades, 31 prestan el servicio de policía municipal y 39 el de vigilancia con soluciones tecnológicas '+M+'. '
 'El reparto sigue el desarrollo social del distrito, según la clasificación de 2023 que la tabla incorpora: la policía municipal cubre 93 de los 123 distritos de mayor desarrollo y 6 de los 58 de desarrollo muy bajo, y la vigilancia tecnológica cubre 95 de los primeros y ninguno de los segundos '+D+'. '
 'El dato no prueba por sí solo una discriminación, porque refleja sobre todo qué municipalidades tienen el servicio, pero muestra dónde la persona cuenta con menos protección municipal.')
# Conclusión
rep('conclusion/src/conclusion.md','un reglamento, un equipo, una partida. El Índice de Cumplimiento',
 'un reglamento, un equipo, una partida. Cuando el índice pregunta por el alcance, la respuesta suele faltar: en 171 de los 491 distritos, la municipalidad no sabe qué cobertura tiene su recolección de residuos '+D+'. El Índice de Cumplimiento')
print('ok')
