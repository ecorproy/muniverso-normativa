import re,sys
f=sys.argv[1]; arts=sys.argv[2:]
t=open(f,encoding='utf-8').read()
for a in arts:
    m=re.search(r'(?im)^\s*\**\s*(ART[IÍ]CULO|Artículo)\s+'+re.escape(a)+r'\s*[\.\-—–:º°o]', t)
    if not m: print(f'## {a}: NO HALLADO'); continue
    nxt=re.search(r'(?im)^\s*\**\s*(ART[IÍ]CULO|Artículo)\s+\d', t[m.end():])
    body=t[m.start(): m.end()+(nxt.start() if nxt else 1500)]
    print(f'## {a}\n'+re.sub(r'\n\s*\n+','\n',body.strip())[:1400]+'\n')
