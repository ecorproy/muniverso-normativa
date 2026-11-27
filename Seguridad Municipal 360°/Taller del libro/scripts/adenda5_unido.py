import sys
c,r,out=sys.argv[1:4]
c=open(c,encoding='utf-8').read(); r=open(r,encoding='utf-8').read()
l=c.split('\n',1)
open(out,'w',encoding='utf-8').write(l[0]+'\n\nNov 26, 2026 · @Edward Cortés García\n'+l[1]+'\n'+r)
