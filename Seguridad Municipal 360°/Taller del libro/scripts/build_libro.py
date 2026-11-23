# build.py: expande macros de cita, coteja cada cita textual contra su fuente,
# cuenta palabras y arma las referencias APA solo de lo citado.
# Uso: python3 -I build.py            (lee /home/claude/art/src/*.md, escribe /home/claude/art/out)
import re, os, sys, glob, json, unicodedata

R = '/home/claude/repo/main'
SRC = os.environ.get('SRC','/home/claude/art/src')
OUT = os.environ.get('OUT','/home/claude/art/out')
MES = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
       'setiembre', 'octubre', 'noviembre', 'diciembre']
ROM = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10}

os.makedirs(OUT, exist_ok=True)
errors, warns, notes = [], [], []


def read(f):
    return open(f, encoding='utf-8', errors='replace').read()


def norm(s):
    s = re.sub(r'[‪-‮​-‏﻿­]', '', s)
    s = s.replace('*', '')
    s = re.sub(r'[“”«»"\'‘’`´]', '', s)
    s = re.sub(r'\s+', '', s)
    return unicodedata.normalize('NFC', s)


def dehyph(s):
    return re.sub(r'(?<=\w)[-\u00ad]\s*\n\s*(?=\w)', '', s)


def norm2(s):
    return norm(s) + '\x00' + norm(dehyph(s))


def meta(f):
    t = read(f)[:5000]
    d = {}
    for k in ['numero', 'nombre', 'fecha', 'fecha_norma', 'hora', 'expediente', 'enlace',
              'ente_emisor', 'titulo', 'institucion', 'consultante', 'tipo']:
        m = re.search(r'(?m)^' + k + r':\s*"([^"]*)"', t)
        d[k] = m.group(1) if m else ''
    return d


def fdate(s):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        y, mo, da = m.groups()
    else:
        m = re.match(r'(\d{2})/(\d{2})/(\d{4})', s)
        if not m:
            return None
        da, mo, y = m.groups()
    return int(y), int(mo), int(da)


def hora(h):
    h = h.strip()
    if not h:
        return ''
    m = re.match(r'0?(\d{1,2}):(\d{2})', h)
    return f'{int(m.group(1))}:{m.group(2)}' if m else h


# ---------- localización de archivos ----------
ESPECIALES = {'7135': '/home/claude/repo/main/Leyes y decretos nacionales/Constitucional/Ley Jurisdicción Constitucional.md'}
ESPECIALES['10939'] = '/home/claude/libro/fuentes/Ley 10939.md'
ESPECIALES['8799'] = '/home/claude/libro/fuentes/Ley 8799.md'
ESPECIALES['9458'] = '/home/claude/libro/fuentes/Ley 9458.md'
ESPECIALES['10594'] = '/home/claude/libro/fuentes/Ley 10594.md'
ESPECIALES['8661'] = '/home/claude/libro/fuentes/Ley 8661.md'
ESPECIALES['7948'] = '/home/claude/libro/fuentes/Ley 7948.md'
FUENTE_LEY = {'10939': 'La Gaceta N.° 91, Alcance N.° 59, 20 de mayo de 2026.'}


def f_ley(n):
    if n in ESPECIALES and os.path.exists(ESPECIALES[n]):
        return ESPECIALES[n]
    base = f'{R}/Leyes y decretos nacionales'
    for pat in (f'{base}/*/Ley {n}.md', f'{base}/*/Ley {n}.md.md', f'{base}/*/Ley {n} *.md'):
        fs = glob.glob(pat)
        if fs:
            return fs[0]
    return None


F_CP = f'{R}/Leyes y decretos nacionales/Constitucional/Constitución Política.md'


FUENTE_DEC = {'42075': 'La Gaceta N.° 80, Alcance N.° 87, 14 de abril de 2020. '}
DEC_ESPECIALES = {'42075': '/home/claude/libro/fuentes/Decreto Ejecutivo 42075.md'}


def f_dec(n):
    if n in DEC_ESPECIALES and os.path.exists(DEC_ESPECIALES[n]):
        return DEC_ESPECIALES[n]
    fs = glob.glob(f'{R}/Leyes y decretos nacionales/*/Decreto Ejecutivo {n}.md')
    return fs[0] if fs else None


