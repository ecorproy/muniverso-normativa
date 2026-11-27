import sys; sys.path.insert(0,'/home/claude/figuras')
from svglib import *
D='/home/claude/figuras/nuevas/'
W=1200
# ===== A. De la meta al servicio prestado
st=[('Concejo Municipal','Aprueba el plan de desarrollo municipal y el plan anual operativo, incorporando las necesidades e intereses de la población (CM, art. 13).','#bdbdbd'),
    ('Alcaldía','Mantiene actualizado el manual de organización y funcionamiento, donde queda escrito el mapa de procesos (CM, art. 130).','#bdbdbd'),
    ('Cada superior','Define los procesos y proyectos de la dependencia y los productos y servicios prestados (Ley 10159, art. 28).','#e6e6e6'),
    ('La jefatura, al inicio del año','Asigna a cada persona servidora entre procesos, proyectos, productos y servicios, con plazos de entrega y tiempo estimado (Ley 10159, art. 29).','#e6e6e6'),
    ('La persona servidora','Mantiene al día su desempeño en el sistema informático que la administración pone a su disposición (Ley 10159, art. 29).','white'),
    ('La evaluación','80 % cumplimiento de metas de productos y servicios; 20 % competencias del puesto valoradas por la jefatura (Ley 2166, art. 48). Motivada y recurrible (voto 2025-008201).','white'),
    ('Los efectos','Anualidad con «muy bueno» o su equivalente (Ley 2166, art. 48); ascensos, promociones, reconocimientos y capacitaciones (art. 49); dos evaluaciones consecutivas inferiores al 70 %: causal de despido (Ley 10159, art. 21).','white'),
    ('La rendición de cuentas','Informe de labores de la alcaldía ante el Concejo, a disposición de los habitantes (CM, art. 17).','#e6e6e6'),
    ('La persona del cantón','¿A quién se le prestó?','#bdbdbd')]
side={3:'Sin seguimiento del plan anual: falta grave, previo procedimiento administrativo (art. 29).',
      4:'Sin registro al día: falta grave, también para todo el nivel directivo (art. 29).'}
x0,bw=120,700; y=30; gap=46; ys=[]
s=SVG(W,10)
for i,(t,b,f) in enumerate(st):
    h=need_h(t,b,bw,26,22,pad=34)
    box(s,x0,y,bw,h,t,b,fill=f,tfs=26,bfs=22,sw=4 if i==8 else 3)
    ys.append((y,h))
    if i in side:
        sh=need_h(None,side[i],300,25,21,pad=30)
        box(s,870,y+h/2-sh/2,300,sh,None,side[i],dash='9,6',bfs=21)
        s.add(f'<line x1="{x0+bw}" y1="{y+h/2}" x2="868" y2="{y+h/2}" stroke="#111" stroke-width="2" stroke-dasharray="6,5"/>')
    if i<8: arrow(s,x0+bw/2,y+h,x0+bw/2,y+h+gap-2)
    y+=h+gap
# lazo de retorno
yl=ys[8][0]+ys[8][1]/2; yt=ys[0][0]+ys[0][1]/2
path(s,f'M {x0} {yl} L 60 {yl} L 60 {yt} L {x0-2} {yt}',dash='10,7')
s.add(f'<text transform="translate(45,{(yl+yt)/2}) rotate(-90)" font-size="21" font-style="italic" text-anchor="middle" fill="#333">sus necesidades vuelven al plan</text>')
s.h=y; s.save(D+'c4_flujo.svg')

