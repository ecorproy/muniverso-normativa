import sys; sys.path.insert(0,'/home/claude/figuras')
from svglib import *
D='/home/claude/figuras/nuevas/'
W=1200
# ---------- F acera (cap01)
s=SVG(W,1000)
cx,cy=600,500
s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="170" ry="80" fill="#e6e6e6" stroke="#111" stroke-width="4"/>')
text(s,cx,cy-8,'La acera',34,bold=True); text(s,cx,cy+30,'un metro y medio de concreto',21,italic=True,fill='#333')
nodes=[(-1,'Tema 18. Trabajo y sustento','San José, 1991: puestos de venta en la acera; permiso de uso precario. Voto 1991-002306.',220,140),
       (1,'Tema 24. Discapacidad','Heredia, 2012-2015: tres años de denuncias de un padre de dos hijos con discapacidad visual. Voto 2015-012020.',980,140),
       (-1,'Tema 34. Cultura','Heredia, 2023: demolición de un pórtico centenario que estorbaba el paso. Voto 2023-027541.',220,500),
       (1,'Tema 30. Ambiente','San Pablo de Heredia, 2025: árboles de una ruta nacional levantaron la acera. Voto 2025-016121.',980,500),
       (-1,'Tema 33. Obra pública','Montes de Oca, 2025-2026: una finca sin acera; la Municipalidad previno y no construyó. Voto 2026-038693.',220,860),
       (1,'Tema 6. Emergencias y presupuesto','Los recursos de 2025 se reasignaron a la quebrada Los Negritos. Voto 2026-038693.',980,860)]
bw=350
import math
for side,t,b,x,y in nodes:
    h=need_h(t,b,bw,25,22)
    bx=x-bw/2; by=y-h/2
    exx=x-side*bw/2; dx=exx-cx; dy=y-cy
    k=1/math.sqrt((dx/170)**2+(dy/80)**2)
    s.add(f'<line x1="{cx+dx*k:.1f}" y1="{cy+dy*k:.1f}" x2="{exx}" y2="{y}" stroke="#111" stroke-width="3"/>')
    box(s,bx,by,bw,h,t,b,tfs=25,bfs=22)
s.save(D+'acera.svg')
# ---------- F muertes (cap01)
rows=[('La captura','plantas que toman carbono de la red sin dar nada','Vermissa: un punto que recibe sin dar'),
      ('El corte','un micelio herido no avisa a su vecino desconectado','el camino a China Kichá: sin escuela y sin EBAIS (voto 2026-013450)'),
      ('El desgaste','las conexiones envejecen y deben rehacerse','Montes de Oca, 2003: la flotilla sin mantenimiento (voto 2003-005006)'),
      ('El envenenamiento','el nitrógeno y la labranza intensiva alteran las micorrizas','la mala práctica repetida hasta volverse costumbre (San Ramón, voto 2023-001782)'),
      ('La sustitución','el fertilizante le quita el trabajo al hongo','la competencia que no se ejerce prepara su traslado'),
      ('El acaparamiento','hongos que retienen el fósforo','Upala, 2020: sesiones del Concejo sin transmitir (voto 2020-016680)')]
H=170+len(rows)*150+190
s=SVG(W,H)
text(s,360,60,'En la red de hongos',27,bold=True); text(s,880,60,'En el cantón',27,bold=True)
s.add('<line x1="40" y1="85" x2="1160" y2="85" stroke="#111" stroke-width="2"/>')
y=110
for t,a,b in rows:
    box(s,40,y,240,120,t,None,fill='#e6e6e6',tfs=23)
    box(s,295,y,365,120,None,a,bfs=21)
    arrow(s,665,y+60,690,y+60)
    box(s,700,y,460,120,None,b,bfs=21)
    y+=150
