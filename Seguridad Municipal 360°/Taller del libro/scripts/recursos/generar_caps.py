import sys,re,json,subprocess,math
sys.path.insert(0,'/home/claude/figuras'); sys.path.insert(0,'/home/claude/recursos')
from svglib import *
from generar import SEC
R='/home/claude/recursos/'; L='/home/claude/libro/'
def png(s,n):
    p=R+f'svg/{n}.svg'; s.save(p); subprocess.run(['rsvg-convert','-w','2100',p,'-o',R+f'png/{n}.png'],check=True)
def icono(s,q,cx,cy,r,c,fill='white'):
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')
    k=r/40
    if q==1:  # corazón
        s.add(f'<path transform="translate({cx-18*k*1.1},{cy-14*k*1.1}) scale({k*1.1})" d="M0,10 C0,-4 18,-6 18,8 C18,-6 36,-4 36,10 C36,24 18,30 18,38 C18,30 0,24 0,10Z" fill="{c}"/>')
    if q==2:  # balanza
        s.add(f'<g stroke="{c}" stroke-width="{3.2*k}" fill="none" stroke-linecap="round"><line x1="{cx}" y1="{cy-22*k}" x2="{cx}" y2="{cy+20*k}"/><line x1="{cx-22*k}" y1="{cy-14*k}" x2="{cx+22*k}" y2="{cy-14*k}"/><line x1="{cx-12*k}" y1="{cy+20*k}" x2="{cx+12*k}" y2="{cy+20*k}"/></g>')
        for sx in (-1,1): s.add(f'<path d="M{cx+sx*22*k-11*k},{cy+2*k} Q{cx+sx*22*k},{cy+14*k} {cx+sx*22*k+11*k},{cy+2*k} Z" fill="{c}"/><line x1="{cx+sx*22*k}" y1="{cy-14*k}" x2="{cx+sx*22*k-9*k}" y2="{cy+2*k}" stroke="{c}" stroke-width="{2*k}"/><line x1="{cx+sx*22*k}" y1="{cy-14*k}" x2="{cx+sx*22*k+9*k}" y2="{cy+2*k}" stroke="{c}" stroke-width="{2*k}"/>')
    if q==3:  # escudo
        s.add(f'<path d="M{cx},{cy-24*k} L{cx+20*k},{cy-16*k} L{cx+20*k},{cy+2*k} Q{cx+20*k},{cy+18*k} {cx},{cy+26*k} Q{cx-20*k},{cy+18*k} {cx-20*k},{cy+2*k} L{cx-20*k},{cy-16*k} Z" fill="{c}"/>')
        s.add(f'<path d="M{cx-8*k},{cy} L{cx-2*k},{cy+7*k} L{cx+10*k},{cy-7*k}" stroke="white" stroke-width="{3.4*k}" fill="none" stroke-linecap="round"/>')
    if q==4:  # hoja
        s.add(f'<path d="M{cx-18*k},{cy+20*k} Q{cx-22*k},{cy-18*k} {cx+22*k},{cy-22*k} Q{cx+20*k},{cy+20*k} {cx-18*k},{cy+20*k} Z" fill="{c}"/>')
        s.add(f'<path d="M{cx-18*k},{cy+20*k} Q{cx},{cy} {cx+14*k},{cy-14*k}" stroke="white" stroke-width="{2.6*k}" fill="none"/>')
CP={1:'CP, art. 21',2:'CP, art. 33',3:'CP, art. 51',4:'CP, art. 50'}
def portada(q):
    info=json.load(open('/home/claude/temas_heads.json',encoding='utf-8'))
    qc,qt,qn=Q[q]
    s=SVG(1200,10)
    s.add(f'<rect x="0" y="0" width="1200" height="230" fill="{qc}"/>')
    icono(s,q,140,115,70,qc)
    text(s,250,95,'CUADRANTE '+qn.split('. ')[0],26,anchor='start',bold=True,fill='white')
    text(s,250,150,qn.split('. ',1)[1],46,anchor='start',bold=True,fill='white')
    text(s,250,192,CP[q]+' · nueve temas',22,anchor='start',italic=True,fill='white')
    y=270
    text(s,40,y,'Las preguntas de este cuadrante',24,anchor='start',bold=True,fill=qc); y+=24
    for n in range((q-1)*9+1,q*9+1):
        t=f't{n:02d}'; tit=info[t]['title'].split('. ',1)[1]
        preg='¿'+[h for h in info[t]['heads'] if h.startswith('Cómo hace')][0]+'?'
        lines=wrap(preg,20,880); rh=36+len(lines)*25+18
        s.add(f'<rect x="30" y="{y}" width="1140" height="{rh}" rx="10" fill="{qt if n%2 else "white"}"/>')
        s.add(f'<circle cx="82" cy="{y+rh/2}" r="30" fill="{qc}"/>'); text(s,82,y+rh/2+10,str(n),28,bold=True,fill='white')
        text(s,140,y+34,tit,24,anchor='start',bold=True,fill=INK)
        text(s,140,y+64,preg,20,anchor='start',italic=True,fill=INK2,width=880,lh=1.25)
        y+=rh+6
    s.h=y+30; png(s,f'cuadrante_{q}')
