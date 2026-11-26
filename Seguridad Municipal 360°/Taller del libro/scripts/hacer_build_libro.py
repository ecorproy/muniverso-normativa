# Genera build_libro.py a partir del build.py del taller: fuentes que faltan avisan y siguen,
# votos también en subcarpetas, y fuentes manuales nuevas del libro.
import re
src = open('/home/claude/scripts/build.py', encoding='utf-8').read()
a = "        if m['file']:\n            raw = read(m['file'])\n            pages = raw.split('\\f')"
assert src.count(a) == 1
src = src.replace(a, "        if m['file'] and os.path.exists(m['file']):\n            raw = read(m['file'])\n            pages = raw.split('\\f')")
b = "    f = f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/Sentencia {x}.md'\n    return f if os.path.exists(f) else None"
assert src.count(b) == 1
src = src.replace(b, "    f = f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/Sentencia {x}.md'\n    if os.path.exists(f):\n        return f\n    fs = glob.glob(f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/*/Sentencia {x}.md')\n    return fs[0] if fs else None")
extra = '''
MANUAL.update({
    'Zaratiegui, 1999': dict(file='/home/claude/libro/fuentes/doctrina/zaratiegui_1999_pag.txt',
        ref='Zaratiegui, J. R. (1999). La gestión por procesos: Su papel e importancia en la empresa. *Economía Industrial*, (330), 81-88.'),
    'Vílchez Ordoñez y Sánchez Davila, 2021': dict(file='/home/claude/libro/fuentes/doctrina/vilchez_2021_pag.txt',
        ref='Vílchez Ordoñez, M., & Sánchez Davila, K. (2021). Gestión por procesos e imagen institucional: En busca de mayor visibilidad municipal para los ciudadanos. *Ciencia Latina Revista Científica Multidisciplinar*, *5*(4), 6444-6468. https://doi.org/10.37811/cl_rcm.v5i4.778'),
    'Soledispa Rodríguez et al., 2020, como se citó en Vílchez Ordoñez y Sánchez Davila, 2021': dict(file='/home/claude/libro/fuentes/doctrina/vilchez_2021_pag.txt', alias='Vílchez Ordoñez y Sánchez Davila, 2021',
        ref='Vílchez Ordoñez, M., & Sánchez Davila, K. (2021). Gestión por procesos e imagen institucional: En busca de mayor visibilidad municipal para los ciudadanos. *Ciencia Latina Revista Científica Multidisciplinar*, *5*(4), 6444-6468. https://doi.org/10.37811/cl_rcm.v5i4.778'),
    'Márquez López, 2017, como se citó en Vílchez Ordoñez y Sánchez Davila, 2021': dict(file='/home/claude/libro/fuentes/doctrina/vilchez_2021_pag.txt', alias='Vílchez Ordoñez y Sánchez Davila, 2021',
        ref='Vílchez Ordoñez, M., & Sánchez Davila, K. (2021). Gestión por procesos e imagen institucional: En busca de mayor visibilidad municipal para los ciudadanos. *Ciencia Latina Revista Científica Multidisciplinar*, *5*(4), 6444-6468. https://doi.org/10.37811/cl_rcm.v5i4.778'),
    'Antón Chávez, 2017, como se citó en Vílchez Ordoñez y Sánchez Davila, 2021': dict(file='/home/claude/libro/fuentes/doctrina/vilchez_2021_pag.txt', alias='Vílchez Ordoñez y Sánchez Davila, 2021',
        ref='Vílchez Ordoñez, M., & Sánchez Davila, K. (2021). Gestión por procesos e imagen institucional: En busca de mayor visibilidad municipal para los ciudadanos. *Ciencia Latina Revista Científica Multidisciplinar*, *5*(4), 6444-6468. https://doi.org/10.37811/cl_rcm.v5i4.778'),
    'Orellana Orellana et al., 2020, como se citó en Vílchez Ordoñez y Sánchez Davila, 2021': dict(file='/home/claude/libro/fuentes/doctrina/vilchez_2021_pag.txt', alias='Vílchez Ordoñez y Sánchez Davila, 2021',
        ref='Vílchez Ordoñez, M., & Sánchez Davila, K. (2021). Gestión por procesos e imagen institucional: En busca de mayor visibilidad municipal para los ciudadanos. *Ciencia Latina Revista Científica Multidisciplinar*, *5*(4), 6444-6468. https://doi.org/10.37811/cl_rcm.v5i4.778'),
    'Cortés García, 2026': dict(file='/home/claude/libro/fuentes/doctrina/cortes_garcia_2026.txt',
        ref='Cortés García, E. (2026). *Derecho municipal: Impugnación, veto y revisión de actos administrativos*. Tirant lo Blanch.'),
    'Medina León et al., 2009': dict(file='/home/claude/libro/fuentes/doctrina/medina_leon_2009_pag.txt',
        ref='Medina León, A., Nogueira Rivera, D., & Hernández Nariño, A. (2009). Relevancia de la gestión por procesos en la planificación estratégica y la mejora continua. *Eídos*, (2), 65-72.'),
    'Bendell et al., 1993, como se citó en Medina León et al., 2009': dict(file='/home/claude/libro/fuentes/doctrina/medina_leon_2009_pag.txt', alias='Medina León et al., 2009',
        ref='Medina León, A., Nogueira Rivera, D., & Hernández Nariño, A. (2009). Relevancia de la gestión por procesos en la planificación estratégica y la mejora continua. *Eídos*, (2), 65-72.'),
    'Leiva Poveda, 2016': dict(file='/home/claude/libro/fuentes/doctrina/leiva_elusiva.txt',
        ref='Leiva Poveda, J. (2016). La elusiva definición de “lo local”, que de existir perjudicaría a las municipalidades. En *Memoria. V Congreso Jurídico Nacional Municipal: Dr. Mauro Murillo Arias. Competencias municipales: ¿Qué es lo local?* Federación Metropolitana de Municipalidades y Municipalidad de San José.'),
    'Ortiz Ortiz, 1987, como se citó en Leiva Poveda, 2016': dict(file='/home/claude/libro/fuentes/doctrina/leiva_elusiva.txt', alias='Leiva Poveda, 2016',
        ref='Leiva Poveda, J. (2016). La elusiva definición de “lo local”, que de existir perjudicaría a las municipalidades. En *Memoria. V Congreso Jurídico Nacional Municipal: Dr. Mauro Murillo Arias. Competencias municipales: ¿Qué es lo local?* Federación Metropolitana de Municipalidades y Municipalidad de San José.'),
    'Jinesta Lobo, 2002, como se citó en Leiva Poveda, 2016': dict(file='/home/claude/libro/fuentes/doctrina/leiva_elusiva.txt', alias='Leiva Poveda, 2016',
        ref='Leiva Poveda, J. (2016). La elusiva definición de “lo local”, que de existir perjudicaría a las municipalidades. En *Memoria. V Congreso Jurídico Nacional Municipal: Dr. Mauro Murillo Arias. Competencias municipales: ¿Qué es lo local?* Federación Metropolitana de Municipalidades y Municipalidad de San José.'),
    'Ariño Ortiz, 1988, como se citó en Leiva Poveda, 2016': dict(file='/home/claude/libro/fuentes/doctrina/leiva_elusiva.txt', alias='Leiva Poveda, 2016',
        ref='Leiva Poveda, J. (2016). La elusiva definición de “lo local”, que de existir perjudicaría a las municipalidades. En *Memoria. V Congreso Jurídico Nacional Municipal: Dr. Mauro Murillo Arias. Competencias municipales: ¿Qué es lo local?* Federación Metropolitana de Municipalidades y Municipalidad de San José.'),
    'García de Enterría, 1999, como se citó en Leiva Poveda, 2016': dict(file='/home/claude/libro/fuentes/doctrina/leiva_elusiva.txt', alias='Leiva Poveda, 2016',
        ref='Leiva Poveda, J. (2016). La elusiva definición de “lo local”, que de existir perjudicaría a las municipalidades. En *Memoria. V Congreso Jurídico Nacional Municipal: Dr. Mauro Murillo Arias. Competencias municipales: ¿Qué es lo local?* Federación Metropolitana de Municipalidades y Municipalidad de San José.'),
    'Organización Panamericana de la Salud, s. f.': dict(file='/home/claude/libro/fuentes/doctrina/ops_seguridad_humana.txt',
        ref='Organización Panamericana de la Salud. (s. f.). [Resumen del documento de referencia técnico sobre salud y seguridad humana]. https://www.paho.org/sites/default/files/D37404-PAHO-ExecutiveSummary-Spn-WEB.pdf'),
    'Conan Doyle, s. f.': dict(file='/home/claude/libro/fuentes/doctrina/conan_doyle_valle.txt',
        ref='Conan Doyle, A. (s. f.). *El valle del terror*. Fundación Carlos Slim. (Obra original publicada en 1915)'),
    'Sheldrake, 2020': dict(file='/home/claude/libro/fuentes/doctrina/sheldrake_2020.txt',
        ref='Sheldrake, M. (2020). *La red oculta de la vida: De qué manera los hongos crean nuestros mundos, cambian nuestra forma de pensar y moldean nuestro futuro* (T. Gras Cardona, Trad.). Editorial Planeta.'),
    'Naciones Unidas, 2016': dict(file='/home/claude/libro/fuentes/doctrina/onu_seguridad_humana_2016.txt',
        ref='Naciones Unidas, Dependencia de Seguridad Humana. (2016). *Manual de seguridad humana: Un enfoque integrado para la consecución de los Objetivos de Desarrollo Sostenible y los ámbitos de acción prioritarios de la comunidad internacional y el sistema de las Naciones Unidas*. Naciones Unidas.'),
    'Pérez Hernández et al., 2019': dict(
        file='/home/claude/libro/fuentes/perez_pag.txt',
        ref='Pérez Hernández, L., Tabares Neyra, L. M. y Díaz Legón, O. J. (2019). Lo local –municipal– como espacio de desarrollo en Cuba. Notas para el perfeccionamiento del régimen jurídico de la administración local. *Universidad de La Habana*, (287), 135-160.'),
    'Katz v. United States, 1967': dict(
        file='/home/claude/libro/fuentes/doctrina/katz_pag.txt',
        ref='*Katz v. United States*, 389 U.S. 347 (1967). Supreme Court of the United States.'),
    'Leaders of a Beautiful Struggle v. Baltimore Police Department, 2021': dict(
        file='/home/claude/libro/fuentes/doctrina/baltimore_pag.txt',
        ref='*Leaders of a Beautiful Struggle v. Baltimore Police Department*, No. 20-1495 (4th Cir. 24 de junio de 2021) (en banc). United States Court of Appeals for the Fourth Circuit.'),
    'STS 797/2025': dict(alias='Espana Tribunal Supremo Penal 2025 797', file='/home/claude/libro/fuentes/doctrina/sts_797_2025.txt',
        ref='España. Tribunal Supremo, Sala de lo Penal. Sentencia 797/2025, de 2 de octubre (recurso 10005/2025). ECLI:ES:TS:2025:4225.'),
    'STS 264/2026': dict(alias='Espana Tribunal Supremo Penal 2026 264', file='/home/claude/libro/fuentes/doctrina/sts_264_2026.txt',
        ref='España. Tribunal Supremo, Sala de lo Penal. Sentencia 264/2026, de 6 de abril (recurso 10648/2025). ECLI:ES:TS:2026:1661.'),
    'STS 1166/2025': dict(alias='Espana Tribunal Supremo Civil 2025 1166', file='/home/claude/libro/fuentes/doctrina/sts_1166_2025.txt',
        ref='España. Tribunal Supremo, Sala de lo Civil. Sentencia 1166/2025, de 17 de julio (recurso 5962/2024).'),
    'SAP Santa Cruz de Tenerife 60/2026': dict(alias='Espana Audiencia Provincial Santa Cruz de Tenerife 2026', file='/home/claude/libro/fuentes/doctrina/sap_tf_60_2026.txt',
        ref='España. Audiencia Provincial de Santa Cruz de Tenerife, Sección Sexta. Sentencia 60/2026, de 23 de marzo (rollo 729/2025). ECLI:ES:APTF:2026:624.'),
    'Cass. pen. 28146/2025': dict(alias='Italia Corte di Cassazione 2025', file='/home/claude/libro/fuentes/doctrina/cass_28146_2025.txt',
        ref='Italia. Corte di Cassazione, Sezione V penale. Sentenza n. 28146, depositata il 31 luglio 2025.'),
    'Fearn v Board of Trustees of the Tate Gallery, 2023': dict(file='/home/claude/libro/fuentes/doctrina/fearn_2023.txt',
        ref='*Fearn and others v Board of Trustees of the Tate Gallery* [2023] UKSC 4 (1 de febrero de 2023). Supreme Court of the United Kingdom.'),
    'Huerta v. Pirker, 2014': dict(file='/home/claude/libro/fuentes/doctrina/pirker_2014.txt',
        ref='*Huerta v. Pirker*, NTSB Order No. EA-5730, Docket CP-217 (National Transportation Safety Board, 18 de noviembre de 2014).'),
    "Conseil d'État, 18 de mayo de 2020": dict(alias="Francia Conseil d Etat 2020a", file='/home/claude/libro/fuentes/doctrina/ce_440442_2020.txt',
        ref="Francia. Conseil d'État, juge des référés. Ordonnance n.° 440442, 440445, de 18 de mayo de 2020 (Association La Quadrature du Net y Ligue des droits de l'homme)."),
    "Conseil d'État, 22 de diciembre de 2020": dict(alias="Francia Conseil d Etat 2020b", file='/home/claude/libro/fuentes/doctrina/ce_446155_2020.txt',
        ref="Francia. Conseil d'État, salas 10.ª y 9.ª reunidas. Décision n.° 446155, de 22 de diciembre de 2020 (Association La Quadrature du Net)."),
    'Conseil constitutionnel, 2021-817 DC': dict(alias='Francia Conseil constitutionnel 2021', file='/home/claude/libro/fuentes/doctrina/cc_2021_817.txt',
        ref='Francia. Conseil constitutionnel. Décision n.° 2021-817 DC, de 20 de mayo de 2021 (Loi pour une sécurité globale préservant les libertés).'),
    'Conseil constitutionnel, 2021-834 DC': dict(alias='Francia Conseil constitutionnel 2022', file='/home/claude/libro/fuentes/doctrina/cc_2021_834.txt',
        ref='Francia. Conseil constitutionnel. Décision n.° 2021-834 DC, de 20 de enero de 2022 (Loi relative à la responsabilité pénale et à la sécurité intérieure).'),
    'Ryneš, 2014': dict(alias='Tribunal de Justicia de la Union Europea 2014', file='/home/claude/libro/fuentes/doctrina/rynes_2014.txt',
        ref='Tribunal de Justicia de la Unión Europea, Sala Cuarta. Sentencia de 11 de diciembre de 2014, *František Ryneš c. Úřad pro ochranu osobních údajů*, asunto C-212/13.'),
    'Long Lake Township v. Maxon, 2024': dict(
        file='/home/claude/libro/fuentes/doctrina/maxon_msc_pag.txt',
        ref='*Long Lake Township v. Maxon*, No. 164948 (Mich. 3 de mayo de 2024). Supreme Court of the State of Michigan.'),
    'Long Lake Township v. Maxon, 2021': dict(
        file='/home/claude/libro/fuentes/doctrina/maxon_coa_pag.txt',
        ref='*Long Lake Township v. Maxon*, No. 349230 (Mich. Ct. App. 18 de marzo de 2021). Court of Appeals of the State of Michigan.'),
    'Harvard Law Review, 2025': dict(
        file='/home/claude/libro/fuentes/doctrina/maxon_pag.txt',
        ref='Harvard Law Review. (2025). Fourth Amendment — Unreasonable searches — Michigan Supreme Court holds exclusionary rule inapplicable in the civil context. Long Lake Township v. Maxon, 15 N.W.3d 118 (Mich. 2024). *Harvard Law Review*, *138*, 1941-1950.'),
    'Wilches-Chaux, 2007': dict(
        file='/home/claude/libro/fuentes/wilches_pag.txt',
        ref='Wilches-Chaux, G. (2007). Lo local-municipal como unidad de gestión. *Medio Ambiente y Urbanización*, (67), 113-126.'),
    'Ley N.° 9059, 2012': dict(
        file=None,
        ref='Ley N.° 9059, *Declara de interés público el desarrollo de una zona económica en la provincia de Cartago*. (2012). Asamblea Legislativa de la República de Costa Rica. Alcance N.° 118 a La Gaceta N.° 162, 23 de agosto de 2012.'),
    'Decreto Ejecutivo N.° 40446-MTSS-MEIC, 2017': dict(
        file=None,
        ref='Decreto Ejecutivo N.° 40446-MTSS-MEIC, *Declara de interés público la creación de una zona económica especial en los cantones de Golfito, Osa, Buenos Aires, Coto Brus y Corredores que promueva el desarrollo económico y la creación de fuentes de empleo*. (2017). Poder Ejecutivo de la República de Costa Rica. La Gaceta N.° 197, 19 de octubre de 2017. https://sinalevi.go.cr/ResultadosNormativa/Informacion?param1=85067&param2=109896&param3=1'),
})
'''
# criterios de la Contraloría que el libro agrega (van dentro del diccionario CGR, que deexp también lee)
cgr_extra = """    'REDCUDI': dict(cita='informe N.° DFOE-BIS-IAD-00010-2023, 2023', file='/home/claude/repo/360/Seguridad Municipal 360°/Criterios CGR/Informe DFOE-BIS-IAD-00010-2023 Gobernanza y calidad de la REDCUDI - texto extraído.txt',
                  ref='Contraloría General de la República. (2023, 23 de octubre). *Informe de auditoría de carácter especial sobre la gobernanza y estándares de calidad de los servicios de cuido y desarrollo infantil de la REDCUDI* (informe N.° DFOE-BIS-IAD-00010-2023).',
                  key=(2023, 10, 23)),
    'R-DCP-SICOP-00770-2024': dict(cita='resolución N.° R-DCP-SICOP-00770-2024, 2024', file='/home/claude/repo/360/Seguridad Municipal 360°/Criterios CGR/Resolución 8072024000000797-2024 (recurso de apelación) CECUDI de Palmares - texto extraído.txt',
                  ref='Contraloría General de la República. (2024, 31 de mayo). *Resolución N.° R-DCP-SICOP-00770-2024. Recurso de apelación contra la declaratoria de desierta de la licitación mayor 2023LY-000001-0002500001 de la Municipalidad de Palmares (operador y administrador del CECUDI)*.',
                  key=(2024, 5, 31)),
    '07359': dict(cita='oficio N.° 07359 [DFOE-DL-0517], 2017', file='/home/claude/libro/fuentes/of07359.txt',
                  ref='Contraloría General de la República. (2017, 29 de junio). *Oficio N.° 07359 (DFOE-DL-0517). Emisión de criterio respecto a las donaciones en especie que realizan las Municipalidades a las Asociaciones Comunales, para el desarrollo de obras*.',
                  key=(2017, 6, 29)),
    '16049': dict(cita='oficio N.° 16049 [DFOE-LOC-1430], 2024', file='/home/claude/libro/fuentes/of16049.txt',
                  ref='Contraloría General de la República. (2024, 8 de octubre). *Oficio N.° 16049 (DFOE-LOC-1430). Opinión sobre el texto dictaminado Reforma del artículo 71 del Código Municipal, Ley n.° 7794, del 30 de abril de 1998 y sus reformas, correspondiente al expediente legislativo n.° 23.777*.',
                  key=(2024, 10, 8)),
    '21709': dict(cita='oficio N.° 21709 [DJ-2194], 2025', file='/home/claude/libro/fuentes/of21709.txt',
                  ref='Contraloría General de la República. (2025, 3 de noviembre). *Oficio N.° 21709 (DJ-2194). Solicitud de criterio relacionado con el proyecto de Ley n° 25.082 \"Ley de autorización a la Municipalidad de Grecia para donar un inmueble de su propiedad a la Asociación Cruz Roja Costarricense\"*.',
                  key=(2025, 11, 3)),
    '03933': dict(cita='oficio N.° 03933 [DJ-0647-2026], 2026', file='/home/claude/libro/fuentes/of03933.txt',
                  ref='Contraloría General de la República. (2026, 8 de abril). *Oficio N.° 03933 (DJ-0647-2026). Se atiende consulta sobre el uso de instalaciones municipales para estacionamiento de vehículos particulares de los funcionarios*.',
                  key=(2026, 4, 8)),
    '07545': dict(cita='oficio N.° 07545 [DCA-2092], 2021', file='/home/claude/libro/fuentes/of07545.txt',
                  ref='Contraloría General de la República. (2021, 25 de mayo). *Oficio N.° 07545 (DCA-2092). Se atiende solicitud de criterio sobre la procedencia de permiso de uso*.',
                  key=(2021, 5, 25)),
    '03078': dict(cita='oficio N.° 03078 [DCA-0690], 2022', file='/home/claude/libro/fuentes/of03078.txt',
                  ref='Contraloría General de la República. (2022, 24 de febrero). *Oficio N.° 03078 (DCA-0690). Se emite criterio sobre la posibilidad de que una Municipalidad realice mediante un convenio intermunicipal con otra municipalidad la adquisición de un bien o un servicio, pagando una contraprestación económica por ese servicio o bien, con esa municipalidad*.',
                  key=(2022, 2, 24)),
    '15562': dict(cita='oficio N.° 15562 [DCA-2950], 2016', file='/home/claude/libro/fuentes/of15562.txt',
                  ref='Contraloría General de la República. (2016, 28 de noviembre). *Oficio N.° 15562 (DCA-2950). Se da respuesta a la solicitud de criterio sobre la facultad del Ministerio de Economía, Industria y Comercio para suscribir convenios con entes de derecho público o privado, con el fin de que se encarguen de la logística de eventos donde se reciban recursos públicos o aportes económicos*.',
                  key=(2016, 11, 28)),
    'R-DC-00080-2024': dict(cita='resolución N.° R-DC-00080-2024, 2024', file='/home/claude/libro/fuentes/rdc00080-2024.txt',
                  ref='Contraloría General de la República. (2024, 20 de agosto). *Resolución N.° R-DC-00080-2024. Lineamientos para la declaración jurada sobre la situación patrimonial de sujetos privados que administren o custodien fondos y actividades públicas*.',
                  key=(2024, 8, 20)),
    '14467': dict(cita='oficio N.° 14467 [DJ-1340], 2018', file='/home/claude/libro/fuentes/of14467.txt',
                  ref='Contraloría General de la República. (2018, 9 de octubre). *Oficio N.° 14467 (DJ-1340). Consulta relacionada con los fondos de la Ley n.º 6282 del 14 de agosto 1979*.',
                  key=(2018, 10, 9)),
    '01889': dict(cita='oficio N.° 01889 [DFOE-IAF-0037], 2023', file='/home/claude/libro/fuentes/of01889.txt',
                  ref='Contraloría General de la República. (2023, 20 de febrero). *Oficio N.° 01889 (DFOE-IAF-0037). Emisión de criterio solicitado por diputado de la Asamblea Legislativa, sobre el mecanismo legal que disponen los Comités Cantonales de Deportes para asignar viáticos a sus atletas*.',
                  key=(2023, 2, 20)),
    '00415': dict(cita='oficio N.° 00415 [DFOE-LOC-0073], 2024', file='/home/claude/libro/fuentes/of00415.txt',
                  ref='Contraloría General de la República. (2024, 19 de enero). *Oficio N.° 00415 (DFOE-LOC-0073). Atención de consulta relacionada al Plan Cantonal de Desarrollo Humano Local (PCDHL)*.',
                  key=(2024, 1, 19)),
    '09880': dict(cita='oficio N.° 09880 [DFOE-CAP-0934], 2025', file='/home/claude/libro/fuentes/of09880.txt',
                  ref='Contraloría General de la República. (2025, 22 de mayo). *Oficio N.° 09880 (DFOE-CAP-0934). Criterio sobre acceso por parte de la Auditoría Interna a sistemas de monitoreo y cámaras de vigilancia*.',
                  key=(2025, 5, 22)),
    '06784': dict(cita='oficio N.° 06784 [DFOE-LOC-0510], 2024', file='/home/claude/libro/fuentes/of06784.txt',
                  ref='Contraloría General de la República. (2024, 23 de abril). *Oficio N.° 06784 (DFOE-LOC-0510). Atención de consulta relacionada con el presupuesto de los Comités Cantonales de Deportes y Recreación*.',
                  key=(2024, 4, 23)),
    '11709': dict(cita='oficio N.° 11709 [DFOE-SOS-0279], 2022', file='/home/claude/libro/fuentes/of11709.txt',
                  ref='Contraloría General de la República. (2022, 13 de julio). *Oficio N.° 11709 (DFOE-SOS-0279). Atención de consulta referente a la presentación de informes económicos, pago de impuestos, fiscalización y rendición de cuentas de los Centros Agrícolas Cantonales*.',
                  key=(2022, 7, 13)),
    '09492': dict(cita='oficio N.° 9492 [DJ-0857], 2025', file='/home/claude/libro/fuentes/of09492.txt',
                  ref='Contraloría General de la República. (2025, 14 de mayo). *Oficio N.° 9492 (DJ-0857). Se atiende consulta sobre la donación de un terreno por parte de determinada Municipalidad a un tercero por medio de un acuerdo del Concejo Municipal*.',
                  key=(2025, 5, 14)),
    '14031': dict(cita='oficio N.° 14031 [DFOE-LOC-1515], 2025', file='/home/claude/libro/fuentes/of14031.txt',
                  ref='Contraloría General de la República. (2025, 5 de agosto). *Oficio N.° 14031 (DFOE-LOC-1515). Emisión de criterio solicitado por el alcalde con relación a los artículos 45 y 46 bis de la Ley Nacional de Emergencias y Prevención del Riesgo*.',
                  key=(2025, 8, 5)),
    '18724': dict(cita='oficio N.° 18724 [DFOE-LOC-2501], 2023', file='/home/claude/libro/fuentes/of18724.txt',
                  ref='Contraloría General de la República. (2023, 20 de diciembre). *Oficio N.° 18724 (DFOE-LOC-2501). Emisión de criterio relativo a la posibilidad de las administraciones municipales de realizar convenios con Asociaciones de Desarrollo Integral, con el fin que estas brinden servicios con cargo a los recursos provenientes de las Leyes n.os 8114 y 9329*.',
                  key=(2023, 12, 20)),
    '22608': dict(cita='oficio N.° 22608 [DFOE-LOC-2154], 2025', file='/home/claude/libro/fuentes/of22608.txt',
                  ref='Contraloría General de la República. (2025, 21 de noviembre). *Oficio N.° 22608 (DFOE-LOC-2154). Emisión de criterio solicitado por el alcalde sobre la utilización de recursos públicos para la atención o mitigación de riesgos ubicados en bienes de propiedad privada con afectación comunal*.',
                  key=(2025, 11, 21)),
    '01835': dict(cita='oficio N.° 01835 [DFOE-LOC-0217], 2025', file='/home/claude/libro/fuentes/of01835.txt',
                  ref='Contraloría General de la República. (2025, 4 de febrero). *Oficio N.° 01835 (DFOE-LOC-0217). Emisión de criterio solicitado por el Alcalde Municipal de Osa, sobre la posibilidad de las administraciones municipales de realizar donaciones de instrumentos a bandas comunales*.',
                  key=(2025, 2, 4)),
    '12990': dict(cita='oficio N.° 12990 [DFOE-LOC-1706], 2023', file='/home/claude/libro/fuentes/of12990.txt',
                  ref='Contraloría General de la República. (2023, 27 de setiembre). *Oficio N.° 12990 (DFOE-LOC-1706). Emisión de criterio relativo a la inversión de recursos en aceras*.',
                  key=(2023, 9, 27)),
    '22430': dict(cita='oficio N.° 22430 [DFOE-LOC-2366], 2022', file='/home/claude/libro/fuentes/of22430.txt',
                  ref='Contraloría General de la República. (2022, 12 de diciembre). *Oficio N.° 22430 (DFOE-LOC-2366). Emisión de criterio relativo a aclarar si el análisis brindado a través de los oficios n.os 11545 (DFOE-LOC-0617)-2021 y 13004 (DFOE-LOC-1320)-2022, es extensible al concepto que aparece en el artículo 2 inciso a) del Decreto Ejecutivo n.° 40137-MOPT*.',
                  key=(2022, 12, 12)),
    '14908': dict(cita='oficio N.° 14908 [DFOE-DEC-4567], 2024', file='/home/claude/libro/fuentes/of14908.txt',
                  ref='Contraloría General de la República. (2024, 23 de setiembre). *Oficio N.° 14908 (DFOE-DEC-4567). Advertencia relacionada con el cumplimiento del marco legal en la constatación de vías como públicas, la declaratoria de estas con fundamento en instrumentos públicos existentes, e inversión de recursos públicos en dichas vías*.',
                  key=(2024, 9, 23)),
    'CGR-IND27': dict(cita='Indicaciones para la formulación de los presupuestos 2027, 2026', file='/home/claude/libro/fuentes/cgr_gl1_indicaciones_2027.txt',
                  ref='Contraloría General de la República. (2026, julio). *Indicaciones para la formulación y presentación de los presupuestos institucionales, año 2027*. División de Fiscalización Operativa y Evaluativa. https://www.cgr.go.cr/05-tramites-ap-gl-27.html',
                  key=(2026, 7, 2)),
    'CGR-EP': dict(cita='estructura programática municipal, s. f.', file='/home/claude/libro/fuentes/cgr_GL-4-Estructura-programatica-Municipal.txt',
                  ref='Contraloría General de la República. (s. f.). *Estructura programática municipal: estructura programática de las municipalidades para incluir la información de los presupuestos y sus variaciones en el Sistema de Información sobre Planes y Presupuestos*. https://www.cgr.go.cr/05-tramites-ap-gl-27.html',
                  key=(2026, 7, 1)),
    'CGR-GIP': dict(cita='modelo de guía interna de verificación del presupuesto, 2026', file='/home/claude/libro/fuentes/cgr_GL-3-Guia-interna-presupuesto.txt',
                  ref='Contraloría General de la República. (2026, julio). *Modelo de guía interna de verificación de requisitos del bloque de legalidad presupuestario que deben cumplir las municipalidades en la formulación de su presupuesto inicial y variaciones sujetas a la aprobación presupuestaria de la Contraloría General de la República*. https://www.cgr.go.cr/05-tramites-ap-gl-27.html',
                  key=(2026, 7, 3)),
    'CGR-CERT': dict(cita='certificación de verificación del bloque de legalidad presupuestario, 2026', file='/home/claude/libro/fuentes/cgr_GL-2-Certificacion-presupuesto.txt',
                  ref='Contraloría General de la República. (2026, julio). *Certificación de verificación de requisitos del bloque de legalidad presupuestario que debe cumplir el presupuesto inicial y sus variaciones, para las municipalidades*. https://www.cgr.go.cr/05-tramites-ap-gl-27.html',
                  key=(2026, 7, 4)),
    'IGSMF': dict(cita='fichas de indicadores del IGSM 2025, 2025', file='/home/claude/repo/360/Seguridad Municipal 360°/Criterios CGR/IGSM 2025 - fichas de indicadores - texto extraído.txt',
                  ref='Contraloría General de la República. (2025). [Fichas de indicadores del Índice de Gestión de Servicios Municipales 2025].',
                  key=(2025, 8, 6)),
    '10092': dict(cita='oficio N.° 10092 [DFOE-SOS-0320], 2024', file='/home/claude/libro/fuentes/of10092.txt',
                  ref='Contraloría General de la República. (2024, 17 de junio). *Oficio N.° 10092 (DFOE-SOS-0320). Emisión de criterio solicitado sobre la naturaleza jurídica de los fondos que reciben las ASADAS*.',
                  key=(2024, 6, 17)),
    '22620': dict(cita='oficio N.° 22620 [DCA-3192], 2022', file='/home/claude/libro/fuentes/of22620.txt',
                  ref='Contraloría General de la República. (2022, 14 de diciembre). *Oficio N.° 22620 (DCA-3192). Se deniega solicitud de refrendo del contrato suscrito por la Municipalidad de Osa para servicios de recolección de residuos sólidos*.',
                  key=(2022, 12, 14)),
    '16050': dict(cita='oficio N.° 16050 [DFOE-LOC-1431], 2024', file='/home/claude/libro/fuentes/of16050.txt',
                  ref='Contraloría General de la República. (2024, 8 de octubre). *Oficio N.° 16050 (DFOE-LOC-1431). Emisión de criterio sobre el uso de recursos provenientes de la Ley sobre la Zona Marítimo Terrestre, N.° 6043*.',
                  key=(2024, 10, 8)),
    '10008': dict(cita='oficio N.° 10008 [DFOE-LOC-1351], 2023', file='/home/claude/libro/fuentes/of10008.txt',
                  ref='Contraloría General de la República. (2023, 28 de julio). *Oficio N.° 10008 (DFOE-LOC-1351). Emisión de criterio solicitado por la alcaldesa de la Municipalidad de Puriscal respecto a la posibilidad de comprar un terreno para inversión en tractos y su inclusión en presupuestos ordinarios*.',
                  key=(2023, 7, 28)),
    '01840': dict(cita='oficio N.° 01840 [DFOE-LOC-0259], 2026', file='/home/claude/libro/fuentes/of01840.txt',
                  ref='Contraloría General de la República. (2026, 16 de febrero). *Oficio N.° 01840 (DFOE-LOC-0259). Emisión de criterio sobre los recursos contenidos en el inciso b) del artículo 59 de la Ley sobre la Zona Marítimo Terrestre*.',
                  key=(2026, 2, 16)),
"""
k = src.index("    'IGSM': dict(")
src = src[:k] + cgr_extra + src[k:]
# señales de redacción artificial que el autor pidió eliminar (26 de noviembre de 2026)
_v = "r'\\bno se trata\\b']"
assert src.count(_v) == 1
src = src.replace(_v, "r'\\bno se trata\\b', r'\\ben suma\\b', r'\\ben s[ií]ntesis\\b', r'\\ben resumen\\b', r'\\ben conclusi[oó]n\\b', r'\\bpor contraste\\b', r'\\bla lecci[oó]n\\b', r'\\bvale la pena\\b', r'\\besa es la tesis\\b', r'\\ben otras palabras\\b', r'\\bdicho esto\\b', r'\\bcabe se[ñn]alar\\b', r'\\bhay una idea\\b', r'\\bno es [^.]{0,60}, sino\\b']")
i = src.index('MANUAL = {'); j = src.index('\ndef ', i)
src = src[:j] + '\n' + extra + src[j:]
# leyes que no están en el repositorio y se leen del diario oficial
e1 = "ESPECIALES = {'7135': '/home/claude/repo/main/Leyes y decretos nacionales/Constitucional/Ley Jurisdicción Constitucional.md'}"
assert src.count(e1) == 1
src = src.replace(e1, e1 + "\nESPECIALES['10939'] = '/home/claude/libro/fuentes/Ley 10939.md'\nESPECIALES['8799'] = '/home/claude/libro/fuentes/Ley 8799.md'\nESPECIALES['9458'] = '/home/claude/libro/fuentes/Ley 9458.md'\nESPECIALES['10594'] = '/home/claude/libro/fuentes/Ley 10594.md'\nESPECIALES['8661'] = '/home/claude/libro/fuentes/Ley 8661.md'\nESPECIALES['7948'] = '/home/claude/libro/fuentes/Ley 7948.md'\nESPECIALES['6968'] = '/home/claude/libro/fuentes/Ley 6968.md'\nESPECIALES['4574'] = '/home/claude/libro/fuentes/Ley 4574.md'\nFUENTE_LEY = {'10939': 'La Gaceta N.° 91, Alcance N.° 59, 20 de mayo de 2026.'}")
src = src.replace("ESPECIALES['10939'] =", "ESPECIALES['9017'] = '/home/claude/repo/main/Leyes locales/Alajuela/Poás/Ley 9017.md'\nESPECIALES['10939'] =", 1)
e2 = "Asamblea Legislativa de la República de Costa Rica. Sistema Costarricense de Información Jurídica.{url}')\n    return y"
assert src.count(e2) == 1
src = src.replace(e2, "Asamblea Legislativa de la República de Costa Rica. {FUENTE_LEY.get(n, 'Sistema Costarricense de Información Jurídica.')}{url}')\n    return y")
# reglamentos y acuerdos municipales del repositorio como fuente: [[RM:clave:art. 3]]
RMBASE = '/home/claude/repo/main/Reglamentos municipales/'
rm_code = """
RM = {
    'talamanca-animales': 'Limón/Talamanca/Reglamento de servicio municipal de atención de animales de compañía (2022).md',
    'paraiso-construcciones': 'Cartago/Paraíso/Reglamento de Construcciones del Cantón de Paraíso (2012).md',
    'oreamuno-construccion': 'Cartago/Oreamuno/Reglamento de Construcción e infraestructura (2025).md',
    'cartago-cmeca': 'Cartago/Cartago/Reglamento de Organización y Funcionamiento del Centro Municipal de Educación para el Cuido Animal (2016).md',
    'invu-construcciones': '/home/claude/libro/fuentes/Reglamento de Construcciones INVU (2018).md',
    'sanrafael-precario': 'Heredia/San Rafael de Heredia/Reglamento de Autorizaciones de Permiso de Uso en Precario de Viviendas en la Municipalidad de San Rafael de H (2016).md',
    'montesdeoro-vivienda': 'Puntarenas/Montes de Oro/Reglamento para el Programa de Vivienda Municipal (2006).md',
    'mora-ayudas': 'San José/Mora/Reglamento para el otorgamiento de ayudas temporales a sujetos privados y públicos del Cantón de Mora que enfr (2023).md',
    'heredia-cementerios': 'Heredia/Heredia/Reglamento de los cementerios de la Municipalidad de Heredia (2026).md',
    'santaana-ayudas': 'San José/Santa Ana/Reglamento para otorgar ayudas temporales en caso de desgracia o infortunio (2022).md',
    'belen-comad': 'Heredia/Belén/Reglamento de la Comisión Permanente de la Condición de la Mujer de la Municipalidad de Belén (2024).md',
    'cobano-ofim': 'Puntarenas/Concejo Municipal de Distrito de Cóbano/Reglamento general del servicio de la Oficina de la mujer del Concejo Municipal del Distrito de Cóbano (2023).md',
    'poas-violencia': 'Alajuela/Poás/Reglamento para prevenir, atender, sancionar y erradicar la violencia contra las mujeres en la política de la Municipalidad de Poás (2024).md',
    'sanjose-becas': 'San José/San José/Reglamento para el otorgamiento de Becas para personas habitantes del Cantón de San José, contempladas en el C (2026).md',
    'upala-becas': 'Alajuela/Upala/Reglamento para el otorgamiento de becas para estudio a los munícipes de Upala (2022).md',
    'sanrafael-becas': 'Heredia/San Rafael de Heredia/Reglamento para el otorgamiento de becas de estudio a estudiantes del cantón de San Rafael de Heredia (2023).md',
    'escazu-becas': 'San José/Escazú/Reforma Integral Reglamento para el otorgamiento de becas para estudio a munícipes de Escazú (2025).md',
    'cartago-tmc': 'Cartago/Cartago/Reforma integral Reglamento del programa de transferencia monetaria condicionada de la Municipalidad de Cartago (2026).md',
    'liberia-ayudas': 'Guanacaste/Liberia/Reglamento para ayudas y becas de la Municipalidad de Liberia (2019).md',
    'matina-ayudas': 'Limón/Matina/Reglamento de ayudas temporales a las y los habitantes del Cantón de Matina (2020).md',
    'alajuela-ventas': 'Alajuela/Alajuela/Reglamento de ventas ambulantes y estacionarias de la Municipalidad de Alajuela (2021).md',
    'curridabat-licencias': 'San José/Curridabat/Reforma integral Reglamento para licencias municipales de la Municipalidad de Curridabat (2017).md',
    'upala-casa': 'Alajuela/Upala/Reglamento Interno de la Casa de los Derechos de las Mujeres (2014).md',
    'coronado-tramites': 'San José/Vázquez de Coronado/Reglamento de simplificación, digitalización de trámites e implementación de firma digital, Ley 8220 y Ley 845 (2025).md',
    'parrita-atencion': 'Puntarenas/Parrita/Reglamento para Regular la Atención al Público (2006).md',
    'desamparados-redes': 'San José/Desamparados/Reglamento de comunicación, página web y redes sociales de la Municipalidad de Desamparados (2024).md',
    'belen-redes': 'Heredia/Belén/Reglamento de uso de redes sociales, de la Municipalidad de Belén (2024).md',
    'sanpablo-redes': 'Heredia/San Pablo de Heredia/Reglamento para el uso de dispositivos móviles institucionales y redes sociales oficiales de la Municipalidad (2026).md',
    'sarapiqui-concejo': 'Heredia/Sarapiquí/Reglamento interno de funcionamiento del Concejo Municipal de Sarapiquí (2021).md',
    'sancarlos-concejo': 'Alajuela/San Carlos/Reglamento de funcionamiento del Concejo Municipal de la Municipalidad de San Carlos (2022).md',
    'sancarlos-distritos': 'Alajuela/San Carlos/Reglamento para el funcionamiento de los Concejos de Distrito en el cantón de San Carlos (2026).md',
    'parrita-sesiones': 'Puntarenas/Parrita/Reglamento de sesiones del concejo municipal de Parrita y sus comisiones (2025).md',
    'buenosaires-sesiones': 'Puntarenas/Buenos Aires/Reglamento de Sesiones del Concejo Municipal del Cantón de Buenos Aires (2026).md',
    'moravia-concejo': 'San José/Moravia/Reglamento del concejo municipal de Moravia (2019).md',
    'quepos-concejo': 'Puntarenas/Quepos/Reglamento del Concejo Municipal de Quepos (2021).md',
    'grecia-consultas': 'Alajuela/Grecia/Reglamento para la celebración de consultas populares en el Cantón de Grecia (2021).md',
    'moravia-participacion': 'San José/Moravia/Reglamento de participación ciudadana de la Municipalidad de Moravia (2026).md',
    'montesdeoca-audiencia': 'San José/Montes de Oca/Reglamento para la audiencia pública del proceso de actualización y modificación del Plan Regulador del Cantón (2026).md',
    'palmares-participacion': 'Alajuela/Palmares/Manual de participación ciudadana en los procesos de planificación, presupuesto y rendición de cuentas, presup (2015).md',
    'sanjose-video': 'San José/San José/Reglamento de video protección del Cantón Central de San José (2024).md',
    'heredia-vigilancia': 'Heredia/Heredia/Reglamento regulador para la vigilancia de vías públicas mediante dispositivos tecnológicos o técnicos (except (2019).md',
    'escazu-sipco': 'San José/Escazú/Reglamento del Sistema Integral Policial de Comando y Control de Escazú (SIPCO) (2020).md',
    'quepos-video': 'Puntarenas/Quepos/Reglamento del Centro de Video Protección y Monitoreo de Municipalidad de Quepos (2026).md',
    'riocuarto-construccion': 'Alajuela/Río Cuarto/Reglamento para el control constructivo de obras civiles de la Municipalidad de Río Cuarto (2025).md',
    'launion-construccion': 'Cartago/La Unión/Reglamento de regularización de construcciones del cantón de la Unión (2022).md',
    'santaana-policia': 'San José/Santa Ana/Reglamento para la Policía Municipal de la Municipalidad de Santa Ana (2026).md',
    'upala-internet': 'Alajuela/Upala/Reglamento para la Instalación de Locales de Servicio Público de Internet (2001).md',
    'sanpablo-internet': 'Heredia/San Pablo de Heredia/Reglamento para Instalación de los Locales de Servicio Público de Internet en el Cantón San Pablo (2001).md',
    'esparza-internet': 'Puntarenas/Esparza/Reglamento para la Instalación de los Locales de Servicio Público de Internet de la Municipalidad de Esparza (2001).md',
    'talamanca-internet': 'Limón/Talamanca/Reglamento para Instalación de los Locales de Servicio Público de Internet (2001).md',
    'poas-telecom': "Alajuela/Poás/La Municipalidad de Poás Adoptar, en todos sus extremos, las disposiciones del Decreto Ejecutivo N° 44335-MICITT, denominado _Reglamento a la Ley para (2024).md",
    'sarapiqui-telecom': 'Heredia/Sarapiquí/La Municipalidad de Sarapiquí adoptar, en todos sus extremos, las disposiciones del Decreto Ejecutivo N° 44335 (2025).md',
    'limon-telecom': 'Limón/Limón/Adhesión de la Municipalidad de Limón al Decreto Ejecutivo N° 44335 Reglamento a la Ley para incentivar y prom (2025).md',
    'alajuela-virtuales': 'Alajuela/Alajuela/Reglamento de sesiones virtuales del concejo municipal de Alajuela (2020).md',
    'sancarlos-ibi': 'Alajuela/San Carlos/Reglamento Declaración del Impuesto de Bienes Inmuebles Vía Internet en el Cantón de San Carlos (2009).md',
    'garabito-ceci': 'Puntarenas/Garabito/Reglamento para el Uso de los Centros Inteligentes (2011).md',
    'paraiso-comisiones': 'Cartago/Paraíso/Reglamento de comisiones permanentes y especiales Virtuales de la Municipalidad de Paraíso (2022).md',
    'santaana-telecom': 'San José/Santa Ana/La Municipalidad de Santa Ana se adhiere al Reglamento a la Ley para Incentivar y Promover la Construcción de Infraestructura de Telecomunicaciones en (2025).md',
    'vazquez-telecom': 'San José/Vázquez de Coronado/Reglamento a la Ley para incentivar y promover la construcción de infraestructura de telecomunicaciones en Cos (2025).md',
    'alajuelita-ventas': 'San José/Alajuelita/Reglamento para la regulación y el otorgamiento de licencias para ventas ambulantes y estacionarias (2025).md',
    'tarrazu-decomisos': 'San José/Tarrazú/Reglamento para el procedimiento de decomisos de mercadería por ventas ambulantes de la Municipalidad de Tarra (2025).md',
    'leoncortes-ventas': 'San José/León Cortés/Reglamento de ventas ambulantes, estacionarias y comercio sobre ruedas en espacios y vías públicas (2025).md',
    'puntarenas-ruedas': 'Puntarenas/Puntarenas/Reglamento para regular el comercio sobre ruedas en el Cantón Central de la Provincia de Puntarenas (2025).md',
    'sarchi-residencias': 'Alajuela/Sarchí/Reglamento a la aplicación de la Ley N.° 10594 que reforma los artículos 88 del Código Municipal y 29 de la Le (2025).md',
    'santaana-residuos': 'San José/Santa Ana/Reglamento para la gestión separada de residuos del Cantón de Santa Ana (2026).md',
    'monteverde-residuos': 'Puntarenas/Monteverde/Reglamento para el Manejo de Residuos Sólidos del Cantón de Monteverde (2026).md',
    'moravia-tasas': 'San José/Moravia/Reglamento para el cobro de tasas por los servicios de manejo integral de residuos sólidos ordinarios, limpiez (2026).md',
    'sancarlos-policia': 'Alajuela/San Carlos/Reglamento del Departamento de Seguridad Ciudadana y Policía Municipal de la Municipalidad de San Carlos (2024).md',
    'sanjose-policia': 'San José/San José/Reglamento del departameno de policía municipal de la Municipalidad del Cantón Central de San José (2021).md',
    'moravia-areas': 'San José/Moravia/Reglamento para el uso de áreas públicas del Cantón (2025).md',
    'montesdeoca-servicios': 'San José/Montes de Oca/Reglamento de servicios públicos de la Municipalidad de Montes de Oca (2023).md',
    'santaana-parques': 'San José/Santa Ana/Reglamento de parques y zonas verdes públicos del Cantón de Santa Ana (2020).md',
    'coronado-parques': 'San José/Vázquez de Coronado/Reglamento sobre el uso, mantenimiento y protección de parques y espacios públicos de la Municipalidad de Vázq (2025).md',
    'heredia-canes': 'Heredia/Heredia/Reglamento para la adquisición, retiro y donación de los canes de la Unidad Canina de la Policía Municipal de (2018).md',
    'oreamuno-patrimonio': 'Cartago/Oreamuno/Reglamento de protección y conservación del patrimonio arquitectónico y cultura del cantón de Oreamuno (2025).md',
    'cartago-bienales': 'Cartago/Cartago/Reglamento de Bienales Bidimensional Y Tridimensional Museo Municipal de Cartago (2026).md',
    'cartago-interescultural': 'Cartago/Cartago/Reglamento para el trámite de declaratorias de interés cultural de la Municipalidad de Cartago (2024).md',
    'escazu-arte': 'San José/Escazú/Reglamento para manejo de obras de arte propiedad de la Municipalidad de Escazú (2022).md',
    'moravia-banda': 'San José/Moravia/Reglamento de organización y funcionamiento de la Benemérita banda Municipal de Moravia (2026).md',
    'montesdeoca-ccmo': 'San José/Montes de Oca/Reglamento de funcionamiento del Centro de la Cultura de Montes de Oca (CCMO) (2026).md',
    'alajuela-teatro': 'Alajuela/Alajuela/Reglamento para el Uso, Funcionamiento y Conservación del Teatro Municipal de Alajuela (2016).md',
    'orotina-festejos': 'Alajuela/Orotina/Reglamento interno de las Comisiones de Festejos Populares de la Municipalidad de Orotina (2026).md',
    'desamparados-sinfonica': 'San José/Desamparados/Reglamento de becas culturales de la Sinfónica Municipal de Desamparados (2022).md',
    'goicoechea-incentivos': 'San José/Goicoechea/Reglamento para el otorgamiento de incentivos económicos para el deporte y la música en el Cantón de Goicoeche (2024).md',
    'moravia-ruedas': 'San José/Moravia/Reglamento para regular el otorgamiento de licencias comerciales para ejercer el comercio sobre ruedas en el c (2025).md',
    'belen-cecudi': 'Heredia/Belén/Reglamento para regular el funcionamiento y operación de los centros de cuido y desarrollo infantil gestionado (2025).md',
    'escazu-cecudi': 'San José/Escazú/Reglamento para regular el funcionamiento y operación de los Centros de Cuido y Desarrollo Infantil CECUDI del (2023).md',
    'parrita-cecudi': 'Puntarenas/Parrita/Reglamento para regular el funcionamiento y operación del centro de cuido y desarrollo infantil CECUDI del Can (2014).md',
    'escazu-ayudas': 'San José/Escazú/Reglamento para otorgar ayudas temporales a vecinos del Cantón de Escazú en situación transitoria de desgracia (2025).md',
    'poas-ayudas': 'Alajuela/Poás/Reglamento para ayudas temporales y subvenciones del Cantón de Poás (2025).md',
    'pococi-becas': 'Limón/Pococí/Reglamento para el otorgamiento de becas, donaciones, subvenciones y ayudas temporales ante estado de desgraci (2025).md',
    'tarrazu-ninez': 'San José/Tarrazú/Política Cantonal de la Niñez y la Adolescencia de Tarrazú 2025-2035 (2025).md',
    'alajuelita-ninez': 'San José/Alajuelita/Política de niñez y adolescencia para el cantón de Alajuelita 2019-2029 (2022).md',
    'sanpablo-parques': 'Heredia/San Pablo de Heredia/Reglamento para el uso de parques y juegos infantiles (2010).md',
    'oreamuno-juegos': 'Cartago/Oreamuno/Reglamento para la instalación de salas de juegos y máquinas pinball en el Cantón de Oreamuno (2018).md',
    'escazu-ccpj': 'San José/Escazú/Reglamento para la conformación, organización y funcionamiento del Comité Cantonal de la Persona Joven de Esca (2024).md',
    'cervantes-ccpj': 'Cartago/Concejo Municipal de Distrito de Cervantes/Reglamento del Comité de la Persona Joven de Cervantes (2026).md',
    'naranjo-parques': 'Alajuela/Naranjo/Reglamento sobre la Protección, Uso y Mantenimiento de Parques y Espacios Públicos de Competencia Municipal (2009).md',
    'naranjo-opamdis': 'Alajuela/Naranjo/Reglamento interno de la oficina municipal de la persona adulta mayor y de la persona con discapacidad de la M (2025).md',
    'escazu-legado': 'San José/Escazú/Reglamento General Programa Municipal para la persona adulta mayor Legado de Alegría (2026).md',
    'cartago-subsidios-am': 'Cartago/Cartago/Reglamento para otorgar subsidios a personas adultas mayores en condición de riesgo social con fondos municipa (2026).md',
    'sarchi-10359': 'Alajuela/Sarchí/Reglamento para la aplicación de la Ley N° 10359 _Apoyo municipal para adultos mayores en pobreza_ y para la condonación administrativa de obligacione (2025).md',
    'coronado-10359': 'San José/Vázquez de Coronado/Reglamento a la Ley N° 10359 Apoyo Municipal para adultos mayores en pobreza de la Municipalidad de Vázquez de (2025).md',
    'curridabat-10359': 'San José/Curridabat/Reglamento apoyo municipal para adultos mayores en pobreza de la Municipalidad de Curridabat (2026).md',
    'santacruz-10359': 'Guanacaste/Santa Cruz/Plan de condonación de conformidad con los parámetros dispuestos por la Ley 10359 apoyo municipal para adultos mayores (2023).md',
    'quepos-comudam': 'Puntarenas/Quepos/Reglamento para la Comisión Municipal de Discapacidad y Adulto Mayor (COMUDAM) de la Municipalidad de Quepos (2025).md',
    'mora-redcuido-am': 'San José/Mora/Reglamento del programa red de atención progresiva para el cuido integral de las personas adultas mayores en e (2022).md',
    'sanjose-opamdis': 'San José/San José/Reglamento para el funcionamiento y operación de la Oficina para la Persona Adulta Mayor y la Persona con Disc (2024).md',
    'golfito-10359': 'Puntarenas/Golfito/Reglamento municipal de Golfito apoyo municipal para adultos mayores en pobreza, ley N° 10359 (2023).md',
    'heredia-comad': 'Heredia/Heredia/Reglamento de la Comisión de Accesibilidad y Discapacidad (COMAD) (2011).md',
    'escazu-transporte': 'San José/Escazú/Reglamento para regular el otorgamiento y funcionamiento del servicio municipal de transporte para personas co (2025).md',
    'moravia-opdis': 'San José/Moravia/Reglamento para regular el funcionamiento y operación de la Oficina de las personas con Discapacidad Municipal (2023).md',
    'launion-peatonal': 'Cartago/La Unión/Reglamento de movilidad peatonal del Cantón de La Unión (2025).md',
    'oreamuno-atencion': 'Cartago/Oreamuno/Manual de atención y servicio al usuario de la Municipalidad de Oreamuno (2019).md',
    'paraiso-comad': 'Cartago/Paraíso/Reglamento de la comisión de accesibilidad y discapacidad COMAD de la Municipalidad de Paraíso (2021).md',
    'launion-opamdis': 'Cartago/La Unión/Reglamento para regular el funcionamiento y operación de la Oficina Municipal de la Persona Adulta Mayor y de (2024).md',
    'cartago-centrodiurno': 'Cartago/Cartago/Reglamento Interno para el ingreso y el uso del Centro Diurno de Atención a la persona Adulta Mayor (2015).md',
    'sanisidro-genero': 'Heredia/San Isidro de Heredia/Política de Igualdad y Equidad de Género 2025-2035 (2025).md',
    'moravia-policia': 'San José/Moravia/Reglamento del Cuerpo de la Policía Municipal Moravia (2014).md',
    'pz-seguridad': 'San José/Pérez Zeledón/Reglamento para la regulación de las funciones y servicios del subproceso de control y seguridad ciudadana de (2017).md',
    'curridabat-espectaculos': 'San José/Curridabat/Reglamento de espectáculos públicos de la Municipalidad de Curriidabat (2024).md',
    'sanjose-perifoneo': 'San José/San José/Reglamento que regula la actividad de perifoneo y otras fuentes emisoras de sonido dentro de la jurisdicción d (2016).md',
    'zarcero-licencias': 'Alajuela/Zarcero/Reglamento para la solicitud de licencias municipales en el Cantón de Zarcero (2020).md',
    'alajuela-espectaculos': 'Alajuela/Alajuela/Reglamento de espectáculos públicos, actividades y eventos de la Municipalidad de Alajuela (2021).md',
    'santaana-casajusticia': 'San José/Santa Ana/Reglamento de Organización, Funcionamiento y Ética de La Casa de Justicia de Santa Ana (2014).md',
    'grecia-policia': 'Alajuela/Grecia/Reglamento de policía municipal del Cantón de Grecia (2026).md',
    'sanjose-casajusticia': 'San José/San José/Reglamento interno de organización, funcionamiento y ética de la Casa de Justicia (2015).md',
    'ifam-casajusticia': 'Entes intermunicipales/IFAM/Reglamento de Organización, Funcionamiento y Ética de las Casas de Justicia (2015).md',
    'desamparados-ninez': 'San José/Desamparados/Política cantonal de niñez y adolescencias del cantón de Desamparados, y su plan de acción interinstitucional (2023).md',
    'guatuso-raos': 'Alajuela/Guatuso/Reglamento Autónomo de Organización y Servicios de la Municipalidad del Cantón de Guatuso (2018).md',
    'grecia-opamdis': 'Alajuela/Grecia/Reglamento para la oficina municipal de la persona adulta mayor y de la persona con discapacidad de Grecia (2025).md',
    'santaana-ensueno': 'San José/Santa Ana/Reglamento para la admisión, permanencia y egreso de personas beneficiarias del Centro Diurno Municipal de adultos mayores Ensueño de Oro (2024).md',
    'escazu-ccdr': 'San José/Escazú/Reforma Integral Reglamento para el nombramiento y funcionamiento del Comité Cantonal de Deportes y Recreación del Cantón de Escazú y de los Comités C (2025).md',
    'goicoechea-estigma': 'San José/Goicoechea/Política publica cantonal declaratoria del cantón libre de estigma y discriminación (2021).md',
    'santaana-joven': 'San José/Santa Ana/Reglamento del comité de la persona joven del cantón de Santa Ana (2025).md',
    'cartago-adicciones': 'Cartago/Cartago/Reglamento para la atención de las adicciones al alcohol y otras sustancias psicoactivas de las personas colab (2024).md',
    'heredia-palacio': 'Heredia/Heredia/Reglamento para la administración y funcionamiento del Palacio de los Deportes de Heredia (2026).md',
    'sancarlos-acoso': 'Alajuela/San Carlos/Reglamento para prevenir, investigar y sancionar el acoso laboral en la Municipalidad de San Carlos (2019).md',
    'santabarbara-so': 'Heredia/Santa Bárbara/Reglamento de salud ocupacional de la Municipalidad de Santa Bárbara (2023).md',
    'sanisidro-teletrabajo': 'Heredia/San Isidro de Heredia/Reglamento para la aplicación del teletrabajo en la Municipalidad de San Isidro de Heredia (2024).md',
    'cnp-pai': '/home/claude/repo/main/Leyes y decretos nacionales/Administrativo/Reglamento del Programa de Abastecimiento Institucional CNP (2023).md',
    'goicoechea-mercadolibre': 'San José/Goicoechea/Reglamento de Organización y Funcionamiento del Mercado Libre de Guadalupe (2005).md',
    'canas-feria': 'Guanacaste/Cañas/Reglamento de la Feria Municipal del Mercado Libre del Agricultor (2004).md',
    'alajuela-mercado': 'Alajuela/Alajuela/Reglamento del Mercado Municipal de Alajuela (2014).md',
    'sancarlos-donaciones': 'Alajuela/San Carlos/Reglamento para entrega de donaciones de la Municipalidad de San Carlos (2026).md',
    'oreamuno-decomisos': 'Cartago/Oreamuno/Reglamento para Decomisos de Mercadería por Ventas en la Vía Pública y Fería del Agricultor (2015).md',
    'tarrazu-bienestar': 'San José/Tarrazú/Política Cantonal de Bienestar Animal de Tarrazú (2026).md',
    'naranjo-policia': 'Alajuela/Naranjo/Reglamento de la policía municipal e inspectores municipales de tránsito de la Municipalidad de Naranjo (2025).md',
    'acosta-reductores': 'San José/Acosta/Reglamento para la instalación y eliminación de reductores de velocidad en las vías públicas terrestres de acu (2018).md',
    'santaana-reductores': 'San José/Santa Ana/Reglamento para la Instalación de Reductores de Velocidad en las Vías Cantonales (2009).md',
    'poas-colosevi': 'Alajuela/Poás/Reglamento del Consejo Local de Seguridad Vial (COLOSEVI-POÁS) (2008).md',
    'atenas-colosevi': 'Alajuela/Atenas/Reglamento del Consejo local de Seguridad Vial (COLOSEVI) de la Municipalidad de Atenas (2012).md',
    'sanjose-riesgo': 'San José/San José/Reglamento para la Gestión Ambiental, Gestión de Riesgo, Atención de Emergencias y Desastres (2005).md',
    'curridabat-riesgo': 'San José/Curridabat/Reglamento para la Gestión de Riesgo y Atención de Emergencias y Desastres en el cantón de Curridabat (2007).md',
    'sanjose-ayudas-emergencia': 'San José/San José/Reglamento para el otorgamiento de ayudas temporales en el cantón San José para situaciones de emergencias o d (2016).md',
    'naranjo-mercado': 'Alajuela/Naranjo/Reglamento de organización, funcionamiento y administración del Mercado Municipal de Naranjo (2020).md',
    'atenas-mercado': 'Alajuela/Atenas/Reglamento General del Mercado (2009).md',
    'orotina-parques': 'Alajuela/Orotina/Reglamento sobre el uso, mantenimiento y protección de parques y espacios públicos de la Municipalidad de Orotina (2017).md',
    'montesdeoca-parques': 'San José/Montes de Oca/Reglamento para el uso, mantenimiento y protección de los parques y espacios públicos del cantón de Montes de (2025).md',
    'barva-ayudas': 'Heredia/Barva/Reglamento para el otorgamiento de ayudas temporales a los y las habitantes del Cantón de Barva (2020).md',
    'ifam-financiamiento': 'Entes intermunicipales/IFAM/Reglamento de financiamiento del Instituto de Fomento y Asesoría Municipal (IFAM) (2021).md',
    'grecia-licores': 'Alajuela/Grecia/Reglamento de Regulación y Comercialización de Bebidas con Contenido Alcohólico de la Municipalidad de Grecia (2015).md',
    'poas-licores': 'Alajuela/Poás/Reglamento de patentes de licores del Cantón de Poás (2022).md',
    'zarcero-trabajo': 'Alajuela/Zarcero/Reglamento interno de trabajo de la Municipalidad de Zarcero (2018).md',
    'escazu-cementerios': 'San José/Escazú/Reglamento municipal de cementerios para el Cantón de Escazú (2017).md',
    'golfito-cementerios': 'Puntarenas/Golfito/Reglamento para la administración de los cementerios Municipales del cantón de Golfito (2021).md',
    'poas-cementerios': 'Alajuela/Poás/Reforma integral Reglamento General de Cementerios Municipalidad del cantón de Poás (2024).md',
    'goicoechea-cementerios': 'San José/Goicoechea/Reglamento de organización y funcionamiento de la junta administrativa de cementerios del cantón de Goicoechea (2023).md',
    'buenosaires-cementerios': 'Puntarenas/Buenos Aires/Reglamento autónomo para la planificación, dirección y administración de los cementerios municipales del cantó (2026).md',
    'tilaran-cementerios': 'Guanacaste/Tilarán/Reglamento de operación y mantenimiento del cementerio municipal de Tilarán (2018).md',
    'escazu-brigadistas': 'San José/Escazú/Reglamento para brigadistas ad-honorem de seguridad vial y atención de emergencias y monitoreos preventivos (2018).md',
    'goicoechea-discriminacion': 'San José/Goicoechea/Reglamento interno contra la discriminación (2013).md',
    'elguarco-diversidad': 'Cartago/El Guarco/Política para la No Discriminación motivada por la Orientación Sexual o la Identidad de Género de la Municipal (2015).md',
    'garabito-diversidad': 'Puntarenas/Garabito/Política de Diversidad, inclusión y no discriminación de Garabito (2020).md',
    'sanisidro-diversidad': 'Heredia/San Isidro de Heredia/Políticas de buenas prácticas para la no discriminación motivada por la orientación sexual o la identidad de g (2014).md',
    'turrialba-albergue-indigena': 'Cartago/Turrialba/Reglamento del DITSÁ KÄPÄ KLÄ JUÍ ( Albergue indígena para población Cabecar) (2020).md',
    'sanisidro-hostigamiento': 'Heredia/San Isidro de Heredia/Reglamento para la prevención y sanción de las conductas que configuren hostigamiento sexual en la Municipalid (2026).md',
    'launion-ccdr-hostigamiento': 'Cartago/La Unión/Reglamento interno contra el hostigamiento y acoso sexual del comité cantonal de deportes y recreación de la u (2025).md',
    'alajuela-licencias': 'Alajuela/Alajuela/Reglamento general de licencias comerciales de la Municipalidad del Cantón Central de Alajuela (2021).md',
    'garabito-ventas': 'Puntarenas/Garabito/Reglamento de ventas ambulantes y estacionarias (2024).md',
    'garabito-ciclismo': 'Puntarenas/Garabito/Reglamento municipal para la implementación de la ley N° 9660 de movilidad y seguridad ciclística en el cantón (2025).md',
    'sanjose-mercados': 'San José/San José/Reglamento general de mercados municipales del Cantón de San José (2016).md',
    'corredores-mercados': 'Puntarenas/Corredores/Reglamento de organización y funcionamiento de los mercados municipales, terminales y otros inmuebles de arrie (2025).md',
    'mora-mercado': 'San José/Mora/Reglamento autónomo de organización y funcionamiento del mercado municipal de Ciudad Colón en el Cantón de Mor (2025).md',
    'quepos-licencias': 'Puntarenas/Quepos/Reglamento de licencias comerciales de la Municipalidad de Quepos (2026).md',
    'lepanto-zmt': 'Puntarenas/Concejo Municipal de Distrito de Lepanto/Reglamento para el otorgamiento de permisos de uso de la Zona Marítimo Terrestre en el Distrito de Lepanto (2024).md',
    'belen-reclutamiento': 'Heredia/Belén/Reglamento de Reclutamiento y Selección de Personal de la Municipalidad de Belén (2026).md',
}
MESES_RM = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'setiembre', 'octubre', 'noviembre', 'diciembre']


def f_rm(k):
    f = RM.get(k, '') if RM.get(k, '').startswith('/') else '""" + RMBASE + """' + RM.get(k, '')
    return f if k in RM and os.path.exists(f) else None


_RM_LETRA = None


def _rm_datos(k):
    d = meta(f_rm(k))
    fd = fdate(d['fecha_norma']) or fdate(d['fecha'])
    autor = d['ente_emisor'].strip()
    autor = {'Municipalidad de León Cortes': 'Municipalidad de León Cortés'}.get(autor, autor)
    return d, fd, autor


def rm_letra(k):
    # APA 7: mismo autor y mismo año en el capítulo -> 2021a, 2021b, por orden alfabético del título
    global _RM_LETRA
    if _RM_LETRA is None:
        _RM_LETRA = {}
        claves = set()
        for g in glob.glob(f'{SRC}/*.md'):
            claves |= set(re.findall(r'RM:([\\w-]+)', open(g, encoding='utf-8').read()))
        grupos = {}
        for c in claves:
            if f_rm(c):
                d, fd, autor = _rm_datos(c)
                grupos.setdefault((autor, fd[0] if fd else ''), []).append((d['nombre'].strip().lower(), c))
        for v in grupos.values():
            if len(v) > 1:
                for i, (_, c) in enumerate(sorted(v)):
                    _RM_LETRA[c] = 'abcdefghij'[i]
    return _RM_LETRA.get(k, '')


def cita_rm(k, loc):
    f = f_rm(k)
    if not f:
        errors.append(f'REGLAMENTO MUNICIPAL sin archivo: {k}')
        return f'(Reglamento municipal {k}, {loc})'
    d = meta(f)
    fd = fdate(d['fecha_norma']) or fdate(d['fecha'])
    y = f'{fd[0]}{rm_letra(k)}' if fd else ''
    fecha = f'{y}, {fd[2]} de {MESES_RM[fd[1] - 1]}' if fd else ''
    url = f' {d["enlace"]}' if d['enlace'] else ''
    autor = d['ente_emisor'].strip()
    autor = {'Municipalidad de León Cortes': 'Municipalidad de León Cortés'}.get(autor, autor)
    add_ref('RM' + k, (autor.lower(), y), f'{autor}. ({fecha}). *{d["nombre"].strip()}*. Sistema Costarricense de Información Jurídica.{url}')
    return f'({autor}, {y}, {loc})' if loc else f'({autor}, {y})'

"""
i = src.index('\ndef expand(macro):')
src = src[:i] + '\n' + rm_code + src[i:]
e3 = "    if kind == 'DE':\n        return cita_dec(p[1], p[2] if len(p) > 2 else '')"
assert src.count(e3) == 1
src = src.replace(e3, e3 + "\n    if kind == 'RM':\n        return cita_rm(p[1], p[2] if len(p) > 2 else '')")
e4 = "        elif kind == 'DE':\n            f = f_dec(p[1])\n            if f:\n                raw = read(f)\n                res = ('art', seg_articulos(raw), norm(raw))"
assert src.count(e4) == 1
src = src.replace(e4, e4 + "\n        elif kind == 'RM':\n            f = f_rm(p[1])\n            if f:\n                raw = read(f)\n                res = ('art', seg_articulos(raw), norm(raw))")
# decretos que no están en el repositorio (texto de SINALEVI aportado por el autor)
e5 = "def f_dec(n):\n    fs = glob.glob(f'{R}/Leyes y decretos nacionales/*/Decreto Ejecutivo {n}.md')"
assert src.count(e5) == 1
src = src.replace(e5, "DEC_ESPECIALES = {'42075': '/home/claude/libro/fuentes/Decreto Ejecutivo 42075.md'}\n\n\ndef f_dec(n):\n    if n in DEC_ESPECIALES:\n        return DEC_ESPECIALES[n]\n    fs = glob.glob(f'{R}/Leyes y decretos nacionales/*/Decreto Ejecutivo {n}.md')")
e6 = "Poder Ejecutivo de la República de Costa Rica. Sistema Costarricense de Información Jurídica.{url}')"
assert src.count(e6) == 1
src = src.replace(e6, "Poder Ejecutivo de la República de Costa Rica. {FUENTE_DEC.get(n, '')}Sistema Costarricense de Información Jurídica.{url}')")
src = src.replace("DEC_ESPECIALES = {", "FUENTE_DEC = {'42075': 'La Gaceta N.° 80, Alcance N.° 87, 14 de abril de 2020. '}\nDEC_ESPECIALES = {", 1)
# votos que no están en el repositorio (texto de NexusPJ aportado por el autor)
e7 = "def f_voto(x):\n"
assert src.count(e7) == 1
src = src.replace(e7, e7 + "    _loc = f'/home/claude/libro/fuentes/votos/Sentencia {x}.md'\n    if os.path.exists(_loc):\n        return _loc\n")
# dictámenes y opiniones jurídicas aportados por el autor (no están en el repositorio)
e8 = "def f_pgr(x):\n"
assert src.count(e8) == 1
src = src.replace(e8, e8 + "    _loc = f'/home/claude/libro/fuentes/dictamenes/Dictamen {x}.md'\n    if os.path.exists(_loc):\n        return _loc\n")
e9 = "    add_ref('D' + x, ('procuraduria', y, mo, da, x), f'Procuraduría General de la República. ({y}, {da} de {MES[mo]}). *Dictamen {x}*.{url}')\n    return f'(Procuraduría General de la República, dictamen {x}, {y}, {loc})' if loc else f'(Procuraduría General de la República, dictamen {x}, {y})'"
assert src.count(e9) == 1
src = src.replace(e9, "    _t = 'opinión jurídica' if x.startswith('OJ') else 'dictamen'\n    add_ref('D' + x, ('procuraduria', y, mo, da, x), f'Procuraduría General de la República. ({y}, {da} de {MES[mo]}). *{_t.capitalize()} {x}*.{url}')\n    return f'(Procuraduría General de la República, {_t} {x}, {y}, {loc})' if loc else f'(Procuraduría General de la República, {_t} {x}, {y})'")
# resoluciones del Tribunal Contencioso aportadas por el autor y macro de la Sala Primera: [[S1:2025-000402:considerando V]]
e10 = "def f_tca(x):\n"
assert src.count(e10) == 1
src = src.replace(e10, e10 + "    _fs = glob.glob(f'/home/claude/libro/fuentes/tca/Sentencia TCA * {x}.md')\n    if _fs:\n        return _fs[0]\n")
s1_code = """
first_s1 = set()


def f_s1(x):
    for b in ('/home/claude/libro/fuentes/sala1', f'{R}/Jurisprudencia de casación (Sala Primera)/Laterales', f'{R}/Jurisprudencia de casación (Sala Primera)'):
        f = f'{b}/Sentencia Sala Primera {x}.md'
        if os.path.exists(f):
            return f
    return None


def cod_s1(x):
    yy, num = x.split('-')
    f = f_s1(x)
    if f:
        m = re.search(r'(?im)^\s*res\s*[.:]?\s*(\d{3,6}-F-(?:S1-)?\d{2,4})', open(f, encoding='utf-8').read())
        if m:
            c = m.group(1)
            c = c if c.startswith(num) else f'{num}-' + c.split('-', 1)[1]
            pre, _, yr = c.rpartition('-')
            return f'{pre}-{yy}' if len(yr) == 2 else c
    return f'{num}-F-S1-{yy}'


def cita_s1(x, loc):
    f = f_s1(x)
    yy, num = x.split('-')
    cod = cod_s1(x)
    if not f:
        errors.append(f'SALA PRIMERA sin archivo: {x}')
        return f'(Sala Primera, resolución N.° {cod}, {loc})'
    d = meta(f)
    y, mo, da = fdate(d['fecha'])
    h = hora(d['hora'])
    hs = f', de las {h} horas' if h else ''
    exp = f' (expediente {d["expediente"]})' if d['expediente'] else ''
    add_ref('S1' + x, ('sala primera', y, mo, da, x), f'Sala Primera de la Corte Suprema de Justicia. ({y}, {da} de {MES[mo]}). *Resolución N.° {cod}{hs}*{exp}. NexusPJ.')
    if x not in first_s1:
        first_s1.add(x)
        base = f'Sala Primera, resolución N.° {cod}, de las {h} horas del {da} de {MES[mo]} de {y}' if h else f'Sala Primera, resolución N.° {cod}, del {da} de {MES[mo]} de {y}'
    else:
        base = f'Sala Primera, resolución N.° {cod}'
    return f'({base}, {loc})' if loc else f'({base})'

"""
e11 = "\ndef expand(macro):"
assert src.count(e11) == 1
src = src.replace(e11, s1_code + e11)
e12 = "    if kind == 'T':\n        return cita_tca(p[1], p[2] if len(p) > 2 else '')"
assert src.count(e12) == 1
src = src.replace(e12, "    if kind == 'S1':\n        return cita_s1(p[1], p[2] if len(p) > 2 else '')\n" + e12)
e13 = "        elif kind == 'T':\n            f = f_tca(p[1])"
assert src.count(e13) == 1
src = src.replace(e13, "        elif kind == 'S1':\n            f = f_s1(p[1])\n            if f:\n                raw = read(f)\n                res = ('cons', seg_considerandos(raw), norm(raw))\n" + e13)

