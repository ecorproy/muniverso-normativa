"""Inserta en src los aportes del Informe Estado de la Nación 2026 (cap. 4),
el ICSC 2025 y el ICDS de MIDEPLAN. Cada inserción va después del párrafo
que empieza con el prefijo indicado."""
import sys
B = '/home/claude/libro'
PEN = 'Programa Estado de la Nación, 2026'
OV = 'Observatorio de la Violencia, 2026'
MID1 = 'Ministerio de Planificación Nacional y Política Económica [MIDEPLAN], 2025'
MID = 'MIDEPLAN, 2025'

INS = {
 't04': [('El índice mide, entonces,', [
  f'Otro índice mide el resultado y no la gestión. El Índice Cantonal de Seguridad Ciudadana 2025, del Observatorio de la Violencia, calcula tasas por cada 100.000 habitantes de doce delitos e infracciones, con datos del propio Observatorio, el INEC, el Ministerio de Seguridad Pública y el OIJ, y las resume en una escala de 0 a 1, en la que el valor más cercano a 1 indica más seguridad ({OV}, pp. 2-3 y 6). Lo compone con tres subíndices: seguridad de los bienes, seguridad personal y seguridad en la edificación o vivienda ({OV}, pp. 5-6). En 2025 encabezó Escazú, con 0,952, y cerró San José, en el puesto 84, con 0,566. Respecto de 2024, 48 cantones bajaron de posición, 31 subieron y 5 se mantuvieron ({OV}, pp. 7 y 9).',
  'Ese índice no evalúa a la policía municipal: un cantón puede subir o bajar sin que cambie nada de lo que hace su municipalidad. Ofrece, en cambio, lo que el índice de la Contraloría no tiene, un dato cantonal de resultado contra el cual la municipalidad puede contrastar las metas de su propio servicio.'])],
 't26': [('El índice de gestión de la Contraloría no mide', [
  f'El dato existe en otra medición. El Índice Cantonal de Seguridad Ciudadana, descrito en el tema 4, incluye las infracciones a la Ley contra la Violencia Doméstica y a la Ley de Penalización de la Violencia contra las Mujeres en el subíndice de seguridad en la edificación o vivienda, junto con el robo a edificación y el robo a vivienda ({OV}, pp. 4-6). Esa agrupación resulta de un análisis estadístico de factores ({OV}, p. 4). La consecuencia para la municipalidad es práctica: la tasa cantonal de esas infracciones ya se calcula, aunque el índice la publique mezclada con los robos.'])],
 't06': [('Fuera del índice hay dos verificaciones.', [
  f'Tampoco el índice cantonal de desarrollo sostenible de MIDEPLAN, para 2020-2022, pudo medir la acción por el clima, porque no obtuvo información cantonal para ese objetivo ni para el de la vida submarina ({MID1}, p. 7). La falta pesa más ante las cifras nacionales. Después de que 2024 registrara el segundo mayor número de desastres asociados a fenómenos climáticos en tres décadas, en 2025 esos desastres se redujeron en un 84,4%, sin que desaparecieran las condiciones de riesgo ni sus costos ({PEN}, p. 185).'])],
 't28': [('El acueducto municipal tiene, además,', [
  f'Otra medida llega desde la regulación. Con datos de la Aresep para 59 de los 84 cantones, el Informe Estado de la Nación de 2026 registra que en 2022 se rechazó una quinta parte de las solicitudes de disponibilidad de agua tramitadas ante el AyA y la ESPH, y presenta el rechazo por cantón ({PEN}, pp. 187 y 243). El dato no mide a los acueductos municipales, pero muestra la dificultad de garantizar el agua a los proyectos constructivos ({PEN}, p. 187).'])],
 't29': [('La tabla de datos que acompaña el índice de 2025 baja', [
  f'Una medición independiente mira la gestión desde la Ley para la Gestión Integral de Residuos. El Programa Estado de la Nación consultó por teléfono a los gobiernos locales entre octubre y diciembre de 2025. Respondieron 73 de 91, y con sus respuestas construyó un índice de 0 a 100 que parte de las percepciones de las personas entrevistadas ({PEN}, p. 221). El promedio más alto correspondió a las herramientas y capacidades, con 75,4, y el más bajo a las acciones municipales, con 55,3 ({PEN}, p. 221). Los 73 gobiernos locales se agrupan en cuatro perfiles: 29 consolidados, con un promedio de 66,9; 19 intermedios con fiscalización, con 59,9; 17 con capacidades sin fiscalización, con 52,3, y 8 rezagados, con 30,5 ({PEN}, p. 222). Los rezagados se ubican en los territorios de menor desarrollo social y alta densidad de población ({PEN}, p. 222).',
  f'El hallazgo más severo es otro. Ninguno de los 73 gobiernos locales ha logrado aplicar las multas que establece la ley, por falta de convenios y de mecanismos de articulación con el Ministerio de Salud, y la fiscalización suele quedar relegada frente a la necesidad de financiar la recolección ({PEN}, pp. 221-222). La medida que falta no es si existe la oficina de denuncias, que el 94,5% tiene ({PEN}, p. 221), sino cuántas denuncias terminaron en una sanción.'])],
 't30': [
  ('A las dos municipalidades les ordenó', [
  f'El Informe Estado de la Nación de 2026 destacó cuatro aportes del voto. Entre ellos, que es la primera formulación explícita del Estado social, democrático y ecológico de Derecho en la jurisprudencia costarricense ({PEN}, p. 239), expresión que la Sala usó al recibir la Opinión Consultiva OC-32/25 de la Corte Interamericana [[V:2026-014917:considerando IV]].']),
  ('Donde hay un área protegida creada por el Poder Ejecutivo,', [
  f'La Zona Protectora Cerros de Escazú muestra lo que ocurre cuando la competencia cede pero el territorio sigue siendo cantonal. El Informe Estado de la Nación de 2026, con base en el estudio de Alfaro y Merino, describe un área protegida de propiedad mayoritariamente privada, en el borde de la Gran Área Metropolitana, regida a la vez por el Plan General de Manejo, que prevalece, los planes reguladores cantonales, el Plan GAM, el Plan de Ordenamiento Ambiental, la Ley Forestal y la evaluación de impacto ambiental. En ella intervienen el Sinac, las municipalidades, la Setena, el INVU y la Dirección de Agua sin una secuencia única de trámites ni una instancia que coordine las decisiones ({PEN}, p. 195). Las personas entrevistadas atribuyen la débil capacidad institucional no a la falta de normas, sino a la fragmentación y a la dificultad de convertirlas en reglas operativas ({PEN}, p. 196).',
  f'El estudio da también la geografía del problema. Entre 2018 y 2025, los cambios de cobertura hacia infraestructura se concentraron en los bordes norte y noreste, en sectores vinculados con Santa Ana y Escazú, y aparecieron también dentro del área protegida, en manchas pequeñas y dispersas frente a calles públicas ({PEN}, pp. 196-197). La revisión de denuncias registra reformas de planes reguladores que flexibilizan condiciones dentro del área, movimientos de tierra, afectación de nacientes y construcciones sin permiso, y varias de esas situaciones llegaron al Tribunal Ambiental Administrativo, la Setena o la Sala ({PEN}, p. 199). En ese territorio, lo que exige el voto del Tempisque, vigilar de oficio lo que ocurre en el cantón aunque la competencia principal sea de otro, se vuelve una tarea diaria.'])],
 'conclusion': [('Tampoco dice que todas las municipalidades', [])],
}

