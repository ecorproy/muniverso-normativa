import sys
p=sys.argv[1]; L=open(p,encoding='utf-8').read().split('\n')
F='/home/claude/figuras/'; N=F+'nuevas/'
# (inicio del párrafo o encabezado ancla, 'despues' o 'antes', imagen, leyenda, ancho)
figs=[('Discapacidad, cultura, ambiente, trabajo, emergencias, presupuesto','despues',N+'acera.png','La acera: un metro y medio de concreto por donde pasan seis temas del libro.','15cm'),
 ('La red también se recupera, y casi siempre empieza por un fragmento','despues',N+'muertes.png','Las seis formas en que muere la red y la regeneración desde un fragmento.','15cm'),
 ('### Lo que queda','antes',N+'linea.png','Lo local en el tiempo: normas, jurisprudencia, Procuraduría y doctrina del capítulo 2.','14cm'),
 ('Aplicada a lo local, la técnica ordena','despues',N+'zonas.png','Las tres zonas del concepto de lo local, con los ejemplos del capítulo 2.','15cm'),
 ('Por la misma razón, cada tema distingue','despues',N+'flujo.png','Ante una necesidad: qué debe hacer el Gobierno Municipal.','14cm'),
 ('### Una célula','despues',F+'celula.png','La célula: el cantón visto desde las dos personas del núcleo.','15cm'),
 ('Cada tema responde una sola pregunta','despues',N+'tema.png','Cómo está hecho cada tema.','15cm'),
 ('Esas dos responsabilidades no deben confundirse','despues',N+'cadena.png','La cadena de obligaciones, de la Constitución a la persona servidora.','14cm'),
 ('Cuando la cadena se rompe, la persona tiene con qué repararla','despues',N+'recursos.png','Dos rutas para reparar la cadena: contra la decisión y contra la omisión.','15cm'),
 ('Las seis preguntas tienen una séptima detrás','despues',N+'preguntas.png','Seis preguntas para diagnosticar una municipalidad, y la séptima.','15cm')]
pos=[]
for a,modo,img,ley,w in figs:
    idx=[i for i,l in enumerate(L) if l.startswith(a)]
    assert len(idx)==1,(a,len(idx))
    pos.append((idx[0],modo,img,ley,w))
orden=sorted(range(len(pos)),key=lambda k:pos[k][0])
num={k:n+1 for n,k in enumerate(orden)}
for k in sorted(range(len(pos)),key=lambda k:-pos[k][0]):
    i,modo,img,ley,w=pos[k]
    linea=f'![Figura {num[k]}. {ley}]({img}){{width={w}}}'
    if modo=='despues': L[i+1:i+1]=['',linea]
    else: L[i:i]=[linea,'']
open(p,'w',encoding='utf-8').write('\n'.join(L))
