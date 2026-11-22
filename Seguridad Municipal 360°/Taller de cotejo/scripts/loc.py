# loc.py: segunda verificación de la ubicación (considerando) de cada cita textual de votos y resoluciones.
# Imprime la cadena de encabezados que precede a la cita en el texto íntegro.
import re, glob, os, sys, unicodedata

R = '/home/claude/repo/main'
SRC = '/home/claude/art/src'
VAL = {}


def roman(s):
    v = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    t = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and v[c] < v[s[i + 1]]:
            t -= v[c]
        else:
            t += v[c]
    return t


def f_voto(x):
    return f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/Sentencia {x}.md'


def f_tca(x):
    fs = glob.glob(f'{R}/Jurisprudencia contencioso administrativa (TCA)/Municipal/Sentencia TCA * {x}.md')
    return fs[0]


def squash(s):
    s = re.sub(r'[‪-‮​-‏﻿­*]', '', s)
    return unicodedata.normalize('NFC', re.sub(r'\s+', ' ', s))


def flex(frag):
    # regex tolerante a espacios y comillas
    core = re.sub(r'[“”«»"\'‘’`´\s]', '', frag)
    return re.compile(r'[“”«»"\'‘’`´\s]*'.join(re.escape(c) for c in core))


HEAD = re.compile(r'(?<![\wÁÉÍÓÚáéíóúñ])([IVXL]{1,7})\s*\)?\s*\.\s*-|(?<![\wÁÉÍÓÚáéíóúñ])([IVXL]{1,7})\s*\.\s+(?=[A-ZÁÉÍÓÚ][a-záéíóú])')

rows = []
for f in sorted(glob.glob(f'{SRC}/*.md')):
    txt = open(f, encoding='utf-8').read()
    for m in re.finditer(r'"([^"]+)"\s*\[\[([^\]]+)\]\]', txt):
        q, mac = m.group(1), m.group(2).replace('!', '')
        p = [x.strip() for x in mac.split(':')]
        if p[0] not in ('V', 'VT', 'T'):
            continue
        x = p[1] if p[0] in ('V', 'T') else p[2]
        loc = p[-1]
        path = f_voto(x) if p[0] != 'T' else f_tca(x)
        t = squash(open(path, encoding='utf-8').read())
        seg = re.split(r'\s*\[…\]\s*', q)[0]
        ms = list(flex(seg).finditer(t))
        if not ms:
            rows.append((os.path.basename(f), x, loc, 'NO HALLADA', q[:50]))
            continue
        pos = ms[-1].start()
        # inicio de la parte considerativa: último "Considerando" antes de la cita
        cs = [c.start() for c in re.finditer(r'(?i)considerando\s*:?', t[:pos])]
        start = cs[-1] if cs else 0
        chain = []
        for h in HEAD.finditer(t, start, pos):
            lab = h.group(1) or h.group(2)
            pre = t[max(0, h.start() - 8):h.start()]
            nested = bool(re.search(r'[“"«(…]\s*(\(…\))?\s*$', pre)) or '(…)' in pre
            chain.append(('q' if nested else '') + lab)
        pt = [c.start() for c in re.finditer(r'(?i)por tanto\s*:', t[start:pos])]
        want = None
        mm = re.search(r'considerando\s+([IVXL]+)', loc)
        if mm:
            want = mm.group(1)
        elif 'por tanto' in loc.lower():
            want = 'PT'
        # ¿cadena simple (estrictamente creciente, sin anidados)?
        plain = [c for c in chain]
        vals = [roman(c) for c in plain if not c.startswith('q')]
        simple = all(not c.startswith('q') for c in plain) and all(b == a + 1 for a, b in zip(vals, vals[1:])) and (not vals or vals[0] == 1)
        last = plain[-1] if plain else '-'
        if want == 'PT':
            estado = 'OK-PT' if pt else 'REVISAR-PT'
        elif simple and last == want and not pt:
            estado = 'OK'
        else:
            estado = 'REVISAR'
        rows.append((os.path.basename(f), x, loc, estado, ' '.join(plain[-14:]) + (' |PT antes' if pt and want != 'PT' else '') + f'  «{q[:38]}»'))

ok = sum(1 for r in rows if r[3].startswith('OK'))
print(f'citas de votos y resoluciones: {len(rows)} | OK automático: {ok}')
for r in rows:
    if not r[3].startswith('OK'):
        print(' ', r[0][:8], r[1], '|', r[2], '|', r[3], '|', r[4])
