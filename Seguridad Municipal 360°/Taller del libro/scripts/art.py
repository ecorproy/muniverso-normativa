# art.py LEY ART [ART...] : texto de los artículos pedidos de una ley del repositorio (Leyes y decretos nacionales/*/Ley N.md)
import sys, glob, re
R = '/home/claude/repo/main/Leyes y decretos nacionales'
n = sys.argv[1]
fs = glob.glob(f'{R}/*/Ley {n}.md') + glob.glob(f'{R}/*/Ley {n}.md.md')
if n == '7794':
    fs = glob.glob(f'{R}/*/Ley 7794*.md') or fs
if not fs:
    print('no está:', n); sys.exit()
t = open(fs[0], encoding='utf-8').read()
print('archivo:', fs[0])
for a in sys.argv[2:]:
    pat = re.compile(r'(?im)^\W*(?:art[íi]culo|artículo)\s+' + re.escape(a) + r'(?![\w])')
    ms = list(pat.finditer(t))
    if not ms:
        print(f'--- art. {a}: no hallado'); continue
    for m in ms[:2]:
        nxt = re.search(r'(?im)^\W*art[íi]culo\s+\d', t[m.end():])
        fin = m.end() + (nxt.start() if nxt else 3000)
        print(f'--- art. {a} @{m.start()}:', re.sub(r'\s+', ' ', t[m.start():min(fin, m.start()+3500)]))
