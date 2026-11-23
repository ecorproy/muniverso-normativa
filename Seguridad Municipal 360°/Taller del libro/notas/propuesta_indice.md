# Seguridad Municipal 360° — el libro: propuesta de índice y reconocimiento

Fecha: 22 de noviembre de 2026. Nota de trabajo de la sesión en que se empezó a pasar el artículo a libro por capítulos.

No sustituye al traspaso vigente. Recoge lo hallado al abrir la sesión y la propuesta de índice, que está **pendiente de aprobación del autor**. Nada de esto se ha escrito todavía en el documento del libro, y nada se subió al repositorio.

## 1. Línea base del taller en esta sesión

- Taller armado con `preparar-taller.sh` (rama `seguridad-municipal-360`, commit 11f3c09). Tocqueville y Madero se bajaron bien de sus enlaces.
- El documento vivo sigue en la revisión 126. El .docx aportado coincide párrafo por párrafo con esa revisión; la única diferencia es «[...]» en lugar de «[…]» dentro de una cita. Las 171 referencias coinciden con las que genera el verificador.
- Recotejo: 329 citas. 310 literales y ubicadas contra su fuente íntegra. 17 sin fuente en la sesión: Pele (14), ISO 18091 (2) y Los Cabos (1); hay que readjuntar los tres PDF para volver a cotejarlas. 2 del IGSM, que se resuelven en el punto 2. Cero errores.
- `build.py` se detiene con error si falta el texto de una fuente externa; no la salta. `all.md` está guardado en forma expandida y no en macros: `chk.py` lo regenera, pero `build.py` no corre sobre él sin pasar antes por `deexp.py`.

## 2. IGSM 2025: cotejo hecho

