"""Lee las listas de referencias impresas en el DOCX, por unidad, y las cruza con las fuentes de la matriz."""
import sys,re,json,difflib,unicodedata
sys.path.insert(0,'/home/claude/division')
from docx import Document
from docx.oxml.ns import qn
from unidades_docx import mapa,T,S
def nz(s): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',s.replace('*','')).encode('ascii','ignore').decode().lower()).strip()
def listas(docx):
    els=list(Document(docx).element.body); M=mapa(els); out=[]; en=None
    for e,u in zip(els,M):
        st,t=S(e),T(e)
        if st.startswith('Heading'):
            en = u if t=='Referencias' else None; continue
        if en and t.strip() and en==u: out.append((u,t.strip()))
    return out
if __name__=='__main__':
    D=json.load(open('fuentes.json')); refs={k:v for k,v in D['referencias'].items() if not k.startswith('RECURSO')}
    idx={nz(v)[:120]:k for k,v in refs.items()}
    claves=list(idx)
    L=listas('/home/claude/Seguridad Municipal 360 (final76).docx')
    nuevas={}; extra=[]; nomatch=0
    for u,t in L:
        n=nz(t)[:120]
        k=idx.get(n)
        if not k:
            c=difflib.get_close_matches(n,claves,n=1,cutoff=0.9)
            k=idx[c[0]] if c else None
        if not k:
            k='R:'+re.sub(r'\W+','-',t[:40]).strip('-'); nuevas[k]=t; nomatch+=1
        extra.append(dict(fuente=k,unidad=u,texto=t))
    json.dump(dict(listas=extra,nuevas=nuevas),open('refs_docx.json','w'),ensure_ascii=False,indent=0)
    print('entradas impresas',len(L),'sin fuente en la matriz',nomatch)
    for k,v in list(nuevas.items())[:40]: print(' ',k,'|',v[:110])
