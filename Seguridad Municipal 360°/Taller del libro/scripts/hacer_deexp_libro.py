# Genera deexp_libro.py a partir del deexp.py del taller: el cuerpo es toda la pestaña (un capítulo no trae
# «## Resumen» ni «## Referencias») y la ubicación verificada a mano vale también para dictámenes.
s = open('/home/claude/scripts/deexp.py', encoding='utf-8').read()
a = "i = t.find('## Resumen'); j = t.find('\\n## Referencias')\nbody = t[i:j if j > 0 else len(t)].strip() + '\\n'"
assert s.count(a) == 1
s = s.replace(a, "body = t.strip() + '\\n'")
b = "return f'[[D:{x}:{loc}]]' if loc else f'[[D:{x}]]'"
assert s.count(b) == 1
s = s.replace(b, "return f'[[D:{x}:{loc}{forced(\"D:\"+x, loc, before)}]]' if loc else f'[[D:{x}]]'")
s = s.replace("/home/claude/scripts/build.py", "/home/claude/mis_scripts/build_libro.py")
open('/home/claude/mis_scripts/deexp_libro.py', 'w', encoding='utf-8').write(s)
print('deexp_libro.py listo')