box(s,40,y+10,1120,130,'La regeneración','"Un fragmento de micelio puede regenerar una red entera" (Sheldrake, 2020, capítulo 2). En Heredia el fragmento fue una persona (voto 2015-012020).',fill='white',dash='10,7',tfs=25,bfs=21)
s.save(D+'muertes.svg')
# ---------- F linea de tiempo (cap02)
ev=[('1949','Constitución Política: los intereses y servicios locales, a cargo del Gobierno Municipal (art. 169).','n'),
    ('1968','Ley de Planificación Urbana (Ley 4240).','n'),('1972','Ley General de Caminos Públicos (Ley 5060).','n'),
    ('1978','Ley General de la Administración Pública (Ley 6227).','n'),
    ('1997','Sala Constitucional, voto 1997-006469: Ordenanzas de 1867 y licencias.','s'),
    ('1998','Código Municipal (Ley 7794).','n'),
    ('1999','Sala Constitucional, voto 1999-005445: competencia originaria; solo una ley la desplaza.','s'),
    ('2001','Reforma del artículo 170: traslado de competencias por ley.','n'),
    ('2006','Sala Constitucional, voto 2006-017907: las aguas pluviales de un barrio.','s'),
    ('2010','Ley 8801, de transferencia de competencias.','n'),
    ('2011','Sala Constitucional, voto 2011-015763: telecomunicaciones.','s'),
    ('2015','Sala Primera, resolución 000164-F-S1-2015: las radiobases en San José.','s'),
    ('2016','Leiva Poveda: «La elusiva definición de “lo local”».','d'),
    ('2017','Sala Primera, resolución 001461-F-S1-2017: la frontera del tributo.','s'),
    ('2019','Procuraduría, C-006-2019: autonomía política frente a los decretos.','p'),
    ('2022','Procuraduría, C-125, C-223, C-231 y C-255-2022: la coordinación como principio estructural; cuando la competencia es de otro, coordinar e instar.','p'),
    ('2024','Procuraduría, C-195-2024: aceras de rutas nacionales y competencia prevalente; C-287-2024: Sistema 9-1-1.','p'),
    ('2026','Procuraduría, C-107-2026: telecomunicaciones.','p')]
lab={'n':'Norma','s':'Jurisprudencia','p':'Procuraduría','d':'Doctrina'}
fill={'n':'#111','s':'#777','p':'white','d':'#cfcfcf'}
step=92; H=140+len(ev)*step
s=SVG(W,H)
x0=240
for i,(k,v) in enumerate(lab.items()):
    xx=120+i*260
    s.add(f'<circle cx="{xx}" cy="50" r="13" fill="{fill[k]}" stroke="#111" stroke-width="3"/>'); text(s,xx+24,58,v,22,anchor='start')
s.add(f'<line x1="{x0}" y1="110" x2="{x0}" y2="{H-60}" stroke="#111" stroke-width="4"/>')
y=140
for a,t,k in ev:
    text(s,x0-30,y+9,a,27,anchor='end',bold=True)
    s.add(f'<circle cx="{x0}" cy="{y}" r="14" fill="{fill[k]}" stroke="#111" stroke-width="3"/>')
    text(s,x0+34,y+8,t,22,anchor='start',width=W-x0-60,lh=1.2)
    y+=step
s.save(D+'linea.svg')
# ---------- F zonas (cap03)
s=SVG(W,900)
s.add('<ellipse cx="420" cy="450" rx="400" ry="400" fill="white" stroke="#111" stroke-width="3" stroke-dasharray="12,8"/>')
s.add('<ellipse cx="420" cy="450" rx="280" ry="280" fill="#e6e6e6" stroke="#111" stroke-width="3"/>')
s.add('<ellipse cx="420" cy="450" rx="150" ry="150" fill="#bdbdbd" stroke="#111" stroke-width="3"/>')
text(s,420,435,'Núcleo',28,bold=True); text(s,420,468,'zona de certeza',21,italic=True)
text(s,420,225,'Halo',28,bold=True); text(s,420,255,'caso por caso, en contacto con la realidad',20,italic=True,width=360)
text(s,420,135,'Zona de certeza negativa',24,bold=True)
zb=[('Núcleo','Desarrollo urbano (Ley 4240, art. 15); calles del cantón (Ley 5060, art. 2); licencias comerciales (voto 1997-006469); pluviales de un barrio (voto 2006-017907).','#bdbdbd',None),
    ('Halo','La mayor parte de la red del capítulo 1. Hechos que el juez comprueba enteros; valores donde la municipalidad tiene margen.','#e6e6e6',None),
    ('Certeza negativa','Sistema 9-1-1 (C-287-2024); telecomunicaciones (voto 2011-015763); aceras de rutas nacionales (C-231-2022); salud de la CCSS (C-125-2022). La municipalidad coordina, comunica e insta.','white','12,8')]
