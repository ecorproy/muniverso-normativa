# senales3.py tNN...: oraciones sospechosas (lee /home/claude/art/tNN/src si existe)
import re, sys, glob, os
R = '/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
BASE = re.compile(r'(\ben suma\b|\ben s[ií]ntesis\b|\ben el fondo\b|\bno es [^.;:]{1,80},? sino\b|\bno solo\b|\bno se trata\b|, no (un|una|a|el|la|los|las) [^.,;]{1,40}\.|\bhay una idea|\blecci[oó]n|\blo que importa|\btesis\b|\bpor contraste|\ben otras palabras|vale la pena|se ordena alrededor|Las secciones (que siguen|siguientes)|por (cinco|seis|cuatro|tres|siete|dos) v[ií]as\.|en la conclusi[oó]n\.|Quedan \w+ dudas|no la produce|^La produce|^(El|La) (primer[oa]|segund[oa]|tercer[oa]|cuart[oa]|quint[oa]|sext[oa]) es (el|la|lo)\b|enseña|se vuelve concret|empieza (a existir )?en el gobierno local|no pidi[oó] un|^Lo que \w+ (es|son)\b|^Y lo que|^El caso (muestra|contiene|deja)|paradoja|La pregunta (útil|de este)|puerta|merece|sin cerrar|literalmente|de verdad\b|un favor|un piso|un techo|deja de ser|es la que|es lo que|\bpesa\b|lo que (no )?admite es|Lo que \w+ (no )?\w+ es\b|el dato|la clave|lo decisivo|en realidad|sin más|nada más\.|y punto)', re.I)
def L(s): return re.sub(r'\s+', ' ', re.sub(r'\[\[[^\]]*\]\]', '§', s)).strip()
for n in sys.argv[1:]:
    d = f'/home/claude/art/{n}/src' if os.path.isdir(f'/home/claude/art/{n}/src') else f'{R}/{n}/src'
    f = glob.glob(f'{d}/*.md')[0]
    t = open(f, encoding='utf-8').read()
    for p in t.split('\n\n'):
        if p.startswith('#'): continue
        ss = [x for x in re.split(r'(?<=[.?!])\s+(?=[A-ZÁÉÍÓÚÑ¿"«])', p) if x.strip()]
        for i, s in enumerate(ss):
            c = L(s); q = re.sub(r'"[^"]*"', '""', c)
            w = len(q.replace('§', '').split())
            short = w <= 8 and not c.startswith('¿') and '§' not in c and not re.match(r'^(Sí|No|Puede|Debe|Lo está|Responden|No basta|No puede)\b', c) and i > 0
            pair = c.startswith('No ') and i > 0 and not ss[i-1].strip().endswith('?')
            if BASE.search(q) or short or pair:
                print(f'{n}: {c.replace("§","")[:240]}')
