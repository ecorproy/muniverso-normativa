# Pendientes inmediatos (22 nov. 2026, tarde). Leer primero si se compacta el contexto.

## Instrucciones del autor de esta tanda (en orden)
1. Mandó Ley 7788, 8436, 8799, 7451, 9458, 8495 (adjuntos) y pegó Ley 10141 y Ley 10812 mirando la pestaña 31, con: «ojo para lo que realmente es esa ley» (la 10141; tenía seleccionado «Ley N.° 10141» en el párrafo de «Con qué medio puede cubrirse»).
2. «otra cosa no puedes andar diciendo unico reglamento, acaso los revisamos todos, baja la intensidad con afirmaciones estúpidas». Regla nueva para todo el libro: nada de «único/un solo/el primero/se adelantó/la más antigua/no se mide/ninguno» sobre el universo de fuentes o de municipalidades. Programa: `/home/claude/mis_scripts/intensidad.py <src>` lista los absolutos fuera de comillas.
3. «sube a github todo lo posible para dejar de depender de buscar online». Pedido expreso de subir.
4. Mandó cinco dictámenes sobre tasas (art. 83 del Código Municipal): PGR-C-050-2026 (Puriscal, tasa de residuos a todos los predios, sin tarifa por uso), C-202-2014 (FEDOMA, limpieza de vías = red vial cantonal; «(Aclarado)»; no estaba en el repositorio), PGR-C-245-2024 (Sarchí), PGR-C-236-2024 (IFAM, «(Aclara)») y PGR-C-334-2021 (Palmares). Sirven al art. 4 de la Ley 10141 (porcentaje de la tasa de limpieza de vías) y al tema 29.

## Hecho
- Las seis leyes de los adjuntos: 7788, 8436, 8495 y 7451 son idénticas a las del repositorio (comparadas por programa, `cmp_pegado.py`). 8799 y 9458 no estaban: convertidas a `/home/claude/libro/fuentes/Ley 8799.md` y `Ley 9458.md` (`sinalevi2md.py`). 10141 y 10812 ya estaban en el repositorio (Municipal).
- Verificador: reconoce artículos quáter, quinquies y sexies (etiqueta sin tilde: «24 quater»); ESPECIALES para 8799 y 9458. Capítulos 28 a 31 dan las mismas salidas.
- Código Penal vigente (repositorio, Ley 4573, versión 104): arts. 279 bis (reformado por Ley 10532 de 18 set. 2024: agrava a dueños y trabajadores de criaderos), 279 ter, 279 quáter, 279 quinquies, 279 sexies, 405 bis, 405 ter. Citar el Código, no la Ley 9458, para los tipos.
- `add_repo` con permiso de escritura concedido para ecorproy/muniverso-normativa.

## Plan del tema 31 (no aplicado todavía)
- Ley 10141: definir el servicio con el art. 2 (tenencia responsable, control humanitario de poblaciones, prevención de zoonosis y bienestar animal; inciso a «en beneficio directo de la salud pública»; b castración y rabia; c tarifas de interés social para «propietarios en desventaja social»; d y e cultura y campañas). Solo animales de compañía. Todo es «podrá». No crea ingreso: art. 4 permite destinar un porcentaje de la tasa de limpieza de vías, que fija el concejo. Sin multas ni albergues en su texto. Quitar «trae su propia caja».
- Añadir: Ley 7451 arts. 7 c y d, 15 bis, 17, 21, 23, 24 bis, 24 quáter; Ley 8495 arts. 6 e, 6 final («una autoridad en salud»), 78 r, 80; Ley 5346 arts. 3, 5, 6, 7 (reformada en 2006 por el art. 108 de la 8495); Ley 2391 arts. 7 y 8; Ley 8799 arts. 2, 3 g, 6, 10 (la policía municipal no está en la lista; la ley no nombra municipalidades: 0 apariciones), 27 (creó el tribunal del Senasa); Ley 8436 arts. 39 y 149 b; Ley 7317 arts. 13 y 89 (cancelar patente); Ley 7788 art. 9 inciso 1; Ley 8839 art. 8 e (animales muertos en vía pública); Ley 10812 arts. 1, 2, 3 y transitorio (2,3% del presupuesto del Senasa a asociaciones; no a municipalidades).
- La regla, ventanilla: sumar art. 15 bis de la 7451 (2017, posterior al voto de Belén de 2012). Calle: la multa al dueño no es municipal (tribunal del Senasa). Servicio: salud animal.
- Lo pendiente: cómo entra el porcentaje en una tasa fijada al costo (Código Municipal art. 83; dictámenes de tasas); reglamento de la Ley 10812; sin voto posterior a la reforma de 2017.
- Bajar intensidad: «La norma más antigua es de 1959», «Cartago se adelantó a la ley», «No se mide.», «Se cuenta con un solo reglamento…», «solo en uno responde…».
- Para otros temas: Ley 7788 arts. 29, 43, 52 y 60 (tema 30); Ley 8436 arts. 52 y 61 B (temas 29 y 30).

## GitHub (decidido)
- Fuentes íntegras → rama `main` (así lo documenta el traspaso: «Rama main: textos íntegros»), solo archivos nuevos. Taller del libro → rama `seguridad-municipal-360`, carpeta `Seguridad Municipal 360°/Taller del libro/`.
- No subir doctrina con derechos (Pérez Hernández, Wilches-Chaux, ISO, Pele, Los Cabos, Tocqueville). Voto 2018-016612: omitir nombre y cédula de la recurrente en la copia pública.
- Cierre de cada mensaje de commit: `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>` y `Claude-Session: https://claude.ai/code/session_017TjMYjBgmiSxeVVNB771KJ`.
