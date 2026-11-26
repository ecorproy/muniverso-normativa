# senales.py ARCHIVO.md [...]: señales de redacción artificial, por oración (macros [[...]] ocultas)
import re, sys

PAT = [
    ('cierre', r'\b(en suma|en s[ií]ntesis|en resumen|en definitiva|en conclusi[oó]n|en el fondo|en esencia|a fin de cuentas|al final del d[ií]a)\b'),
    ('negación paralela', r'\bno es [^.;:]{1,70}, sino\b|\bno solo\b|\bno s[oó]lo\b|\bno se trata\b|\bno es (solo|s[oó]lo|simplemente|una cortes)|, no (un|una|a|el|la|los|las) [^.,;]{1,40}\.|\bm[aá]s que (un|una) [^.,;]{1,30}\.'),
    ('revelación con dos puntos', r'\b(hay una idea|la lecci[oó]n|la clave|la respuesta es|esa es la tesis|la tesis de|lo que importa|la verdadera|el punto es|la idea es|la raz[oó]n es simple|la diferencia es)\b'),
    ('vocabulario', r'\b(crucial|clave|panorama|entramado|subraya|destaca|robust[oa]s?|integral(es)?|hol[ií]stic|juega un papel|cabe (se[ñn]alar|destacar|recordar)|vale la pena|en este sentido|en ese sentido|a lo largo de|por contraste|dicho de otro modo|en otras palabras|dicho esto|sin duda|precisamente por eso|es decir,|pilar|hito|potenci|fomenta|multifac|exhaustiv|meticulos|aborda|navega|desentra|arroj[ao] luz|allana)'),
    ('fundamental fuera de derecho', r'(?<!derecho )(?<!derechos )(?<!libertades )\bfundamental(es)?\b'),
    ('gerundio de remate', r', (garantizando|reflejando|subrayando|destacando|evidenciando|consolidando|fortaleciendo|asegurando|permitiendo|generando)\b'),
    ('raya', r'[—–]'),
    ('negrita', r'\*\*'),
    ('triada de cierre', r'\b\w+(an|en|a|e), \w+(an|en|a|e) y \w+(an|en|a|e)\b\.$'),
]
CORTA = 9  # palabras: oración final de párrafo que suena a moraleja

def limpiar(s): return re.sub(r'\[\[[^\]]*\]\]', '', s).replace('  ', ' ').strip()

for f in sys.argv[1:]:
    t = open(f, encoding='utf-8').read()
    n = 0
    for p in t.split('\n\n'):
        if p.startswith('#') or not p.strip(): continue
        ss = [x for x in re.split(r'(?<=[.?!])\s+(?=[A-ZÁÉÍÓÚÑ¿"«])', p) if x.strip()]
        for i, s in enumerate(ss):
            c = limpiar(s)
            if c.startswith('"') and c.count('"') >= 2 and c.rstrip('.').endswith('"'): continue
            sin_citas = re.sub(r'"[^"]*"', '""', c)
            for nom, rx in PAT:
                if re.search(rx, sin_citas, re.I):
                    print(f'{f.split("/")[-1]}\t{nom}\t{c[:200]}'); n += 1
            w = len(sin_citas.split())
            if i == len(ss) - 1 and len(ss) > 1 and w <= CORTA and '"' not in c and not c.startswith('¿'):
                print(f'{f.split("/")[-1]}\tremate corto\t{c}'); n += 1
            if i == 0 and w <= 5 and len(ss) > 1 and not c.startswith('¿'):
                print(f'{f.split("/")[-1]}\tarranque fragmento\t{c}'); n += 1
    print(f'# {f.split("/")[-1]}: {n}', file=sys.stderr)
