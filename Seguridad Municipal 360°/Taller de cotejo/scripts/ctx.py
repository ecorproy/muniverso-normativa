import re,sys
def norm(t):
    t=re.sub(r'\s+',' ',t)
    t=re.sub(r' ?([áéíóúñüÁÉÍÓÚÑÜ]) ?',r'\1',t)
    return t
f,pat=sys.argv[1],sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 250; k=int(sys.argv[4]) if len(sys.argv)>4 else 2
t=norm(open(f,encoding='utf-8').read())
ms=list(re.finditer(pat,t,re.I)); print(f'[{f}] {len(ms)} hits')
for m in ms[:k]: print('...',t[max(0,m.start()-n):m.end()+n],'...\n')
