# cite.py MACRO [MACRO...]  -> cadena de cita expandida (para votos: forma larga y corta) y existencia de la fuente
# cite.py --first DOC.md MACRO...  -> tiene en cuenta los votos ya citados antes en DOC.md
import sys, re, os, io, contextlib
os.environ['SRC'] = '/nonexistent'; os.environ['OUT'] = '/tmp'
code = open('/home/claude/scripts/build.py', encoding='utf-8').read()
code = re.sub(r'\nmain\(\)\s*$', '\n', code)
ns = {}
exec(compile(code, 'build.py', 'exec'), ns)
args = sys.argv[1:]
for mac in args:
    kind = mac.split(':')[0]
    ns['errors'].clear()
    if kind in ('V', 'VT'):
        ns['first_v'].clear()
        a = ns['expand'](mac); b = ns['expand'](mac)
        print(f'{mac}\n   1.ª: {a}\n   resto: {b}')
    else:
        print(f'{mac}\n   {ns["expand"](mac)}')
    for e in ns['errors']:
        print('   !!', e)