- El informe completo está en el sitio oficial del índice, https://sites.google.com/cgr.go.cr/igsm/ (licencia CC BY-SA 4.0). Es el PDF «DFOE-LOC-SGP-00002-2025», de 17 páginas, fechado el 5 de agosto de 2025: https://drive.google.com/file/d/1nVSyp0XtsunyvNz-BeIUjQ4YK5HTuERa/view
- Las dos citas textuales del libro están literales en la **página 2** («Panorama General»). En esa misma página constan todas las paráfrasis que el libro hace del informe: los diez servicios, 8 de 10 sin cambios y 2 en retroceso, las 26 municipalidades con alcantarillado pluvial, la gestión vial, los residuos y la acción de incluir la voz de los usuarios. Distribución por madurez: 7 en inicial, 57 en básico, 20 en intermedio, ninguna en avanzado ni en optimizando.
- Falta: poner «p. 2» en las dos citas del documento y actualizar el registro de citas.
- **Hallazgo de fondo.** Las fichas de indicadores de 2025 (172 páginas, 159 indicadores: https://drive.google.com/file/d/1A2113Y8VT9hMPl5FnnjZkxKflEINHr3q/view) traen un indicador «Grado de satisfacción del usuario» en cada uno de los diez servicios (folios 25, 37, 54, 78, 93, 105, 119, 139, 153, 167 y 170), seguido de otro sobre el plan de mejora. La ficha pregunta si la municipalidad evaluó la calidad del servicio y con qué resultado, y el puntaje se obtiene si la evaluación se hizo. La metodología pondera planificación 50 %, ejecución 30 % y evaluación 20 %. La página 2 del informe afirma además que el índice permite conocer si las municipalidades responden bien a las necesidades de la población.
- Consecuencia: hay que rectificar, en la Introducción y en la sección 4, las frases «Ninguno pregunta qué recibió la persona» y «esa voz todavía no forma parte de la medida». La tesis se sostiene mejor dicha con precisión: el índice premia que la municipalidad haya hecho la evaluación, y una encuesta de satisfacción no equivale a comprobar el servicio prestado a cada persona.

## 3. Lo que el texto actual deja sin usar

Conteo automático sobre el texto de la revisión 126 y las capas del repositorio; puede variar en una o dos unidades.

- El texto cita 53 leyes distintas, 37 dictámenes, 65 votos de la Sala Constitucional y 6 resoluciones del Tribunal Contencioso Administrativo.
- Las capas asignan por tema 81 dictámenes de clase A y 221 de clase B, 21 documentos de la Contraloría, 88 votos propios de la Sala y 18 resoluciones del Tribunal.
- No cita ningún artículo de la Ley de Aguas (13 en el inventario), de la Ley de Planificación Urbana (41) ni de la Ley General de Caminos Públicos (25). De la Ley de Construcciones cita 2 de 58 (arts. 1 y 87). De la Ley N.° 8828 cita 1 de 24 (art. 2). Tampoco cita la Ley N.° 8801.
- No cita el voto N.° 5445-99 ni el N.° 6469-97, que están íntegros en el repositorio (carpeta `Citadas en otros votos`). 76 dictámenes del repositorio usan la expresión «lo local».

| N.° | Tema | Palabras hoy | Leyes citadas / cuerpo legal | Dictámenes citados / capa (clase A) | CGR en la capa | Votos propios citados / capa | TCA citadas / capa |
|---|---|---|---|---|---|---|---|
| 1 | Salud física | 475 | 3 / 7 | 1 / 2 (1) | 0 | 0 / 0 | 0 / 0 |
| 2 | Salud mental | 235 | 2 / 2 | 0 / 0 (0) | 0 | 0 / 0 | 0 / 0 |
| 3 | Alimentación | 328 | 3 / 5 | 0 / 1 (0) | 0 | 1 / 1 | 0 / 0 |
| 4 | Integridad personal y de bienes | 777 | 1 / 8 | 5 / 11 (4) | 0 | 3 / 3 | 2 / 4 |
| 5 | Seguridad vial | 464 | 3 / 9 | 1 / 12 (3) | 0 | 2 / 2 | 0 / 0 |
| 6 | Emergencias y desastres | 624 | 1 / 7 | 1 / 5 (1) | 2 | 2 / 2 | 0 / 0 |
| 7 | Adicciones | 538 | 1 / 4 | 2 / 20 (7) | 0 | 4 / 5 | 2 / 4 |
| 8 | Personas en situación de calle | 370 | 2 / 2 | 0 / 0 (0) | 0 | 1 / 1 | 0 / 0 |
| 9 | Final de la vida | 325 | 1 / 3 | 2 / 7 (4) | 0 | 1 / 1 | 0 / 0 |
| 10 | Igualdad y no discriminación | 345 | 2 / 2 | 1 / 1 (1) | 0 | 0 / 0 | 0 / 0 |
| 11 | Igualdad de género | 279 | 3 / 4 | 0 / 0 (0) | 0 | 0 / 0 | 0 / 0 |
| 12 | Personas migrantes y refugiadas | 234 | 1 / 2 | 0 / 0 (0) | 0 | 1 / 2 | 0 / 0 |
| 13 | Trato y trámites | 371 | 2 / 3 | 1 / 8 (1) | 0 | 2 / 3 | 0 / 0 |
| 14 | Información y transparencia | 353 | 1 / 2 | 1 / 9 (4) | 0 | 2 / 5 | 0 / 0 |
| 15 | Participación | 295 | 2 / 5 | 0 / 5 (1) | 1 | 2 / 2 | 0 / 0 |
| 16 | Intimidad y datos personales | 246 | 1 / 1 | 1 / 5 (2) | 0 | 0 / 0 | 0 / 0 |
| 17 | Acceso digital | 341 | 1 / 5 | 1 / 9 (1) | 0 | 0 / 0 | 0 / 0 |
| 18 | Trabajo y sustento | 239 | 3 / 7 | 1 / 3 (1) | 0 | 1 / 1 | 0 / 0 |
| 19 | Familia | 179 | 1 / 3 | 1 / 1 (1) | 0 | 0 / 0 | 0 / 0 |
| 20 | Maternidad y primera infancia | 225 | 1 / 2 | 0 / 1 (0) | 0 | 1 / 4 | 0 / 0 |
| 21 | Niñez | 307 | 3 / 5 | 0 / 0 (0) | 0 | 0 / 0 | 0 / 0 |
| 22 | Adolescencia y juventud | 296 | 2 / 5 | 2 / 4 (1) | 0 | 1 / 1 | 0 / 0 |
| 23 | Personas adultas mayores | 242 | 2 / 7 | 1 / 1 (1) | 0 | 1 / 2 | 0 / 0 |
| 24 | Personas con discapacidad | 401 | 1 / 8 | 2 / 2 (0) | 0 | 3 / 4 | 0 / 0 |
| 25 | Cuido | 385 | 0 / 3 | 1 / 1 (1) | 3 | 0 / 1 | 0 / 0 |
| 26 | Violencia doméstica | 209 | 2 / 3 | 0 / 0 (0) | 0 | 0 / 0 | 0 / 0 |
| 27 | Convivencia vecinal | 189 | 1 / 6 | 0 / 0 (0) | 0 | 2 / 2 | 0 / 4 |
| 28 | Agua y saneamiento | 392 | 1 / 5 | 2 / 9 (6) | 1 | 3 / 14 | 0 / 0 |
| 29 | Residuos y limpieza | 275 | 1 / 4 | 2 / 9 (6) | 1 | 1 / 4 | 0 / 0 |
| 30 | Ambiente y arbolado | 366 | 3 / 9 | 1 / 41 (7) | 2 | 2 / 8 | 0 / 1 |
| 31 | Animales | 361 | 3 / 5 | 0 / 0 (0) | 0 | 0 / 1 | 0 / 0 |
| 32 | Vivienda | 280 | 2 / 9 | 1 / 7 (2) | 0 | 0 / 0 | 0 / 0 |
| 33 | Espacio público y movilidad | 664 | 1 / 12 | 1 / 62 (17) | 6 | 3 / 15 | 0 / 4 |
| 34 | Cultura y patrimonio | 275 | 0 / 12 | 2 / 15 (3) | 1 | 1 / 2 | 0 / 0 |
| 35 | Deporte y recreación | 240 | 1 / 5 | 1 / 17 (3) | 2 | 1 / 2 | 0 / 0 |
| 36 | Economía local | 378 | 1 / 13 | 1 / 34 (2) | 2 | 0 / 0 | 0 / 4 |

Los votos de un tema que la capa remite a otro («Ver voto…») no están contados como propios.

## 4. Índice propuesto

**Preliminares.** Portada con el emblema, epígrafe y una nota breve al lector. El Resumen y el Abstract salen del cuerpo.

**Introducción. Lo local**

1. El valle y el cantón. Entra la Introducción actual. Falta la apertura con el valle de Vermissa de Doyle y el plan del libro.
2. Lo local en el artículo 169. Entra el párrafo del artículo 169 con Tocqueville, el pasaje del dictamen C-015-2013 y los artículos 1 y 4 del Código Municipal de la apertura de la sección 5. Falta casi todo: votos 5445-99 y 6469-97, artículo 170 y Ley N.° 8801, la lectura que el legislador hizo del 169 antes del Código (Aguas 1942, Construcciones 1949, Planificación Urbana 1968, Caminos Públicos 1972, salud 1973), la línea de la Procuraduría sobre lo local y la doctrina aportada.
3. La red: el régimen municipal como micelio. Todo por escribir.

**Primera parte. El concepto**

4. De la seguridad del territorio a la seguridad de la persona. Entran los dos primeros apartados de la sección 2. Falta el Manual de seguridad humana de las Naciones Unidas, el documento de la Contraloría sobre seguridad ciudadana y desarrollo social, y el artículo de Quirós, Acuña y Álvarez.
5. La cadena de normas. Entra «El derecho vigente: una cadena de normas», salvo el tramo del 169. Falta profundizar cada eslabón y dar referencia propia a la Ley N.° 10974.
6. Quién dice el derecho municipal y con qué fuerza. Entran los párrafos sobre los artículos 7, 8 y 9 de la LGAP, el 13 de la Ley N.° 7135, el 2 de la Ley N.° 6815 y el 29 de la Ley N.° 7428. Falta distinguir el dictamen vinculante para quien consulta de la jurisprudencia administrativa para las demás administraciones, y la vía contencioso administrativa.
7. El concepto. Entra la sección 3 hasta el pasaje de los 360 grados. Falta la clasificación de los deberes, la diferencia entre responder y garantizar todo resultado, y la justificación de los nueve temas por cuadrante.
8. Cómo se exige: las reglas de la jurisprudencia. Entran las ocho reglas. Falta mostrar cada caso, la parte de límites de la capa constitucional y el Tribunal Contencioso Administrativo.

**Segunda parte. La medida y los medios**

9. Lo que la ley manda medir. Entra la sección 4 hasta los artículos 144 y 146 del Código Municipal. Falta distinguir producto, resultado e impacto, y lo atribuible a una persona servidora.
10. Lo que hoy se mide. Entran los pasajes del IGSM, el ICN y la REDCUDI. Falta el IGSM completo con su rectificación, el ICN a fondo y la Contraloría sobre evaluación de resultados.
11. Con qué se cumple: los medios, y la sociedad pública de economía mixta. Todo por escribir salvo una oración del tema 36. El material está íntegro en el repositorio: Ley N.° 8828, diez pronunciamientos de la Procuraduría y los oficios 10500 y 11530 de la Contraloría.

**Tercera parte. Los treinta y seis temas**

12. La base común. Entra la apertura de la sección 5. Faltan las leyes de Construcciones, Planificación Urbana, Caminos Públicos y Aguas, y las Leyes N.° 8801 y 9329.

Cuadrantes I a IV, con su apertura y su cierre actuales. Cada tema es un capítulo con su número de tema, del 1 al 36.

**Cierre.** Conclusión (entra la sección 6), lo pendiente (los 360 grados no se inventan; consultas a la Procuraduría; la medición), referencias y, si el autor lo quiere, un anexo sobre cómo se armaron el inventario y el corpus.

## 5. Orden de cada tema

En prosa continua y siempre en el mismo orden: el caso de una persona; lo que manda la ley, con su verbo y su clase de deber; lo que dictaminaron la Procuraduría y la Contraloría; lo que resolvieron la Sala y el Tribunal, con hechos, razonamiento y orden; la regla que queda y lo que exige a una municipalidad; con qué medio puede cubrirse; lo que hoy se mide y el dato que la ley o la sentencia piden; lo pendiente.

Regla de profundidad propuesta: desarrollo completo para todo voto, toda resolución del Tribunal, todo documento de la Contraloría y todo dictamen de clase A; los de clase B, agrupados por línea, con al menos una cita textual por línea.

## 6. Documentos

Propuesta: una pestaña por capítulo o por tema, que es la unidad de exportación y de cotejo, y ninguna por encima de unas 12.000 palabras.

- Maestro: el enlace de siempre. Pestaña nueva con portada, índice con enlaces y estado del cotejo. La pestaña actual queda congelada como «Artículo, revisión 126».
- Introducción (capítulos 1 a 3).
- Primera parte (capítulos 4 a 8).
- Segunda parte (capítulos 9 a 11).
- Cuatro documentos de cuadrante; el primero lleva además el capítulo 12.
- Cierre y referencias.

Ajustes al taller que esto pide: `chk.py` por pestaña y un modo libro que una las referencias; primera mención en forma larga por capítulo; registro de las fuentes nuevas; que el verificador avise y siga cuando falte una fuente.

## 7. Fuentes nuevas

Pasajes ubicados, todavía sin pasar por el verificador.

| Fuente | Datos | Paginación | Estado |
|---|---|---|---|
| Sheldrake, M. (2020). *La red oculta de la vida* (T. Gras Cardona, trad.). Planeta | Libro electrónico, ISBN 978-84-08-23577-4 | Sin paginación de imprenta; el PDF aportado tiene 631 páginas | El autor decide: página del archivo, como Tocqueville, o edición impresa |
| Conan Doyle, A. (s. f.). *El valle del terror*. Fundación Carlos Slim | Sin traductor ni año | Folio impreso igual a página del archivo | Pasajes en pp. 18, 84 y 109 |
| Wilches-Chaux, G. (2007). Lo local-municipal como unidad de gestión. *Medio Ambiente y Urbanización*, (67), 113-126 | Revista de IIED-América Latina, Buenos Aires; número de noviembre de 2007, dedicado a cambio climático, vulnerabilidad y adaptación en ciudades de América Latina; ISSN 0326-7857. IngentaConnect lo cataloga como volumen 67, número 1 | Folios impresos 114 a 126; la primera página, sin folio, es la 113 | Listo para usar. El PDF no nombra la revista: el dato sale de los metadatos del archivo (título, autor, generado el 17 de enero de 2008), del catálogo de IngentaConnect y de una cita de terceros en el repositorio SEDICI de la UNLP. No se pudo abrir el índice del número. La EIRD publicó un capítulo 9 con el mismo título en *La gestión del riesgo de desastres hoy*; las páginas aportadas son las de la revista |
| Pérez Hernández, L., Tabares Neyra, L. M. y Díaz Legón, O. J. (2019). *Universidad de La Habana*, (287), 135-160 | Revista y número según el sitio de la revista (núm. 287, enero-junio de 2019) y SciELO Cuba | PDF aportado; folios impresos 135 a 160 | Las once citas, literales y con página: punto 10 |
| Quirós, B., Acuña, A. y Álvarez, C. (2007). *Ciencias Económicas*, 25(1), 199-217 | Completo | Folios impresos | Listo para usar |
| Naciones Unidas, Dependencia de Seguridad Humana (2016). *Manual de seguridad humana* | Completo | Folios impresos | Listo para usar |
| Contraloría General de la República (2025). Opiniones y sugestiones DFOE-GOB-OS-00001-2025 | Completo | Folios impresos | Listo para usar; efecto en cantones vecinos, pp. 34-35; evaluación de resultados, p. 42 |

Sheldrake, por página del archivo: red sin centro de control y fragmento que regenera la red, p. 54 (cap. 2); ramificación y fusión de hifas, p. 39 (cap. 1); fuente y sumidero, pp. 159-160 (cap. 6); organismos que son siempre sumideros, p. 160; reservas del autor sobre las metáforas, pp. 162-163, 173 y 175 (cap. 6).

Doyle: el concejal McGinty, p. 84; teorizar con datos insuficientes, p. 18; el valle, p. 109.

## 8. La imagen del micelio

Sirve para tres cosas: la red no tiene centro de control; las hifas se ramifican y se fusionan; los recursos se mueven de donde sobran a donde faltan.

Se rompe en cinco puntos. El micelio no tiene capital ni sede de gobierno, y Costa Rica es un Estado unitario con rectores nacionales. En el hongo el reparto sigue gradientes; en el derecho solo ocurre por ley, presupuesto o convenio. Hay organismos que solo toman de la red. Las municipalidades son personas jurídicas separadas, con electorado propio. Y una red no rinde cuentas, que es el centro del concepto. El propio Sheldrake enumera, sin adoptar ninguna, las lecturas de estas redes como socialismo, mercado o feudalismo (p. 173 del archivo), y escribe que las analogías con la política son limitativas (p. 175).

El único dato del corpus sobre conexión entre cantones es el de la Contraloría (2025), y se refiere a inversión social nacional, no a servicios municipales.

## 9. Faltantes y decisiones del autor

- Readjuntar la vista previa de ISO 18091 y Los Cabos (2020). Pele (2015) ya llegó (punto 10).
- PDF de Pérez Hernández, Tabares Neyra y Díaz Legón (2019): recibido (punto 10).
- Datos de publicación de Wilches-Chaux: resueltos por búsqueda (punto 7).
- Paginación de Sheldrake y uso de Doyle.
- Tamaño: con la regla de profundidad del punto 5, la estimación es de 140.000 a 190.000 palabras, frente a 28.300 de hoy. Un tomo o dos.
- Anexo sobre el inventario y el corpus, sí o no.
- La Ley N.° 10974 consta en el repositorio con fecha 7 de octubre de 2026; la fecha de publicación no se pudo confirmar.

## 10. Segunda entrega de material (22 de noviembre de 2026)

El autor aportó el PDF de Pele (2015), el PDF de Pérez Hernández, Tabares Neyra y Díaz Legón (2019) y el texto de SINALEVI de cuatro leyes: Aguas (N.° 276), Construcciones (N.° 833), Planificación Urbana (N.° 4240) y Caminos Públicos (N.° 5060). No respondió todavía sobre el índice ni sobre las decisiones del punto 9.

**Pele.** `preparar-taller.sh` lo procesó. Recotejo del texto vigente: 329 citas, 324 literales y ubicadas, 2 del IGSM verificadas a mano contra el informe (p. 2), 3 sin fuente en la sesión (ISO 18091, 2; Los Cabos, 1). Cero errores.

**Pérez Hernández, Tabares Neyra y Díaz Legón (2019).** El PDF trae folio impreso al pie, del 135 al 160; página impresa = página del archivo + 134. Recibido el 21/07/2018 y aceptado el 02/09/2018. El nombre de la revista y el número no figuran en el PDF: constan en el sitio de la revista (*Universidad de La Habana*, núm. 287, enero-junio de 2019: https://revistas.uh.cu/revuh/article/view/2718) y en SciELO Cuba. Las once citas de la nota del autor están literales:

| Cita | Página | Observación |
|---|---|---|
| A | 139 | Los autores exponen a Arocena (2001, pp. 22-24 y 65) |
| B | 139 | Igual que A |
| C | 142 | Se traslapa con D |
| D | 142 | Se traslapa con C |
| E | 142 | |
| F | 143 | |
| G | 144 | |
| H | 145 | |
| I | 145 | El párrafo cierra con remisión a García (2004, pp. 51-52) |
| J | 152 | La oración que sigue cierra con la remisión a Guzón (2016): la idea puede ser de esa autora |
| K | 153 | Nombra a Cuba |

Todas tienen 40 palabras o más, de modo que enteras van en bloque. Es doctrina sobre el municipio cubano: sirve para la teoría de lo local, no como autoridad sobre el derecho costarricense. En la p. 142 los autores advierten que las cuotas de poder del municipio son siempre una parcela del poder del Estado, lo cual sirve al límite de la imagen del micelio.

**Las cuatro leyes.** Coinciden artículo por artículo con las del repositorio, que guarda las mismas versiones de SINALEVI (276: 4 de 4; 833: 5 de 5; 4240: 9 de 9; 5060: 7 de 7). El texto de SINALEVI, igual en el repositorio y en lo pegado por el autor, trae dos lecturas que parecen erratas y que hay que copiar tal cual o dejar fuera de la cita: «las medidas necesarias pendientes a lograr» en el art. 13 de la Ley N.° 833 y «de las salud» en el art. 19 de la Ley N.° 4240. No se cotejaron contra la publicación original.

**Cambio normativo en curso.** La Ley N.° 10983, del 9 de noviembre de 2026, rige a partir del 1 de mayo de 2027. Reforma los arts. 20, 28, 99, 104 y 188 de la Ley de Aguas y toca otras diez leyes del cuerpo legal de los 36 temas: N.° 3859, 6227 (arts. 23 y 47), 7410, 7440, 7739 (art. 16), 9078 (art. 240), 9095, 9145, 9221 y 9552. Ninguno de los artículos que el libro cita hoy está entre los reformados. Toda cita nueva de esas leyes debe revisarse contra el texto que regirá. El repositorio tiene la Ley N.° 10983, pero su copia de la Ley de Aguas no trae la nota de SINALEVI que la anuncia.

**Pasaje por actualizar (tema 33).** El art. 4 de la Ley N.° 5060 fue reformado por la Ley N.° 10343, del 29 de marzo de 2023, vigente desde el 12 de abril de 2023: exceptúa del ancho mínimo las rutas y calles públicas ya reconocidas, inventariadas, codificadas y georreferenciadas, «para su debida intervención, conservación, mejoramiento y rehabilitación». El libro cita dos veces el oficio 22430 (DFOE-LOC-2366) de la Contraloría, del 12 de diciembre de 2022 (pp. 5 y 6), que razona sobre el texto anterior y sobre el dictamen C-234-2022. No cita la Ley N.° 5060, la Ley N.° 10343 ni la línea de la Procuraduría, que está íntegra en el repositorio:

- C-234-2022, del 30 de octubre de 2022 (Atenas): sin autorización legal para usar recursos de la Ley N.° 8114 en caminos vecinales de menos de catorce metros, pero sí con otras fuentes, porque lo contrario «sería condenar al abandono a la red vial cantonal» (conclusiones e y f). Capa administrativa: clase B.
- C-133-2024, del 24 de junio de 2024 (San Isidro de Heredia): tras la reforma, los caminos ya declarados que no cumplan el ancho pueden ser intervenidos con los recursos de la Ley N.° 8114 (conclusión 1); el plan regulador no puede fijar para los caminos vecinales una medida distinta de la legal, pero sí la de las calles locales (conclusiones 3 y 4). Capa: clase B.
- C-286-2024, del 9 de diciembre de 2024 (Bagaces): consulta inadmisible; remite al C-133-2024 y transcribe sus conclusiones. No está en la capa.
- C-014-2026, del 23 de enero de 2026 (Zarcero): integración de la red vial cantonal y licencia de construcción con acceso a vía de ancho menor, condicionada a lo que disponga el plan regulador. No está en la capa.
- C-184-2026, del 19 de octubre de 2026 (Upala): es posible reconocer y certificar rutas cantonales de menos de catorce metros al amparo de la Ley N.° 10343, si constaban en los registros al 12 de abril de 2023 (conclusión 3). Su conclusión 1 dice «artículo 14» donde corresponde el 4. Capa: clase B.

**Punto ciego del inventario.** El inventario no declara con qué términos se armó. En las leyes que contiene hay 14 artículos, en 12 leyes, que dicen «municipio» sin ninguna otra voz de la familia y que el inventario no trae; tres son de la Ley de Aguas (arts. 20, 93 y 122). El art. 93 faculta al municipio para desecar terrenos pantanosos declarados insalubres. Conteo automático, sin revisión artículo por artículo fuera de la Ley de Aguas.

**Artículos de las cuatro leyes que entran al libro**

| Ley | Artículos | Dónde |
|---|---|---|
| Planificación Urbana (1968) | 15 (deriva del art. 169 de la Constitución la competencia de planificar y controlar el desarrollo urbano); 1 y 19 (seguridad, salud, comodidad y bienestar de la comunidad) | Capítulo 2 |
| | 62 (convenios entre municipalidades contiguas); 63 a 65 (órgano intermunicipal del Área Metropolitana, con aporte de diez municipalidades, Escazú entre ellas) | Capítulos 3 y 11 |
| | 16 (contenido del plan regulador); 17 (audiencia pública); 25 y 58 inciso 5 (áreas inundables y peligrosas); 28 y 29 (certificado de uso y patentes); 39 (la municipalidad queda obligada a ejecutar las obras); 40 (parques y juegos infantiles: diez metros cuadrados por familia); 43 a 45 (dominio municipal y cambio de destino) | Capítulo 12 y temas 6, 15, 21, 32, 33, 35 y 36 |
| Construcciones (1949) | 1 (seguridad, salubridad, comodidad y belleza); 13 (tránsito de vehículos y peatones fácil, cómodo y seguro) | Capítulos 2 y 12, temas 5 y 33 |
| | 83 (convenios de apoyo técnico con las municipalidades más cercanas para el control constructivo; párrafo agregado por la Ley N.° 9482, de 2017) | Capítulos 3 y 11 |
| | 4 a 7 (vía pública); 14 (predio abandonado, insalubre, inseguro o molesto); 29 a 33 (anuncios); 37 a 41 (parques y jardines, con los animales que viven en ellos); 60 a 67 (lugares de reunión y uso peligroso); 68 a 73 (establecimientos molestos y malsanos); 74, 83 bis, 87 a 96 (licencia, vigilancia y sanciones) | Temas 1, 4, 6, 18, 27, 29, 30, 31, 32, 33 y 35 |
| Caminos Públicos (1972) | 1 y 2 (red vial cantonal y propiedad municipal de las calles); 3 (calles que una carretera nacional toma al cruzar una población, previa consulta con la municipalidad); 4 (ancho y excepción de 2023) | Capítulo 12, temas 5 y 33 |
| | 2 bis y 2 ter (obstáculos, alcantarillas, muros y puentes en cauces); 19 (toda construcción frente a caminos vecinales y calles requiere aprobación escrita de la municipalidad); 20 y 21 (desagües y vegetación a cargo de los poseedores, a requerimiento municipal); 28 (ocupación del derecho de vía); 32 y 33 (reapertura de un camino cerrado en plazo no mayor de tres días) | Temas 4, 5, 6, 17, 28, 30 y 33 |
| | 12 (detalles de caminos según las necesidades del cantón, con prioridad a los distritos más necesitados) | Capítulos 7 y 9 |
| Aguas (1942) | 41 (cañerías a cargo de las municipalidades); 27 y 34 (preferencia de las poblaciones y cincuenta litros diarios por habitante, veinte de ellos potables); 37 (bocas contra incendios) | Tema 28 y capítulo 10 |
| | 70 (deber de las municipalidades de colaborar en la vigilancia y el control de la extracción de materiales en cauces); 145 y 154 a 157 (árboles, tierras municipales en márgenes de ríos y reforestación sin pérdida de tiempo) | Temas 30 y 36 |
| | 93 (desecación de terrenos insalubres por el municipio); 186 a 198 (inspector cantonal de aguas, censo de aprovechamientos y conflictos entre vecinos) | Temas 1, 27 y 28 |
