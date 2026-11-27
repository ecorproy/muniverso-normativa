"""Emparejamiento estricto fuente ↔ entrada de índice, por título o número distintivo."""
import re,unicodedata,sys
sys.path.insert(0,'/home/claude/division')
from empareja import carga
def nz(s): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip()
def claves(f,ref):
    k=f.split(':')[0]; out=[]
    m=re.search(r'\*([^*]+)\*',ref)
    if k in ('V','S1','T','J'):
        out+=re.findall(r'\d{4}-\d{6}|\d{2,4}-\d{4}(?:-[A-Z]+)?|N\.° [\d-]+',ref)[:2]
    if k=='D': out.append(f.split(':')[1])
    if k=='L': out.append('Ley N.° '+f.split(':')[1]+',')
    if k=='DE': out.append('N.° '+f.split(':')[1])
    if k=='O':
        mm=re.search(r'N\.° ?\d+',ref); 
        if mm: out.append(mm.group(0))
    if m: out.append(m.group(1).rstrip('.'))
    if k=='M': out.append(ref.split('(')[0].strip().rstrip('.,'))
    return [nz(x) for x in out if x and len(nz(x))>3]
def empareja_estricto():
    D,U,R=carga(); refs=D['referencias']
    ent=[(i,nz(nombre),set(uni or []),nombre) for ind,cat,i,nombre,uni in R]
    asign={}; libres=set(e[0] for e in ent)
    pares=[]
    for f in U:
        for c in claves(f,refs.get(f,'')):
            for i,n,us,nombre in ent:
                if c in n: pares.append((len(c),f,i))
    for L,f,i in sorted(pares,reverse=True):
        if f in asign or i not in libres: continue
        asign[f]=i; libres.discard(i)
    E={e[0]:e for e in ent}
    return D,U,R,asign,libres,E
if __name__=='__main__':
    D,U,R,asign,libres,E=empareja_estricto()
    sin=[f for f in U if f not in asign]
    dif=[(f,E[i][3][:60],sorted(E[i][2]-U[f]),sorted(U[f]-E[i][2])) for f,i in asign.items() if E[i][2]!=U[f]]
    print('emparejadas',len(asign),'entradas sin fuente',len(libres),'fuentes sin entrada',len(sin))
    print('SIN ENTRADA:',sin)
    print('ENTRADAS LIBRES:',[E[i][3][:80] for i in libres])
    print('DIFERENCIAS (sobra en índice / falta en índice):')
    for x in dif: print(' ',x)
