import json,sys,re
from docx import Document
from docx.oxml.ns import qn
def norm(s): return re.sub(r'\s+',' ',s).strip()
def elems(d):
    L=[]
    for e in d.element.body:
        tag=e.tag.split('}')[1]
        txt=norm(''.join(t.text or '' for t in e.iter(qn('w:t'))))
        sty=''
        if tag=='p':
            s=e.find(qn('w:pPr')+'/'+qn('w:pStyle')); sty=s.get(qn('w:val')) if s is not None else ''
        ext=e.findall('.//'+qn('wp:extent'))
        fig=bool(ext) and (tag=='tbl' or sty=='CaptionedFigure')
        h=max((int(x.get('cy')) for x in ext),default=0)
        L.append(dict(e=e,tag=tag,txt=txt,sty=sty,fig=fig,h=h,brk=e.find('.//'+qn('w:pageBreakBefore')) is not None))
    return L
def localiza(L,gaps):
    cur=0; out=[]
    for g in gaps:
        sn=norm(g['snip'])[:40]; j=None
        for k in range(cur,len(L)):
            if sn and sn in L[k]['txt']: j=k; break
        if j is None: out.append((g,None,'no hallado')); continue
        cur=j
        f=next((k for k in range(j+1,min(j+4,len(L))) if L[k]['fig']),None)
        if f is None: out.append((g,None,'sin figura')); continue
        nxt=L[f+1] if f+1<len(L) else None
        ok=L[f]['txt'].startswith(norm(g['sig'])[:20]) or (nxt and nxt['txt'].startswith(norm(g['sig'])[:20]))
        if L[f]['brk'] or (nxt and nxt['brk'] and not L[f]['txt']): out.append((g,f,'apertura')); continue
        out.append((g,f,'ok' if ok else 'sig≠'))
    return out
if __name__=='__main__':
    d=Document(sys.argv[1]); L=elems(d); gaps=json.load(open(sys.argv[2]))
    for g,f,st in localiza(L,gaps):
        h=L[f]['h']/914400*2.54 if f is not None else 0
        print(g['p'],g['gap'],st,f, L[f]['tag'] if f is not None else '', round(h,1),'cm |',g['sig'][:45])
