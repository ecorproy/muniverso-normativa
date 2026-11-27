"""Mide huecos: fracción en blanco al pie de cada página renderizada."""
import sys,subprocess,os,glob
from PIL import Image
pdf=sys.argv[1]; d=pdf+'_r'; os.makedirs(d,exist_ok=True)
if not glob.glob(d+'/*.png'):
    subprocess.run(['pdftoppm','-r','12','-gray','-png',pdf,d+'/p'],check=True)
res=[]
for f in sorted(glob.glob(d+'/*.png')):
    im=Image.open(f).convert('L'); w,h=im.size; px=im.load()
    top=int(h*0.09); bot=int(h*0.91)   # márgenes aprox.
    last=top
    for y in range(top,bot):
        if any(px[x,y]<200 for x in range(int(w*.1),int(w*.9))): last=y
    res.append((bot-last)/(bot-top))
n=len(res); g=[i+1 for i,r in enumerate(res) if r>0.30]
print('paginas',n,'con hueco >30%:',len(g)); print(g[:80])