def f_voto(x):
    _loc = f'/home/claude/libro/fuentes/votos/Sentencia {x}.md'
    if os.path.exists(_loc):
        return _loc
    f = f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/Sentencia {x}.md'
    if os.path.exists(f):
        return f
    fs = glob.glob(f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/*/Sentencia {x}.md')
    return fs[0] if fs else None


def f_pgr(x):
    _loc = f'/home/claude/libro/fuentes/dictamenes/Dictamen {x}.md'
    if os.path.exists(_loc):
        return _loc
    fs = glob.glob(f'{R}/Jurisprudencia administrativa (PGR)/*/Dictamen {x}.md')
    return fs[0] if fs else None


def f_tca(x):
    _fs = glob.glob(f'/home/claude/libro/fuentes/tca/Sentencia TCA * {x}.md')
    if _fs:
        return _fs[0]
    fs = glob.glob(f'{R}/Jurisprudencia contencioso administrativa (TCA)/Municipal/Sentencia TCA * {x}.md')
    return fs[0] if fs else None


CGR = {
    '14908': dict(cita='oficio N.° 14908 [DFOE-DEC-4567], 2024',
                  file='/home/claude/cgr/Oficio 14908-2024 (DFOE-DEC-4567) Declaratoria de vías públicas, San Rafael de Heredia.txt',
                  ref='Contraloría General de la República. (2024, 23 de setiembre). *Oficio N.° 14908 (DFOE-DEC-4567). Advertencia relacionada con el cumplimiento del marco legal en la constatación de vías como públicas*. https://cgrfiles.cgr.go.cr/publico/docs_cgr/2024/SIGYD_D/SIGYD_D_2024017885.pdf',
                  key=(2024, 9, 23)),
    '12990': dict(cita='oficio N.° 12990 [DFOE-LOC-1706], 2023',
                  file='/home/claude/cgr/Oficio 12990-2023 (DFOE-LOC-1706) Inversión en aceras, Poás.txt',
                  ref='Contraloría General de la República. (2023, 27 de setiembre). *Oficio N.° 12990 (DFOE-LOC-1706). Emisión de criterio relativo a la inversión de recursos en aceras*. https://cgrfiles.cgr.go.cr/publico/docs_cgr/2023/SIGYD_D/SIGYD_D_2023015565.pdf',
                  key=(2023, 9, 27)),
    '22430': dict(cita='oficio N.° 22430 [DFOE-LOC-2366], 2022',
                  file='/home/claude/cgr/Oficio 22430-2022 (DFOE-LOC-2366) Calles locales de menos de 14 metros, Paraíso.txt',
                  ref='Contraloría General de la República. (2022, 12 de diciembre). *Oficio N.° 22430 (DFOE-LOC-2366)*. https://cgrfiles.cgr.go.cr/publico/docs_cgr/2022/SIGYD_D/SIGYD_D_2022025236.pdf',
                  key=(2022, 12, 12)),
    '14467': dict(cita='oficio N.° 14467 [DJ-1340], 2018',
                  file='/home/claude/cgr/Oficio 14467-2018 (DJ-1340) Bibliotecas municipales.txt',
                  ref='Contraloría General de la República. (2018, 9 de octubre). *Oficio N.° 14467 (DJ-1340). Consulta relacionada con los fondos de la Ley N.° 6282*.',
                  key=(2018, 10, 9)),
    'REDCUDI': dict(cita='informe N.° DFOE-BIS-IAD-00010-2023, 2023',
                    file='/home/claude/cgr/Informe DFOE-BIS-IAD-00010-2023 Gobernanza y calidad de la REDCUDI.txt',
                    ref='Contraloría General de la República. (2023, 23 de octubre). *Informe de auditoría de carácter especial sobre la gobernanza y estándares de calidad de los servicios de cuido y desarrollo infantil de la REDCUDI* (informe N.° DFOE-BIS-IAD-00010-2023). https://cgrfiles.cgr.go.cr/publico/docs_cgr/2023/SIGYD_D/SIGYD_D_2023017941.pdf',
                    key=(2023, 10, 23)),
    'PALMARES': dict(cita='resolución N.° R-DCP-SICOP-00770-2024, 2024',
                     file='/home/claude/cgr/Resolución 8072024000000797-2024 (recurso de apelación) CECUDI de Palmares.txt',
                     ref='Contraloría General de la República. (2024, 31 de mayo). *Resolución N.° R-DCP-SICOP-00770-2024 (documento N.° 8072024000000797). Recurso de apelación en la licitación mayor N.° 2023LY-000001-0002500001, Municipalidad de Palmares*. https://cgrfiles.cgr.go.cr/publico/docs_cgr/2024/SIGYD_D/SIGYD_D_2024011182.pdf',
                     key=(2024, 5, 31)),
    'REDCUDI': dict(cita='informe N.° DFOE-BIS-IAD-00010-2023, 2023', file='/home/claude/repo/360/Seguridad Municipal 360°/Criterios CGR/Informe DFOE-BIS-IAD-00010-2023 Gobernanza y calidad de la REDCUDI - texto extraído.txt',
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
                  ref='Contraloría General de la República. (2025, 3 de noviembre). *Oficio N.° 21709 (DJ-2194). Solicitud de criterio relacionado con el proyecto de Ley n° 25.082 "Ley de autorización a la Municipalidad de Grecia para donar un inmueble de su propiedad a la Asociación Cruz Roja Costarricense"*.',
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
    '01840': dict(cita='oficio N.° 01840 [DFOE-LOC-0259], 2026', file='/home/claude/libro/fuentes/of01840.txt',
                  ref='Contraloría General de la República. (2026, 16 de febrero). *Oficio N.° 01840 (DFOE-LOC-0259). Emisión de criterio sobre los recursos contenidos en el inciso b) del artículo 59 de la Ley sobre la Zona Marítimo Terrestre*.',
                  key=(2026, 2, 16)),
    'IGSM': dict(cita='informe N.° DFOE-LOC-SGP-00002-2025, 2025', file='/home/claude/cgr/IGSM 2025 (extracto público).txt',
                 ref='Contraloría General de la República. (2025, 5 de agosto). *Índice de Gestión de Servicios Municipales 2025* (informe N.° DFOE-LOC-SGP-00002-2025). https://sites.google.com/cgr.go.cr/igsm/',
                 key=(2025, 8, 5)),
}

MANUAL = {
    'Organización Internacional de Normalización, 2019': dict(
        file='/home/claude/pdf/iso.txt', roman=True,
        ref='Organización Internacional de Normalización. (2019). *Sistemas de gestión de la calidad. Directrices para la aplicación de la Norma ISO 9001 en el gobierno local* (ISO 18091:2019, traducción oficial, 2.ª ed.) [Vista previa]. https://standards.iteh.ai/catalog/standards/iso/cd68e4c6-4c21-46f2-9612-21902b913172/iso-18091-2019'),
    'Consejo para la Promoción de la Competitividad, 2026': dict(
        file='/home/claude/icn/icn.txt',
        ref='Consejo para la Promoción de la Competitividad. (2026). *Índice de Competitividad Nacional 2026*. https://icn.cr/'),
    'Observatorio Ciudadano Integral de Los Cabos, 2020': dict(
        file='/home/claude/pdf/cabos.txt',
        ref='Observatorio Ciudadano Integral de Los Cabos. (2020). *Herramienta del ISO 18091: acciones enfocadas a la mitigación del COVID-19 desde los gobiernos locales. XIII Administración Municipal, Los Cabos, B.C.S., marzo a mayo de 2020*.'),
    'Programa de las Naciones Unidas para el Desarrollo, 1994': dict(
        file=None,
        ref='Programa de las Naciones Unidas para el Desarrollo. (1994). *Informe sobre Desarrollo Humano 1994*. Fondo de Cultura Económica. https://digitallibrary.un.org/record/240220/files/hdr_1994_es_completo_nostats.pdf'),
    'Madero Gómez, 2023': dict(
        file='/home/claude/madero/madero_pag.txt',
        ref='Madero Gómez, S. (2023). Percepción de la jerarquía de necesidades de Maslow y su relación con los factores de atracción y retención del talento humano. *Contaduría y Administración*, *68*(1), 235-259. https://doi.org/10.22201/fca.24488410e.2023.3416'),
    'Pele, 2015': dict(
        file='/home/claude/pele/pele_pag.txt',
        ref='Pele, A. (2015). Kant y la dignidad humana. *Revista Brasileira de Estudos Políticos*, *111*, 15-46. https://doi.org/10.9732/P.0034-7191.2016V111P15'),
    'Kant, 1785/2003, como se citó en Pele, 2015': dict(
        file='/home/claude/pele/pele_pag.txt', alias='Pele, 2015',
        ref='Pele, A. (2015). Kant y la dignidad humana. *Revista Brasileira de Estudos Políticos*, *111*, 15-46. https://doi.org/10.9732/P.0034-7191.2016V111P15'),
    'Sarlet, 2006, como se citó en Pele, 2015': dict(
        file='/home/claude/pele/pele_pag.txt', alias='Pele, 2015',
        ref='Pele, A. (2015). Kant y la dignidad humana. *Revista Brasileira de Estudos Políticos*, *111*, 15-46. https://doi.org/10.9732/P.0034-7191.2016V111P15'),
    'como se citó en Pele, 2015': dict(
        file='/home/claude/pele/pele_pag.txt', alias='Pele, 2015',
        ref='Pele, A. (2015). Kant y la dignidad humana. *Revista Brasileira de Estudos Políticos*, *111*, 15-46. https://doi.org/10.9732/P.0034-7191.2016V111P15'),
    'Tocqueville, s. f.': dict(
        file='/home/claude/tocq/tocq.txt',
        ref='Tocqueville, A. de. (s. f.). *La democracia en América*. https://www.suneo.mx/literatura/subidas/Alexis%20de%20Tocqueville%20La%20Democracia%20en%20America.pdf'),
    'Maslow, 1943': dict(
        file=None,
        ref='Maslow, A. H. (1943). A theory of human motivation. *Psychological Review*, *50*(4), 370-396. https://doi.org/10.1037/h0054346'),
    'Max-Neef et al., 1986': dict(
        file=None,
        ref='Max-Neef, M., Elizalde, A. y Hopenhayn, M. (1986). Desarrollo a escala humana: una opción para el futuro. *Development Dialogue*, número especial. CEPAUR y Fundación Dag Hammarskjöld.'),
}

# ---------- segmentación de fuentes ----------
ART_RE = re.compile(r'(?im)^\W{0,6}(?:ART[IÍ]CULO|Artículo)\s+(\d+)(?!\d)(?:[\s*]*(bis|ter|qu[aá]ter|quinquies|sexies)\b)?[\s*]*[\.\-—–:º°o*]')
HEAD_RE = re.compile(r'(?m)^\W{0,6}([IVXL]{1,7})\s*\)?\s*\.?\s*[-–—.]+\s*\S')



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

def seg_articulos(raw):
    ms = list(ART_RE.finditer(raw))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(raw)
        lab = m.group(1) + (' ' + m.group(2).lower().replace('á', 'a') if m.group(2) else '')
        out.append((lab, norm(raw[m.start():end])))
    return out


def seg_considerandos(raw):
    ms = list(HEAD_RE.finditer(raw))
    pt = [m.start() for m in re.finditer(r'(?im)^\W{0,6}por tanto\s*:?', raw)]
    ptpos = pt[-1] if pt else len(raw)
    out = []
    ci = [m.start() for m in re.finditer(r'(?im)^\W{0,6}considerando\s*:?\s*$', raw)]
    if ci:
        out.append(('RESULTANDO', norm(raw[:ci[-1]])))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(raw)
        if m.start() >= ptpos:
            break
        out.append((m.group(1), norm(raw[m.start():min(end, ptpos)])))
    out.append(('POR TANTO', norm(raw[ptpos:])))
    return out


def find_segments(hay, segs):
    """busca los fragmentos en orden dentro de hay; devuelve True/False"""
    pos = 0
    for s in segs:
        k = hay.find(s, pos)
        if k < 0:
            return False
        pos = k + len(s)
    return True


# ---------- estado ----------
first_v = set()
cited = {}          # clave -> (orden, texto de referencia)
quotes_report = []  # (archivo, n palabras, cita, estado, detalle)


def add_ref(key, sortkey, text):
    if key not in cited:
        cited[key] = (sortkey, text)


def ref_ley(n):
    if n == 'CP':
        d = meta(F_CP)
        url = f' {d["enlace"]}' if d['enlace'] else ''
        add_ref('CP', ('constitucion', 0), f'Constitución Política de la República de Costa Rica. (1949). Asamblea Nacional Constituyente. Sistema Costarricense de Información Jurídica.{url}')
        return 1949
    f = f_ley(n)
    if not f:
        errors.append(f'LEY sin archivo: {n}')
        return None
    d = meta(f)
    fd = fdate(d['fecha_norma']) or fdate(d['fecha']) or fdate({'30': '19/04/1885'}.get(n, ''))
    if not fd:
        errors.append(f'LEY sin fecha: {n}')
        return None
    y = fd[0]
    url = f' {d["enlace"]}' if d['enlace'] else ''
    nombre = d['nombre'].strip()
    add_ref('L' + n, ('ley n', int(n)), f'Ley N.° {n}, *{nombre}*. ({y}). Asamblea Legislativa de la República de Costa Rica. {FUENTE_LEY.get(n, 'Sistema Costarricense de Información Jurídica.')}{url}')
    return y


def cita_dec(n, loc):
    f = f_dec(n)
    if not f:
        errors.append(f'DECRETO sin archivo: {n}')
        return f'(Decreto Ejecutivo N.° {n}, {loc})'
    d = meta(f)
    fd = fdate(d['fecha_norma']) or fdate(d['fecha'])
    y = fd[0] if fd else ''
    url = f' {d["enlace"]}' if d['enlace'] else ''
    add_ref('DE' + n, ('decreto ejecutivo', int(n)), f'Decreto Ejecutivo N.° {n}, *{d["nombre"].strip()}*. ({y}). Poder Ejecutivo de la República de Costa Rica. {FUENTE_DEC.get(n, '')}Sistema Costarricense de Información Jurídica.{url}')
    return f'(Decreto Ejecutivo N.° {n}, {y}, {loc})' if loc else f'(Decreto Ejecutivo N.° {n}, {y})'


def ref_voto(x):
    f = f_voto(x)
    if not f:
        errors.append(f'VOTO sin archivo: {x}')
        return None
    d = meta(f)
    y, mo, da = fdate(d['fecha'])
    h = hora(d['hora'])
    hs = f', de las {h} horas' if h else ''
    exp = f' (expediente {d["expediente"]})' if d['expediente'] else ''
    url = f' {d["enlace"]}' if d['enlace'] else ''
    add_ref('V' + x, ('sala constitucional', y, mo, da, x), f'Sala Constitucional de la Corte Suprema de Justicia. ({y}, {da} de {MES[mo]}). *Voto N.° {x}{hs}*{exp}. NexusPJ.{url}')
    return (h, da, mo, y)


def cita_voto(x, loc):
    r = ref_voto(x)
    if not r:
        return f'(Sala Constitucional, voto N.° {x}, {loc})'
    h, da, mo, y = r
    if x not in first_v:
        first_v.add(x)
        hs = f'de las {h} horas del ' if h else 'del '
        base = f'Sala Constitucional, voto N.° {x}, {hs}{da} de {MES[mo]} de {y}'
    else:
        base = f'Sala Constitucional, voto N.° {x}'
    return f'({base}, {loc})' if loc else f'({base})'


def cita_vt(a, b, loc):
    r = ref_voto(b)
    if not r:
        return f'(Sala Constitucional, voto N.° {a}, transcrito en el voto N.° {b}, {loc})'
    h, da, mo, y = r
    if b not in first_v:
        first_v.add(b)
        hs = f'de las {h} horas del ' if h else 'del '
        tail = f'voto N.° {b}, {hs}{da} de {MES[mo]} de {y}'
    else:
        tail = f'voto N.° {b}'
    return f'(Sala Constitucional, voto N.° {a}, transcrito en el {tail}, {loc})'


def cita_pgr(x, loc):
    f = f_pgr(x)
    if not f:
        errors.append(f'PGR sin archivo: {x}')
        return f'(Procuraduría General de la República, dictamen {x}, {loc})'
    d = meta(f)
    y, mo, da = fdate(d['fecha'])
    url = f' Sistema Costarricense de Información Jurídica. {d["enlace"]}' if d['enlace'] else ''
    _t = 'opinión jurídica' if x.startswith('OJ') else 'dictamen'
    add_ref('D' + x, ('procuraduria', y, mo, da, x), f'Procuraduría General de la República. ({y}, {da} de {MES[mo]}). *{_t.capitalize()} {x}*.{url}')
    return f'(Procuraduría General de la República, {_t} {x}, {y}, {loc})' if loc else f'(Procuraduría General de la República, {_t} {x}, {y})'


def cita_tca(x, loc):
    f = f_tca(x)
    if not f:
        errors.append(f'TCA sin archivo: {x}')
        return f'(Tribunal Contencioso Administrativo, resolución N.° {x}, {loc})'
    d = meta(f)
    y, mo, da = fdate(d['fecha'])
    h = hora(d['hora'])
    sec = os.path.basename(f).split()[2]
    yy, num = x.split('-')
    num = str(int(num))
    secs = {'I': 'Sección I', 'II': 'Sección II', 'III': 'Sección III', 'IV': 'Sección IV'}.get(sec)
    org = f'Tribunal Contencioso Administrativo, {secs}' if secs else 'Tribunal Contencioso Administrativo'
    orgref = f'Tribunal Contencioso Administrativo, {secs}' if secs else 'Tribunal Contencioso Administrativo y Civil de Hacienda'
    hs = f', de las {h} horas' if h else ''
    exp = f' (expediente {d["expediente"]})' if d['expediente'] else ''
    add_ref('T' + x, ('tribunal contencioso', y, mo, da, x), f'{orgref}. ({y}, {da} de {MES[mo]}). *Resolución N.° {num}-{yy}{hs}*{exp}. NexusPJ.')
    return f'({org}, resolución N.° {num}-{yy}, {loc})' if loc else f'({org}, resolución N.° {num}-{yy})'


def cita_cgr(k, loc):
    c = CGR[k]
    add_ref('O' + k, ('contraloria',) + c['key'] + (k,), c['ref'])
    return f'(Contraloría General de la República, {c["cita"]}, {loc})' if loc else f'(Contraloría General de la República, {c["cita"]})'



RM = {
    'talamanca-animales': 'Limón/Talamanca/Reglamento de servicio municipal de atención de animales de compañía (2022).md',
    'paraiso-construcciones': 'Cartago/Paraíso/Reglamento de Construcciones del Cantón de Paraíso (2012).md',
    'oreamuno-construccion': 'Cartago/Oreamuno/Reglamento de Construcción e infraestructura (2025).md',
    'cartago-cmeca': 'Cartago/Cartago/Reglamento de Organización y Funcionamiento del Centro Municipal de Educación para el Cuido Animal (2016).md',
    'invu-construcciones': '/home/claude/repo/main/Leyes y decretos nacionales/Municipal/Reglamento de Construcciones INVU (2018).md',
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
    'desamparados-ninez': 'San José/Desamparados/Política cantonal de niñez y adolescencias del cantón de Desamparados, y su plan de acción interinstitucional (2023).md',
    'guatuso-raos': 'Alajuela/Guatuso/Reglamento Autónomo de Organización y Servicios de la Municipalidad del Cantón de Guatuso (2018).md',
    'grecia-opamdis': 'Alajuela/Grecia/Reglamento para la oficina municipal de la persona adulta mayor y de la persona con discapacidad de Grecia (2025).md',
    'santaana-ensueno': 'San José/Santa Ana/Reglamento para la admisión, permanencia y egreso de personas beneficiarias del Centro Diurno Municipal de adultos mayores Ensueño de Oro (2024).md',
    'escazu-ccdr': 'San José/Escazú/Reforma Integral Reglamento para el nombramiento y funcionamiento del Comité Cantonal de Deportes y Recreación del Cantón de Escazú y de los Comités C (2025).md',
    'tarrazu-bienestar': 'San José/Tarrazú/Política Cantonal de Bienestar Animal de Tarrazú (2026).md',
}
MESES_RM = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'setiembre', 'octubre', 'noviembre', 'diciembre']


def f_rm(k):
    f = RM.get(k, '') if RM.get(k, '').startswith('/') else '/home/claude/repo/main/Reglamentos municipales/' + RM.get(k, '')
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


first_s1 = set()


def f_s1(x):
    for b in ('/home/claude/libro/fuentes/sala1', f'{R}/Jurisprudencia de casación (Sala Primera)/Municipal', f'{R}/Jurisprudencia de casación (Sala Primera)/Laterales', f'{R}/Jurisprudencia de casación (Sala Primera)'):
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


def expand_larga(macro):
    macro = macro.replace('!', '')
    p = [x.strip() for x in macro.split(':')]
    kind = p[0]
    if kind == 'CP':
        ref_ley('CP')
        return f'(Constitución Política de la República de Costa Rica, 1949, {p[1]})'
    if kind == 'L':
        y = ref_ley(p[1])
        return f'(Ley N.° {p[1]}, {y}, {p[2]})'
    if kind == 'DE':
        return cita_dec(p[1], p[2] if len(p) > 2 else '')
    if kind == 'RM':
        return cita_rm(p[1], p[2] if len(p) > 2 else '')
    if kind == 'V':
        return cita_voto(p[1], p[2] if len(p) > 2 else '')
    if kind == 'VT':
        return cita_vt(p[1], p[2], p[3])
    if kind == 'D':
        return cita_pgr(p[1], p[2] if len(p) > 2 else '')
    if kind == 'S1':
        return cita_s1(p[1], p[2] if len(p) > 2 else '')
    if kind == 'T':
        return cita_tca(p[1], p[2] if len(p) > 2 else '')
    if kind == 'O':
        return cita_cgr(p[1], p[2] if len(p) > 2 else '')
    errors.append(f'MACRO desconocida: {macro}')
    return f'[[{macro}]]'



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


# ---------- cotejo ----------
_cache = {}


def source_units(macro=None, manual=None):
    """devuelve (tipo, unidades [(etiqueta, texto normalizado)], texto normalizado completo)"""
    if macro:
        macro = macro.replace('!', '')
    key = macro or manual
    if key in _cache:
        return _cache[key]
    res = None
    if macro:
        p = [x.strip() for x in macro.split(':')]
        kind = p[0]
        if kind == 'CP':
            raw = read(F_CP)
            res = ('art', seg_articulos(raw), norm(raw))
        elif kind == 'L':
            f = f_ley(p[1])
            if f:
                raw = read(f)
                res = ('art', seg_articulos(raw), norm(raw))
        elif kind == 'DE':
            f = f_dec(p[1])
            if f:
                raw = read(f)
                res = ('art', seg_articulos(raw), norm(raw))
        elif kind == 'RM':
            f = f_rm(p[1])
            if f:
                raw = read(f)
                res = ('art', seg_articulos(raw), norm(raw))
        elif kind in ('V', 'VT'):
            x = p[1] if kind == 'V' else p[2]
            f = f_voto(x)
            if f:
                raw = read(f)
                res = ('cons', seg_considerandos(raw), norm(raw))
        elif kind == 'D':
            f = f_pgr(p[1])
            if f:
                raw = read(f)
                i = [m.start() for m in re.finditer(r'(?i)\n[^\n]{0,25}conclusi[oó]n', raw)]
                concl = raw[i[-1]:] if i else ''
                secs = [(lab, txt) for lab, txt in seg_considerandos(raw) if lab != 'POR TANTO']
                res = ('pgr', [('conclusión', norm(concl))] + secs, norm(raw))
        elif kind == 'S1':
            f = f_s1(p[1])
            if f:
                raw = read(f)
                res = ('cons', seg_considerandos(raw), norm(raw))
        elif kind == 'T':
            f = f_tca(p[1])
            if f:
                raw = read(f)
                res = ('cons', seg_considerandos(raw), norm(raw))
        elif kind == 'O':
            c = CGR[p[1]]
            if c['file']:
                raw = read(c['file'])
                pages = raw.split('\f')
                res = ('pag', [(str(i + 1), norm2(pg)) for i, pg in enumerate(pages)], norm2(raw))
    else:
        m = MANUAL[manual]
        if m['file'] and os.path.exists(m['file']):
            raw = read(m['file'])
            pages = raw.split('\f')
            res = ('pag', [(str(i + 1), norm2(pg)) for i, pg in enumerate(pages)], norm2(raw))
    _cache[key] = res
    return res


manual_ok = []


def check_quote(fname, quote, macro=None, manual=None, loc=''):
    forced = bool(macro and macro.endswith('!'))
    if macro:
        macro = macro.replace('!', '')
    loc = loc.replace('!', '')
    words = len(re.findall(r'\w+', quote.replace('[…]', ' '), flags=re.UNICODE))
    segs = [norm(s) for s in re.split(r'\s*\[…\]\s*', quote) if norm(s)]
    su = source_units(macro=macro, manual=manual)
    label = macro or f'{manual} | {loc}'
    if su is None:
        quotes_report.append((fname, words, label, 'SIN FUENTE LOCAL', quote[:60]))
        return words
    tipo, units, full = su
    if not find_segments(full, segs):
        quotes_report.append((fname, words, label, 'NO LITERAL', quote[:90]))
        errors.append(f'[{fname}] NO LITERAL: "{quote[:80]}" → {label}')
        return words
    where = [lab for lab, txt in units if find_segments(txt, segs)]
    want = None
    if tipo == 'art':
        m = re.search(r'art\.\s*(\d+(?:\s*(?:bis|ter|qu[aá]ter|quinquies|sexies)\b)?)', loc)
        want = re.sub(r'\s+', ' ', m.group(1)).replace('á', 'a') if m else None
    elif tipo == 'cons':
        if re.search(r'por tanto', loc, re.I):
            want = 'POR TANTO'
        elif re.search(r'resultando', loc, re.I):
            want = 'RESULTANDO'
        else:
            m = re.search(r'considerando\s+([IVXL]+)', loc)
            want = m.group(1) if m else None
    elif tipo == 'pgr':
        if re.search(r'conclusi', loc, re.I):
            want = 'conclusión'
        else:
            m = re.search(r'apartado\s+([IVXL]+)', loc)
            want = m.group(1) if m else None
    elif tipo == 'pag':
        m = re.search(r'p\.\s*([ivxlc]+|\d+)', loc)
        if m:
            g = m.group(1)
            want = str(ROM[g]) if g in ROM else g
    if want is None:
        st = 'LITERAL (sin localización que cotejar)'
    elif want in where:
        st = 'OK'
    elif forced:
        st = 'OK'
        manual_ok.append(f'[{fname}] {label}: "{quote[:50]}" (segmentador: {where[:4]})')
    else:
        st = f'LITERAL, PERO UBICACIÓN: citado {want}; hallado en {where[:6]}'
        errors.append(f'[{fname}] UBICACIÓN: "{quote[:60]}" → {label}: citado {want}, hallado en {where[:6]}')
    quotes_report.append((fname, words, label, st, quote[:60]))
    return words


MACRO_RE = r'\[\[([^\]]+)\]\]'
PAREN_RE = r'\(([^()]*(?:\[[^\]]*\])?[^()]*)\)'
QUOTE_RE = re.compile(r'"([^"]+)"(\s*)(?:' + MACRO_RE + r'|' + PAREN_RE + r')?')


def process(fname, text):
    # 1) cotejo de citas textuales
    for line in text.split('\n'):
        is_block = line.startswith('>')
        for m in QUOTE_RE.finditer(line):
            q, sp, macro, paren = m.group(1), m.group(2), m.group(3), m.group(4)
            if macro and '|' in macro:
                errors.append(f'[{fname}] CITA TEXTUAL con macro agrupada: "{q[:50]}"')
                continue
            if macro:
                p = [x.strip() for x in macro.split(':')]
                loc = p[-1] if len(p) > 2 or p[0] == 'CP' else ''
                w = check_quote(fname, q, macro=macro, loc=loc)
            elif paren:
                man = None
                for k in MANUAL:
                    if paren.startswith(k):
                        man = k
                if not man:
                    errors.append(f'[{fname}] CITA TEXTUAL con paréntesis no reconocido: "{q[:50]}" ({paren[:60]})')
                    continue
                w = check_quote(fname, q, manual=man, loc=paren[len(man):])
            else:
                errors.append(f'[{fname}] COMILLAS SIN FUENTE: "{q[:70]}"')
                continue
            if w >= 40 and not is_block:
                errors.append(f'[{fname}] CITA DE {w} PALABRAS EN LÍNEA (debe ir en bloque): "{q[:50]}"')
            if w < 40 and is_block:
                warns.append(f'[{fname}] bloque con cita de {w} palabras: "{q[:50]}"')
    # 2) referencias manuales citadas
    for k, v in MANUAL.items():
        if '(' + k in text or k in text:
            kk = v.get('alias', k)
            add_ref('M' + kk, (re.sub(r'[^a-z]', '', unicodedata.normalize('NFD', kk.lower())),), v['ref'])
    # 3) expansión (en forma corta, la primera mención se cuenta por capítulo)
    if CORTA:
        vistos.clear(); first_v.clear(); first_s1.clear()
    out = re.sub(MACRO_RE, lambda m: expand(m.group(1)), text)
    if CORTA:
        out = manual_corta(out)
    # 4) estilo
    body = re.sub(r'"[^"]*"', '""', out)
    for pat, msg in [(r'[—–]', 'raya'), (r'[«»“”]', 'comillas no rectas'), (r'(?m)^\s*[-*•]\s', 'viñeta'),
                     (r'(?m)^\s*\d+\.\s', 'lista numerada'), (r'\*\*', 'negrita'), (r'\|', 'tabla')]:
        for mm in re.finditer(pat, body):
            ctx = body[max(0, mm.start() - 40):mm.start() + 40].replace('\n', ' ')
            warns.append(f'[{fname}] estilo ({msg}): …{ctx}…')
    for pat in [r'\bno solo\b', r'\bcrucial', r'\bclave\b', r'\brobust', r'\bpanorama\b', r'\bentramado\b', r'\baborda', r'\bsubraya',
                r'\bdestaca', r'\ben definitiva\b', r'\bcabe destacar\b', r'\bes importante señalar\b', r'\bfundamental(es)?\b',
                r'\bmultifac', r'\bpotenci', r'\bfomenta', r'\bgarantizando\b', r'\breflejando\b', r'\bsin duda\b', r'\bexhaustiv',
                r'\bintegral(es)?\b', r'\bhito\b', r'\bpilar(es)?\b', r'\bholístic', r'\ben este sentido\b', r'\bjuega un papel\b',
                r'\ba lo largo de\b', r'\bno se trata\b']:
        for mm in re.finditer(pat, body, re.I):
            ctx = body[max(0, mm.start() - 45):mm.start() + 45].replace('\n', ' ')
            notes.append(f'[{fname}] vocabulario «{mm.group(0)}»: …{ctx}…')
    return out


def main():
    files = sorted(glob.glob(f'{SRC}/*.md'))
    total_words = 0
    for f in files:
        name = os.path.basename(f)
        out = process(name, read(f))
        open(f'{OUT}/{name}', 'w', encoding='utf-8').write(out)
        n = len(re.findall(r'\w+', out))
        total_words += n
        print(f'{name}: {n} palabras, {len(out.encode("utf-8"))} bytes')
        for lab in ('Resumen', 'Abstract'):
            m = re.search(r'(?ms)^##\s*' + lab + r'\s*\n+(.*?)(?=\n\n\*\*|\n\n##|\n\nPalabras clave|\n\nKeywords|\Z)', out)
            if m:
                print(f'   {lab}: {len(re.findall(chr(92)+"w+", m.group(1)))} palabras')
    # referencias
    items = sorted(cited.values(), key=lambda kv: tuple(str(x).zfill(12) if isinstance(x, int) else str(x) for x in kv[0]))
    refs = '## Referencias\n\n' + '\n\n'.join(t for _, t in items) + '\n'
    open(f'{OUT}/zz_referencias.md', 'w', encoding='utf-8').write(refs)
    print(f'referencias: {len(items)} | total palabras cuerpo: {total_words}')
    # informe
    rep = []
    ok = sum(1 for q in quotes_report if q[3] == 'OK')
    rep.append(f'CITAS TEXTUALES: {len(quotes_report)} | OK: {ok}')
    for fn, w, lab, st, q in quotes_report:
        if st != 'OK':
            rep.append(f'  [{fn}] {w}p | {lab} | {st} | "{q}"')
    rep.append(f'\nUBICACIONES VERIFICADAS A MANO ({len(manual_ok)}):')
    rep += ['  ' + e for e in manual_ok]
    rep.append(f'\nERRORES ({len(errors)}):')
    rep += ['  ' + e for e in errors]
    rep.append(f'\nAVISOS ({len(warns)}):')
    rep += ['  ' + e for e in warns]
    rep.append(f'\nNOTAS DE VOCABULARIO ({len(notes)}):')
    rep += ['  ' + e for e in notes]
    open(f'{OUT}/zz_informe.txt', 'w', encoding='utf-8').write('\n'.join(rep))
    json.dump([dict(archivo=a, palabras=w, fuente=l, estado=s, cita=q) for a, w, l, s, q in quotes_report],
              open(f'{OUT}/zz_citas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n'.join(rep[:1]))
    print(f'errores: {len(errors)} | avisos: {len(warns)} | notas: {len(notes)}')


main()
