# senales2.py tNN...: oraciones con plantillas de redacción artificial (sin macros), una por línea
import re, sys, glob
R = '/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
PAT = re.compile(r'(\ben suma\b|\ben s[ií]ntesis\b|\ben el fondo\b|\bno es [^.;:]{1,80}, sino\b|\bno es [^.;:]{1,60} sino\b|\bno solo\b|\bno se trata\b|, no (un|una|a|el|la|los|las) [^.,;]{1,40}\.|\bhay una idea|\blecci[oó]n|\blo que importa|\btesis\b|\bpor contraste|\ben otras palabras|vale la pena|se ordena alrededor|Las secciones (que siguen|siguientes)|por (cinco|seis|cuatro|tres|siete|dos) v[ií]as\.|en la conclusi[oó]n\.|Quedan \w+ dudas|no la produce|^La produce|^(El|La) (primer[oa]|segund[oa]|tercer[oa]|cuart[oa]|quint[oa]|sext[oa]) es (el|la|lo)\b|enseña|se vuelve concret|empieza (a existir )?en el gobierno local|no pidi[oó] un|^Lo que \w+ (es|son)\b|^Y lo que|^El caso (muestra|contiene|deja)|paradoja|La pregunta (útil|de este)|puerta|^[A-ZÁÉÍÓÚ]\w*( \w+){0,3}\.$|^Y \w+( \w+){0,3}\.$|merece|sin cerrar|literalmente|de verdad\b|no es un favor|un piso|un techo)', re.I)
def L(s): return re.sub(r'\s+', ' ', re.sub(r'\[\[[^\]]*\]\]', '', s)).strip()
for n in sys.argv[1:]:
    f = glob.glob(f'{R}/{n}/src/*.md')[0]
    t = open(f, encoding='utf-8').read()
    for p in t.split('\n\n'):
        if p.startswith('#'): continue
        for s in re.split(r'(?<=[.?!])\s+(?=[A-ZÁÉÍÓÚÑ¿"«])', p):
            c = L(s)
            if c and PAT.search(re.sub(r'"[^"]*"', '""', c)):
                print(f'{n}: {c[:300]}')
