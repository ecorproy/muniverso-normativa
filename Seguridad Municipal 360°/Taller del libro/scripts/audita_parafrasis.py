# Cribado de paráfrasis: compara cada oración que cita un artículo (sin cita textual) con el texto del artículo.
import re,sys,glob,unicodedata,collections,os
src=open('/home/claude/mis_scripts/build_libro.py').read().replace('\nmain()\n','\n')
os.environ.setdefault('SRC','/home/claude/libro/cap01/src'); os.environ.setdefault('OUT','/tmp/x')
g={'__name__':'bl'}; exec(compile(src,'bl','exec'),g)
STOP=set('el la los las de del y a en que por con para un una se su sus lo al o no es son como más ser sin sobre entre cuando también ya le les debe puede este esta esto ese esa cada otra otro donde quien ley artículo municipalidad municipal municipalidades código'.split())
def toks(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(ch for ch in s if unicodedata.category(ch)!='Mn')
    return {w for w in re.findall(r'[a-zñ]{4,}',s) if w not in STOP}
res=[]
for f in sorted(glob.glob('/home/claude/libro/*/src/*.md')):
    c=f.split('/')[-3]; t=open(f).read()
    for par in t.split('\n\n'):
        if par.startswith(('|','#','<?')): continue
        for s in re.split(r'(?<=[\.\?!])\s+(?=[A-ZÁÉÍÓÚÑ¿])',par):
            if '"' in s: continue
            for m in re.finditer(r'\[\[(L|CP|DE):([^\]]+)\]\]',s):
                mac=m.group(0)[2:-2]; p=mac.split(':')
                try: su=g['source_units'](macro=mac)
                except Exception as e: continue
                if not su: continue
                tipo,units,full=su
                loc=p[-1]; mm=re.search(r'art\.\s*(\d+(?:\s*bis|\s*ter)?)',loc)
                if not mm: continue
                want=re.sub(r'\s+',' ',mm.group(1))
                txt=' '.join(u for lab,u in units if lab==want)
                if not txt: res.append((0,c,mac,'ARTÍCULO NO HALLADO',s[:200])); continue
                frase=re.sub(r'\[\[[^\]]+\]\]','',s)
                a=toks(frase)
                bt=unicodedata.normalize('NFD',txt.lower()); bt=''.join(ch for ch in bt if unicodedata.category(ch)!='Mn')
                if not a: continue
                ov=sum(1 for w in a if w[:6] in bt)/len(a)
                res.append((ov,c,mac,'',frase[:220]))
res.sort(key=lambda x:x[0])
print('oraciones con paráfrasis de artículo:',len(res))
print('no hallados:',sum(1 for r in res if r[3]))
for r in res[:60]: print(f'{r[0]:.2f}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}')