# ===== B. Cuadro comparativo: cuatro fuentes por etapa
cols=['Ley 2166','Ley 10159 (Ley Marco)','Código Municipal','Código de Trabajo']
cw=[185,310,310,310,300]
SR='Sin regla propia.'
rows=[('Finalidad y alcance',
  'Mejora continua de la gestión pública y del desempeño y desarrollo integral de los funcionarios (art. 45).',
  'La misma finalidad; el instrumento debe ser objetivo, sin perjuicio por injerencia política, persecución o acoso laboral (art. 27). Cubre a municipalidades y concejos municipales de distrito (art. 2, inc. c).',
  'Evaluación y calificación anual de los servicios de cada trabajador municipal (art. 144). Regula incentivos y beneficios (art. 143).',
  'La persona trabajadora ejecuta el trabajo con intensidad, cuidado y esmero, en la forma, tiempo y lugar convenidos (art. 71, inc. b).'),
 ('Quién fija el método',
  'Rectoría de Mideplán (art. 46); lineamientos generales con las salvedades respectivas (art. 47). La Dirección General de Servicio Civil dicta cada año lineamientos técnicos y metodológicos (art. 49).',
  'Mideplán emite lineamientos y principios generales, salvo funciones exclusivas de los entes con autonomía de gobierno (art. 7, inc. f; art. 28). En la municipalidad, la define el propio ente (C-136-2026).',
  'Recursos Humanos confecciona los formularios, previa consulta a la alcaldía; sin esa oficina, los elabora la alcaldía (art. 144).',
  'El servicio se desempeña bajo la dirección del patrono o su representante (art. 71, inc. a).'),
 ('Qué se mide',
  'Indicadores cuantitativos de metas individuales de productos y servicios prestados, vinculados a procesos y proyectos; también el cuerpo gerencial (art. 47).',
  'El mismo método y el cuerpo de los niveles directivos (art. 28). La alta dirección: evaluación rigurosa por eficacia, eficiencia y control de resultados (art. 17, inc. c).',
  'El rendimiento del servidor en cada factor que influye en su desempeño general (art. 146).',
  SR),
 ('Plan y registro',
  'La jefatura asigna al inicio del año, con plazos y tiempos; sistema informático al día, también para el nivel directivo; incumplir es falta grave (art. 48).',
  'Igual, y la falta grave se declara previo procedimiento administrativo; el sistema se alimenta solo durante la jornada (art. 29).',
  'Primera quincena de junio; Recursos Humanos vela por que cada jefatura evalúe (art. 146). Personal en propiedad con un año continuo (art. 147) y reglas para quien no lo completó (art. 148).',
  SR),
 ('Escala',
  '80 % metas anuales y 20 % competencias valoradas por la jefatura (art. 48).',
  'Da al artículo 48 de la Ley 2166 su redacción vigente (art. 49).',
  'Regular, Bueno, Muy bueno y Excelente (art. 146).',
  SR),
 ('Desacuerdo y control',
  SR,
  'La jefatura que califica y la autoridad que confirma deben justificar la nota; cuentan solo evaluaciones en firme (art. 21).',
  'Lo resuelve la alcaldía, previa audiencia a todas las partes (art. 149).',
  SR),
 ('Efectos favorables',
  'Anualidad solo con Muy bueno o su equivalente, en salario compuesto (art. 48); ascensos, promociones, reconocimientos y capacitaciones (art. 49).',
  SR,
  'Reconocimiento y estímulo; cuenta para selección, capacitación, ascensos, aumento de sueldo, permisos y reducciones forzosas (art. 145); derecho al reconocimiento del buen desempeño (art. 155, inc. c).',
  SR),
 ('Efectos desfavorables',
  'Falta grave por no dar seguimiento al plan o no registrar (art. 48).',
  'Dos evaluaciones consecutivas inferiores al 70 %, en firme y con responsabilidad acreditada, tras un plan remedial pactado: despido (art. 21).',
  'Dos calificaciones consecutivas de Regular: falta grave (art. 150); sanciones de amonestación a despido (art. 158).',
  'Negarse de modo reiterado a las normas de eficacia y rendimiento; incapacidad demostrada; otra falta grave al contrato (art. 81, incs. h, j y l).'),
 ('Despido',
  SR,
  'Procedimiento especial único, con acto final en dos meses (art. 21, inc. a).',
  'Solo por las causales del Código de Trabajo y con el procedimiento del Código (art. 155, inc. a); lo acuerda la alcaldía y se apela ante el tribunal de trabajo (arts. 158 y 159).',
  'Causas justas de terminación del contrato (art. 81).')]
W2=sum(cw)+60
def cuadro(filas,nombre,pie=True,bfs=23,lfs=23):
    s=SVG(W2,10); xs=[30]
    for w in cw: xs.append(xs[-1]+w)
    y=30; hh=80
    for j,c in enumerate(cols):
        k=j+1
        box(s,xs[k],y,cw[k],hh,None,None,fill='#111' if k<3 else '#555',r=0,sw=2)
        text(s,xs[k]+cw[k]/2,y+50,c,23,bold=True,fill='white',width=cw[k]-16)
    y+=hh
    for r in filas:
        lab,cells=r[0],r[1:]
        h=max([need_h(None,t,cw[k+1],bfs,bfs,pad=28) for k,t in enumerate(cells)]+[need_h(lab,None,cw[0],lfs,lfs,pad=28)])
        box(s,xs[0],y,cw[0],h,lab,None,fill='#e6e6e6',r=0,tfs=lfs,sw=2)
        for k,t in enumerate(cells):
            box(s,xs[k+1],y,cw[k+1],h,None,t,fill='#f4f4f4' if t==SR else 'white',r=0,bfs=bfs,sw=2)
        y+=h
    if pie:
        text(s,W2/2,y+40,'La Ley Marco no derogó el capítulo de la Ley 2166, y ambas se complementan con los artículos 144 a 150 del Código Municipal (C-131-2026).',21,italic=True,fill='#333',width=W2-80)
        text(s,W2/2,y+120,'El Código de Trabajo entra por remisión del Código Municipal (arts. 155, 157 y 159). La evaluación es motivada y recurrible (voto 2025-008201).',21,italic=True,fill='#333',width=W2-80)
        y+=170
    else: y+=30
    s.h=y; s.save(D+nombre)
