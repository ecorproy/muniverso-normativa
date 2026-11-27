"""Planifica (acumulando) operaciones para cerrar huecos causados por figuras."""
import json,sys,math
sys.path.insert(0,'/home/claude/adenda_scripts')
from figuras_hueco import elems,localiza
from docx import Document
from docx.oxml.ns import qn
PAG=22.9; LIN=0.6; ESP=0.21; CPL=92
docx,gj=sys.argv[1],sys.argv[2]
d=Document(docx); L=elems(d); gaps=json.load(open(gj))
OP='/home/claude/adenda_scripts/huecos_ops.json'; ops=json.load(open(OP))
def alto(x): return math.ceil(max(1,len(x['txt']))/CPL)*LIN+ESP
def es_texto(x): return x['tag']=='p' and not x['fig'] and x['sty'] in ('BodyText','FirstParagraph','Compact','BlockText')
for g,f,st in localiza(L,gaps):
    if f is None or st=='apertura' or (g['sig'][:2].rstrip('.').isdigit() and st!='ok' and L[f]['tag']!='tbl'): continue
    x=L[f]; k=x['e'].find('.//'+qn('a:blip')).get(qn('r:embed')); op=ops.setdefault(k,{})
    gap=g['gap']*PAG; h=x['h']/914400*2.54+(1.4 if x['tag']=='tbl' else 0.3)+0.4
    if h<=gap+0.5 or (h*0.85<=gap and 'escala' not in op):
        op['escala']=round(min(0.97,op.get('escala',1)*max(0.8,(gap-0.6)/h)),3); print(g['p'],'escala',op['escala']); continue
    cum=0;n=0;j=f+1
    while j<len(L) and es_texto(L[j]) and cum+alto(L[j])<=gap: cum+=alto(L[j]); n+=1; j+=1
    if n and gap-cum<0.25*PAG: op['mov']=op.get('mov',0)+n; print(g['p'],'mov +',n,'→',op['mov']); continue
    cum=0;n=0;j=f-1
    while j>=0 and es_texto(L[j]) and n<4 and gap+cum<h: cum+=alto(L[j]); n+=1; j-=1
    if gap+cum>=h: op['mov']=op.get('mov',0)-n; print(g['p'],'mov -',n,'→',op['mov']); continue
    s=round(max(0.75,(gap+cum-0.6)/h),3); op['escala']=round(op.get('escala',1)*s,3); op['mov']=op.get('mov',0)-n
    print(g['p'],'mov -',n,'+ escala',op['escala'])
json.dump({k:v for k,v in ops.items() if v},open(OP,'w'),indent=1)
