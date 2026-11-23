# Taller del libro Seguridad Municipal 360°

Capítulos, programas y bitácora con que se escribe y se verifica el libro. Complementa el `Taller de cotejo` del artículo, que está en esta misma carpeta y cuyos programas base (`scripts/`) siguen siendo necesarios.

## Qué hay

- `Capítulos/`: cada capítulo escrito, en su carpeta (`cap02` y `t01` a `t36`).
  - `src/`: la fuente con macros de cita (`[[V:…]]`, `[[D:…]]`, `[[L:…]]`…). Es el texto que se edita.
  - `out/`: la salida del verificador: el capítulo con las citas expandidas (es el texto publicado), `zz_referencias.md` (lista de referencias en APA 7), `zz_informe.txt` (resultado del cotejo de cada cita textual) y `zz_citas.json`.
  - `cap02` trae además la plantilla, el espejo y los bancos de citas con que se armó.
  - El tema 19 está en versión 2, verificada y todavía sin publicar. Los temas 20 a 27 no están escritos.
- `scripts/`: programas propios del libro. Los principales:
  - `hacer_build_libro.py` genera `build_libro.py` (el verificador) y `cite_libro.py` a partir de `Taller de cotejo/scripts/build.py` y `cite.py`.
  - `build_libro.py` expande las macros de un capítulo (`[[V:…]]`, `[[D:…]]`, `[[L:…]]`, `[[DE:…]]`, `[[O:…]]`, `[[T:…]]`, `[[S1:…]]`, `[[RM:…]]`) y coteja cada cita textual contra su fuente: literalidad y ubicación. No coteja paráfrasis.
  - `seg.py` muestra la estructura de un voto y el texto de un considerando o del por tanto; `conc.py` imprime las conclusiones de un dictamen; `tema.py` lo que el cuerpo legal y las capas asignan a un tema; `intensidad.py` las afirmaciones absolutas fuera de las citas; `hbloques.py` compara los bloques publicados con la salida; `esperado.py` compara la pestaña publicada con la salida verificada.
  - `nexus2md.py`, `nexus2md_otros.py`, `pgr2md.py` y `sinalevi2md.py` convierten textos pegados de NexusPJ y SINALEVI al formato del repositorio.
- `fuentes/`: texto de los oficios de la Contraloría que usa el verificador (extraído de los PDF del repositorio).
- `notas/`: pendientes, ajustes de ubicación verificados a mano (`overrides_libro.json`), reemplazos de redacción, propuesta de índice y coberturas.
- `Bitácora del taller.md`: estado de cada capítulo, reglas del autor, método, mecánica de publicación y lo que no se usó.
- `preparar-libro.sh`: rearma el taller en una sesión nueva.

## Dónde están las fuentes

Los textos íntegros están en la rama `main` de este repositorio: leyes y decretos, votos de la Sala Constitucional, dictámenes de la Procuraduría, sentencias del Tribunal Contencioso Administrativo y de la Sala Primera, y reglamentos municipales. Los criterios de la Contraloría, el Índice de Gestión de Servicios Municipales y el Índice de Competitividad Nacional están en `Criterios CGR` y `Referencias externas`, en esta rama.

No se guardan aquí los textos de doctrina con derechos de autor (Pérez Hernández, Tabares Neyra y Díaz Legón, 2019; Wilches-Chaux, 2007; ISO 18091; Pele; Los Cabos). Para volver a verificar el capítulo 2 hay que adjuntar esos PDF.

## Cómo rearmar el taller en una sesión nueva

1. `bash "Seguridad Municipal 360°/Taller de cotejo/preparar-taller.sh"` (clona las dos ramas en `/home/claude/repo` y deja los programas base en `/home/claude/scripts`).
2. `bash "/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/preparar-libro.sh"` (deja los programas en `/home/claude/mis_scripts`, los capítulos y las fuentes en `/home/claude/libro` y genera el verificador).
3. Cada capítulo se verifica desde `/home/claude/art` con `SRC=/home/claude/libro/<capítulo>/src OUT=/home/claude/libro/<capítulo>/out python3 -I /home/claude/mis_scripts/build_libro.py`.

Los capítulos publicados viven en los documentos del autor en Claude; los identificadores de cada documento y pestaña están en la bitácora.
