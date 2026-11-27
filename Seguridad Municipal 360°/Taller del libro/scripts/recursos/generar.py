import sys,re,glob,importlib.util,json,html
sys.path.insert(0,'/home/claude/figuras')
from svglib import *
import segno
R='/home/claude/recursos/'; L='/home/claude/libro/'
D={}
for f in sorted(glob.glob(R+'datos_*.py')):
    sp=importlib.util.spec_from_file_location('d',f); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    D.update({k:v for k,v in m.D.items() if v})
ACT={'P':(TE,'Persona o comunidad'),'M':(AZ,'Municipalidad'),'S':(VI,'Sala o tribunal'),'G':(PE,'Procuraduría'),'C':(AM,'Contraloría'),'O':(GR,'Otra institución')}
SEC={'caso':(TE,'El caso'),'des':(AZ,'Normas y casos'),'din':(AM,'Con qué se paga'),'como':(VE,'Cómo lo hace'),'med':(GR,'Lo que hoy se mide'),'con':(AZ,'Conclusión')}
def tipo(h):
    if h=='El caso': return 'caso'
    if h.startswith('Con qué se paga'): return 'din'
    if h.startswith('Cómo hace'): return 'como'
    if h.startswith('Lo que hoy se mide'): return 'med'
    if h.startswith('Conclusión'): return 'con'
    return 'des'
def fuente_caso(t):
    src=open(glob.glob(L+f'{t}/src/*.md')[0],encoding='utf-8').read()
    caso=re.split(r'\n(?=## )',src)
    caso=[x for x in caso if x.startswith('## El caso')][0]
    refs=open(f'/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos/{t}/out/zz_referencias.md',encoding='utf-8').read().split('\n\n')
    for m in re.finditer(r'\[\[(V|S1|T|D|L|DE|RM|O):([^:\]]+)',caso):
        k,c=m.groups()
        code={'V':c,'S1':c.split('-')[0] if False else c,'T':c,'D':c}.get(k)
        if not code: continue
        key=code if k!='S1' else code
        for r in refs:
            if (key in r or key.replace('-','-F-S1-') in r) and 'http' in r:
                url=re.search(r'https?://\S+',r).group(0).rstrip('.')
                lab={'V':'Voto '+c,'S1':'Sala Primera, '+c,'T':'TCA, '+c,'D':'Dictamen '+c}[k]
                return url,lab
    for m in re.finditer(r'\[\[(V|S1|T):([^:\]]+)',caso):
        k,c=m.groups()
        fs=glob.glob(f'/home/claude/repo/main/**/Sentencia {c}.md',recursive=True)+glob.glob(f'/home/claude/repo/main/**/*{c}*.md',recursive=True)
        for f in fs:
            mm=re.search(r'^enlace: "(https?://[^"]+)"',open(f,encoding='utf-8').read(),re.M)
            if mm: return mm.group(1),{'V':'Voto '+c,'S1':'Sala Primera, '+c,'T':'TCA, '+c}[k]
        break
    return None,None