CONC_OLD = 'trece veces menos (Instituto de Fomento y Asesoría Municipal [IFAM], 2025, pp. 29 y 123).'
CONC_NEW = CONC_OLD + f' La distancia en el dinero no se traslada entera a la medición del desarrollo. En el índice cantonal de desarrollo sostenible de 2022, Belén ocupa el tercer puesto, con 94,68, y Alajuelita el vigesimoprimero, con 77,90, en una escala relativa que da 100 a Escazú y 0 a Talamanca ({MID1}, pp. 13 y 15). El propio Ministerio recomienda usar ese índice como herramienta complementaria y evitar las comparaciones simplistas ({MID}, p. 48).'

for c, lst in INS.items():
    f = f'{B}/{c}/src/{c}.md'
    s = open(f, encoding='utf-8').read()
    if c == 'conclusion':
        assert s.count(CONC_OLD) == 1, c
        if 'MIDEPLAN' not in s:
            s = s.replace(CONC_OLD, CONC_NEW)
        open(f, 'w', encoding='utf-8').write(s)
        continue
    paras = s.split('\n\n')
    for pref, nuevos in lst:
        if nuevos[0][:60] in s:
            continue
        idx = [i for i, p in enumerate(paras) if p.startswith(pref)]
        assert len(idx) == 1, (c, pref, idx)
        paras[idx[0] + 1:idx[0] + 1] = nuevos
        s = '\n\n'.join(paras)
    open(f, 'w', encoding='utf-8').write(s)
    print(c, 'ok')
