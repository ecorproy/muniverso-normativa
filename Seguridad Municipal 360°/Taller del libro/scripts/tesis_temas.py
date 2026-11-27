"""Tesis de cada tema, en voz del autor, al inicio del tema (antes de «El caso»).
Se redactan a partir de la conclusión de cada tema; no agregan fuentes nuevas."""
T = {
 1: 'la salud física existe en el cantón cuando el gobierno local presta bien los servicios que la ley considera esenciales para la salud ambiental, vigila lo que autoriza, gasta en salud lo que la ley le manda y coordina con la autoridad sanitaria sin esconderse detrás de ella. La municipalidad no dirige la salud pública, pero administra el entorno sin el cual la salud no se protege.',
 2: 'la salud mental existe en el cantón cuando el gobierno local cuida el entorno que la produce, acompaña a las personas en los servicios que ya presta, trata bien a quienes trabajan para él y coordina con la autoridad sanitaria lo que solo él sabe del territorio. La municipalidad no atiende trastornos mentales, pero administra muchas de las condiciones de las que depende que la gente no los sufra, o que los sufra acompañada.',
 3: 'la alimentación existe en el cantón cuando el gobierno local abre el lugar donde el productor encuentra al consumidor, gobierna con reglas claras su propio mercado, compra para sus servicios a quien la ley le indica, licencia con agilidad y con la condición sanitaria a quien abastece y hace llegar la ayuda a quien la necesita.',
 4: 'la integridad personal y de bienes existe en el cantón cuando el gobierno local tiene una policía que hace cumplir sus decisiones dentro de los límites que protegen a las personas, registra lo que ocurre y deja registrarlo, custodia lo que retiene y vigila lo que otros instalan en el espacio público. La misma potestad que protege a los vecinos puede lesionarlos, y la municipalidad responde en los dos casos.',
 5: 'la seguridad vial existe en el cantón cuando el gobierno local sabe cuáles calles son suyas, las señala y demarca conforme a la técnica sin esperar permiso, decide los reductores por estudio, hace cumplir la señal con una policía investida y deja constancia cuando el riesgo está en una calle ajena.',
 6: 'la seguridad frente al desastre existe en el cantón cuando el gobierno local trata el riesgo como asunto de todos los días: sabe dónde está, no deja construir donde el río vuelve, mantiene lo que es suyo, activa a los demás cuando no basta con lo propio y presupuesta con años de anticipación. La declaratoria de emergencia y los informes ajenos no sustituyen las potestades ordinarias del gobierno local.',
 7: 'en las adicciones la municipalidad no cura, pero decide cuántos lugares de venta hay y dónde, otorga con reglas, vigila lo que ocurre alrededor del mostrador y, como patrono, ofrece tratamiento antes de sancionar. Cada decisión preventiva tiene su lugar en el ciclo de la licencia, y tomarla en el lugar equivocado la vuelve ilegal.',
 8: 'la persona en situación de calle es sujeto de un servicio y no un asunto de ornato. La ley permite crear albergues y obliga a reglamentarlos; las reglas de uso del espacio público deben leerse de modo compatible con esa condición, y la necesidad de un albergue es un hecho que la municipalidad debe averiguar en su cantón.',
 9: 'el cementerio municipal es un servicio que debe alcanzar a todos los habitantes del cantón, y las reglas sobre el uso de sus espacios deben leerse de modo compatible con esa finalidad, que saca del comercio el lugar de los muertos para proteger a las familias.',
 10: 'el gobierno local hace que exista la igualdad cuando reparte sus servicios de modo que nadie quede excluido por lo que es o por dónde vive, y cuando corrige la exclusión que producen sus propios criterios.',
 11: 'el gobierno local hace que exista la igualdad de género cuando cumple el ciclo que el Código Municipal le asigna, desde el programa de la alcaldía hasta el informe anual, y cuando revisa sus servicios y su propio empleo con las necesidades diferenciadas de mujeres y hombres a la vista.',
 12: 'el Código Municipal ya dice a quién servir, y la nacionalidad o la condición migratoria no forman parte de esa respuesta. Las distinciones por esos motivos solo caben cuando las establece la Constitución o la ley; el reglamento municipal puede aplicarlas, pero no crearlas.',
 13: 'el trato y los trámites son el lugar donde la persona se encuentra con la municipalidad, y la ley ya dice cómo debe ser ese encuentro. El reglamento puede organizar la recepción, pero no convertir una regla de oficina en la pérdida de un derecho.',
 14: 'la información de la municipalidad pertenece a los vecinos, y la ley ya dice qué se publica, qué se entrega y qué se reserva. Una reserva que no nace de la ley no es válida.',
 15: 'la participación del vecino en las decisiones del gobierno local es un mandato de la Constitución y del Código, y cada instrumento de participación tiene efectos propios. Cumplir la forma de una audiencia o de una consulta es condición de validez de lo que se decide después.',
 16: 'cada cámara, dron, expediente o ficha municipal contiene datos de alguien, y la seguridad municipal no puede comprarse con la intimidad de las personas. La regla es el acceso de la persona a sus propios datos; la negativa es la excepción y debe justificarse.',
 17: 'el acceso digital es un derecho, y la municipalidad lo afecta por dos caminos: la infraestructura que facilita o entorpece y los canales propios que abre o cierra. En el primero su autonomía cede ante una política nacional; en el segundo sus deberes son propios y tienen plazos.',
 18: 'el puesto de quien vende en la calle es precario frente al destino del bien público, pero no frente a la forma. La municipalidad puede trasladar o retirar el permiso, y debe hacerlo con un acto motivado, comunicado y con plazo, porque para quien vive de ese puesto la sorpresa es la lesión.',
 19: 'el gobierno local protege a la familia en tres papeles: como acreedor que modera su cobro, como autoridad que ayuda ante la desgracia y como vía de acceso a los programas del Estado. En los tres, la ley le da reglas precisas.',
 20: 'el gobierno local protege a la madre y al niño pequeño como colaborador del Patronato y como integrante de la red de cuido. No dirige la política nacional, pero opera centros, dicta reglamentos, emplea madres y atiende público, y la ley regula cada uno de esos papeles.',
 21: 'el gobierno local colabora en la protección especial de la niñez desde tres lugares: su asiento en el sistema de protección, sus competencias sobre el territorio y su condición de administración que emplea personas y presta servicios.',
 22: 'ante el niño el gobierno local protege; ante el adolescente y el joven, además de proteger, tiene que compartir decisiones.',
 23: 'el gobierno local cumple la protección especial de la persona adulta mayor en tres ámbitos: la atención al público, la hacienda y el territorio.',
 24: 'el gobierno local cumple la igualdad de oportunidades de las personas con discapacidad en cuatro ámbitos: la obra, el permiso, la atención al público y el Concejo.',
 25: 'el cuido ocurre en una casa del cantón y no en la sede de una institución nacional. Aunque el gobierno local no decide los cupos ni el financiamiento de los centros, sí puede ver y acompañar a quien necesita cuidado y a quien lo da.',
 26: 'aunque la ley no pone a la municipalidad en la lista del sistema nacional contra la violencia doméstica, la municipalidad no puede ser ajena. Su oficina, su plataforma de servicios y su policía son, muchas veces, el primer lugar al que llega la mujer agredida, y deben saber qué hacer.',
 27: 'la convivencia vecinal existe en el cantón cuando el gobierno local usa bien las potestades que tiene sobre lo que autoriza, sobre lo que posee y sobre el uso del suelo, y ofrece un lugar para resolver lo que no admite sanción. No existe por prohibiciones generales de actividades lícitas, que la ley reserva al legislador.',
 28: 'el cumplimiento en agua y saneamiento se mide por la solución material que recibe la persona, no por la gestión de la oficina. La administración del acueducto municipal y la rectoría nacional recaen sobre aspectos distintos del servicio, y ninguna excusa a la otra.',
 29: 'la recolección de residuos es un servicio continuo, y la continuidad se prevé. El plan municipal es el lugar donde se anticipa lo que falla, y la escasez de recursos no justifica dejar de recoger.',
 30: 'el deber ambiental municipal no depende del permiso ni de la denuncia. La municipalidad debe vigilar de oficio lo que ocurre en su territorio, aunque el permiso o la concesión sean de otro.',
 31: 'la protección de los animales es un servicio local con reglas precisas, y la regla más reciente desplaza a la antigua. La municipalidad que recoge un animal responde por lo que pasa con él y por lo que sabe la persona que lo busca.',
 32: 'la municipalidad no está obligada a construir viviendas, pero sí a ordenar el territorio donde se construyen. Sus instrumentos son el plan regulador, el permiso y, si decide hacerlo, la vivienda municipal que la ley le permite.',
 33: 'la acera es un servicio municipal y no una carga del vecino. Desde 2021 su mantenimiento corresponde a la municipalidad, y el cumplimiento se mide por el tiempo que tarda en corregirse la acera denunciada.',
 34: 'el patrimonio cultural del cantón no se protege solo con la declaratoria. La municipalidad puede autorizar la demolición de lo que no está declarado, pero si el bien muestra indicios de valor cultural debe pedir antes el estudio al Ministerio, porque la obligación de resguardar la cultura persiste sin declaratoria.',
 35: 'la municipalidad responde por las canchas y los parques aunque los administre su comité de deportes. El comité es un órgano adscrito de la propia corporación, no un tercero, y ni su reglamento ni un convenio de cesión liberan a la municipalidad frente al vecino.',
 36: 'el gobierno local hace que la riqueza se produzca con instrumentos que la ley ya le dio, y ninguno exige rebajar tributos. Le corresponde prestar bien los servicios que crean el entorno para producir y distinguir entre quien invierte y quien sobrevive.',
}
import os, shutil
B = '/home/claude/libro'
R = '/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
for n, t in T.items():
    c = f't{n:02d}'
    os.makedirs(f'{B}/{c}/src', exist_ok=True)
    f = f'{B}/{c}/src/{c}.md'
    if not os.path.exists(f):
        shutil.copy(f'{R}/{c}/src/{c}.md', f)
    s = open(f, encoding='utf-8').read()
    par = '*Tesis del tema.* Este libro sostiene que ' + t
    if '*Tesis del tema.*' not in s:
        assert s.count('\n## El caso') == 1, c
        s = s.replace('\n## El caso', '\n' + par + '\n\n## El caso', 1)
        open(f, 'w', encoding='utf-8').write(s)
print('ok', len(T))
