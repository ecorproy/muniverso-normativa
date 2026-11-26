# aplicar.py EDITS.json: aplica reemplazos (sin macros) a /home/claude/art/<tema>/src, regenera y deja ops de Docs
import json, os, re, shutil, subprocess, sys
R = '/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
E = json.load(open(sys.argv[1], encoding='utf-8'))
for tema, eds in E.items():
    d = f'/home/claude/art/{tema}'
    os.makedirs(d, exist_ok=True)
    for s in (() if os.environ.get('SEGUIR') else ('src', 'out')):
        if os.path.isdir(f'{d}/{s}'): shutil.rmtree(f'{d}/{s}')
        shutil.copytree(f'{R}/{tema}/{s}', f'{d}/{s}')
    f = [x for x in os.listdir(d + '/src') if x.endswith('.md')][0]
    p = f'{d}/src/{f}'; t = open(p, encoding='utf-8').read()
    ops = []
    for a, b in eds:
        k = t.count(a)
        if k != 1: print(f'!! {tema}: {k} apariciones de «{a[:70]}»'); continue
        if '[[' in a or '[[' in b: print(f'!! {tema}: macro en «{a[:50]}»'); continue
        t = t.replace(a, b)
        ops.append({"op": "delete", "target": {"kind": "find", "text": a}} if b == '' else {"op": "replace", "target": {"kind": "find", "text": a}, "with": {"as": "text", "from": {"kind": "inline", "content": b}}})
    open(p, 'w', encoding='utf-8').write(t)
    r = subprocess.run(['python3', '-I', '/home/claude/mis_scripts/build_libro.py'], cwd='/home/claude/art',
                       env={**os.environ, 'CITA': 'corta', 'SRC': f'{tema}/src', 'OUT': f'{tema}/out'}, capture_output=True, text=True)
    print(tema, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:])
    o = f'{d}/out'; md = [x for x in os.listdir(o) if x.endswith('.md') and not x.startswith(('zz_', 'unido'))][0]
    open(f'{o}/unido.md', 'w', encoding='utf-8').write(open(f'{o}/{md}', encoding='utf-8').read() + '\n' + open(f'{o}/zz_referencias.md', encoding='utf-8').read())
    jf = f'/home/claude/art/limpieza/{tema}.json'
    prev = json.load(open(jf))['ops'] if (os.environ.get('SEGUIR') and os.path.exists(jf) and not os.environ.get('NUEVO')) else []
    json.dump({"ops": prev + ops}, open(jf, 'w'), ensure_ascii=False)
    print(tema, len(ops), 'ops')
