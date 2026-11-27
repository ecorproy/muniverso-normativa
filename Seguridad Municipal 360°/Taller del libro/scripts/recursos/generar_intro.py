import sys,subprocess
sys.path.insert(0,'/home/claude/figuras')
from svglib import *
R='/home/claude/recursos/'
def png(s,n):
    p=R+f'svg/{n}.svg'; s.save(p); subprocess.run(['rsvg-convert','-w','2100',p,'-o',R+f'png/{n}.png'],check=True)
def cabecera(s,sub,tit):
    s.add(f'<rect x="0" y="0" width="1200" height="78" fill="{AZ}"/>')
    text(s,40,50,'SEGURIDAD MUNICIPAL 360°',22,anchor='start',bold=True,fill='white')
    text(s,1160,54,'INTRODUCCIÓN',30,anchor='end',bold=True,fill='white')
    text(s,40,140,sub,22,anchor='start',italic=True,fill=AZ)
    text(s,40,188,tit,38,anchor='start',bold=True)

# ---------- mapa del viaje ----------
EST=[('Bajo tierra','Capítulo 1. La red','Casi nada ocurre solo: un caso toca varios temas a la vez.',VE,VEt),
     ('El texto','Capítulo 2. Lo local en el artículo 169','Lo local es una reserva constitucional sin lista, que se precisa caso por caso.',VI,VIt),
     ('El concepto','Capítulo 3. El concepto','Una definición, una célula y dos personas en su núcleo.',AM,AMt),
     ('La persona','Capítulo 4. La persona en el centro','Qué se deben quien recibe el servicio y quien lo presta.',TE,TEt),
     ('El territorio','Cuatro cuadrantes, treinta y seis temas','Cada tema: el caso, quién manda, normas y jueces, con qué se paga, cómo se hace y qué se mide.',None,GRt),
     ('El regreso','Conclusión. Volver al núcleo','Seis preguntas para diagnosticar una municipalidad, y la séptima.',AZ,AZt)]
