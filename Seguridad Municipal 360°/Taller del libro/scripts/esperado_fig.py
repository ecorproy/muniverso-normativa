# Inserta en un unido las líneas que Docs exporta por cada figura y compara sha y bytes.
import sys,hashlib,importlib.util
u,sha,nb=sys.argv[1],sys.argv[2],int(sys.argv[3])
F=[('Discapacidad, cultura, ambiente, trabajo, emergencias, presupuesto','d',1,'La acera: un metro y medio de concreto por donde pasan seis temas del libro.'),
 ('La red también se recupera, y casi siempre empieza por un fragmento','d',2,'Las seis formas en que muere la red y la regeneración desde un fragmento.'),
 ('## Lo que queda','a',3,'Lo local en el tiempo: normas, jurisprudencia, Procuraduría y doctrina del capítulo 2.'),
 ('Aplicada a lo local, la técnica ordena','d',4,'Las tres zonas del concepto de lo local, con los ejemplos del capítulo 2.'),
 ('Por la misma razón, cada tema distingue','d',5,'Ante una necesidad: qué debe hacer el Gobierno Municipal.'),
 ('## Una célula','d',6,'La célula: el cantón visto desde las dos personas del núcleo.'),
 ('Cada tema responde una sola pregunta','d',7,'Cómo está hecho cada tema.'),
 ('Las dos leyes no están solas en una municipalidad','d',8,'La evaluación del desempeño en la Ley 2166, la Ley Marco de Empleo Público, el Código Municipal y el Código de Trabajo.'),
 ('De esa revisión salen rasgos','d',9,'Anatomía de un proceso y mapa de procesos de una municipalidad.'),
 ('Los mismos autores proponen que identificar','d',10,'Del plan a la persona: cómo se encadenan el plan, los procesos, las metas, la evaluación y la rendición de cuentas.'),
 ('La Ley Marco agrega además una consecuencia','d',11,'Cómo se compone la calificación y qué produce.'),
 ('En una municipalidad estas reglas tienen un límite','d',12,'Quién fija cómo se evalúa al personal municipal.'),
 ('Esa lectura tiene apoyo técnico','d',13,'Producto interno y servicio prestado.'),
 ('Esas dos responsabilidades no deben confundirse','d',14,'La cadena de obligaciones, de la Constitución a la persona servidora.'),
 ('Cuando la cadena se rompe, la persona tiene con qué repararla','d',15,'Dos rutas para reparar la cadena: contra la decisión y contra la omisión.'),
 ('Las seis preguntas tienen una séptima detrás','d',16,'Seis preguntas para diagnosticar una municipalidad, y la séptima.')]
P=open(u,encoding='utf-8').read().replace('[','\\[').replace(']','\\]').replace('_','\\_').split('\n\n')
out=[]
for p in P:
    hit=[f for f in F if p.startswith(f[0])]
    blk=lambda f:[f'&#91;image: Figura {f[2]}. {f[3]}\\]',f'*Figura {f[2]}. {f[3]}*']
    for f in hit:
        if f[1]=='a': out+=blk(f)
    out.append(p)
    for f in hit:
        if f[1]=='d': out+=blk(f)
t='\n\n'.join(out).encode()
print('IDÉNTICO' if hashlib.sha256(t).hexdigest()==sha and len(t)==nb else f'DISTINTO {len(t)} {hashlib.sha256(t).hexdigest()[:12]}')
