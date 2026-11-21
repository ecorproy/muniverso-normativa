# Muniverso — Normativa costarricense

Repositorio de normas y dictámenes en Markdown, cada uno con su ficha (número, nombre, estado, versión de SINALEVI, fecha y enlace oficial). Lo usa la app Muniverso.

## Organización

- **Leyes y decretos nacionales/** (456 documentos): leyes, códigos, decretos ejecutivos y tratados, por materia.
- **Leyes locales/** (108 documentos): leyes de patentes, impuestos municipales y licencias comerciales, por provincia y cantón.
- **Reglamentos municipales/** (4311 documentos): reglamentos de cada municipalidad y concejo municipal de distrito, por provincia y cantón; los de federaciones, UNGL e IFAM van en «Entes intermunicipales».
- **Jurisprudencia constitucional (Sala Constitucional)/**: sentencias de la Sala Constitucional bajadas de NexusPJ (texto anonimizado por el Poder Judicial), por tema.
- **Jurisprudencia administrativa (PGR)/** (1945 documentos): dictámenes de la Procuraduría General de la República, por área temática.

## Contenido

### Leyes y decretos nacionales

- Administrativo: 64
- Agrario: 1
- Ambiental: 29
- Civil: 4
- Comercial: 1
- Constitucional: 44
- Derechos humanos: 1
- Electoral: 4
- Familia: 3
- Hacienda pública: 21
- Internacional: 13
- Laboral: 41
- Municipal: 152
- Penal: 14
- Seguridad social: 9
- Servicios públicos: 31
- Social: 12
- Tributario: 12

### Leyes locales

- Alajuela: 21
- Cartago: 10
- Guanacaste: 17
- Heredia: 14
- Limón: 6
- Puntarenas: 16
- San José: 24

### Reglamentos municipales

- Alajuela: 554
- Cartago: 524
- Entes intermunicipales: 113
- Guanacaste: 375
- Heredia: 575
- Limón: 341
- Puntarenas: 723
- San José: 1106

### Jurisprudencia administrativa (PGR)

- 01 Autonomía y régimen municipal: 224
- 02 Concejo Municipal: 99
- 03 Alcaldía: 30
- 04 Organización administrativa: 77
- 05 Legalidad, reglamentos y procedimiento: 216
- 06 Planificación y participación ciudadana: 39
- 07 Presupuesto municipal: 62
- 08 Tributación municipal: 127
- 09 Contabilidad, tesorería y patrimonio: 61
- 10 Contratación pública: 29
- 11 Empleo público municipal: 430
- 12 Servicios municipales: 37
- 13 Gestión ambiental: 27
- 14 Ordenamiento territorial y urbanismo: 144
- 15 Infraestructura vial y obra pública: 51
- 16 Catastro, valoración y bienes inmuebles: 29
- 17 Licencias comerciales y desarrollo económico: 53
- 18 Seguridad y gestión del riesgo: 24
- 19 Desarrollo social, cultura y deporte: 43
- 20 Control interno, probidad y transparencia: 105
- 21 Gobierno digital y gestión documental: 38

## Criterios

- Normas: última versión publicada en SINALEVI al momento de la descarga; se excluyen las derogadas y las reformas sueltas (cada norma base ya las incorpora).
- Reglamentos municipales: cuando un cantón tiene dos reglamentos de la misma materia sin derogatoria expresa, rige el más reciente.
- Dictámenes: texto completo tomado del SCIJ/SINALEVI; la ficha indica número, fecha, institución consultante y temas.

## Actualización automática desde La Gaceta

Todos los días a las 06:00 (hora de Costa Rica) el proceso `.github/workflows/gaceta-diaria.yml` lee La Gaceta y sus Alcances en el sitio de la Imprenta Nacional. Detecta las leyes sancionadas (`DECRETO LEGISLATIVO N.º …`) y las leyes que esas leyes reforman, adicionan o derogan, y baja de SINALEVI la versión vigente de cada una.

- Si la ley ya está en el repositorio y SINALEVI tiene una versión más reciente, reemplaza el archivo.
- Si no está, la agrega en `Leyes y decretos nacionales/<Materia>/Ley N.md`.
- Si SINALEVI todavía no incorpora la ley o la reforma, la deja en `herramientas/leyes_pendientes.json` y la reintenta cada día, hasta por 15 días.
- `herramientas/ultimo_informe.md` resume la última actualización.

También se puede ejecutar a mano desde la pestaña **Actions → La Gaceta diaria → Run workflow**. Las apps de Muniverso reciben los cambios con la sincronización normal de la biblioteca.
