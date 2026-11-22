# Compara por párrafos el .docx (convertido con pandoc) con el texto de la revisión 126 del taller.
import re, unicodedata
def norm(t):
    t=unicodedata.normalize('NFC',t).replace('\\','')
    t=re.sub(r'[*_#>]','',t)
    t=re.sub(r'<(https?://[^>\s]+)>',r'\1',t)
    t=re.sub(r'\[(https?://[^\]\s]+)\]\((https?://[^)\s]+)\)',r'\1',t)
    return re.sub(r'\s+',' ',t).strip()
d=open('/home/claude/libro/docx/libro.md',encoding='utf-8').read()
a=open('/home/claude/art/src3/all.md',encoding='utf-8').read()
i=d.find('**Resumen**'); j=d.find('**Referencias**')
P=lambda t:[x for x in (norm(p) for p in re.split(r'\n\s*\n',t)) if x]
D=P(d[i:j]); A=P(a)
print('párrafos docx:',len(D),'| párrafos taller (rev. 126):',len(A),'| idénticos:',D==A)
if D!=A:
    sa=set(A); sd=set(D)
    print('solo en taller:',len(sa-sd),'| solo en docx:',len(sd-sa))
    for x in list(sa-sd)[:6]: print('  TALLER:',x[:200])
    for x in list(sd-sa)[:6]: print('  DOCX  :',x[:200])
refs=P(d[j:])[1:]
g=[x.strip() for x in open('/home/claude/libro/base126/out/zz_referencias.md',encoding='utf-8').read().split('\n\n')[1:] if x.strip()]
N=lambda s: norm(s).replace(' ','')
G={N(x):x for x in g}; R={N(x):x for x in refs}
print('referencias en el docx:',len(refs),'| generadas por el verificador:',len(g),'| faltan en docx:',len(set(G)-set(R)),'| sobran en docx:',len(set(R)-set(G)))
for k in list(set(G)-set(R))[:5]: print('  +',G[k][:140])
for k in list(set(R)-set(G))[:5]: print('  -',R[k][:140])
