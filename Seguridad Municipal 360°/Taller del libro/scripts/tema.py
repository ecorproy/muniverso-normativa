# tema.py N [máx. caracteres por capa]: lo que el cuerpo legal y las tres capas asignan al tema N
import re, sys
R = '/home/claude/repo/360/Seguridad Municipal 360°/'
n = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
for f in ['Cuerpo legal de los 36 temas.md', 'Capa de jurisprudencia administrativa de los 36 temas.md',
          'Capa de jurisprudencia constitucional de los 36 temas.md', 'Capa de jurisprudencia contencioso administrativa de los 36 temas.md']:
    t = open(R + f, encoding='utf-8').read()
    m = re.search(r'(?ms)^(\*\*)' + n + r'\. [^\n]*\n(.*?)(?=^\*\*\d+\. |^#{2,5}\s)', t)
    print('=====', f[:48], '|', (m.group(0).split('\n')[0] if m else 'NO HALLADO'))
    if m:
        s = re.sub(r'\(https?://[^)]*\)', '', m.group(2))
        print(s.strip()[:mx]); print()