cuadro(rows,'c4_cuadro.svg')
cuadro(rows[:5],'c4_cuadro_a.svg',pie=False)
cuadro(rows[5:],'c4_cuadro_b.svg')

# ===== C. Anatomía de un proceso y mapa de procesos
s=SVG(W,1330)
text(s,W/2,40,'Un proceso',28,bold=True)
box(s,40,70,600,100,'Responsable: el superior','define procesos, productos y servicios (Ley 10159, art. 28)',fill='#e6e6e6',tfs=23,bfs=19)
s.add('<circle cx="900" cy="125" r="95" fill="white" stroke="#111" stroke-width="3"/>')
text(s,900,92,'Ciclo de',19,bold=True); text(s,900,116,'Deming',19,bold=True)
text(s,900,146,'planear, hacer,',16,fill='#333'); text(s,900,166,'verificar,',16,fill='#333'); text(s,900,186,'actuar',16,fill='#333')
arrow(s,440,170,440,226)
xs=[40,320,600,880]; ws=[240,240,240,280]
lab=[('Entradas',None,'white'),('Actividades','secuencia ordenada y repetitiva','#e6e6e6'),('Salidas','resultados programados','#e6e6e6'),('Destinataria','la persona del cantón','#bdbdbd')]
for k,(t,b,f) in enumerate(lab):
    box(s,xs[k],230,ws[k],130,t,b,fill=f,tfs=24,bfs=19,sw=4 if k==3 else 3)
    if k<3: arrow(s,xs[k]+ws[k]+2,295,xs[k+1]-4,295)
path(s,'M 1020 360 L 1020 410 L 440 410 L 440 365',dash='9,6')
text(s,1150,445,'juzga la validez de lo que recibe (Medina León et al., 2009, p. 68)',19,anchor='end',italic=True,fill='#333')
box(s,40,480,520,85,None,'El proceso necesita indicadores que muestren de forma gráfica su evolución (Medina León et al., 2009, p. 68)',dash='9,6',bfs=19)
s.add('<line x1="40" y1="600" x2="1160" y2="600" stroke="#111" stroke-width="2"/>')
text(s,W/2,650,'El mapa de procesos de una municipalidad',28,bold=True)
bands=[('Estratégicos','Concejo y Alcaldía: definen y controlan metas, políticas y estrategias (plan de desarrollo y plan anual operativo, CM, art. 13).','#bdbdbd'),
       ('Operativos','Los servicios que llegan a las personas: la basura, la acera, el permiso, la atención.','#e6e6e6'),
       ('De apoyo','La administración que los sostiene: presupuesto, proveeduría, recursos humanos, sistemas.','white')]
y=690
for t,b,f in bands:
    box(s,40,y,240,160,t,None,fill=f,tfs=25)
    box(s,290,y,700,160,None,b,fill=f,bfs=21)
    y+=190
box(s,1010,880,150,160,'Persona','del cantón',fill='#bdbdbd',tfs=22,bfs=19,sw=4)
arrow(s,992,960,1006,960)
arrow(s,640,850,640,876); arrow(s,640,1070,640,1044)
text(s,W/2,1290,'Fuentes: Zaratiegui (1999, pp. 82-85); Medina León et al. (2009, pp. 67-70).',19,italic=True,fill='#333')
s.save(D+'c4_proceso.svg')

# ===== D. Producto interno y servicio prestado
s=SVG(W,700)
box(s,40,40,420,300,'Producto interno','Un oficio archivado. Un informe que nadie usa. Un trámite que pasó de una oficina a otra.',fill='white',dash='10,7',tfs=27,bfs=22)
box(s,740,40,420,300,'Servicio prestado','La basura recogida. La acera construida. La solicitud resuelta en plazo.',fill='#bdbdbd',tfs=27,bfs=22,sw=4)
arrow(s,465,190,734,190,sw=4)
text(s,600,150,'solo cuenta',20,italic=True,fill='#333')
text(s,600,236,'si el expediente',18,italic=True,fill='#333'); text(s,600,258,'termina en algo que',18,italic=True,fill='#333'); text(s,600,280,'una persona recibió',18,italic=True,fill='#333')
s.add('<ellipse cx="600" cy="450" rx="300" ry="70" fill="#e6e6e6" stroke="#111" stroke-width="4"/>')
text(s,600,462,'¿A quién se le prestó?',32,bold=True)
foot=['Servir a cada administrado (LGAP, art. 114) y leer las normas por su fin (LGAP, art. 10).',
      'Ninguna evaluación contra reglas unívocas de la ciencia o de la técnica (LGAP, art. 16).',
      'Premiar el desempeño deficiente viola la idoneidad comprobada (voto 2025-008201).']
