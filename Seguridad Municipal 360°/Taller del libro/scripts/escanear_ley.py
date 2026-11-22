# Lista artículos de una ley del repositorio que contienen un patrón, con la frase que lo contiene.
import re, sys, glob
n, pat = sys.argv[1], sys.argv[2]
modo = sys.argv[3] if len(sys.argv) > 3 else 'frases'
fs = glob.glob(f'/home/claude/libro/fuentes/Ley {n}.md') or glob.glob(f'/home/claude/repo/360/Leyes y decretos nacionales/*/Ley {n}.md')
s = open(fs[0], encoding='utf-8').read()
s = re.sub(r'(?s)\A---\n.*?\n---\n', '', s).replace('**', '')
parts = re.split(r'(?im)^(?=\s*art[íi]culo\s+\d+)', s)
rx = re.compile(pat, re.I)
for p in parts:
    m = re.match(r'(?i)\s*(art[íi]culo\s+\d+\s*(?:bis|ter|qu[aá]ter|quinquies|sexies)?)[\s\.\-º°—–]*([^\n]{0,90})', p)
    head = (m.group(1) + ' ' + m.group(2)).strip() if m else '(preliminar)'
    if modo == 'titulos':
        if not sys.argv[4:] or int(re.search(r'\d+', head).group()) >= int(sys.argv[4]) if m else False:
            print(re.sub(r'\s+', ' ', head)[:120])
        continue
    if rx.search(p):
        print('##', re.sub(r'\s+', ' ', head)[:110])
        for sent in re.split(r'(?<=[\.\:;])\s+|\n+', p):
            if rx.search(sent):
                print('    ·', re.sub(r'\s+', ' ', sent)[:420])
