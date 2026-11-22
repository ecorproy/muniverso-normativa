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


def f_ley(n):
    if n in ESPECIALES:
        return ESPECIALES[n]
    base = f'{R}/Leyes y decretos nacionales'
    for pat in (f'{base}/*/Ley {n}.md', f'{base}/*/Ley {n}.md.md', f'{base}/*/Ley {n} *.md'):
        fs = glob.glob(pat)
        if fs:
            return fs[0]
    return None


F_CP = f'{R}/Leyes y decretos nacionales/Constitucional/Constitución Política.md'


def f_dec(n):
    fs = glob.glob(f'{R}/Leyes y decretos nacionales/*/Decreto Ejecutivo {n}.md')
    return fs[0] if fs else None


def f_voto(x):
    f = f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/Sentencia {x}.md'
    return f if os.path.exists(f) else None


def f_pgr(x):
    fs = glob.glob(f'{R}/Jurisprudencia administrativa (PGR)/*/Dictamen {x}.md')
    return fs[0] if fs else None


def f_tca(x):
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
ART_RE = re.compile(r'(?im)^\W{0,6}(?:ART[IÍ]CULO|Artículo)\s+(\d+)(?!\d)(?:\s*(bis|ter)\b)?\s*[\.\-—–:º°o*]')
HEAD_RE = re.compile(r'(?m)^\W{0,6}([IVXL]{1,7})\s*\)?\s*\.?\s*[-–—.]+\s*\S')


def seg_articulos(raw):
    ms = list(ART_RE.finditer(raw))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(raw)
        lab = m.group(1) + (' ' + m.group(2).lower() if m.group(2) else '')
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
    fd = fdate(d['fecha_norma']) or fdate(d['fecha'])
    if not fd:
        errors.append(f'LEY sin fecha: {n}')
        return None
    y = fd[0]
    url = f' {d["enlace"]}' if d['enlace'] else ''
    nombre = d['nombre'].strip()
    add_ref('L' + n, ('ley n', int(n)), f'Ley N.° {n}, *{nombre}*. ({y}). Asamblea Legislativa de la República de Costa Rica. Sistema Costarricense de Información Jurídica.{url}')
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
    add_ref('DE' + n, ('decreto ejecutivo', int(n)), f'Decreto Ejecutivo N.° {n}, *{d["nombre"].strip()}*. ({y}). Poder Ejecutivo de la República de Costa Rica. Sistema Costarricense de Información Jurídica.{url}')
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
    add_ref('D' + x, ('procuraduria', y, mo, da, x), f'Procuraduría General de la República. ({y}, {da} de {MES[mo]}). *Dictamen {x}*.{url}')
    return f'(Procuraduría General de la República, dictamen {x}, {y}, {loc})' if loc else f'(Procuraduría General de la República, dictamen {x}, {y})'


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


def expand(macro):
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
    if kind == 'V':
        return cita_voto(p[1], p[2] if len(p) > 2 else '')
    if kind == 'VT':
        return cita_vt(p[1], p[2], p[3])
    if kind == 'D':
        return cita_pgr(p[1], p[2] if len(p) > 2 else '')
    if kind == 'T':
        return cita_tca(p[1], p[2] if len(p) > 2 else '')
    if kind == 'O':
        return cita_cgr(p[1], p[2] if len(p) > 2 else '')
    errors.append(f'MACRO desconocida: {macro}')
    return f'[[{macro}]]'


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
        if m['file']:
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
        m = re.search(r'art\.\s*(\d+(?:\s*(?:bis|ter))?)', loc)
        want = m.group(1) if m else None
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
    # 3) expansión
    out = re.sub(MACRO_RE, lambda m: expand(m.group(1)), text)
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