# tribunales laterales (penal, familia): [[J:TASP-2017-001529:considerando III]]
jur_code = """
JUR = {
    'TASP': dict(org='Tribunal de Apelación de Sentencia Penal del II Circuito Judicial de San José', sig='TASP', pref='Sentencia TASP'),
    'TF': dict(org='Tribunal de Familia', sig='TF', pref='Sentencia TF'),
    'TSE': dict(org='Tribunal Supremo de Elecciones', sig='TSE', pref='Resolución TSE', dir='Jurisprudencia electoral (TSE)/Municipal', base=''),
}
first_j = set()


def f_j(x):
    t, num = x.split('-', 1)
    f = f'{R}/{JUR[t].get("dir", "Jurisprudencia penal y de familia (laterales)")}/{JUR[t]["pref"]} {num}.md'
    return f if os.path.exists(f) else None


def cita_j(x, loc):
    f = f_j(x)
    t, num = x.split('-', 1)
    yy, n = num.split('-')
    cod = f'{int(n)}-{yy}'
    org = JUR[t]['org']
    if not f:
        errors.append(f'TRIBUNAL sin archivo: {x}')
        return f'({org}, resolución N.° {cod}, {loc})'
    d = meta(f)
    _mcod = re.search(r'(?m)^codigo:\\s*"([^"]*)"', read(f)[:3000])
    cod = _mcod.group(1).strip() if _mcod else cod
    y, mo, da = fdate(d['fecha'])
    h = hora(d['hora'])
    hs = f', de las {h} horas' if h else ''
    exp = f' (expediente {d["expediente"]})' if d['expediente'] else ''
    bd = JUR[t].get('base', 'NexusPJ')
    bd = f' {bd}.' if bd else ''
    add_ref('J' + x, (org.lower(), y, mo, da, x), f'{org}. ({y}, {da} de {MES[mo]}). *Resolución N.° {cod}{hs}*{exp}.{bd}')
    if x not in first_j:
        first_j.add(x)
        base = f'{org} [{t}], resolución N.° {cod}, de las {h} horas del {da} de {MES[mo]} de {y}' if h else f'{org} [{t}], resolución N.° {cod}, del {da} de {MES[mo]} de {y}'
    else:
        base = f'{org}, resolución N.° {cod}'
    return f'({base}, {loc})' if loc else f'({base})'

"""
src = src.replace(e11, jur_code + e11, 1)
src = src.replace("    if kind == 'S1':\n        return cita_s1(", "    if kind == 'J':\n        return cita_j(p[1], p[2] if len(p) > 2 else '')\n    if kind == 'S1':\n        return cita_s1(", 1)
src = src.replace("        elif kind == 'S1':\n            f = f_s1(p[1])\n", "        elif kind == 'J':\n            f = f_j(p[1])\n            if f:\n                raw = read(f)\n                res = ('cons', seg_considerandos(raw), norm(raw))\n        elif kind == 'S1':\n            f = f_s1(p[1])\n", 1)
e14 = "(?!\\d)(?:\\s*(bis|ter)\\b)?\\s*[\\.\\-—–:º°o*]')"
assert src.count(e14) == 1, src.count(e14)
src = src.replace(e14, "(?!\\d)(?:[\\s*]*(bis|ter|qu[aá]ter|quinquies|sexies)\\b)?[\\s*]*[\\.\\-—–:º°o*]')")
e15 = "lab = m.group(1) + (' ' + m.group(2).lower() if m.group(2) else '')"
assert src.count(e15) == 1
src = src.replace(e15, "lab = m.group(1) + (' ' + m.group(2).lower().replace('á', 'a') if m.group(2) else '')")
e16 = "        m = re.search(r'art\\.\\s*(\\d+(?:\\s*(?:bis|ter))?)', loc)\n        want = m.group(1) if m else None"
assert src.count(e16) == 1, src.count(e16)
src = src.replace(e16, "        m = re.search(r'art\\.\\s*(\\d+(?:\\s*(?:bis|ter|qu[aá]ter|quinquies|sexies)\\b)?)', loc)\n        want = re.sub(r'\\s+', ' ', m.group(1)).replace('á', 'a') if m else None")
# rutas del taller con respaldo en el repositorio (rama main), para que el verificador funcione en una sesión nueva
e17 = "    if n in ESPECIALES:\n        return ESPECIALES[n]"
assert src.count(e17) == 1
src = src.replace(e17, "    if n in ESPECIALES and os.path.exists(ESPECIALES[n]):\n        return ESPECIALES[n]")
e18 = "    if n in DEC_ESPECIALES:\n        return DEC_ESPECIALES[n]"
assert src.count(e18) == 1
src = src.replace(e18, "    if n in DEC_ESPECIALES and os.path.exists(DEC_ESPECIALES[n]):\n        return DEC_ESPECIALES[n]")
e19 = "    for b in ('/home/claude/libro/fuentes/sala1', "
assert src.count(e19) == 1
src = src.replace(e19, e19 + "f'{R}/Jurisprudencia de casación (Sala Primera)/Municipal', ")
e20 = "'/home/claude/libro/fuentes/Reglamento de Construcciones INVU (2018).md'"
assert src.count(e20) == 1
src = src.replace(e20, "'/home/claude/repo/main/Leyes y decretos nacionales/Municipal/Reglamento de Construcciones INVU (2018).md'")
# leyes cuya ficha no trae fecha: se toma de la nota del propio texto
e21 = "    fd = fdate(d['fecha_norma']) or fdate(d['fecha'])\n    if not fd:\n        errors.append(f'LEY sin fecha: {n}')"
assert src.count(e21) == 1, src.count(e21)
src = src.replace(e21, "    fd = fdate(d['fecha_norma']) or fdate(d['fecha']) or fdate({'30': '19/04/1885'}.get(n, ''))\n    if not fd:\n        errors.append(f'LEY sin fecha: {n}')")
# --- forma corta de las citas (CITA=corta), 23 de noviembre de 2026 ---
# Se agrega al final de hacer_build_libro.py, antes de escribir build_libro.py.
corta_code = r'''
# ---------- forma corta de las citas: CITA=corta ----------
# Primera mención por capítulo: cita completa (APA 7) con la sigla entre corchetes si la fuente la tiene.
# Menciones siguientes: forma corta. Sin CITA=corta, el verificador produce la forma larga de siempre.
CORTA = os.environ.get('CITA', '').lower() == 'corta'
SIGLAS = {'CP': 'CP', '7794': 'CM', '6227': 'LGAP', '30': 'CC', '2': 'CT', '7135': 'LJC', '4755': 'CNPT',
          '8508': 'CPCA', '4240': 'LPU', '5395': 'LGS', '7739': 'CNA', '9609': 'CPA', '9342': 'CPC',
          '7554': 'LOA', '9986': 'LGCP', '4573': 'CPen'}
MANUAL_CORTA = {
    'Consejo para la Promoción de la Competitividad, 2026': (
        'Consejo para la Promoción de la Competitividad, Índice de Competitividad Nacional [ICN], 2026', 'ICN'),
}
vistos = set()


def abrev(loc):
    s = loc
    for a, b in [(r'\bconsiderandos\b', 'cons.'), (r'\bconsiderando\b', 'cons.'), (r'\bapartados\b', 'aps.'),
                 (r'\bapartado\b', 'ap.'), (r'\bconclusiones\b', 'concls.'), (r'\bconclusión\b', 'concl.'),
                 (r'\bresultandos\b', 'result.'), (r'\bresultando\b', 'result.'), (r'\bartículos\b', 'arts.'),
                 (r'\bartículo\b', 'art.')]:
        s = re.sub(a, b, s)
    return s


def _par(base, loc):
    return f'({base}, {loc})' if loc else f'({base})'


def _cgr_nombre():
    if 'CGR' in vistos:
        return 'CGR'
    vistos.add('CGR')
    return 'Contraloría General de la República [CGR]'


def expand_corta(macro, larga):
    p = [x.strip() for x in macro.replace('!', '').split(':')]
    kind = p[0]
    loc = p[2] if len(p) > 2 else ''
    if kind == 'CP':
        loc = p[1] if len(p) > 1 else ''
        if 'CP' not in vistos:
            vistos.add('CP')
            return _par('Constitución Política de la República de Costa Rica [CP], 1949', loc)
        return _par('CP', abrev(loc))
    if kind == 'L':
        n = p[1]; sig = SIGLAS.get(n); k = 'L' + n
        if k not in vistos:
            vistos.add(k)
            if not sig:
                return larga
            m = re.match(r'\(Ley N\.° \S+, ([^,]+), ', larga + ', ')
            y = m.group(1).rstrip(')') if m else ''
            return _par(f'Ley N.° {n} [{sig}], {y}', loc)
        return _par(sig or f'Ley {n}', abrev(loc))
    if kind == 'DE':
        k = 'DE' + p[1]
        if k not in vistos:
            vistos.add(k); return larga
        return _par(f'Decreto Ejecutivo {p[1]}', abrev(loc))
    if kind == 'RM':
        return larga
    if kind == 'V':
        k = 'V' + p[1]
        if k not in vistos:
            vistos.add(k); return larga
        return _par(f'voto {p[1]}', abrev(loc))
    if kind == 'VT':
        k = 'V' + p[2]
        if k not in vistos:
            vistos.add(k); return larga
        return f'(voto {p[1]}, transcrito en el voto {p[2]}, {abrev(p[3])})'
    if kind == 'D':
        k = 'D' + p[1]
        if k not in vistos:
            vistos.add(k); return larga
        return _par(p[1], abrev(loc))
    if kind == 'J':
        t, num = p[1].split('-', 1); yy, n = num.split('-'); cod = f'{int(n)}-{yy}'; k = 'J' + p[1]
        _mc = re.search(r'resolución N\.° (\S+?)[,)]', larga)
        if _mc: cod = _mc.group(1)
        if k not in vistos:
            vistos.add(k); return larga
        return _par(f'{t}, {cod}', abrev(loc))
    if kind == 'S1':
        yy, num = p[1].split('-'); cod = cod_s1(p[1]); k = 'S1' + p[1]
        if k not in vistos:
            vistos.add(k); return larga
        return _par(f'Sala Primera, {cod}', abrev(loc))
    if kind == 'T':
        k = 'T' + p[1]
        m = re.match(r'\(Tribunal Contencioso Administrativo(?:, Sección (\w+))?, resolución N\.° (\S+?)[,)]', larga)
        sec = m.group(1) if m else None; num = m.group(2) if m else p[1]
        sig = f'TCA {sec}' if sec else 'TCA'
        if k not in vistos:
            vistos.add(k)
            org = f'Tribunal Contencioso Administrativo, Sección {sec}' if sec else 'Tribunal Contencioso Administrativo'
            return _par(f'{org} [{sig}], resolución N.° {num}', loc)
        return _par(f'{sig}, {num}', abrev(loc))
    if kind == 'O':
        c = p[1]; k = 'O' + c
        if c in ('IGSM', 'IGSMF'):
            if k not in vistos:
                vistos.add(k)
                nom = _cgr_nombre()
                if c == 'IGSM':
                    vistos.add('IGSM-sigla')
                    return _par(f'{nom}, Índice de Gestión de Servicios Municipales 2025 [IGSM], informe N.° DFOE-LOC-SGP-00002-2025, 2025', loc)
                t = 'fichas de indicadores del IGSM 2025' if 'IGSM-sigla' in vistos else 'fichas de indicadores del Índice de Gestión de Servicios Municipales 2025'
                vistos.add('IGSM-sigla')
                return _par(f'{nom}, {t} [IGSM, fichas], 2025', loc)
            return _par('IGSM' if c == 'IGSM' else 'IGSM, fichas', loc)
        cita = CGR[c]['cita']
        if k not in vistos:
            vistos.add(k)
            return _par(f'{_cgr_nombre()}, {cita}', loc)
        m = re.match(r'(oficio|informe|resolución) N\.° (\S+)', cita)
        doc = f'{m.group(1)} {m.group(2).rstrip(",")}' if m else cita
        return _par(f'CGR, {doc}', abrev(loc))
    return larga


def manual_corta(text):
    for key, (primera, sig) in MANUAL_CORTA.items():
        def rep(mm):
            resto = mm.group(1)
            if key not in vistos:
                vistos.add(key)
                return f'({primera}{resto})'
            return f'({sig}{resto})'
        text = re.sub(r'\(' + re.escape(key) + r'((?:, [^()]*)?)\)', rep, text)
    return text

'''
i = src.index('\ndef expand(macro):')
src = src[:i] + '\n' + corta_code + src[i:]
# expand original -> expand_larga; expand nuevo con grupos (A|B) y forma corta
src = src.replace('\ndef expand(macro):', '\ndef expand_larga(macro):', 1)
nuevo = r'''

def expand(macro):
    partes = [x for x in macro.split('|') if x.strip()]
    if len(partes) > 1:
        # dentro de un grupo, el autor que se repite en la fuente siguiente no se vuelve a escribir
        piezas, prev = [], None
        for x in partes:
            s = expand(x)[1:-1]
            aut = s.split(', ')[0]
            if prev and aut == prev and len(s.split(', ')) > 2:
                s = s[len(aut) + 2:]
            prev = aut
            piezas.append(s)
        return '(' + '; '.join(piezas) + ')'
    larga = expand_larga(macro)
    if not CORTA or larga.startswith('[['):
        return larga
    return expand_corta(macro, larga)

'''
j = src.index('\n# ---------- cotejo ----------')
src = src[:j] + nuevo + src[j:]
# una cita textual no puede llevar una macro agrupada
g1 = "            if macro:\n                p = [x.strip() for x in macro.split(':')]"
assert src.count(g1) == 1
src = src.replace(g1, "            if macro and '|' in macro:\n                errors.append(f'[{fname}] CITA TEXTUAL con macro agrupada: \"{q[:50]}\"')\n                continue\n" + g1)
# primera mención por capítulo y forma corta de las fuentes manuales
g2 = "    # 3) expansión\n    out = re.sub(MACRO_RE, lambda m: expand(m.group(1)), text)"
assert src.count(g2) == 1
src = src.replace(g2, "    # 3) expansión (en forma corta, la primera mención se cuenta por capítulo)\n    if CORTA:\n        vistos.clear(); first_v.clear(); first_s1.clear()\n    out = re.sub(MACRO_RE, lambda m: expand(m.group(1)), text)\n    if CORTA:\n        out = manual_corta(out)")

# secciones del Tribunal Contencioso más allá de la IV (tema 27: Sección IX)
_e = "secs = {'I': 'Sección I', 'II': 'Sección II', 'III': 'Sección III', 'IV': 'Sección IV'}"
assert src.count(_e) == 1
src = src.replace(_e, "secs = {k: f'Sección {k}' for k in ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X')}")
open('/home/claude/mis_scripts/build_libro.py', 'w', encoding='utf-8').write(src)
c = open('/home/claude/scripts/cite.py', encoding='utf-8').read().replace('/home/claude/scripts/build.py', '/home/claude/mis_scripts/build_libro.py')
open('/home/claude/mis_scripts/cite_libro.py', 'w', encoding='utf-8').write(c)
print('build_libro.py y cite_libro.py listos')