yy=20
for t,bb,f,d in zb:
    h=need_h(t,bb,340,24,21,pad=30); box(s,845,yy,340,h,t,bb,fill=f,dash=d,tfs=24,bfs=21); yy+=h+18
s.h=max(900,yy+10)
s.save(D+'zonas.svg')
# ---------- F flujograma (cap03)
s=SVG(W,1650)
cx=430
box(s,cx-260,30,520,90,None,'Una necesidad de una persona del cantón',fill='#e6e6e6',bfs=24)
arrow(s,cx,120,cx,170)
diamond(s,cx,265,560,190,'¿Importa de manera directa e inmediata a las personas del cantón?')
box(s,815,180,360,170,None,'Corresponde a otra institución: la municipalidad la insta a atenderla y lleva a la persona hasta ella',bfs=21)
arrow(s,cx+280,265,813,265,label='No',lx=cx+300,ly=252)
arrow(s,cx,360,cx,410,label='Sí',lx=cx+12,ly=395)
diamond(s,cx,500,560,180,'¿Una ley la organizó para todo el país?')
box(s,815,440,360,120,None,'Zona de certeza negativa: coordinar, comunicar e instar',bfs=21)
arrow(s,cx+280,500,813,500,label='Sí',lx=cx+300,ly=487)
arrow(s,cx,590,cx,640,label='No',lx=cx+12,ly=625)
diamond(s,cx,735,560,190,'¿Hay que restringir derechos o sancionar?')
box(s,815,675,360,120,None,'Hace falta ley; no basta un reglamento (LGAP, art. 12)',bfs=21)
arrow(s,cx+280,735,813,735,label='Sí',lx=cx+300,ly=722)
path(s,'M 995 790 L 995 850 L 460 850 L 460 880')
text(s,1010,830,'con ley habilitante',19,anchor='start',italic=True,fill='#333')
arrow(s,cx,830,cx,880,label='No',lx=cx-60,ly=865)
diamond(s,cx,975,560,190,'¿Tiene capacidad real y técnica?')
box(s,815,895,360,170,None,'Coordinar y llevar a la persona a la institución competente; la obligación propia no se extingue',bfs=21)
arrow(s,cx+280,975,813,975,label='No',lx=cx+300,ly=962)
arrow(s,cx,1070,cx,1120,label='Sí',lx=cx+12,ly=1105)
box(s,cx-300,1120,600,130,'Prestar','de manera planificada, regular, eficiente, continua y en condiciones de igualdad',fill='#e6e6e6',tfs=26,bfs=21)
arrow(s,cx,1250,cx,1300)
box(s,cx-300,1300,600,110,'Medir y rendir cuentas','¿qué recibió la persona y quién se lo prestó?',tfs=26,bfs=21)
s.add(f'<text x="40" y="1520" font-size="20" font-style="italic" fill="#333">En toda la ruta rige la misma regla: la municipalidad no puede contestar que el asunto no le toca</text>')
s.add(f'<text x="40" y="1550" font-size="20" font-style="italic" fill="#333">porque ninguna ley lo menciona.</text>')
s.h=1590; s.save(D+'flujo.svg')
# ---------- F estructura de cada tema (cap03)
st=[('1','El caso','ilustra y prueba'),('2','Las normas','competencia, instrumentos y límites'),('3','Votos y dictámenes','la jurisprudencia y la Procuraduría'),
    ('4','Con qué se paga','cuando el bien exige gasto propio'),('5','Cómo lo hace','el gobierno local hace que el bien exista'),
    ('6','Lo que hoy se mide','qué se registra y qué falta'),('7','Conclusión','los deberes del gobierno local')]
s=SVG(W,560)
bw=150; gap=(W-80-7*bw)/6
for i,(n,t,b) in enumerate(st):
    x=40+i*(bw+gap)
    s.add(f'<circle cx="{x+bw/2}" cy="70" r="30" fill="#111"/>'); text(s,x+bw/2,80,n,28,bold=True,fill='white')
    box(s,x,120,bw,300,t,b,fill='#e6e6e6' if i in (1,4) else 'white',tfs=22,bfs=19)
    if i<6: arrow(s,x+bw+4,270,x+bw+gap-4,270,sw=3)
