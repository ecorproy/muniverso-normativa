# contexto.py ARCHIVO: oraciones con señales y la siguiente, sin macros
import re, sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
PAT = re.compile(r'(\ben suma\b|\ben s[ií]ntesis\b|\ben el fondo\b|\bno es [^.;:]{1,70}, sino\b|\bno solo\b|\bno se trata\b|, no (un|una|a|el|la|los|las) [^.,;]{1,40}\.|\bhay una idea|\bla lecci[oó]n|\blo que importa|\bla tesis|\bpor contraste|\ben otras palabras|vale la pena|se ordena alrededor|Las secciones (que siguen|siguientes)|por (cinco|seis|cuatro|tres|siete|dos) v[ií]as|en la conclusi[oó]n\.|Quedan \w+ dudas|no la produce|La produce|^(El|La) (primer[oa]|segund[oa]|tercer[oa]|cuart[oa]|quint[oa]|sext[oa]) es\b|enseña|^Y [a-z])', re.I)
def L(s): return re.sub(r'\s+',' ',re.sub(r'\[\[[^\]]*\]\]','',s)).strip()
for f in sys.argv[1:]:
    t=open(f,encoding='utf-8').read()
    for p in t.split('\n\n'):
        if p.startswith('#'): continue
        ss=[x for x in re.split(r'(?<=[.?!])\s+(?=[A-ZÁÉÍÓÚÑ¿"«])',p) if x.strip()]
        for i,s in enumerate(ss):
            c=L(s); w=len(re.sub(r'"[^"]*"','',c).split())
            frag = (i==0 and w<=5 and len(ss)>1 and not c.startswith('¿')) or (i==len(ss)-1 and len(ss)>1 and w<=9 and '"' not in c and not c.startswith('¿') and not re.search(r'tema \d',c))
            if PAT.search(c) or frag:
                nx = L(ss[i+1])[:160] if i+1<len(ss) else ''
                print(f"{f.split('/')[-3] if 'Cap' in f else f}: «{c[:260]}» ⟶ {nx}")
