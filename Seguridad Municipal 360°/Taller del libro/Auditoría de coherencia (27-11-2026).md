# Auditoría de coherencia e incongruencia (27 de noviembre de 2026)

Alcance: los cambios de los Word final45 a final48 (familias de puestos, orden proceso → proyecto → servicio → producto, Ortíz-Fernandez et al., 2024, pregunta del libro, artículo 28 y planificador institucional) y su efecto en el resto del libro. Se revisaron las 41 fuentes del taller (capítulos 1 a 4, temas 1 a 36 y conclusión), las 16 figuras, el documento de Docs y el Word. Resultado: Word final49, fuentes y Docs coinciden; las pestañas tocadas cotejan IDÉNTICO.

## Hallazgos y lo que se hizo

| N.° | Hallazgo | Tipo | Estado |
| --- | --- | --- | --- |
| 1 | Los cambios de los finales 45 a 48 se habían hecho solo en el Word; las fuentes del capítulo 4 y de la conclusión y el documento de Docs seguían con el texto anterior. | Desfase entre versiones | Corregido: fuentes con macros actualizadas, verificadas y publicadas en Docs |
| 2 | Conclusión, «Lo que se repite en los temas»: «y un servicio solo se presta a alguien» repetía la tesis anterior, ya retirada del capítulo 4. | Contradicción de fondo | Corregido: «el servicio se presta a alguien, y el producto es lo que esa persona recibe» |
| 3 | Figura 11 («La calificación»): «metas anuales de productos y servicios» en la voz del libro. | Incongruencia con el orden adoptado | Corregido y regenerado |
| 4 | Capítulo 4, «De ese mismo deber…»: la jefatura asignaba «sus productos y plazos», sin los servicios. | Incongruencia con el orden adoptado | Corregido: «sus servicios, productos y plazos» |
| 5 | Capítulo 4, «En una municipalidad estas reglas…»: «En ese mismo voto» remitía a un voto citado varios párrafos antes, con una forma de cita secundaria que el verificador no puede cotejar. | Remisión y cita | Corregido: «En el voto que examinó el proyecto de la Ley Marco» y cita al C-136-2026 |
| 6 | Capítulo 4, «La frontera…»: entre la cita textual del voto 2021-017098 y su macro había texto, y el verificador la marcó como comillas sin fuente. | Cita | Corregido: «Según transcribe el reglamento de la ley, …» y la macro pegada a las comillas |
| 7 | Primera mención de la Ley 8131: la forma completa aparecía en el segundo uso. | Formato de cita | Corregido en el final48; el generador lo confirma |
| 8 | Docs: figuras 5, 9, 10, 11 y 13 con las imágenes anteriores; leyenda de la figura 13 con el título viejo. | Desfase | Corregido: imágenes nuevas como blobs, leyenda e índice al día |

## Lo que se conserva a propósito

- «Productos y servicios» se mantiene cuando el texto refiere lo que dice la ley: el título de la sección «Productos y servicios prestados», cuatro pasajes del capítulo 4, uno del capítulo 3, la figura 8 (que transcribe el art. 47 de la Ley 2166) y todas las citas textuales. En la voz del libro el orden es «servicios y productos».
- En los 36 temas no se encontró la fórmula vieja, ni «producto interno», ni «a quién se le prestó».

## Cotejo contra fuentes

- Capítulo 4: 154 citas textuales. Todas las nuevas quedaron cotejadas contra su fuente: Ley 10159 (arts. 6, 7, 13, 28, 29, 32 y 33); Código Municipal (arts. 13, 17, 124, 129 y 156); CP, art. 169; LGAP, art. 133; Ley 8131 (arts. 4 y 5); Ley 5525, art. 3; dictámenes C-136-2026 (ap. IV y V), C-078-2025 (conclusión) y C-016-2024 (ap. II); Decreto Ejecutivo 43952 (considerando IX, búsqueda literal); y Ortíz-Fernandez et al. (2024), pp. 8, 9, 12, 13, 18 y 19, contra el texto paginado de la revista.
- Conclusión: 21 citas, 0 errores.
- Sin cotejo posible en esta sesión, porque no hay archivo local: voto 2025-008201 y doctrina con derechos de autor que no se guarda en el repositorio (Zaratiegui, Medina León, Vílchez Ordoñez y Sánchez Davila, Cortés García). Son citas que ya estaban, verificadas en sesiones anteriores, y no cambiaron.
- Exportaciones de Docs (sha256 y bytes contra `esperado_fig.py`): capítulo 3, capítulo 4 y conclusión IDÉNTICO.

## Pendientes

1. Voto 2021-017098: fecha cotejada en NexusPJ (31 de julio de 2021, 23:15 horas, expediente 21-011713-0007-CO); el C-136-2026 la da como 1 de julio. Falta el texto completo del voto para pasar de cita indirecta a cita directa.
2. El Word no puede rearmarse desde las fuentes porque `post.py`, `ref.docx` y el logo no están en el repositorio. Por eso se corrige directamente. Conviene guardar ese juego de armado en la rama.
3. Ley 5525: el texto la usa solo para decir que el sistema incluye las unidades de planificación locales. La ley no obliga a la municipalidad a crear una (su art. 12 nombra ministerios e instituciones autónomas y semiautónomas).
