import sys
p = '/home/claude/libro/propuesta_indice.md'
t = open(p, encoding='utf-8').read()
def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:70])
    t = t.replace(old, new)

rep("| Pérez Hernández, L., Tabares Neyra, L. M. y Díaz Legón, O. J. (2019). *Universidad de La Habana*, (287), 135-160 | Datos según el sitio de la revista y SciELO Cuba | No se pudo abrir el PDF desde la sesión | Pedir el PDF; sin él las once citas quedan fuera |",
    "| Pérez Hernández, L., Tabares Neyra, L. M. y Díaz Legón, O. J. (2019). *Universidad de La Habana*, (287), 135-160 | Revista y número según el sitio de la revista (núm. 287, enero-junio de 2019) y SciELO Cuba | PDF aportado; folios impresos 135 a 160 | Las once citas, literales y con página: punto 10 |")

rep("- Readjuntar Pele (2015), la vista previa de ISO 18091 y Los Cabos (2020).\n- PDF de Pérez Hernández, Tabares Neyra y Díaz Legón (2019).",
    "- Readjuntar la vista previa de ISO 18091 y Los Cabos (2020). Pele (2015) ya llegó (punto 10).\n- PDF de Pérez Hernández, Tabares Neyra y Díaz Legón (2019): recibido (punto 10).")

rep("El nombre de la revista y el número no figuran en el PDF: salen del sitio de la revista (Universidad de La Habana, n.° 287).",
    "El nombre de la revista y el número no figuran en el PDF: constan en el sitio de la revista (*Universidad de La Habana*, núm. 287, enero-junio de 2019: https://revistas.uh.cu/revuh/article/view/2718) y en SciELO Cuba.")

rep("| J | 152 | La oración siguiente remite a Guzón (2016) |",
    "| J | 152 | La oración que sigue cierra con la remisión a Guzón (2016): la idea puede ser de esa autora |")

rep("El texto de SINALEVI trae dos erratas que hay que copiar tal cual o dejar fuera de la cita: «pendientes» por «tendientes» en el art. 13 de la Ley N.° 833 y «de las salud» en el art. 19 de la Ley N.° 4240.",
    "El texto de SINALEVI, igual en el repositorio y en lo pegado por el autor, trae dos lecturas que parecen erratas y que hay que copiar tal cual o dejar fuera de la cita: «las medidas necesarias pendientes a lograr» en el art. 13 de la Ley N.° 833 y «de las salud» en el art. 19 de la Ley N.° 4240. No se cotejaron contra la publicación original.")

rep("**Pasaje por actualizar.** El art. 4 de la Ley N.° 5060 fue reformado por la Ley N.° 10343, del 29 de marzo de 2023: exceptúa del ancho mínimo las vías inventariadas, codificadas y georreferenciadas, para su intervención y conservación. El oficio 22430 de la Contraloría, que el tema 33 usa, es del 12 de diciembre de 2022 y razona sobre el texto anterior.",
    "**Pasaje por actualizar (tema 33).** El art. 4 de la Ley N.° 5060 fue reformado por la Ley N.° 10343, del 29 de marzo de 2023, vigente desde el 12 de abril de 2023: exceptúa del ancho mínimo las rutas y calles públicas ya reconocidas, inventariadas, codificadas y georreferenciadas, «para su debida intervención, conservación, mejoramiento y rehabilitación». El libro cita dos veces el oficio 22430 (DFOE-LOC-2366) de la Contraloría, del 12 de diciembre de 2022 (pp. 5 y 6), que razona sobre el texto anterior y sobre el dictamen C-234-2022. No cita la Ley N.° 5060, la Ley N.° 10343 ni la línea de la Procuraduría, que está íntegra en el repositorio:\n\n"
    "- C-234-2022, del 30 de octubre de 2022 (Atenas): sin autorización legal para usar recursos de la Ley N.° 8114 en caminos vecinales de menos de catorce metros, pero sí con otras fuentes, porque lo contrario «sería condenar al abandono a la red vial cantonal» (conclusiones e y f). Capa administrativa: clase B.\n"
    "- C-133-2024, del 24 de junio de 2024 (San Isidro de Heredia): tras la reforma, los caminos ya declarados que no cumplan el ancho pueden ser intervenidos con los recursos de la Ley N.° 8114 (conclusión 1); el plan regulador no puede fijar para los caminos vecinales una medida distinta de la legal, pero sí la de las calles locales (conclusiones 3 y 4). Capa: clase B.\n"
    "- C-286-2024, del 9 de diciembre de 2024 (Bagaces): consulta inadmisible; remite al C-133-2024 y transcribe sus conclusiones. No está en la capa.\n"
    "- C-014-2026, del 23 de enero de 2026 (Zarcero): integración de la red vial cantonal y licencia de construcción con acceso a vía de ancho menor, condicionada a lo que disponga el plan regulador. No está en la capa.\n"
    "- C-184-2026, del 19 de octubre de 2026 (Upala): es posible reconocer y certificar rutas cantonales de menos de catorce metros al amparo de la Ley N.° 10343, si constaban en los registros al 12 de abril de 2023 (conclusión 3). Su conclusión 1 dice «artículo 14» donde corresponde el 4. Capa: clase B.")

rep("**Punto ciego del inventario.** El inventario se armó sobre el término «municipal». En las leyes que contiene hay 14 artículos más, en 12 leyes, que dicen «municipio» sin ese término; tres son de la Ley de Aguas (arts. 20, 93 y 122).",
    "**Punto ciego del inventario.** El inventario no declara con qué términos se armó. En las leyes que contiene hay 14 artículos, en 12 leyes, que dicen «municipio» sin ninguna otra voz de la familia y que el inventario no trae; tres son de la Ley de Aguas (arts. 20, 93 y 122). El art. 93 faculta al municipio para desecar terrenos pantanosos declarados insalubres. Conteo automático, sin revisión artículo por artículo fuera de la Ley de Aguas.")

rep("19 (postes); 20 y 21 (desagües, vegetación y derrumbes)",
    "19 (toda construcción frente a caminos vecinales y calles requiere aprobación escrita de la municipalidad); 20 y 21 (desagües y vegetación a cargo de los poseedores, a requerimiento municipal)")
rep("3 (travesías a cargo del MOPT)", "3 (calles que una carretera nacional toma al cruzar una población, previa consulta con la municipalidad)")
rep("83 (convenios de apoyo técnico con las municipalidades más cercanas)", "83 (convenios de apoyo técnico con las municipalidades más cercanas para el control constructivo; párrafo agregado por la Ley N.° 9482, de 2017)")
rep("70 (vigilancia municipal de la extracción de materiales en cauces)", "70 (deber de las municipalidades de colaborar en la vigilancia y el control de la extracción de materiales en cauces)")
open(p, 'w', encoding='utf-8').write(t)
print('ok', len(t.split()), 'palabras')
