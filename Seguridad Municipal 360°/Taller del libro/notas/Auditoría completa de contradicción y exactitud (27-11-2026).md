# Auditoría completa de contradicción y exactitud (27 de noviembre de 2026)

Sustituye en alcance a la auditoría parcial del mismo día. Se revisó el libro entero: introducción, capítulos 1 a 4, los 36 temas, la conclusión y los anexos.

## 1. Citas textuales: literalidad y ubicación

**Cómo se hizo.** Se reconstruyeron los 43 textos con el verificador.

- Cada cita textual se buscó en su fuente local.
- Se comprobó que estuviera en el artículo, considerando, apartado o página citados.
- El tema 20 no se podía reconstruir porque faltaba el texto local de la estructura programática de la CGR. Se regeneró desde el PDF del repositorio, y su salida coincide con la publicada.

**Resultado.**

| Situación | Citas |
|---|---|
| Total en el libro | unas 2.100 |
| Literales, en el lugar citado según el cotejo automático | unas 1.930 |
| Ubicación forzada a mano, re-verificadas una por una | 94 |
| Literales, sin página que cotejar (publicación de la PGR) | 4 |
| Sin copia local de la fuente | 74 |
| No literales | 0 |

**Las 94 ubicaciones forzadas a mano.** Se ubicó cada una en el texto de su fuente, una por una, y todas están donde se citan.

- Los casos que parecían dudosos eran transcripciones de votos anteriores dentro del considerando citado. Por ejemplo, 2024-023302, 2020-016680 y 2025-016121.
- En el voto 2024-029734, cada pasaje aparece dos veces: en el resultando (informe de la Procuraduría) y en el considerando citado. El libro cita el considerando.

**Hallazgo 1: páginas de las fichas del IGSM 2025.** La página impresa es la del PDF menos uno, por la portada. El libro cita la página impresa, pero el verificador comparaba con la página del PDF.

- Por eso cinco citas del tema 29 usaban la numeración del PDF:
  - dos citas textuales con p. 15, que es la p. 14;
  - una cita textual con p. 8, que es la p. 7;
  - dos paráfrasis con p. 7, que es la p. 6;
  - dos paráfrasis con p. 8, que es la p. 7.
- Todas se corrigieron.
- El verificador ahora aplica la diferencia de una página (`hacer_build_libro.py`).
- Se revisaron con `audita_igsmf.py` todas las citas de las fichas, textuales y paráfrasis. Las 23 citas textuales quedan en la página impresa. Fuera del tema 29 no hay otro desfase: el caso del tema 5 (p. 74, puentes) es correcto.

**Hallazgo 2: fuentes sin copia local.** Algunas se consiguieron y cotejaron en esta auditoría, sin subirlas al repositorio:

| Fuente | Resultado |
|---|---|
| Zaratiegui (1999) | 7 citas, literales y en página |
| Medina León et al. (2009) | 8 citas, literales y en página |
| Bendell et al. (1993), citado en Medina León | 1 cita, literal y en página |
| Vílchez y Sánchez (2021) | 2 citas, literales y en página |
| OPS (s. f.) | 1 cita, literal, en la p. 2 |
| Naciones Unidas (2016) | 4 citas, confirmadas en las pp. 5, 6, 6 y 10 por consulta al PDF oficial |

Quedan sin cotejo:

| Fuente | Citas | Por qué |
|---|---|---|
| Sheldrake (2020) | 16 | libro con derechos, sin copia |
| Cortés García (2026) | 12 | obra del autor |
| Conan Doyle (s. f.) | 12 | edición de la Fundación Carlos Slim |
| Pérez Hernández et al. (2019) | 8 | sin copia |
| Wilches-Chaux (2007) | 3 | sin copia |

**Hallazgo 3: introducción.** La cita del artículo 62 original del Código Municipal no tiene fuente local. El autor la aportó desde el SCIJ, versión 1 de 6. Sigue pendiente confirmarla.

## 2. Word contra fuente verificada

Se comparó con `audita_word.py` cada párrafo del Word con el texto verificado de su capítulo o tema, incluidas las referencias.

- Coinciden todos.
- La única excepción es la leyenda de la figura 6, que solo existe en el Word.
- Dos referencias del Tribunal Contencioso (temas 29 y 36) traen en el Word el enlace a NexusPJ y en la fuente no. El Word está más completo; no es un error.
- No hay la misma fuente citada con datos distintos en dos capítulos: votos, dictámenes, leyes y oficios tienen siempre la misma fecha y hora.

## 3. Paráfrasis de artículos

Se cribaron con `audita_parafrasis.py` las 2.032 oraciones que parafrasean un artículo sin cita textual. Para cada una se midió cuánto vocabulario comparte con el artículo citado.

- Se revisaron a mano las 70 de menor coincidencia. Todas están bien atribuidas.
- La baja coincidencia se debe a oraciones con varias citas o a artículos de remisión.
- Diez artículos no se localizaron por un defecto de las fuentes, no del libro:
  - la Ley 9028 escribe «ARTÍTULO 33»;
  - la Ley 6227 escribe «Artículos 274»;
  - las leyes aprobatorias de tratados (4534 y 7184) no separan los artículos del tratado;
  - el resto son macros agrupadas.

## 4. Tesis de los 36 temas

Cada tesis se contrastó con la síntesis «Cómo hace el gobierno local…» y con la conclusión de su tema.

| Tema | Problema | Corrección |
|---|---|---|
| 15 | Generalizaba: cualquier audiencia o consulta sería condición de validez | Solo la audiencia del plan regulador y la consulta pública de los reglamentos |
| 18 | Cubría solo al vendedor callejero | Ahora cubre las cuatro vías del tema: licencia, acera, mercado y empleo |
| 33 | Cubría solo la acera | Ahora cubre el espacio público: recibirlo, ordenarlo y mantenerlo |

Las otras 33 tesis son coherentes con su tema.

## 5. Coherencia entre capítulos

- **Definición de lo local.** Aparece con las mismas palabras en el cap. 3 y en la conclusión.
- **Tesis de la introducción.** Remiten a los lugares donde se demuestran. Por ejemplo, la regla de la escasez está en el cap. 4, en el cap. 3 y en la conclusión.
- **Remisiones de los capítulos a los temas.** Son 50, y cada caso aludido está en el tema indicado.
- **Regla de la «Sala».** No hay ningún «la Sala» que pueda leerse como la Sala Primera.
- **Otras comprobaciones.** No aparece «Sala IV». No hay autocitas en tercera persona. No hay comillas sin fuente.

## 6. Pendiente de estilo: más de dos citas por oración

Hay 205 oraciones con tres o más citas, en 30 capítulos y temas. La lista completa está en `notas/Oraciones con más de dos citas (27-11-2026).tsv`.

- No contienen errores de exactitud.
- Incumplen la regla de estilo del libro.
- Los temas 10 a 14, 18, 28 y 31 a 34 ya no tienen ninguna.
- Corregirlas exige partir cada oración, así que queda para una pasada dedicada.

## 7. Límites

- El cotejo de las paráfrasis es un cribado automático. Las 1.960 de mayor coincidencia no se leyeron una por una.
- Las citas de las cinco fuentes sin copia necesitan que el autor aporte los textos.
