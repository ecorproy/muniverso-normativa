import sys,json,re,difflib,unicodedata
sys.path.insert(0,'/home/claude/division')
from indices import lee
from docx import Document
from collections import defaultdict
def nz(s): return re.sub(r'\s+',' ',unicodedata.normalize('NFC',s)).strip().lower()
def carga(docx='/home/claude/Seguridad Municipal 360 (final76).docx'):
    D=json.load(open('/home/claude/division/fuentes.json'))
    U=defaultdict(set)
    for a in D['apariciones']:
        if not a['fuente'].startswith('RECURSO'): U[a['fuente']].add(D['etiquetas'][a['unidad']])
    R=lee(list(Document(docx).element.body))
    return D,U,R
CAT={'Constitución':['CP'],'Leyes':['L'],'Decretos ejecutivos':['DE'],'Reglamentos y políticas municipales':['RM'],'Reglamentos de otras instituciones':['RM','DE','L'],
 'Procuraduría General de la República':['D'],'Sala Constitucional':['V'],'Otros tribunales':['T','J'],'Contraloría General de la República':['O'],
 'Sala Primera':['S1'],'Jurisprudencia extranjera':['M'],None:['M','O']}
def empareja(D,U,R):
    refs=D['referencias']; usado=defaultdict(list); par=[]
    for ind,cat,i,nombre,uni in R:
        tipos=CAT.get(cat,list({k.split(':')[0] for k in U}))
        cands=[f for f in U if f.split(':')[0] in tipos]
        n=nz(nombre)
        ids=re.findall(r'\d{4}-\d{6}|[A-Z]{1,3}-\d{2,4}-\d{4}|N\.° [\d.]+|\d{3,}',nombre)
        def score(f):
            r=nz(refs.get(f,''))
            s=difflib.SequenceMatcher(None,n,r[:len(n)+40]).ratio()
            if ids and all(nz(x) in r for x in ids): s+=1
            s+=0.5*len(U[f]&set(uni))/max(1,len(U[f]|set(uni)))
            return s
        best=max(cands,key=score) if cands else None
        par.append((ind,cat,i,nombre,uni,best,score(best) if best else 0))
        usado[best].append(i)
    return par,usado
if __name__=='__main__':
    D,U,R=carga(); par,usado=empareja(D,U,R)
    dif=[(p[3][:70],p[5],sorted(set(p[4])^U[p[5]])) for p in par if set(p[4])!=U[p[5]]]
    print('entradas',len(par),'con unidades distintas',len(dif))
    for x in dif[:40]: print(x)
    print('fuentes no indexadas',[f for f in U if f not in usado][:40])
    print('fuentes con dos entradas',{f:v for f,v in usado.items() if len(v)>1})
