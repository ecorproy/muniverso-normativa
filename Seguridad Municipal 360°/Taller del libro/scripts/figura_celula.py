import math, random
random.seed(360)
W=2100; C=W/2
out=[]
A=out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{W}" viewBox="0 0 {W} {W}" font-family="DejaVu Serif, serif">')
A('<rect width="100%" height="100%" fill="white"/>')
R_out=640
QC=['#2A8C6E','#8A4F9E','#C94158','#2F86AE']
# hifas: ramas desde la membrana hacia afuera
def rama(x,y,ang,largo,grosor,prof):
    if prof==0 or largo<12: return
    pts=[(x,y)]
    for i in range(6):
        ang+=random.uniform(-0.35,0.35)
        x+=math.cos(ang)*largo/6; y+=math.sin(ang)*largo/6
        pts.append((x,y))
    d='M'+' L'.join(f'{a:.1f},{b:.1f}' for a,b in pts)
    g=['#4F7942','#5E8A50','#7AA36B','#A9C79C'][min(3,4-prof)]
    A(f'<path d="{d}" fill="none" stroke="{g}" stroke-width="{grosor:.1f}" stroke-linecap="round"/>')
    for _ in range(2):
        rama(x,y,ang+random.uniform(-0.8,0.8),largo*0.62,grosor*0.62,prof-1)
for k in range(22):
    a=2*math.pi*k/22+random.uniform(-0.08,0.08)
    x=C+math.cos(a)*(R_out+8); y=C+math.sin(a)*(R_out+8)
    rama(x,y,a,150,5.5,4)
# membrana exterior (doble trazo) y citoplasma
A(f'<circle cx="{C}" cy="{C}" r="{R_out}" fill="#EEF5EA" stroke="#1F4E79" stroke-width="10"/>')
A(f'<circle cx="{C}" cy="{C}" r="{R_out-16}" fill="none" stroke="#9DBAD8" stroke-width="2"/>')
A(f'<defs><path id="arcOut" d="M {C-R_out+48},{C} A {R_out-48},{R_out-48} 0 0,1 {C+R_out-48},{C}"/>'
  f'<path id="arcNuc" d="M {C-200},{C} A 200,200 0 0,1 {C+200},{C}"/>'
  f'<path id="arcLocal" d="M {C-560},{C} A 560,560 0 0,0 {C+560},{C}"/></defs>')
A(f'<text x="{C}" y="{C-578}" font-size="27" letter-spacing="2" text-anchor="middle" fill="#1F4E79">BLOQUE DE LEGALIDAD</text>')
A(f'<text x="{C}" y="{C-548}" font-size="21" font-style="italic" text-anchor="middle" fill="#44505F">membrana exterior</text>')
A(f'<text x="{C}" y="{C+538}" font-size="27" letter-spacing="2" text-anchor="middle" fill="#4F7942">LO LOCAL · CP, art. 169</text>')
A(f'<text x="{C}" y="{C+566}" font-size="18" font-style="italic" text-anchor="middle" fill="#44505F">36 temas · los puntos son grados por nombrar</text>')
# 36 temas en cuatro cuadrantes, con huecos entre ellos
R_t=470
quad=[(['I. Vida'],'CP, art. 21'),(['II. Dignidad'],'CP, art. 33'),(['III. Protección','especial'],'CP, art. 51'),(['IV. Bienestar','y entorno'],'CP, art. 50')]
n=1
for q in range(4):
    base=-90+q*90
    for i in range(9):
        ang=math.radians(base+4.5+i*9.0)
        x=C+math.cos(ang)*R_t; y=C+math.sin(ang)*R_t
        A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="25" fill="{QC[q]}" stroke="{QC[q]}" stroke-width="3"/>')
        A(f'<text x="{x:.1f}" y="{y+9:.1f}" font-size="24" font-weight="bold" text-anchor="middle" fill="white">{n}</text>')
        n+=1
        # grados aún sin nombre entre un tema y el siguiente
        for j in (1,2):
            a2=math.radians(base+4.5+i*9.0+j*3.0)
            if i==8 and j==2: break
            A(f'<circle cx="{C+math.cos(a2)*R_t:.1f}" cy="{C+math.sin(a2)*R_t:.1f}" r="6" fill="{QC[q]}" fill-opacity="0.45"/>')
    mid=math.radians(base+45)
    lx=C+math.cos(mid)*345; ly=C+math.sin(mid)*345
    lines=quad[q][0]
    for k,t in enumerate(lines):
        A(f'<text x="{lx:.1f}" y="{ly-20+k*28:.1f}" font-size="24" font-weight="bold" text-anchor="middle" fill="{QC[q]}">{t}</text>')
    A(f'<text x="{lx:.1f}" y="{ly-20+len(lines)*28:.1f}" font-size="21" text-anchor="middle" fill="#44505F">{quad[q][1]}</text>')
# envoltura nuclear doble: la Constitución
A(f'<circle cx="{C}" cy="{C}" r="250" fill="white" stroke="#1F4E79" stroke-width="9"/>')
A(f'<circle cx="{C}" cy="{C}" r="232" fill="none" stroke="#1F4E79" stroke-width="5"/>')
A(f'<text x="{C}" y="{C-170}" font-size="17" letter-spacing="1" text-anchor="middle" fill="#1F4E79">CONSTITUCIÓN POLÍTICA</text>')
A(f'<text x="{C}" y="{C-147}" font-size="16" font-style="italic" text-anchor="middle" fill="#44505F">envoltura doble del núcleo</text>')
# núcleo: dos personas en simbiosis
def persona(x,y,c):
    A(f'<circle cx="{x}" cy="{y-58}" r="30" fill="{c}"/>')
    A(f'<path d="M {x-50},{y+40} Q {x-50},{y-22} {x},{y-22} Q {x+50},{y-22} {x+50},{y+40} Z" fill="{c}"/>')
persona(C-125,C+20,'#B5543A'); persona(C+125,C+20,'#1F4E79')
A(f'<defs><marker id="pt" markerWidth="12" markerHeight="12" refX="6" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 Z" fill="#1E2A38"/></marker></defs>')
A(f'<path d="M {C-60},{C-35} Q {C},{C-75} {C+60},{C-35}" fill="none" stroke="#1E2A38" stroke-width="4" marker-end="url(#pt)"/>')
A(f'<path d="M {C+60},{C+35} Q {C},{C+75} {C-60},{C+35}" fill="none" stroke="#1E2A38" stroke-width="4" marker-end="url(#pt)"/>')
A(f'<text x="{C-125}" y="{C+100}" font-size="22" text-anchor="middle" fill="#1E2A38">persona</text>')
A(f'<text x="{C-125}" y="{C+125}" font-size="22" text-anchor="middle" fill="#1E2A38">servida</text>')
A(f'<text x="{C+125}" y="{C+100}" font-size="22" text-anchor="middle" fill="#1E2A38">persona</text>')
A(f'<text x="{C+125}" y="{C+125}" font-size="22" text-anchor="middle" fill="#1E2A38">servidora</text>')
A(f'<text x="{C}" y="{C+162}" font-size="19" font-style="italic" text-anchor="middle" fill="#44505F">beneficio mutuo</text>')
A('</svg>')
open('/home/claude/figuras/celula.svg','w',encoding='utf-8').write('\n'.join(out))
