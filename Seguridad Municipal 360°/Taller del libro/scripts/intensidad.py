# Lista, fuera de las citas textuales, las palabras absolutas o excluyentes de un capítulo.
import re, sys
PAT = r'\b(únic[oa]s?|únicamente|sol[oa]s?|solamente|ning[uú]n[oa]?s?|nunca|siempre|jamás|tod[oa]s?|nadie|nada|primer[oa]?s?|se adelant\w+|antigu[oa]s?|por primera vez|exclusiv\w+|sin excepción|cualquier|apenas|tampoco|ni siquiera|nadie|el mayor|la mayor|el mejor|la mejor|el peor|la peor|más \w+ de|jamás|inédit\w+|pioner\w+|siempre que|nunca antes|hasta hoy|hoy no|no hay|no existe\w*|no se mide|no es municipal|no figura\w*|no aparece\w*|no menciona\w*|no nombra\w*|no dice|no trae|no tiene)\b'
for f in sys.argv[1:]:
    t = open(f, encoding='utf-8').read()
    sinc = re.sub(r'"[^"]*"', lambda m: '"' + '·' * (len(m.group(0)) - 2) + '"', t)
    print('=====', f.split('/')[-1])
    n = 0
    for m in re.finditer(PAT, sinc, flags=re.I):
        a = max(0, m.start() - 75); b = min(len(t), m.end() + 75)
        ctx = re.sub(r'\s+', ' ', sinc[a:b]).replace('·', '')
        ctx = re.sub(r'\[\[[^\]]*\]\]', '§', ctx)
        n += 1
        print(f'{n:3d} [{m.group(0)}] …{ctx}…')