def mapa():
    s=SVG(1200,10); cabecera(s,'Mapa del viaje','Seis estaciones, de la red a la persona')
    y=250
    # salida
    s.add(f'<circle cx="600" cy="{y}" r="34" fill="{INK}"/>')
    for dx in (-14,0,14): s.add(f'<path d="M{600+dx},{y-14} q{dx*0.4},14 {dx*0.2},28" stroke="white" stroke-width="4" fill="none" stroke-linecap="round"/>')
    text(s,650,y-4,'Salida',22,anchor='start',bold=True)
    text(s,650,y+24,'Una pregunta, octubre de 2016',20,anchor='start',italic=True,fill=INK2)
    y+=34; top=y; cards=[]
    yy=y+40; w=500
    for i,(et,cap,lleva,c,ct) in enumerate(EST):
        nt=len(wrap(cap,24,w-48)); nb=len(wrap(lleva,20,w-48))
        h=74+nt*30+6+nb*25+26+(4*40+8 if i==4 else 0)
        left=(i%2==0); x=60 if left else 640
        cards.append((x,yy,w,h,et,cap,lleva,c,ct,left,i,nt,nb)); yy+=max(h-60,120)
    end=max(c_[1]+c_[3] for c_ in cards)+150
    s.add(f'<line x1="600" y1="{top}" x2="600" y2="{end-60}" stroke="{GR}" stroke-width="14" stroke-linecap="round"/>')
    s.add(f'<line x1="600" y1="{top}" x2="600" y2="{end-60}" stroke="white" stroke-width="3" stroke-dasharray="16 14"/>')
    for (x,y0,w,h,et,cap,lleva,c,ct,left,i,nt,nb) in cards:
        cc=c or INK; cy=y0+44
        s.add(f'<line x1="{x+w if left else x}" y1="{cy}" x2="600" y2="{cy}" stroke="{cc}" stroke-width="4"/>')
        s.add(f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" rx="16" fill="{ct}" stroke="{cc}" stroke-width="3"/>')
        s.add(f'<circle cx="600" cy="{cy}" r="30" fill="{cc}" stroke="white" stroke-width="4"/>')
        text(s,600,cy+10,str(i+1),28,bold=True,fill='white')
        text(s,x+24,y0+40,'ESTACIÓN '+str(i+1)+' · '+et.upper(),18,anchor='start',bold=True,fill=cc)
        text(s,x+24,y0+74,cap,24,anchor='start',bold=True,width=w-48)
        text(s,x+24,y0+74+nt*30+6,lleva,20,anchor='start',italic=True,fill=INK2,width=w-48)
        if i==4:
            by=y0+74+nt*30+6+nb*25+6
            for q in (1,2,3,4):
                qc,qt,qn=Q[q]; lab=qn.split('. ',1)[1]
                s.add(f'<rect x="{x+24}" y="{by}" width="{w-48}" height="32" rx="8" fill="{qc}"/>')
                text(s,x+40,by+22,lab,17,anchor='start',bold=True,fill='white')
                text(s,x+w-40,by+22,f'temas {(q-1)*9+1} a {q*9}',17,anchor='end',fill='white')
                by+=40
    # llegada
    s.add(f'<rect x="562" y="{end-70}" width="76" height="62" rx="6" fill="{TE}"/>')
    s.add(f'<path d="M548,{end-66} L600,{end-112} L652,{end-66} Z" fill="{TE}"/>')
    s.add(f'<rect x="588" y="{end-44}" width="24" height="36" rx="3" fill="white"/>')
    text(s,670,end-60,'Llegada',22,anchor='start',bold=True,fill=TE)
    text(s,670,end-32,'La persona, en la puerta de su casa',20,anchor='start',italic=True,fill=INK2)
    s.h=end+20; png(s,'intro_mapa')

# ---------- rutas de lectura ----------
RUT=[('Concejo Municipal o Alcaldía','Conclusión: las preguntas de diagnóstico',AZ,AZt,'Los temas con cuentas pendientes y el capítulo 4'),
     ('Persona servidora municipal','El tema de su área',GR,GRt,'Su mapa, el caso y la lista Revise en su municipalidad'),
     ('Asesoría, litigio o resolución','Capítulos 2 y 3',VI,VIt,'Normas, votos y dictámenes de cada tema'),
     ('Vecina o vecino','El tema que le preocupa',TE,TEt,'El caso: qué pidió otra persona y qué resolvieron'),
     ('Estudio o docencia','Capítulo 1',VE,VEt,'El orden del libro, hasta volver al núcleo')]
def rutas():
    s=SVG(1200,10); cabecera(s,'Por dónde entrar','Cinco rutas de lectura')
    y=240
    text(s,40,y,'Quien lee',20,anchor='start',bold=True,fill=INK2)
    text(s,430,y,'Empieza por',20,anchor='start',bold=True,fill=INK2)
    text(s,820,y,'Y sigue con',20,anchor='start',bold=True,fill=INK2)
    y+=20
    for i,(quien,emp,c,ct,sig) in enumerate(RUT):
        h=max(need_h(None,sig,320,22,20,pad=36),need_h(None,emp,330,22,22,pad=36),96)
        s.add(f'<rect x="30" y="{y}" width="1140" height="{h}" rx="14" fill="{ct if i%2==0 else "white"}" stroke="{GRt}" stroke-width="2"/>')
        # persona
        s.add(f'<circle cx="74" cy="{y+h/2-12}" r="13" fill="{INK}"/><path d="M52,{y+h/2+26} q22,-34 44,0 Z" fill="{INK}"/>')
        text(s,112,y+h/2+8-(13 if len(wrap(quien,22,290))>1 else 0),quien,22,anchor='start',bold=True,width=290)
        box(s,425,y+14,330,h-28,None,emp,fill=c,stroke=c,bcol='white',bfs=22,sw=2)
        s.add(f'<path d="M770,{y+h/2} L800,{y+h/2}" stroke="{c}" stroke-width="5"/><path d="M800,{y+h/2-10} L814,{y+h/2} L800,{y+h/2+10} Z" fill="{c}"/>')
        text(s,825,y+h/2+(-10 if len(wrap(sig,20,320))>1 else 7),sig,20,anchor='start',italic=True,fill=INK,width=320)
        y+=h+10
    s.h=y+30; png(s,'intro_rutas')
mapa(); rutas()
