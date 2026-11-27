import sys, copy
from docx import Document
f_in,f_out=sys.argv[1],sys.argv[2]
d=Document(f_in); P=d.paragraphs
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
XS='{http://www.w3.org/XML/1998/namespace}space'
def par(start):
    c=[p for p in P if p.text.startswith(start)]; assert len(c)==1,(start,len(c)); return c[0]
def rep(start, old, new):
    p=par(start); hits=[r for r in p.runs if old in r.text]
    assert len(hits)==1,(start,old,len(hits)); hits[0].text=hits[0].text.replace(old,new,1)
# 1. orden en la voz del libro
rep('El Código Municipal tiene ese momento' if False else 'Los mismos autores proponen que identificar','los productos y servicios de la dependencia','los servicios y productos de la dependencia')
cambios=[
 ('Del mismo método salen tres herramientas','entre los procesos, productos y servicios de la dependencia','entre los procesos, servicios y productos de la dependencia'),
 ('En uno y otro caso, los deberes realmente','indicadores de productos y servicios prestados','indicadores de servicios prestados y productos'),
 ('La misma lógica alcanza a cada persona servidora','entre los procesos, proyectos, productos y servicios de la dependencia','entre los procesos, proyectos, servicios y productos de la dependencia'),
 ('Dos de los estudios que revisan tratan','Si las metas de productos y servicios prestados','Si las metas de servicios prestados y productos'),
 ('El cuarto eslabón es el empleo público','responde por metas de productos y servicios prestados','responde por metas de servicios prestados y productos'),
]
for s,o,n in cambios: rep(s,o,n)
p345=[p for p in P if 'lo que se califica con la escala municipal son metas de productos y servicios prestados' in p.text]; assert len(p345)==1
r=[r for r in p345[0].runs if 'metas de productos y servicios prestados' in r.text]; assert len(r)==1
r[0].text=r[0].text.replace('metas de productos y servicios prestados','metas de servicios prestados y productos')
# 2. salvedad de los lineamientos
rep('En una municipalidad estas reglas tienen un límite','y con eso la responsabilidad de que la evaluación mida bien queda también en el cantón.',
    'y con eso la responsabilidad de que la evaluación mida bien queda también en el cantón. La salvedad cubre a la familia propia de la municipalidad: si el Concejo y la Alcaldía dejan algunos puestos de servicios comunes bajo la rectoría nacional, a esos puestos sí les alcanzan los lineamientos de Mideplán (Ley 10159, art. 7).')
def nuevo(base,texto):
    el=copy.deepcopy(base._p); rs=el.findall(W+'r')
    for x in rs[1:]: el.remove(x)
    t=rs[0].find(W+'t'); t.text=texto; t.set(XS,'preserve'); return el
A=('El artículo 28 tiene la misma inversión. Funda la evaluación en "indicadores cuantitativos de cumplimiento de metas individuales de productos y servicios prestados" (Ley 10159, art. 28), pero en el orden del trabajo el superior define los procesos y proyectos, de ellos salen los servicios que la dependencia presta y los productos que recibe la persona, y la jefatura reparte unos y otros al inicio del año (Ley 10159, art. 29). '
   'La meta individual es esa porción asignada, con su plazo y su tiempo estimado, y el indicador mide si se cumplió. Por eso la meta no puede medir solo el servicio prestado: una inspección hecha o un expediente tramitado son actividad, y la meta se cumple cuando el producto llega. '
   'El principio de programación, que rige también para las municipalidades, pide que los presupuestos expresen "los objetivos, las metas y los productos que se pretenden alcanzar" (Ley N.° 8131, 2001, art. 5).')
q=par('Queda el orden de las palabras'); q._p.addnext(nuevo(q,A))
B=('La cadena necesita quien la arme. La ley reparte la responsabilidad entre el superior, que define (Ley 10159, art. 28), la jefatura, que distribuye y da seguimiento, y cada persona servidora, que registra a diario lo que hizo (Ley 10159, art. 29), pero ninguno de ellos, por sí solo, asegura que las metas individuales sumen el plan. Esa es la tarea del planificador institucional. '
   'El plan de desarrollo y el plan anual operativo que elabora la persona titular de la alcaldía y aprueba el Concejo "constituyen la base del proceso presupuestario" (CM, art. 13), y todo presupuesto público debe responder a los planes operativos institucionales (Ley 8131, art. 4). La Ley de Planificación Nacional incluye en su sistema a las unidades de planificación de las entidades públicas locales (Ley N.° 5525, 1974, art. 3). '
   'La persona profesional en planificación traduce el plan en procesos, servicios, productos y metas, arma con cada jefatura la ficha del proceso, diseña los indicadores y cuida que el sistema del artículo 29 registre lo que el plan prometió. No sustituye al superior, que conserva la responsabilidad de definir y dar seguimiento, pero sin ella el registro diario se reduce a una planilla de actividades sin relación con el plan que aprobó el Concejo.')
m=par('La misma lógica alcanza a cada persona servidora'); m._p.addnext(nuevo(m,B))
# 3. referencias: Ley 5525 y Ley 8131 antes de Ley N.° 10159 en la lista del capítulo
P=d.paragraphs
iq=next(i for i,p in enumerate(P) if p.text.startswith('Queda el orden de las palabras'))
iref=next(i for i,p in enumerate(P) if i>iq and p.text.startswith('Ley N.° 10159, Ley Marco de Empleo Público.'))
base=P[iref]
def ref(texto_ini):
    el=copy.deepcopy(base._p); rs=el.findall(W+'r')
    full=''.join((r.find(W+'t').text or '') for r in rs if r.find(W+'t') is not None)
    return el
for num,tit,anio,url in [('Ley N.° 5525,','Ley de Planificación Nacional','1974','https://sinalevi.go.cr/ResultadosNormativa/Informacion?param1=34439&param2=145310&param3=1'),
                          ('Ley N.° 8131,','Ley de la Administración Financiera de la República y Presupuestos Públicos','2001','https://sinalevi.go.cr/ResultadosNormativa/Informacion?param1=47258&param2=142574&param3=1')]:
    el=copy.deepcopy(base._p); rs=el.findall(W+'r'); ts=[r.find(W+'t') for r in rs]
    assert len(ts)==4
    ts[0].text=num; ts[2].text=tit
    ts[3].text=f'. ({anio}). Asamblea Legislativa de la República de Costa Rica. Sistema Costarricense de Información Jurídica. {url}'
    for x in ts: x.set(XS,'preserve')
    base._p.addprevious(el)
d.save(f_out); print('ok')
