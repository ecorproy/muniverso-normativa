# deexp.py DOC.md OUTDIR [OVERRIDES.json]
# Convierte el markdown exportado del documento a la forma con macros que entiende build.py (para cotejar el documento mismo).
import sys, re, os, json, unicodedata
src, outdir = sys.argv[1], sys.argv[2]
ovr = json.load(open(sys.argv[3], encoding='utf-8')) if len(sys.argv) > 3 and os.path.exists(sys.argv[3]) else []
code = open('/home/claude/mis_scripts/build_libro.py', encoding='utf-8').read()
m = re.search(r"\nCGR = \{.*?\n\}\n", code, re.S)
ns = {}
exec(m.group(0), ns)
CGR = ns['CGR']
t = open(src, encoding='utf-8').read()
t = t.replace('\\[', '[').replace('\\]', ']').replace('\\*', '*').replace('\\_', '_').replace('\\>', '>').replace('\\#', '#')
# cuerpo: desde "## Resumen" hasta antes de "## Referencias"
body = t.strip() + '\n'
FECHA = r'(?:, de las [\d:]+ horas del \d+ de \w+ de \d{4}|, del \d+ de \w+ de \d{4})?'
def nq(s):
    s = unicodedata.normalize('NFC', s)
    return re.sub(r'[\s"«»“”‘’\'*]', '', s)[:28]
def forced(macro_src, loc, before):
    mq = re.search(r'"([^"]+)"\s*$', before)
    if not mq: return ''
    q = nq(mq.group(1))
    for o in ovr:
        if o['src'] == macro_src and o['loc'] == loc and nq(o['q']) == q:
            return '!'
    return ''
def sub(pat, fn, s):
    out = []; last = 0
    for mm in re.finditer(pat, s):
        out.append(s[last:mm.start()]); out.append(fn(mm, s[max(0, mm.start() - 900):mm.start()])); last = mm.end()
    out.append(s[last:]); return ''.join(out)
def f_sala(mm, before):
    a, b, loc = mm.group('a'), mm.group('b'), (mm.group('loc') or '').strip()
    if b:
        return f'[[VT:{a}:{b}:{loc}{forced("VT:"+a+":"+b, loc, before)}]]'
    return f'[[V:{a}:{loc}{forced("V:"+a, loc, before)}]]' if loc else f'[[V:{a}]]'
body = sub(r'\(Sala Constitucional, voto N\.° (?P<a>[\d-]+)' + FECHA + r'(?:, transcrito en el voto N\.° (?P<b>[\d-]+)' + FECHA + r')?(?:, (?P<loc>[^()]*))?\)', f_sala, body)
def f_pgr(mm, before):
    x, loc = mm.group('x'), (mm.group('loc') or '').strip()
    return f'[[D:{x}:{loc}{forced("D:"+x, loc, before)}]]' if loc else f'[[D:{x}]]'
body = sub(r'\(Procuraduría General de la República, dictamen (?P<x>[A-Z]+(?:-[A-Z]+)?-\d+-\d{4}), \d{4}(?:, (?P<loc>[^()]*))?\)', f_pgr, body)
def f_tca(mm, before):
    n, y, loc = mm.group('n'), mm.group('y'), (mm.group('loc') or '').strip()
    key = f'{y}-{int(n):06d}'
    return f'[[T:{key}:{loc}{forced("T:"+key, loc, before)}]]' if loc else f'[[T:{key}]]'
body = sub(r'\(Tribunal Contencioso Administrativo(?:, Sección [IVX]+)?, resolución N\.° (?P<n>\d+)-(?P<y>\d{4})(?:, (?P<loc>[^()]*))?\)', f_tca, body)
def f_cgr(mm, before):
    inner = mm.group('inner')
    for k, c in CGR.items():
        if inner == c['cita']:
            return f'[[O:{k}]]'
        if inner.startswith(c['cita'] + ', '):
            return f'[[O:{k}:{inner[len(c["cita"]) + 2:]}]]'
    return mm.group(0)
body = sub(r'\(Contraloría General de la República, (?P<inner>[^()]*)\)', f_cgr, body)
def f_ley(mm, before):
    n, loc = mm.group('n'), (mm.group('loc') or '').strip()
    return f'[[L:{n}:{loc}]]' if loc else mm.group(0)
body = sub(r'\(Ley N\.° (?P<n>\d+), \d{4}(?:, (?P<loc>[^()]*))?\)', f_ley, body)
def f_dec(mm, before):
    n, loc = mm.group('n'), (mm.group('loc') or '').strip()
    return f'[[DE:{n}:{loc}]]' if loc else f'[[DE:{n}]]'
body = sub(r'\(Decreto Ejecutivo N\.° (?P<n>\d+), \d{4}(?:, (?P<loc>[^()]*))?\)', f_dec, body)
def f_cp(mm, before):
    loc = (mm.group('loc') or '').strip()
    return f'[[CP:{loc}]]' if loc else mm.group(0)
body = sub(r'\(Constitución Política de la República de Costa Rica, 1949(?:, (?P<loc>[^()]*))?\)', f_cp, body)
os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    if f.endswith('.md'): os.remove(os.path.join(outdir, f))
open(os.path.join(outdir, 'all.md'), 'w', encoding='utf-8').write(body)
print('macros:', len(re.findall(r'\[\[', body)), '| paréntesis de fuente sin convertir:', len(re.findall(r'\((?:Sala Constitucional|Procuraduría General|Tribunal Contencioso|Ley N\.°|Decreto Ejecutivo|Constitución Política|Contraloría General)[^()]*\)', body)))
for mm in re.finditer(r'\((?:Sala Constitucional|Procuraduría General|Tribunal Contencioso|Ley N\.°|Decreto Ejecutivo|Constitución Política|Contraloría General)[^()]*\)', body):
    print('   sin convertir:', mm.group(0)[:140])
