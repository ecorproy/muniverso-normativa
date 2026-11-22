# cons.py FILE            -> lista de encabezados
# cons.py FILE VII [kw]   -> texto del considerando VII (si kw, ventana alrededor)
import re,sys,os
L=int(os.environ.get('L','1500'))
f=sys.argv[1]; raw=open(f,encoding='utf-8').read()
def fix(t):
    t=re.sub(r'(?<=\w) ([áéíóúñüÁÉÍÓÚÑÜ]) (?=\w)',r'\1',t)
    return re.sub(r'(?<=\w) ([áéíóú])(?=[\s,.;:)])',r'\1',t)
ci=[m.start() for m in re.finditer(r'(?im)^\W{0,6}considerando\s*:?\s*$',raw)]
start=ci[-1] if ci else raw.find('Texto de la resoluci')
hs=[(m.start(),m.group(1)) for m in re.finditer(r'(?m)^\W{0,6}([IVXL]{1,7})\)?\s*\.?\s*[-–—.]+\s*\S',raw) if m.start()>=start]
pt=[m.start() for m in re.finditer(r'(?im)^\W{0,6}por tanto\s*:?',raw) if m.start()>=start]
end=pt[-1] if pt else len(raw)
print('## '+os.path.basename(f)+f'  (considerandos desde {start}, por tanto en {end})')
if len(sys.argv)==2:
    for p,h in hs:
        if p<end: print('  ',h,'|',fix(re.sub(r'\s+',' ',raw[p:p+110])))
    print('   POR TANTO |',fix(re.sub(r'\s+',' ',raw[end:end+900])))
else:
    r=sys.argv[2]; kw=sys.argv[3] if len(sys.argv)>3 else None
    for i,(p,h) in enumerate(hs):
        if h==r and p<end:
            q=hs[i+1][0] if i+1<len(hs) else end
            seg=fix(re.sub(r'\s+',' ',raw[p:min(q,end)]))
            if kw:
                for m in list(re.finditer(kw,seg,re.I))[:2]:
                    print('  …'+seg[max(0,m.start()-L//2):m.end()+L//2]+'…\n')
            elif os.environ.get('TAIL'): print('  …'+seg[-L:])
            else: print('  '+seg[:L]+(' …' if len(seg)>L else ''))
            break
    else: print('   no hallado',r)