y=575
for f in foot: text(s,W/2,y,f,20,fill='#333'); y+=34
s.save(D+'c4_contraste.svg')

# ===== E. Quién fija cómo se evalúa
s=SVG(W,640)
box(s,40,60,440,270,'Poder Ejecutivo: Mideplán','Rectoría y lineamientos generales para homogeneizar los métodos de evaluación (Ley 10159, art. 28).',fill='white',tfs=25,bfs=21)
box(s,720,60,440,270,'Municipalidad','Concejo y Alcaldía definen cómo se evalúa a su personal, «de forma exclusiva y excluyente» (C-136-2026, ap. IV).',fill='#bdbdbd',tfs=25,bfs=21,sw=4)
s.add('<rect x="575" y="30" width="50" height="330" fill="#555" stroke="#111" stroke-width="2"/>')
text(s,600,395,'Autonomía municipal',22,bold=True)
text(s,600,425,'«con las salvedades respectivas» (art. 28)',20,italic=True,fill='#333')
arrow(s,482,195,570,195,sw=3)
text(s,526,180,'',18)
text(s,W/2,500,'La ley marco no puede vaciar de contenido la autonomía de las municipalidades',21,fill='#333')
text(s,W/2,530,'(Sala Constitucional, según C-136-2026, ap. IV).',21,fill='#333')
text(s,W/2,590,'La responsabilidad de que la evaluación mida bien queda en el cantón.',22,italic=True)
s.save(D+'c4_autonomia.svg')

# ===== F. La nota
s=SVG(W,800)
text(s,40,50,'Cómo se compone la calificación',26,anchor='start',bold=True)
x0,x1=40,1160; L=x1-x0; y=80
s.add(f'<rect x="{x0}" y="{y}" width="{L*0.8}" height="90" fill="#555" stroke="#111" stroke-width="3"/>')
s.add(f'<rect x="{x0+L*0.8}" y="{y}" width="{L*0.2}" height="90" fill="#e6e6e6" stroke="#111" stroke-width="3"/>')
text(s,x0+L*0.4,y+40,'80 %',30,bold=True,fill='white'); text(s,x0+L*0.4,y+72,'cumplimiento de las metas anuales de productos y servicios',19,fill='white')
text(s,x0+L*0.9,y+40,'20 %',30,bold=True); text(s,x0+L*0.9,y+72,'competencias del puesto',17)
text(s,W/2,y+125,'Ley 2166, art. 48, en la redacción que le dio la Ley 10159',19,italic=True,fill='#333')
y=290
text(s,40,y,'Qué produce la calificación',26,anchor='start',bold=True)
y+=30
bx=[('«Muy bueno» o su equivalente','Incentivo por anualidad, para quien labora con salario compuesto (Ley 2166, art. 48).','#e6e6e6'),
    ('Toda calificación','Se considera para ascensos, promociones, reconocimientos, capacitaciones y adiestramientos (Ley 2166, art. 49).','white'),
    ('Inferior al 70 % dos veces seguidas','Causal de despido, con las condiciones que fija la norma (Ley 10159, art. 21).','#555')]
w=360
for k,(t,b,f) in enumerate(bx):
    xx=40+k*(w+20)
    box(s,xx,y,w,300,None,None,fill=f)
    col='white' if f=='#555' else '#111'
    text(s,xx+w/2,y+50,t,23,bold=True,width=w-30,fill=col)
    text(s,xx+w/2,y+140,b,21,width=w-30,fill=col if f=='#555' else '#333')
y+=340
box(s,40,y,1120,150,'Cada puntaje es un acto administrativo','Debe estar motivado y admite los recursos ordinarios; la aplicación individual se discute en la vía de legalidad (voto 2025-008201, cons. XXVIII). Sin motivación se lesionan el debido proceso y el derecho de defensa (Cortés García, 2026, capítulo 25).',dash='10,7',tfs=24,bfs=19)
s.h=y+170; s.save(D+'c4_nota.svg')
