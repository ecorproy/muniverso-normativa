import re,sys,os
L=int(os.environ.get('L','650'))
f=sys.argv[1]; arts=sys.argv[2:]
t=open(f,encoding='utf-8').read()
print('## '+os.path.basename(f))
for a in arts:
    m=re.search(r'(?im)^\W{0,6}(ART[IÍ]CULO|Artículo)\s+'+re.escape(a)+r'\b\s*[\.\-—–:º°o*]', t)
    if not m: print(f'  art {a}: NO HALLADO'); continue
    nxt=re.search(r'(?im)^\W{0,6}(ART[IÍ]CULO|Artículo)\s+\d', t[m.end():])
    body=t[m.start(): m.end()+(nxt.start() if nxt else 2500)]
    body=re.sub(r'\s+',' ',body).strip()
    print(f'  art {a}: '+body[:L]+('…' if len(body)>L else ''))
