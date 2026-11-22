# Taller de cotejo

Herramientas con que se verifica, letra por letra, cada cita textual del libro *Seguridad Municipal 360°*. Se guardan aquí porque el espacio de trabajo en que corren es temporal: muere al cerrarse la sesión, y sin él no hay forma de cotejar nada.

La regla que hacen cumplir es una sola: ninguna cita entra al libro si no se copió del texto íntegro y se ubicó con precisión (artículo, considerando, conclusión, página). Lo que no se puede ubicar, se deja fuera.

## Estado al 22 de noviembre de 2026

- Documento vivo del libro: `https://claude.ai/artifact/DzwAPMmiL2Kd1tDFsiDfy5` (revisión 126).
- 329 citas textuales. 327 cotejadas contra su fuente íntegra con localización verificada.
- 2 sin cotejar contra el original: las del Índice de Gestión de Servicios Municipales 2025 de la CGR, conocido solo por reproducción parcial en vLex. Van sin página. Ver la ficha en `../Referencias externas/`.
- 171 referencias, una por fuente citada y ninguna sin cita.
- Formas de cita canónicas, verificadas por comparación automática.

La bitácora completa, con las decisiones tomadas y lo que queda pendiente, está en `NOTAS.md`.

## Contenido

| Archivo | Qué es |
| --- | --- |
| `NOTAS.md` | Bitácora de trabajo: directrices del autor, estructura, estado por revisión, material hallado, pendientes. Se lee primero. |
| `all.md` | El texto del libro con las citas reducidas a macros (`V:`, `L:`, `D:`, `T:`, `O:`, `DE:`). Es la forma en que el verificador lo procesa. |
| `citas verificadas.json` | Registro de las 329 citas: fuente, localización, número de palabras, estado del cotejo. |
| `overrides.json` | Localizaciones verificadas a mano que el buscador automático no acierta. |
| `refs/` | Fichas de leyes (`leyes.json`), de jurisprudencia (`juris.json`) y referencias en APA (`refs.md`). |
| `articulo-src/` | Secciones de la versión 2 del artículo, en macros. Quedan como archivo de citas ya verificadas. |
| `scripts/` | Los programas. |

## Los programas

Todos se corren con `python3 -I`.

**Cotejo**

- `chk.py <archivo exportado>` es la entrada principal. Toma la exportación del documento, la decodifica, convierte las citas a macros, corre el verificador y reporta: citas con error, diferencias entre la forma de cita del documento y la canónica, y qué referencias faltan o sobran.
- `build.py` es el verificador. Busca cada cita en el texto íntegro de su fuente, comprueba que esté literal y que la localización indicada la contenga, y genera la lista de referencias en APA 7. No se corre solo; lo llama `chk.py`.
- `deexp.py` convierte el texto con citas expandidas en texto con macros.
- `cmpdoc.py` compara dos versiones del texto.

**Consulta de fuentes**

- `cite.py "V:2020-020109:considerando III" "L:8839:art. 8" "D:C-015-2013:conclusión" "T:2015-000321:considerando IV" "O:14908:p. 13" "DE:43952:art. 28"` imprime la cadena de cita exacta. Para votos da la forma larga de primera mención y la corta.
- `arts.py LEY art…` imprime el texto literal de un artículo (variable `L` para el largo máximo).
- `concl.py C-043-2016 …` imprime conclusiones de dictámenes.
- `cons.py`, `ctx.py`, `pas.py`, `q.py`, `loc.py` buscan considerandos, contexto y pasajes.
- `leyes.py`, `refs.py` mantienen las fichas de `refs/`.

**Edición del documento**

- `blocks.py <archivo de lectura>` convierte una lectura del documento en un mapa de bloques (`blocks.json`), que es lo que permite editar por identificador.
- `sec.py DESDE HASTA` lista los bloques de una sección.
- `refplan.py` cruza el mapa de bloques con el delta de referencias y escribe las operaciones de inserción y borrado que hay que enviar.

## Cómo rearmar el taller en una sesión nueva

Correr `preparar-taller.sh`. Reconstruye la estructura de carpetas que los programas esperan por ruta absoluta:

```
/home/claude/scripts/          los programas
/home/claude/art/              NOTAS.md, overrides.json, src/, src3/, out3/
/home/claude/refs/             leyes.json, juris.json, refs.md
/home/claude/repo/main/        este repositorio, rama main (normativa y jurisprudencia)
/home/claude/repo/360/         este repositorio, rama seguridad-municipal-360
/home/claude/cgr/              textos extraídos de los documentos de la CGR
/home/claude/export/           exportaciones del documento
```

Lo que el script no puede reponer son los textos de obras ajenas que no se guardan en este repositorio, por ser público. Cada una tiene su ficha en `../Referencias externas/`, con su enlace y las páginas de las que se tomó cada cita. El script baja las que tienen enlace abierto y deja dicho cuáles hay que volver a aportar.

## Si se cambia una cita del libro

El orden es siempre el mismo, y no admite atajos:

1. Escribir el pasaje en el documento con la cita ya expandida.
2. Exportar el documento en markdown.
3. Correr `chk.py` sobre la exportación.
4. Corregir lo que reporte: citas que no están literales, localizaciones que no contienen la cita, formas de cita no canónicas, referencias que faltan o sobran.
5. Repetir hasta que no haya errores y las referencias coincidan con las generadas.

Una cita que no pasa el paso 4 no se arregla cambiando la cita: se quita, o se busca bien la fuente.
