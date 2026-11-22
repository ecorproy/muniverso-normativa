# Compara el texto exportado del documento con los archivos out/ verificados.
import sys, json, base64, re, glob, os, unicodedata, difflib
exp_path, out_dir, dump = sys.argv[1], sys.argv[2], sys.argv[3]
j = json.loads(open(exp_path, encoding='utf-8').read())
def find_b64(o):
    best = ''
    if isinstance(o, dict):
        for v in o.values():
            c = find_b64(v)
            if len(c) > len(best): best = c
    elif isinstance(o, list):
        for v in o:
            c = find_b64(v)
            if len(c) > len(best): best = c
    elif isinstance(o, str):
        if len(o) > 1000 and re.fullmatch(r'[A-Za-z0-9+/=\s]+', o): best = o
    return best
md = base64.b64decode(find_b64(j)).decode('utf-8')
open(dump, 'w', encoding='utf-8').write(md)
print('keys:', list(j.keys()), '| data keys:', list(j.get('data', {}).keys()))
print('exportado:', len(md), 'caracteres;', len(md.split()), 'palabras')
files = sorted(f for f in glob.glob(os.path.join(out_dir, '*.md')) if not os.path.basename(f).startswith('zz_refs_'))
print('archivos out:', [os.path.basename(f) for f in files])
src = '\n\n'.join(open(f, encoding='utf-8').read().strip() for f in files)
def norm(t):
    t = unicodedata.normalize('NFC', t)
    t = t.replace('\\', '')
    t = re.sub(r'[*_#>]', '', t)
    t = re.sub(r'<(https?://[^>\s]+)>', r'\1', t)
    t = re.sub(r'\[(https?://[^\]\s]+)\]\((https?://[^)\s]+)\)', r'\1', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()
a, b = norm(src), norm(md)
print('normalizado fuente:', len(a), '| doc:', len(b))
# localizar el cuerpo del artículo en el doc (después de título y firma)
i = b.find('Resumen')
print('inicio doc:', repr(b[:260]))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
print('diferencias:', len(ops))
for tag, i1, i2, j1, j2 in ops[:60]:
    print('-' * 60)
    print(tag, '| fuente[%d:%d] doc[%d:%d]' % (i1, i2, j1, j2))
    print('  FUENTE: …' + a[max(0, i1 - 60):i1] + '【' + a[i1:i2][:300] + '】' + a[i2:i2 + 60] + '…')
    print('  DOC   : …' + b[max(0, j1 - 60):j1] + '【' + b[j1:j2][:300] + '】' + b[j2:j2 + 60] + '…')
