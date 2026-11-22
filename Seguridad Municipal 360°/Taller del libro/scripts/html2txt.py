# Extrae el texto visible de un HTML (sin scripts ni estilos). Uso: python3 -I html2txt.py ENTRADA.html SALIDA.txt
import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.skip=0; s.out=[]
    def handle_starttag(s,t,a):
        if t in('script','style','noscript','svg'): s.skip+=1
        if t in('p','div','br','li','h1','h2','h3','h4','h5','tr','section'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in('script','style','noscript','svg') and s.skip: s.skip-=1
        if t in('p','div','li','h1','h2','h3','h4','h5','tr','section'): s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
t=''.join(p.out); t=re.sub(r'[ \t\xa0]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t).strip()
open(sys.argv[2],'w',encoding='utf-8').write(t)
print(sys.argv[2], len(t),'caracteres', len(t.split()),'palabras')
