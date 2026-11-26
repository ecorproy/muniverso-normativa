# Inserta las figuras en libro.md antes de pandoc. Uso: python3 -I figuras.py libro.md
import sys
p=sys.argv[1]; L=open(p,encoding='utf-8').read().split('\n')
fig='![Figura 1. La célula: el cantón visto desde las dos personas del núcleo.](/home/claude/figuras/celula.png){width=15cm}'
if fig not in L:
    i=L.index('### Una célula'); L[i+1:i+1]=['',fig]
open(p,'w',encoding='utf-8').write('\n'.join(L))