def qr_svg(s,url,x,y,size):
    q=segno.make(url,error='m'); mat=list(q.matrix); n=len(mat); cell=size/(n+8)
    s.add(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="white" stroke="{GR}" stroke-width="2" rx="8"/>')
    for i,row in enumerate(mat):
        for j,v in enumerate(row):
            if v: s.add(f'<rect x="{x+(j+4)*cell:.2f}" y="{y+(i+4)*cell:.2f}" width="{cell+0.05:.2f}" height="{cell+0.05:.2f}" fill="{INK}"/>')
def banda(s,qn,n,txt,W=1200):
    qc,qt,qnom=Q[qn]
    s.add(f'<rect x="0" y="0" width="{W}" height="78" fill="{qc}"/>')
    text(s,40,50,('CUADRANTE '+qnom).upper(),22,anchor='start',bold=True,fill='white')
    text(s,W-40,54,txt,30,anchor='end',bold=True,fill='white')
def mapa(t,info):
    n=int(t[1:]); qn=cuadrante(n); qc,qt,_=Q[qn]
    s=SVG(1200,10); banda(s,qn,n,f'TEMA {n}')
    titulo=info['title'].split('. ',1)[1]
    y=140; text(s,40,y,'Mapa del tema',22,anchor='start',italic=True,fill=qc)
    y+=48; h=text(s,40,y,titulo,38,anchor='start',bold=True,width=760); y+=h+6
    preg=[x for x in info['heads'] if x.startswith('Cómo hace')][0]
    preg='¿'+preg+'?'
    hq=need_h(None,preg,760,24,25,pad=40)
    box(s,40,y,760,hq,None,preg,fill=qt,stroke=qc,bcol=INK,bfs=25,sw=3)
    text(s,52,y-8,'La pregunta del tema',17,anchor='start',bold=True,fill=qc)
    y+=hq+46
    text(s,40,y,'La ruta',24,anchor='start',bold=True,fill=INK); y+=20
    for i,h in enumerate(info['heads']):
        c,_=SEC[tipo(h)]
        lines=wrap(h,23,680); rh=max(46,len(lines)*29+18)
        s.add(f'<line x1="62" y1="{y+rh/2}" x2="62" y2="{y+rh/2+ (rh if i<len(info["heads"])-1 else 0)}" stroke="#C9CED6" stroke-width="3"/>')
        s.add(f'<circle cx="62" cy="{y+rh/2}" r="19" fill="{c}"/>')
        text(s,62,y+rh/2+7,str(i+1),19,bold=True,fill='white')
        text(s,100,y+rh/2+8-(len(lines)-1)*29/2,h,23,anchor='start',width=680,lh=1.25)
        y+=rh
    yl=y
    # columna derecha: QR y leyenda
    x0=850; yy=150
    url,lab=fuente_caso(t)
    if url:
        qr_svg(s,url,x0+15,yy,290)
        text(s,x0+160,yy+322,'El caso, en la fuente',19,bold=True,fill=TE)
        text(s,x0+160,yy+348,lab,18,fill=INK2,width=300)
        yy+=400
    text(s,x0,yy,'Colores de la ruta',19,anchor='start',bold=True,fill=INK); yy+=18
    for k in ('caso','des','din','como','med','con'):
        c,nom=SEC[k]
        s.add(f'<circle cx="{x0+14}" cy="{yy+16}" r="11" fill="{c}"/>'); text(s,x0+36,yy+23,nom,18,anchor='start',fill=INK2); yy+=36
    s.h=max(yl,yy)+40
    return s
def caso(t,info,ev):
    n=int(t[1:]); qn=cuadrante(n); qc,qt,_=Q[qn]
    s=SVG(1200,10); banda(s,qn,n,f'TEMA {n}')
    y=135; text(s,40,y,'El caso, paso a paso',30,anchor='start',bold=True,fill=TE)
    text(s,40,y+34,info['title'].split('. ',1)[1],21,anchor='start',italic=True,fill=INK2)
    y+=80; x0=250
    top=y
    rows=[]
    for fe,a,tx in ev:
        lines=wrap(tx,23,820); rh=max(64,len(lines)*29+30); rows.append((fe,a,tx,rh))
    tot=sum(r[3] for r in rows)
    s.add(f'<line x1="{x0}" y1="{top+20}" x2="{x0}" y2="{top+tot-rows[-1][3]/2}" stroke="#C9CED6" stroke-width="5"/>')
    for fe,a,tx,rh in rows:
        c,_=ACT[a]; cy=y+rh/2
        text(s,x0-34,cy+7,fe,20,anchor='end',bold=True,fill=INK,width=200)
        s.add(f'<circle cx="{x0}" cy="{cy}" r="17" fill="{c}" stroke="white" stroke-width="4"/>')
        nl=len(wrap(tx,23,820))
        box(s,x0+36,y+8,900,rh-16,None,None,fill='white',stroke=c,sw=2,r=10)
        text(s,x0+56,cy+8-(nl-1)*29/2,tx,23,anchor='start',width=860,lh=1.25)
        y+=rh
    y+=26
    pres=[a for a in 'PMSGCO' if any(e[1]==a for e in ev)]
    x=40
    for a in pres:
        c,nom=ACT[a]
        s.add(f'<circle cx="{x+12}" cy="{y}" r="11" fill="{c}"/>'); text(s,x+30,y+7,nom,18,anchor='start',fill=INK2); x+=40+len(nom)*10.5
    s.h=y+36
    return s
def check(t,info,items):
    n=int(t[1:]); qn=cuadrante(n); qc,qt,_=Q[qn]
    s=SVG(1200,10); banda(s,qn,n,f'TEMA {n}')
    y=135; text(s,40,y,'Revise en su municipalidad',30,anchor='start',bold=True,fill=VE)
    text(s,40,y+34,info['title'].split('. ',1)[1],21,anchor='start',italic=True,fill=INK2)
    y+=70
    for i,it in enumerate(items):
        lines=wrap(it,23,990); rh=len(lines)*29+34
        s.add(f'<rect x="30" y="{y}" width="1140" height="{rh}" rx="10" fill="{VEt if i%2==0 else "white"}"/>')
        s.add(f'<rect x="52" y="{y+rh/2-17}" width="34" height="34" rx="6" fill="white" stroke="{VE}" stroke-width="3"/>')
        text(s,112,y+rh/2+8-(len(lines)-1)*29/2,it,23,anchor='start',width=990,lh=1.25)
        y+=rh+8
    text(s,40,y+30,'Una casilla vacía es una tarea, y a veces un riesgo de condena.',19,anchor='start',italic=True,fill=INK2)
    s.h=y+60
    return s
if __name__=='__main__':
    info=json.load(open('/home/claude/temas_heads.json',encoding='utf-8'))
    import subprocess
    sel=sys.argv[1:] or sorted(D)
    for t in sel:
        for nom,fn in (('mapa',lambda:mapa(t,info[t])),('caso',lambda:caso(t,info[t],D[t]['caso'])),('lista',lambda:check(t,info[t],D[t]['check']))):
            s=fn(); p=R+f'svg/{t}_{nom}.svg'; s.save(p)
            subprocess.run(['rsvg-convert','-w','2100',p,'-o',R+f'png/{t}_{nom}.png'],check=True)
        print(t,'ok')
