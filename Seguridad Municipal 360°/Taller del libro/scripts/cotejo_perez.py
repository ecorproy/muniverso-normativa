# Coteja las once citas (A-K) de la nota del autor contra el PDF de Pérez Hernández, Tabares Neyra y Díaz Legón (2019).
# Página impresa = página del archivo + 134.
import re, unicodedata, sys
def norm(s):
    s = re.sub(r'[‪-‮​-‏﻿­]', '', s)
    s = s.replace('*', '')
    s = re.sub(r'[“”«»"\'‘’`´]', '', s)
    s = re.sub(r'\s+', '', s)
    return unicodedata.normalize('NFC', s)
def dehyph(s): return re.sub(r'(?<=\w)[-­]\s*\n\s*(?=\w)', '', s)
pages = open('/home/claude/libro/perez/perez.txt', encoding='utf-8').read().split('\f')
# quitar el folio del pie para que no se meta dentro de frases que cruzan página
clean = []
for p in pages:
    ls = p.rstrip().split('\n')
    if ls and re.fullmatch(r'\s*\d{3}\s*', ls[-1]): ls = ls[:-1]
    clean.append('\n'.join(ls))
N = [norm(p) + '\x00' + norm(dehyph(p)) for p in clean]
full = norm('\n'.join(clean)); fullh = norm(dehyph('\n'.join(clean)))
# posiciones de inicio de cada página en el texto completo normalizado
starts = []; acc = 0
for p in clean:
    starts.append(acc); acc += len(norm(p))
def pagina_de(pos):
    k = 0
    for i, s in enumerate(starts):
        if s <= pos: k = i
    return k + 1 + 134
nota = open('/mnt/user-data/uploads/c7d4173f-attachment.txt', encoding='utf-8').read().split('\n')
letras = 'ABCDEFGHIJK'; citas = {}
cur = None
for ln in nota[:47]:
    m = re.match(r'([A-K])\. ', ln)
    if m: cur = m.group(1); continue
    if cur and ln.strip().startswith('"') and cur not in citas:
        q = ln.strip()
        q = q[1:q.rindex('"')]
        citas[cur] = q
for k in letras:
    q = citas[k]
    segs = [s.strip(' ;') for s in re.split(r'\s*(?:\.\.\.|…)\s*', q) if s.strip(' ;')]
    print(f'--- {k} ({len(re.findall(chr(92)+"w+", q))} palabras, {len(segs)} tramo(s))')
    for s in segs:
        n = norm(s); pos = full.find(n)
        if pos < 0:
            # probar sin el punto o signo final y por mitades para ubicar la diferencia
            n2 = n.rstrip('.,;:'); pos = full.find(n2)
            if pos >= 0:
                print(f'   LITERAL (salvo signo final) p. {pagina_de(pos)}' + (f'-{pagina_de(pos+len(n2)-1)}' if pagina_de(pos+len(n2)-1)!=pagina_de(pos) else '') + f' | {s[:70]}…')
                continue
            # localizar el mayor prefijo que sí está
            lo, hi = 0, len(n)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if full.find(n[:mid]) >= 0: lo = mid
                else: hi = mid - 1
            p0 = full.find(n[:lo]) if lo > 15 else -1
            print(f'   NO LITERAL | coincide hasta el carácter {lo} de {len(n)}' + (f' (p. {pagina_de(p0)})' if p0 >= 0 else '') + f' | {s[:60]}…')
            if p0 >= 0:
                print(f'       nota : …{n[max(0,lo-40):lo+60]}')
                print(f'       texto: …{full[p0+max(0,lo-40):p0+lo+60]}')
        else:
            a, b = pagina_de(pos), pagina_de(pos + len(n) - 1)
            print(f'   LITERAL p. {a}' + (f'-{b}' if b != a else '') + f' | {s[:70]}…')
