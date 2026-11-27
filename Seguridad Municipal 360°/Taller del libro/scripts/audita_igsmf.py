# Las fichas del IGSM 2025 se citan por página impresa (= página del PDF menos uno).
# Compara cada oración que cita O:IGSMF:p. N con la página impresa N y con la N-1 / N+1.
import re,glob,unicodedata,sys
f='/home/claude/repo/360/Seguridad Municipal 360°/Criterios CGR/IGSM 2025 - fichas de indicadores - texto extraído.txt'
P=open(f).read().split('\f')
def sinac(s):
    s=unicodedata.normalize('NFD',s.lower()); return ''.join(ch for ch in s if unicodedata.category(ch)!='Mn')
STOP=set('para como esta este sobre entre cuando tambien donde segun cada desde hasta porque pero sino solo otra otro mide miden fichas ficha indice contraloria municipalidad municipal municipalidades servicio servicios cuenta tiene pregunta preguntan'.split())
def toks(s): return {w for w in re.findall(r'[a-zñ]{5,}',sinac(s)) if w not in STOP}
PT=[toks(p) for p in P]
def imp(n): # texto de la página impresa n
    i=n+1
    return PT[i-1] if 1<=i<=len(PT) else set()
out=[]
for fs in sorted(glob.glob('/home/claude/libro/*/src/*.md')):
    c=fs.split('/')[-3]; t=open(fs).read()
    for par in t.split('\n\n'):
        for s in re.split(r'(?<=[\.\?!])\s+(?=[A-ZÁÉÍÓÚÑ¿])',par):
            for m in re.finditer(r'\[\[O:IGSMF:p\. (\d+)!?\]\]',s):
                n=int(m.group(1))
                pre=s[:m.start()]; seg=re.split(r'\]\]',pre)[-1]  # trozo de la oración que precede a la cita
                a=toks(re.sub(r'"[^"]*"','',seg)) or toks(seg)
                if len(a)<2: continue
                sc={k:len(a&imp(k))/len(a) for k in (n-1,n,n+1)}
                best=max(sc,key=sc.get)
                if best!=n and sc[best]>sc[n]+0.15:
                    out.append((c,n,best,round(sc[n],2),round(sc[best],2),seg.strip()[-150:]))
for o in out: print('\t'.join(map(str,o)))
print('posibles desfases:',len(out))
