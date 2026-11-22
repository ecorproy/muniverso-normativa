# Taller del libro Seguridad Municipal 360°

Programas y bitácora con que se escriben y se verifican los capítulos del libro. Complementa el `Taller de cotejo` del artículo, que está en esta misma carpeta y cuyos programas base (`scripts/`) siguen siendo necesarios.

## Qué hay

- `scripts/`: programas propios del libro. Los principales:
  - `hacer_build_libro.py` genera `build_libro.py` (el verificador) y `cite_libro.py` a partir de `Taller de cotejo/scripts/build.py` y `cite.py`.
  - `build_libro.py` expande las macros de cita de un capítulo (`[[V:…]]`, `[[D:…]]`, `[[L:…]]`, `[[DE:…]]`, `[[O:…]]`, `[[T:…]]`, `[[S1:…]]`, `[[RM:…]]`) y coteja cada cita textual contra su fuente: literalidad y ubicación. No coteja paráfrasis.
  - `nexus2md.py`, `nexus2md_otros.py`, `pgr2md.py` y `sinalevi2md.py` convierten textos pegados de NexusPJ y SINALEVI al formato del repositorio.
  - `cmp_pegado.py` compara una norma pegada con la copia del repositorio; `escanear_ley.py` lista los artículos de una ley que contienen un patrón; `intensidad.py` lista las afirmaciones absolutas de un capítulo que están fuera de las citas; `esperado.py` compara la pestaña publicada con la salida verificada.
- `Bitácora del taller.md`: estado de cada capítulo, reglas del autor, método y mecánica de publicación.

## Dónde están las fuentes

Los textos íntegros están en la rama `main` de este repositorio: leyes y decretos, votos de la Sala Constitucional, dictámenes de la Procuraduría, sentencias del Tribunal Contencioso Administrativo y de la Sala Primera, y reglamentos municipales. Los criterios de la Contraloría y el Índice de Gestión de Servicios Municipales están en `Criterios CGR`, en esta rama.

## Cómo rearmar el taller en una sesión nueva

Los programas usan rutas fijas. Hay que dejar:

- la rama `main` clonada en `/home/claude/repo/main` y esta rama en `/home/claude/repo/360`;
- `Taller de cotejo/scripts/` copiado en `/home/claude/scripts/` (lo hace `Taller de cotejo/preparar-taller.sh`);
- `Taller del libro/scripts/` copiado en `/home/claude/mis_scripts/`.

Después se corre `python3 -I /home/claude/mis_scripts/hacer_build_libro.py`. Cada capítulo se verifica desde `/home/claude/art` con `SRC=<carpeta>/src OUT=<carpeta>/out python3 -I /home/claude/mis_scripts/build_libro.py`.

Los capítulos no están aquí. Viven en los documentos del autor; `deexp_libro.py` devuelve un texto publicado a su forma con macros.
