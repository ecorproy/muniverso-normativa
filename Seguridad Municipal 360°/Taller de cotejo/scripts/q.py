import re,sys
def norm(t):
    t=re.sub(r'[ \t]+',' ',t)
    t=re.sub(r' ?([áéíóúñüÁÉÍÓÚÑÜ]) ?',r'\1',t)  # artifact fix (may over-join)
    return t
f=sys.argv[1]; phrases=sys.argv[2:]
raw=open(f,encoding='utf-8').read()
t=norm(raw)
heads=[(m.start(),m.group(1)) for m in re.finditer(r'(?m)^\W{0,4}([IVXL]{1,6})\s*\.?\s*[\-–—\.]\s*\S',t)]
pt=re.search(r'(?i)por tanto',t)
for p in phrases:
    pn=norm(p); i=t.find(pn)
    if i<0:
        i2=re.sub(r'\s+',' ',t).find(re.sub(r'\s+',' ',pn))
        print('NO HALLADO:',p[:70]); continue
    h=[x for x in heads if x[0]<i]
    cons=h[-1][1] if h else '?'
    inpt = pt and i>pt.start()
    lit = p in re.sub(r'[ \t]+',' ',raw).replace('\n',' ')
    print(f'OK cons={cons}{" (por tanto)" if inpt else ""} literal_raw={lit} :: {p[:90]}')
