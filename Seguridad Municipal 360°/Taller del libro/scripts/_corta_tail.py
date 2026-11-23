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
        doc = f'{m.group(1)} {m.group(2)}' if m else cita
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
