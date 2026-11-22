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
})
'''
# criterios de la Contraloría que el libro agrega (van dentro del diccionario CGR, que deexp también lee)
cgr_extra = """    '10092': dict(cita='oficio N.° 10092 [DFOE-SOS-0320], 2024', file='/home/claude/libro/fuentes/of10092.txt',
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
"""
k = src.index("    'IGSM': dict(")
src = src[:k] + cgr_extra + src[k:]
i = src.index('MANUAL = {'); j = src.index('\ndef ', i)
src = src[:j] + '\n' + extra + src[j:]
# leyes que no están en el repositorio y se leen del diario oficial
e1 = "ESPECIALES = {'7135': '/home/claude/repo/main/Leyes y decretos nacionales/Constitucional/Ley Jurisdicción Constitucional.md'}"
assert src.count(e1) == 1
src = src.replace(e1, e1 + "\nESPECIALES['10939'] = '/home/claude/libro/fuentes/Ley 10939.md'\nESPECIALES['8799'] = '/home/claude/libro/fuentes/Ley 8799.md'\nESPECIALES['9458'] = '/home/claude/libro/fuentes/Ley 9458.md'\nFUENTE_LEY = {'10939': 'La Gaceta N.° 91, Alcance N.° 59, 20 de mayo de 2026.'}")
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
open('/home/claude/mis_scripts/build_libro.py', 'w', encoding='utf-8').write(src)
c = open('/home/claude/scripts/cite.py', encoding='utf-8').read().replace('/home/claude/scripts/build.py', '/home/claude/mis_scripts/build_libro.py')
open('/home/claude/mis_scripts/cite_libro.py', 'w', encoding='utf-8').write(c)
print('build_libro.py y cite_libro.py listos')
