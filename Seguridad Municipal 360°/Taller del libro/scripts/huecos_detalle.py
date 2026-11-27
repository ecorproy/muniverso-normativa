"""Para cada página con hueco >30 % seguida de una figura a mitad de sección,
devuelve página, fracción en blanco y el texto que abre la página siguiente."""
import sys,subprocess,os,glob,json
from PIL import Image
pdf=sys.argv[1]; d=pdf+'_r'
if not glob.glob(d+'/*.png'):
    os.makedirs(d,exist_ok=True); subprocess.run(['pdftoppm','-r','12','-gray','-png',pdf,d+'/p'],check=True)
res=[]
for f in sorted(glob.glob(d+'/*.png')):
    im=Image.open(f).convert('L'); w,h=im.size; px=im.load()
    top=int(h*0.09); bot=int(h*0.91); last=top
    for y in range(top,bot):
        if any(px[x,y]<200 for x in range(int(w*.1),int(w*.9))): last=y
    res.append((bot-last)/(bot-top))
out=[]
for i,r in enumerate(res):
    p=i+1
    if r<=0.30 or p+1>len(res): continue
    t=subprocess.run(['pdftotext','-f',str(p),'-l',str(p),pdf,'-'],capture_output=True,text=True).stdout
    t2=subprocess.run(['pdftotext','-f',str(p+1),'-l',str(p+1),pdf,'-'],capture_output=True,text=True).stdout
    lines=[x.strip() for x in t.split('\n') if len(x.strip())>30]
    sig=next((x.strip() for x in t2.split('\n') if x.strip()),'')
    out.append({'p':p,'gap':round(r,3),'sig':sig,'snip':lines[-1] if lines else ''})
json.dump(out,open(pdf+'_gaps.json','w'),ensure_ascii=False,indent=0)
print(len(out))