CAPS={'cap01':('1. La red','¿Por qué un cantón funciona como una red, cómo muere y cómo se recupera?','cap01.md'),
      'cap02':('2. Lo local en el artículo 169','¿Qué han entendido por lo local la Constitución, la ley, los jueces, la Procuraduría y la doctrina?','all.md'),
      'cap03':('3. El concepto','¿Qué es lo local y cómo está organizado este libro para estudiarlo?','cap03.md'),
      'cap04':('4. La persona en el centro','¿Quiénes son las dos personas del núcleo y qué se deben una a la otra?','cap04.md'),
      'conclusion':('Conclusión. Volver al núcleo','¿Qué queda del recorrido y cómo se diagnostica una municipalidad?','conclusion.md')}
def mapa_cap(c):
    tit,preg,f=CAPS[c]
    heads=[h for h in re.findall(r'^## (.+)$',open(L+f'{c}/out/{f}',encoding='utf-8').read(),re.M) if h!='Referencias']
    s=SVG(1200,10)
    s.add(f'<rect x="0" y="0" width="1200" height="78" fill="{AZ}"/>')
    text(s,40,50,'SEGURIDAD MUNICIPAL 360°',22,anchor='start',bold=True,fill='white')
    text(s,1160,54,'CAPÍTULO '+tit.split('.')[0] if c!='conclusion' else '',30,anchor='end',bold=True,fill='white')
    y=140; text(s,40,y,'Mapa del capítulo',22,anchor='start',italic=True,fill=AZ)
    y+=48; h=text(s,40,y,tit.split('. ',1)[1],38,anchor='start',bold=True,width=1100); y+=h+6
    hq=need_h(None,preg,1120,24,25,pad=40)
    box(s,40,y,1120,hq,None,preg,fill=AZt,stroke=AZ,bcol=INK,bfs=25,sw=3)
    text(s,52,y-8,'La pregunta del capítulo',17,anchor='start',bold=True,fill=AZ)
    y+=hq+46; text(s,40,y,'La ruta',24,anchor='start',bold=True); y+=20
    half=(len(heads)+1)//2
    for i,h in enumerate(heads):
        col=0 if i<half else 1; row=i if i<half else i-half
        x=40+col*570; yy=y+row*52
        s.add(f'<circle cx="{x+22}" cy="{yy+24}" r="19" fill="{AZ}"/>'); text(s,x+22,yy+31,str(i+1),19,bold=True,fill='white')
        text(s,x+56,yy+32,h,22,anchor='start',width=490)
    s.h=y+half*52+40; png(s,f'{c}_mapa')
def sintesis(n,titulo,centro,items):
    s=SVG(1200,10)
    text(s,40,56,'Lo esencial',22,anchor='start',italic=True,fill=AZ)
    text(s,40,100,titulo,32,anchor='start',bold=True,width=1120)
    k=len(items); cx=600; Rx=300 if k<=5 else 410; Ry=300 if k<=5 else 330; cy=150+Ry+90; R_=Ry
    s.add(f'<circle cx="{cx}" cy="{cy}" r="118" fill="{TEt}" stroke="{TE}" stroke-width="5"/>')
    text(s,cx,cy-8,centro[0],30,bold=True,fill=TE); text(s,cx,cy+28,centro[1],20,italic=True,fill=INK2,width=200)
    for i,(t,b,c,ct) in enumerate(items):
        a=math.radians(-90+i*360/k); x=cx+Rx*math.cos(a); y=cy+Ry*math.sin(a)
        s.add(f'<line x1="{cx+118*math.cos(a):.0f}" y1="{cy+118*math.sin(a):.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{c}" stroke-width="3"/>')
        w=330 if k<=5 else 300; h=need_h(t,b,w,22,19,pad=26)
        box(s,x-w/2,y-h/2,w,h,t,b,fill=ct,stroke=c,tcol=c,tfs=22,bfs=19)
    s.h=cy+Ry+110; png(s,n)
if __name__=='__main__':
    for q in (1,2,3,4): portada(q)
    for c in CAPS: mapa_cap(c)
    sintesis('cap02_sintesis','La regla que deja el artículo 169',('Lo local','en el artículo 169'),[
      ('Reserva','constitucional de materia a favor del Gobierno Municipal',AZ,AZt),
      ('Sin lista','es genérica: la precisan la ley y, a falta de ella, el examen de cada caso',AM,AMt),
      ('Convive','con las competencias nacionales en el mismo territorio, por coordinación',VE,VEt),
      ('No se vacía','ni puede dejar a los habitantes de un cantón en inferioridad',RO,ROt),
      ('Capacidad','real y técnica; su falta no extingue el deber, y es el criterio para trasladarla por ley',GR,GRt)])
    sintesis('cap03_sintesis','Qué es lo local',('Lo local','la persona del cantón'),[
      ('Importa','de manera directa e inmediata a las personas que viven en el cantón',TE,TEt),
      ('Se conoce','mirando la necesidad concreta de cada persona',TE,TEt),
      ('Reservada','al Gobierno Municipal: originaria, genérica y obligatoria',AZ,AZt),
      ('Se cumple','cuando el servicio llega y la persona recibe lo que necesitaba',TE,TEt),
      ('Se precisa','por la ley o por el examen de cada caso: lo hace la municipalidad, lo revisa el juez',AM,AMt),
      ('Se coordina','con lo nacional: insta a la otra institución y lleva a la persona hasta ella',VE,VEt),
      ('Requiere capacidad','real y técnica; su falta no quita la titularidad ni el deber',GR,GRt)])
    print('ok')
