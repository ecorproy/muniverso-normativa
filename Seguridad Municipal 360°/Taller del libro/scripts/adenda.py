# adenda.py EDITS.json: aplica reemplazos (con macros) a copia fresca de cada tema, regenera y deja ops de Docs
# (replace por ventana de texto; insert de párrafos nuevos con ANCLA = texto del párrafo previo, para resolver luego a id)
import json, os, re, shutil, subprocess, sys, difflib
R = '/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
E = json.load(open(sys.argv[1], encoding='utf-8'))
def paras(t): return [b for b in t.split('\n\n') if b.strip()]
for tema, eds in E.items():
    d = f'/home/claude/art/{tema}'
    for s in (() if os.environ.get('SEGUIR') else ('src', 'out')):
        if os.path.isdir(f'{d}/{s}'): shutil.rmtree(f'{d}/{s}')
        shutil.copytree(f'{R}/{tema}/{s}', f'{d}/{s}')
    f = [x for x in os.listdir(d + '/src') if x.endswith('.md')][0]
    p = f'{d}/src/{f}'; t = open(p, encoding='utf-8').read()
    base = open(f'{d}/out/unido.md', encoding='utf-8').read() if os.environ.get('SEGUIR') else open(f'{R}/{tema}/out/unido.md', encoding='utf-8').read() if os.path.exists(f'{R}/{tema}/out/unido.md') else None
    for a, b in eds:
        k = t.count(a)
        if k != 1: print(f'!! {tema}: {k} apariciones de «{a[:70]}»'); sys.exit(1)
        t = t.replace(a, b)
    open(p, 'w', encoding='utf-8').write(t)
    r = subprocess.run(['python3', '-I', '/home/claude/mis_scripts/build_libro.py'], cwd='/home/claude/art',
                       env={**os.environ, 'CITA': 'corta', 'SRC': f'{tema}/src', 'OUT': f'{tema}/out'}, capture_output=True, text=True)
    print(tema, '\n'.join(r.stdout.strip().splitlines()[-3:]) if r.stdout.strip() else r.stderr[-600:])
    o = f'{d}/out'; md = [x for x in os.listdir(o) if x.endswith('.md') and not x.startswith(('zz_', 'unido'))][0]
    new = open(f'{o}/{md}', encoding='utf-8').read() + '\n' + open(f'{o}/zz_referencias.md', encoding='utf-8').read()
    open(f'{o}/unido.md', 'w', encoding='utf-8').write(new)
    old = base
    A, B = paras(old), paras(new); ops = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag == 'equal': continue
        if tag == 'replace' and i2 - i1 == j2 - j1:
            for x, y in zip(A[i1:i2], B[j1:j2]):
                pr = 0
                while pr < min(len(x), len(y)) and x[pr] == y[pr]: pr += 1
                su = 0
                while su < min(len(x), len(y)) - pr and x[-1 - su] == y[-1 - su]: su += 1
                L = pr
                while True:
                    L = max(0, L - 50); L = x.rfind(' ', 0, L) + 1 if L else 0
                    w = x[L:len(x) - su]
                    if not w.strip() or old.count(w) == 1 or L == 0: break
                ops.append({"op": "replace", "target": {"kind": "find", "text": w},
                            "with": {"as": "text", "from": {"kind": "inline", "content": y[L:len(y) - su]}}})
                if old.count(w) != 1 or not w.strip(): print('!! ventana no única', tema, w[:60])
        elif tag == 'insert':
            ops.append({"op": "insert", "ANCLA": A[i1 - 1][:120], "side": "after",
                        "source": {"as": "markdown", "from": {"kind": "inline", "content": '\n\n'.join(B[j1:j2])}}})
        else:
            print('!! diff complejo', tema, tag, i1, i2, j1, j2)
    json.dump({"ops": ops}, open(f'/home/claude/art/cgr27/{tema}.json', 'w'), ensure_ascii=False, indent=1)
    print(tema, len(ops), 'ops', [o['op'] for o in ops])
