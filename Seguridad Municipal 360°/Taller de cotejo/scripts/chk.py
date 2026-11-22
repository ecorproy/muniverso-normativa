# chk.py EXPORT_FILE  -> decodifica el export del doc, lo coteja (citas literales, ubicaciones, formas de cita) y resume.
import sys, json, base64, re, os, subprocess, unicodedata, difflib
exp = sys.argv[1]
raw = open(exp, encoding='utf-8').read()
j = json.loads(raw)
if isinstance(j, list):
    cand = None
    for it in j:
        t = it.get('text', '') if isinstance(it, dict) else ''
        k = t.find('{"verdict"')
        if k >= 0:
            try:
                cand = json.JSONDecoder().raw_decode(t[k:])[0]
            except Exception:
                pass
    j = cand
md = base64.b64decode(j['data']['bytes_b64']).decode('utf-8')
os.makedirs('/home/claude/export', exist_ok=True)
open('/home/claude/export/doc.md', 'w', encoding='utf-8').write(md)
print('doc rev', j.get('rev'), '|', len(md), 'caracteres |', len(md.split()), 'palabras')
r = subprocess.run(['python3', '-I', '/home/claude/scripts/deexp.py', '/home/claude/export/doc.md', '/home/claude/art/src3', '/home/claude/art/overrides.json'], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()[:800])
env = dict(os.environ, SRC='/home/claude/art/src3', OUT='/home/claude/art/out3')
r = subprocess.run(['python3', '-I', '/home/claude/scripts/build.py'], capture_output=True, text=True, env=env, cwd='/home/claude/art')
print('\n'.join(r.stdout.strip().split('\n')[-4:])); print(r.stderr.strip()[:1500])
rep = open('/home/claude/art/out3/zz_informe.txt', encoding='utf-8').read()
i = rep.find('NOTAS DE VOCABULARIO')
print(rep[:i].strip()[:6000])
def norm(t):
    t = unicodedata.normalize('NFC', t).replace('\\', '')
    t = re.sub(r'[*_#>]', '', t)
    return re.sub(r'\s+', ' ', t).strip()
body_doc = md[md.find('## Resumen'): md.find('\n## Referencias') if '\n## Referencias' in md else len(md)]
def paras(t):
    return [x for x in (norm(p) for p in re.split(r'\n\s*\n', t)) if x]
A = paras(open('/home/claude/art/out3/all.md', encoding='utf-8').read()); B = paras(body_doc)
if A == B:
    print('\nFORMAS DE CITA: el cuerpo del documento coincide con la forma canónica.')
else:
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    n = 0; out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        if tag == 'replace' and (i2 - i1) == (j2 - j1):
            for a, b in zip(A[i1:i2], B[j1:j2]):
                s2 = difflib.SequenceMatcher(None, a, b, autojunk=False)
                for t2, x1, x2, y1, y2 in s2.get_opcodes():
                    if t2 == 'equal':
                        continue
                    n += 1
                    out.append('  CANON: …' + a[max(0, x1 - 70):x1] + '【' + a[x1:x2][:200] + '】' + a[x2:x2 + 30] + '\n  DOC  : …' + b[max(0, y1 - 70):y1] + '【' + b[y1:y2][:200] + '】' + b[y2:y2 + 30] + '\n')
        else:
            n += 1
            out.append('  BLOQUE ' + tag + ' | CANON: ' + ' ¶ '.join(x[:90] for x in A[i1:i2]) + '\n           | DOC  : ' + ' ¶ '.join(x[:90] for x in B[j1:j2]) + '\n')
    print(f'\nFORMAS DE CITA: {n} diferencias (canónico -> documento):')
    for o in out[:int(os.environ.get('MAXD', '60'))]:
        print(o)
# referencias: comparar lista generada con la del doc
gen = [x.strip() for x in open('/home/claude/art/out3/zz_referencias.md', encoding='utf-8').read().split('\n\n')[1:] if x.strip()]
k = md.find('\n## Referencias')
cur = [x.strip() for x in md[k:].split('\n\n')[1:] if x.strip()] if k >= 0 else []
ng = lambda s: norm(s)
G = {ng(x): x for x in gen}; C = {ng(x): x for x in cur}
add = [G[x] for x in G if x not in C]; rem = [C[x] for x in C if x not in G]
print(f'\nREFERENCIAS: generadas {len(gen)} | en el doc {len(cur)} | faltan en el doc {len(add)} | sobran en el doc {len(rem)}')
json.dump(dict(add=add, rem=rem, gen=gen), open('/home/claude/export/refs_delta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for x in add[:60]: print('  + ' + x[:110])
for x in rem[:60]: print('  - ' + x[:110])
