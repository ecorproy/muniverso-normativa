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
    'Pérez Hernández et al., 2019': dict(
        file='/home/claude/libro/fuentes/perez_pag.txt',
        ref='Pérez Hernández, L., Tabares Neyra, L. M. y Díaz Legón, O. J. (2019). Lo local –municipal– como espacio de desarrollo en Cuba. Notas para el perfeccionamiento del régimen jurídico de la administración local. *Universidad de La Habana*, (287), 135-160.'),
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
i = src.index('MANUAL = {'); j = src.index('\ndef ', i)
src = src[:j] + '\n' + extra + src[j:]
# leyes que no están en el repositorio y se leen del diario oficial
e1 = "ESPECIALES = {'7135': '/home/claude/repo/main/Leyes y decretos nacionales/Constitucional/Ley Jurisdicción Constitucional.md'}"
assert src.count(e1) == 1
src = src.replace(e1, e1 + "\nESPECIALES['10939'] = '/home/claude/libro/fuentes/Ley 10939.md'\nESPECIALES['8799'] = '/home/claude/libro/fuentes/Ley 8799.md'\nESPECIALES['9458'] = '/home/claude/libro/fuentes/Ley 9458.md'\nESPECIALES['10594'] = '/home/claude/libro/fuentes/Ley 10594.md'\nESPECIALES['8661'] = '/home/claude/libro/fuentes/Ley 8661.md'\nESPECIALES['7948'] = '/home/claude/libro/fuentes/Ley 7948.md'\nFUENTE_LEY = {'10939': 'La Gaceta N.° 91, Alcance N.° 59, 20 de mayo de 2026.'}")
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
    'santaana-policia': 'San José/Santa Ana/Reglamento para la Policía Municipal de la Municipalidad de Santa Ana (2026).md',
    'paraiso-comisiones': 'Cartago/Paraíso/Reglamento de comisiones permanentes y especiales Virtuales de la Municipalidad de Paraíso (2022).md',
    'santaana-telecom': 'San José/Santa Ana/La Municipalidad de Santa Ana se adhiere al Reglamento a la Ley para Incentivar y Promover la Construcción de Infraestructura de Telecomunicaciones en (2025).md',
    'vazquez-telecom': 'San José/Vázquez de Coronado/Reglamento a la Ley para incentivar y promover la construcción de infraestructura de telecomunicaciones en Cos (2025).md',
    'alajuelita-ventas': 'San José/Alajuelita/Reglamento para la regulación y el otorgamiento de licencias para ventas ambulantes y estacionarias (2025).md',
    'tarrazu-decomisos': 'San José/Tarrazú/Reglamento para el procedimiento de decomisos de mercadería por ventas ambulantes de la Municipalidad de Tarra (2025).md',
    'leoncortes-ventas': 'San José/León Cortés/Reglamento de ventas ambulantes, estacionarias y comercio sobre ruedas en espacios y vías públicas (2025).md',
    'puntarenas-ruedas': 'Puntarenas/Puntarenas/Reglamento para regular el comercio sobre ruedas en el Cantón Central de la Provincia de Puntarenas (2025).md',
    'sarchi-residencias': 'Alajuela/Sarchí/Reglamento a la aplicación de la Ley N.° 10594 que reforma los artículos 88 del Código Municipal y 29 de la Le (2025).md',
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
    'desamparados-ninez': 'San José/Desamparados/Política cantonal de niñez y adolescencias del cantón de Desamparados, y su plan de acción interinstitucional (2023).md',
    'guatuso-raos': 'Alajuela/Guatuso/Reglamento Autónomo de Organización y Servicios de la Municipalidad del Cantón de Guatuso (2018).md',
    'grecia-opamdis': 'Alajuela/Grecia/Reglamento para la oficina municipal de la persona adulta mayor y de la persona con discapacidad de Grecia (2025).md',
    'santaana-ensueno': 'San José/Santa Ana/Reglamento para la admisión, permanencia y egreso de personas beneficiarias del Centro Diurno Municipal de adultos mayores Ensueño de Oro (2024).md',
    'escazu-ccdr': 'San José/Escazú/Reforma Integral Reglamento para el nombramiento y funcionamiento del Comité Cantonal de Deportes y Recreación del Cantón de Escazú y de los Comités C (2025).md',
    'tarrazu-bienestar': 'San José/Tarrazú/Política Cantonal de Bienestar Animal de Tarrazú (2026).md',
}
MESES_RM = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'setiembre', 'octubre', 'noviembre', 'diciembre']


def f_rm(k):
    f = RM.get(k, '') if RM.get(k, '').startswith('/') else '""" + RMBASE + """' + RM.get(k, '')
    return f if k in RM and os.path.exists(f) else None


def cita_rm(k, loc):
    f = f_rm(k)
    if not f:
        errors.append(f'REGLAMENTO MUNICIPAL sin archivo: {k}')
        return f'(Reglamento municipal {k}, {loc})'
    d = meta(f)
    fd = fdate(d['fecha_norma']) or fdate(d['fecha'])
    y = fd[0] if fd else ''
    fecha = f'{fd[0]}, {fd[2]} de {MESES_RM[fd[1] - 1]}' if fd else ''
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


def cita_s1(x, loc):
    f = f_s1(x)
    yy, num = x.split('-')
    cod = f'{num}-F-S1-{yy}'
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
}
first_j = set()


def f_j(x):
    t, num = x.split('-', 1)
    f = f'{R}/Jurisprudencia penal y de familia (laterales)/{JUR[t]["pref"]} {num}.md'
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
    y, mo, da = fdate(d['fecha'])
    h = hora(d['hora'])
    hs = f', de las {h} horas' if h else ''
    exp = f' (expediente {d["expediente"]})' if d['expediente'] else ''
    add_ref('J' + x, (org.lower(), y, mo, da, x), f'{org}. ({y}, {da} de {MES[mo]}). *Resolución N.° {cod}{hs}*{exp}. NexusPJ.')
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
        if k not in vistos:
            vistos.add(k); return larga
        return _par(f'{t}, {cod}', abrev(loc))
    if kind == 'S1':
        yy, num = p[1].split('-'); cod = f'{num}-F-S1-{yy}'; k = 'S1' + p[1]
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
open('/home/claude/mis_scripts/build_libro.py', 'w', encoding='utf-8').write(src)
c = open('/home/claude/scripts/cite.py', encoding='utf-8').read().replace('/home/claude/scripts/build.py', '/home/claude/mis_scripts/build_libro.py')
open('/home/claude/mis_scripts/cite_libro.py', 'w', encoding='utf-8').write(c)
print('build_libro.py y cite_libro.py listos')
