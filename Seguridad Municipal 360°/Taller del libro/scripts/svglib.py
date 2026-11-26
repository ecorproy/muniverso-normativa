import html
FONT='DejaVu Serif, serif'
class SVG:
    def __init__(s,w,h): s.w,s.h=w,h; s.o=[]
    def add(s,x): s.o.append(x)
    def save(s,p):
        head=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}" font-family="{FONT}">'
              '<defs><marker id="ar" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto" markerUnits="userSpaceOnUse">'
              '<path d="M0,0 L14,7 L0,14 Z" fill="#111"/></marker></defs><rect width="100%" height="100%" fill="white"/>')
        open(p,'w',encoding='utf-8').write(head+'\n'.join(s.o)+'</svg>')
def wrap(t,fs,width):
    maxc=max(4,int(width/(fs*0.56)))
    out=[]
    for para in t.split('\n'):
        line=''
        for w in para.split(' '):
            if len(line)+len(w)+(1 if line else 0)>maxc and line: out.append(line); line=w
            else: line=(line+' '+w) if line else w
        out.append(line)
    return out
def text(s,x,y,t,fs=26,anchor='middle',width=10000,bold=False,italic=False,fill='#111',lh=1.25):
    lines=wrap(t,fs,width); w='bold' if bold else 'normal'; st='italic' if italic else 'normal'
    for i,l in enumerate(lines):
        s.add(f'<text x="{x:.1f}" y="{y+i*fs*lh:.1f}" font-size="{fs}" font-weight="{w}" font-style="{st}" text-anchor="{anchor}" fill="{fill}">{html.escape(l)}</text>')
    return len(lines)*fs*lh
def box(s,x,y,w,h,title=None,body=None,fill='white',stroke='#111',sw=3,r=14,tfs=27,bfs=22,dash=None,center=True):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    lines_t=wrap(title,tfs,w-30) if title else []; lines_b=wrap(body,bfs,w-30) if body else []
    tot=len(lines_t)*tfs*1.2+(10 if title and body else 0)+len(lines_b)*bfs*1.25
    yy=y+(h-tot)/2+tfs*0.85 if center else y+tfs+12
    cx=x+w/2
    if title: yy+=text(s,cx,yy,title,tfs,width=w-30,bold=True,lh=1.2)+ (10 if body else 0)
    if body: text(s,cx,yy-(0 if title else 0)+(bfs*0.1 if title else 0),body,bfs,width=w-30,fill='#333')
def need_h(title,body,w,tfs=27,bfs=22,pad=36):
    lt=len(wrap(title,tfs,w-30)) if title else 0; lb=len(wrap(body,bfs,w-30)) if body else 0
    return lt*tfs*1.2+lb*bfs*1.25+(10 if title and body else 0)+pad
def arrow(s,x1,y1,x2,y2,sw=3,dash=None,label=None,fs=21,lx=None,ly=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="{sw}" marker-end="url(#ar)"{d}/>')
    if label: text(s,lx if lx is not None else (x1+x2)/2+8, ly if ly is not None else (y1+y2)/2,label,fs,anchor='start',italic=True,fill='#333')
def path(s,d,sw=3,arrowend=True,dash=None):
    m=' marker-end="url(#ar)"' if arrowend else ''; da=f' stroke-dasharray="{dash}"' if dash else ''
    s.add(f'<path d="{d}" fill="none" stroke="#111" stroke-width="{sw}"{m}{da}/>')
def diamond(s,cx,cy,w,h,t,fs=22):
    s.add(f'<polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}" fill="#f2f2f2" stroke="#111" stroke-width="3"/>')
    lines=wrap(t,fs,w*0.62); y0=cy-(len(lines)-1)*fs*1.2/2+fs*0.35
    text(s,cx,y0,t,fs,width=w*0.62,lh=1.2)
