# Compara el texto pegado de SINALEVI con el del repositorio, artículo por artículo.
# Uso: python3 -I cmp_ley.py PEGADO.txt REPO.md
import sys, re, unicodedata
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'[‪-‮​-‏﻿­]', '', s)
    s = re.sub(r'Ficha Art[ií]culo[^\n]*', '', s)
    s = re.sub(r'[*_#>\[\]\\]', '', s)
    s = re.sub(r'\(https?://[^)]*\)', '', s)
    return re.sub(r'\s+', '', s).lower()
ART = re.compile(r'(?im)^\W{0,6}(?:ART[IÍ]CULO|Art[ií]culo|Articulo)\s+(\d+)(?:\s*(bis|ter))?\s*[º°o]?\s*[\.\-—–:]')
def arts(raw):
    ms = list(ART.finditer(raw)); out = {}
    for i, m in enumerate(ms):
        end = ms[i+1].start() if i+1 < len(ms) else len(raw)
        k = m.group(1) + (' ' + m.group(2).lower() if m.group(2) else '')
        out.setdefault(k, []).append(norm(raw[m.start():end]))
    return out
a = open(sys.argv[1], encoding='utf-8').read(); b = open(sys.argv[2], encoding='utf-8').read()
b = re.sub(r'(?s)^---.*?---', '', b, count=1)
A, B = arts(a), arts(b)
ka, kb = set(A), set(B)
dif = [k for k in sorted(ka & kb, key=lambda x: (int(x.split()[0]), x)) if A[k] != B[k]]
print(f'artículos en el pegado: {len(ka)} | en el repositorio: {len(kb)} | solo pegado: {sorted(ka-kb)} | solo repositorio: {sorted(kb-ka)} | con diferencias: {dif}')
print('texto completo idéntico (normalizado):', norm(a[a.find('Versión de la Norma'):]).replace('©2026procuraduríadelarepublica.todoslosderechosreservados.1','')[40:200] != '' and (norm(b) in norm(a) or norm(a) in norm(b)))
for k in dif[:6]:
    x, y = ''.join(A[k]), ''.join(B[k])
    i = next((j for j, (p, q) in enumerate(zip(x, y)) if p != q), min(len(x), len(y)))
    print(f'  art. {k}: pegado …{x[max(0,i-50):i+70]}… | repo …{y[max(0,i-50):i+70]}…')