text(s,W/2,480,'La pregunta del tema: cómo puede y debe el gobierno local hacer que el bien exista en el cantón.',22,italic=True,width=W-80)
s.save(D+'tema.svg')
# ---------- F cadena (cap04)
ch=[('Constitución','Gobierno responsable (CP, art. 9); los funcionarios cumplen los deberes que la ley les impone (CP, art. 11).'),
    ('Jurisprudencia de la Sala','Derecho exigible al buen funcionamiento de los servicios públicos (voto 2003-011382).'),
    ('Ley General de la Administración Pública','Continuidad, eficiencia, adaptación e igualdad del servicio (LGAP, art. 4).'),
    ('Empleo público','Personas idóneas; participación, rendición de cuentas y evaluación de resultados (Ley 10159, art. 4).'),
    ('Responsabilidad','La institución responde por su funcionamiento (LGAP, art. 190); la persona servidora, por dolo o culpa grave (LGAP, art. 199).')]
s=SVG(W,1220)
y=30
for i,(t,b) in enumerate(ch):
    s.add(f'<ellipse cx="110" cy="{y+90}" rx="70" ry="85" fill="none" stroke="#111" stroke-width="9"/>')
    text(s,110,y+104,str(i+1),40,bold=True)
    box(s,220,y+20,940,140,t,b,fill='#e6e6e6' if i==0 else 'white',tfs=26,bfs=21)
    y+=225
text(s,W/2,y+20,'La cadena termina en la persona servidora que firma una meta.',23,italic=True)
s.h=y+50; s.save(D+'cadena.svg')
# ---------- F recursos (cap04)
s=SVG(W,760)
box(s,40,30,520,120,'Una decisión','de una persona servidora que no depende del Concejo',fill='#e6e6e6',tfs=26,bfs=21)
box(s,640,30,520,120,'Una omisión','el órgano no adopta la conducta debida',fill='#e6e6e6',tfs=26,bfs=21)
arrow(s,300,150,300,210); arrow(s,900,150,900,210)
box(s,40,210,520,140,'Revocatoria','ante quien dictó el acto, dentro del quinto día',tfs=25,bfs=21)
box(s,640,210,520,140,'Requerimiento','al órgano, para que en quince días adopte la conducta debida',tfs=25,bfs=21)
arrow(s,300,350,300,410); arrow(s,900,350,900,410,label='si la omisión persiste',lx=912,ly=388)
box(s,40,410,520,140,'Apelación','ante la alcaldía, dentro del quinto día',tfs=25,bfs=21)
box(s,640,410,520,140,'Vía judicial','queda abierta',tfs=25,bfs=21)
text(s,300,600,'CM, art. 171',22,italic=True); text(s,900,600,'CPCA, art. 35',22,italic=True)
text(s,W/2,680,'La omisión no puede volverse un obstáculo para la persona (Cortés García, 2026, capítulo 12).',22,italic=True,width=W-80)
s.save(D+'recursos.svg')
# ---------- F seis preguntas (conclusion)
import math
s=SVG(W,1060)
cx,cy=600,530
q=[('La captura','¿Quién recibe sin dar?'),('El corte','¿Dónde se cae el expediente?'),('El desgaste','¿Qué no se está renovando?'),
   ('El envenenamiento','¿Qué mala práctica se volvió costumbre?'),('La sustitución','¿Qué hace otro por la municipalidad?'),
   ('El acaparamiento','¿Qué información o qué recurso queda retenido en un punto?')]
R=360
for i in range(6):
    a=math.radians(-90+i*60)
    x=cx+R*math.cos(a); y=cy+R*math.sin(a)
    s.add(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#111" stroke-width="2" stroke-dasharray="6,6"/>')
for i,(t,b) in enumerate(q):
    a=math.radians(-90+i*60)
    x=cx+R*math.cos(a); y=cy+R*math.sin(a)
    box(s,x-170,y-80,340,160,t,b,tfs=24,bfs=21)
s.add(f'<circle cx="{cx}" cy="{cy}" r="150" fill="#e6e6e6" stroke="#111" stroke-width="4"/>')
text(s,cx,cy-30,'La séptima',24,bold=True)
text(s,cx,cy+8,'¿Qué fragmento sigue vivo?',24,width=230,italic=True)
s.save(D+'preguntas.svg')
