# Compara un pegado de SINALEVI con la copia del repositorio, por artículos.
import re, sys, difflib, unicodedata
def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'(?s)\A---\n.*?\n---\n', '', s)
    s = s.replace('**', '')
    s = re.sub(r'(?m)^\s*Ficha Art[íi]culo.*$', '', s)
    s = re.sub(r'(?m)^-Usted está en la última versión de la norma-\s*$', '', s)
    s = re.sub(r'(?m)^Versión de la Norma:.*$', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()
def arts(s):
    # corta por encabezados de artículo
    parts = re.split(r'(?i)(?=\bart[íi]culo\s+\d+\s*(?:bis|ter|qu[aá]ter|quinquies|sexies)?\s*[\.\-º°—–])', s)
    d = {}
    for p in parts:
        m = re.match(r'(?i)art[íi]culo\s+(\d+\s*(?:bis|ter|qu[aá]ter|quinquies|sexies)?)', p)
        k = re.sub(r'\s+', ' ', m.group(1).lower()) if m else 'pre'
        d.setdefault(k, '')
        d[k] += p
    return d
a = open(sys.argv[1], encoding='utf-8').read(); b = open(sys.argv[2], encoding='utf-8').read()
va = re.search(r'Versión de la Norma:\s*(.+)', a); vb = re.search(r'version_sinalevi:\s*"(.+?)"', b)
print('pegado: versión', va.group(1).strip() if va else '?', '| repositorio: versión', vb.group(1) if vb else '?')
na, nb = norm(a), norm(b)
print('caracteres normalizados: pegado', len(na), '| repositorio', len(nb), '| idénticos:', na == nb)
if na != nb:
    da, db = arts(na), arts(nb)
    difer = [k for k in da if k in db and da[k] != db[k]]
    solo_a = [k for k in da if k not in db]; solo_b = [k for k in db if k not in da]
    print('artículos que difieren:', difer[:60]); print('solo en el pegado:', solo_a[:40]); print('solo en el repositorio:', solo_b[:40])
    for k in difer[:6]:
        sm = difflib.SequenceMatcher(None, da[k], db[k], autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                print('  art.', k, tag, '| pegado:', repr(da[k][max(0,i1-40):i2+40][:220]), '| repo:', repr(db[k][max(0,j1-40):j2+40][:220])); break
