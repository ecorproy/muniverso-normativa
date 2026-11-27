import copy, sys
from docx import Document
src, out = sys.argv[1], sys.argv[2]
d = Document(src)
P = d.paragraphs
i_ancla = next(i for i,p in enumerate(P) if p.text.startswith('Los mismos autores proponen que identificar'))
i_lim = next(i for i,p in enumerate(P) if p.text.startswith('En una municipalidad estas reglas tienen un límite'))
assert i_lim > i_ancla

N = [
'La clasificación de la figura 9 tiene también un efecto jurídico, porque la Ley Marco agrupa a las personas servidoras por la función que cumplen. Crea un único régimen general de empleo público formado por familias de puestos que se aplican "según las funciones que ejecute su personal" (Ley 10159, art. 13). Los entes con autonomía de gobierno u organizativa, entre ellos la municipalidad, tienen cada uno su propia familia, integrada por las personas servidoras con funciones administrativas, profesionales o técnicas "que sean exclusivas y excluyentes para el ejercicio de las competencias constitucionalmente asignadas" (Ley 10159, art. 13). Quién entra en ella lo determina el propio ente, y esas relaciones de empleo quedan fuera de la rectoría de Mideplán (Ley 10159, art. 6). Los demás puestos de la municipalidad siguen en las familias generales, bajo esa rectoría.',
'La frontera la trazó la Sala Constitucional al examinar el proyecto de ley. Declaró contrario a la Constitución, en cuanto a las municipalidades, el artículo 13 del proyecto, junto con otros, "por violación a la autonomía de gobierno de las municipalidades, consagrada constitucionalmente" (voto 2021-017098, como se citó en Decreto Ejecutivo N.° 43952, 2023, considerando IX). En el mismo voto separó tres grupos de personal. Quienes participan de la gestión pública relativa a los fines constitucionales del ente, y el personal de apoyo profesional o técnico que el propio ente defina, no pueden quedar bajo el poder de dirección del Poder Ejecutivo, porque forman "un núcleo duro, un indisponible para el Poder Ejecutivo" (voto 2021-017098, como se citó en Procuraduría General de la República, dictamen C-136-2026, 2026, apartado IV). Los servicios administrativos básicos, auxiliares y comunes a toda la Administración sí pueden someterse a esa dirección, y establecer cuáles son corresponde de manera exclusiva y excluyente al Concejo y a la persona titular de la alcaldía (voto 2021-017098, como se citó en C-136-2026, ap. IV).',
'Esa división coincide con el mapa de procesos. Los procesos estratégicos son el gobierno del cantón, a cargo del Concejo y de la Alcaldía (CM, arts. 13 y 17), y los operativos son los servicios locales mismos, cuya administración la Constitución confía al Gobierno Municipal (CP, art. 169). Las personas que trabajan en unos y otros participan de la gestión pública relativa a los fines constitucionales del ente y forman el núcleo de la familia municipal. La decisión está en los procesos de apoyo. Una parte del apoyo es necesaria para ejercer la competencia, como la proveeduría que compra el camión de la recolección o la unidad de presupuesto que financia el servicio, y el ente puede incluirla en su familia. Otra parte es común a cualquier institución pública, y es la que el Concejo y la Alcaldía pueden dejar bajo la rectoría nacional. El mapa no toma esa decisión, pero muestra dónde está y le da al acto que la adopta un motivo verificable, que debe existir tal y como se tomó en cuenta para dictarlo (LGAP, art. 133).',
'La determinación puede hacerse por funciones y no por una lista de plazas. El Directorio de la Asamblea Legislativa acordó que la familia legislativa la integran las funciones y labores administrativas, profesionales y técnicas de su personal, con la sola exclusión del personal sujeto a la ley de incentivos médicos, y no enumeró puestos, con lo que hizo "una determinación funcional y estructural" (C-136-2026, ap. IV). La Procuraduría tuvo por cumplido así el deber de definir los puestos exclusivos y excluyentes, pero advirtió que la exclusión "es únicamente respecto de la rectoría de MIDEPLAN" (C-136-2026, ap. V) y no de la ley, cuyas reglas siguen obligando a toda la familia. Pertenecer a una familia distinta tampoco libra de las normas generales. El plan para nombrar en propiedad las plazas interinas alcanza a todos los órganos y entes cubiertos por la ley, incluidas las fuerzas de policía, que la ley agrupa en otra familia (Procuraduría General de la República, dictamen C-078-2025, 2025, conclusión). Una municipalidad puede usar el mismo criterio material, y el mapa de procesos le da contenido: su familia puede definirse como el personal de los procesos estratégicos y operativos más el de apoyo que el Concejo y la Alcaldía declaren necesario para ellos.',
'Los artículos 32 y 33 de la Ley Marco llevan la clasificación del proceso al puesto. Dentro de su familia, la municipalidad define los grados, cada uno de los cuales agrupa puestos "con perfil similar" (Ley 10159, art. 32), y desarrolla la clasificación de esos puestos en familias y grados (Ley 10159, art. 33). Los puestos que quedan fuera de la familia deben tener un manual detallado en el formato que especifique Mideplán, con descripciones que reflejen "los deberes realmente desempeñados" (Ley 10159, art. 33). El Código Municipal ya exigía un Manual Descriptivo de Puestos General, cuyo diseño está a cargo de la Unión Nacional de Gobiernos Locales, y prohíbe crear plazas cuyo perfil ocupacional no esté en él (CM, art. 129). Las dos normas pueden leerse juntas. La Procuraduría sostuvo que la rectoría de Mideplán no suprimió, sin norma expresa, las competencias técnicas que la ley ya había dado a otro órgano sobre los manuales de puestos, porque la derogación tácita exige una incompatibilidad que impida aplicar una norma sin desaplicar la otra (Procuraduría General de la República, dictamen C-016-2024, 2024, apartado II). Con el mismo razonamiento cabe sostener que el formato nacional del artículo 33 no desplaza el manual que el Código Municipal confía al régimen municipal.',
'En uno y otro caso, los deberes realmente desempeñados son la parte de los procesos que la jefatura asigna a cada persona servidora (Ley 10159, art. 29), y la ficha de cada proceso es la fuente más fiel para describirlos. La progresión salarial dentro de un grado "siempre estará supeditada a una evaluación satisfactoria del desempeño profesional" (Ley 10159, art. 32), y esa evaluación se hace con los indicadores de productos y servicios prestados que salen del mismo mapa (Ley 10159, art. 28). La clasificación toca también la remuneración, porque las directrices anuales de Mideplán sobre la progresión dentro de los grados no alcanzan a las personas de la familia propia del ente (Ley 10159, art. 32). El Código Municipal pide que la carrera administrativa propicie "la correspondencia entre la responsabilidad y las remuneraciones" (CM, art. 124). El mapa de procesos es el instrumento que permite saber cuál es esa responsabilidad.',
]

def clon_texto(base, texto):
    el = copy.deepcopy(base._p)
    runs = el.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
    for r in runs[1:]: el.remove(r)
    t = runs[0].find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
    t.text = texto
    t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    return el

ancla = P[i_ancla]
prev = ancla._p
for txt in N:
    el = clon_texto(ancla, txt)
    prev.addnext(el); prev = el

# párrafo del límite: primera mención del voto y del C-136 ya ocurre arriba
pl = P[i_lim]; assert len(pl.runs)==1
t = pl.runs[0].text
t2 = t.replace('Al examinar el proyecto que se convirtió en la Ley Marco, la Sala Constitucional sostuvo','En ese mismo voto, la Sala Constitucional sostuvo')
t2 = t2.replace('(Procuraduría General de la República, dictamen C-136-2026, 2026, apartado IV)','(voto 2021-017098, como se citó en C-136-2026, ap. IV)')
assert t2 != t and t2.count('C-136-2026') == t.count('C-136-2026')
pl.runs[0].text = t2

# referencias del capítulo
P = d.paragraphs
i136 = next(i for i,p in enumerate(P) if i>i_lim and p.text.startswith('Procuraduría General de la República. (2026, 17 de agosto). Dictamen C-136-2026'))
i084 = i136
while P[i084-1].text.startswith('Procuraduría General de la República.'): i084 -= 1
def ref_pgr(fecha, num, param):
    el = copy.deepcopy(P[i136]._p)
    W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    rs = el.findall(W+'r'); ts=[r.find(W+'t') for r in rs]
    ts[0].text = f'Procuraduría General de la República. ({fecha}).'
    ts[2].text = f'Dictamen {num}'
    ts[3].text = f'. Sistema Costarricense de Información Jurídica. https://sinalevi.go.cr/ResultadosPronunciamiento/Informacion?param1={param}&param2=0'
    return el
a = ref_pgr('2024, 12 de febrero','C-016-2024','24246')
b = ref_pgr('2025, 21 de abril','C-078-2025','24934')
P[i084]._p.addprevious(a); P[i084]._p.addprevious(b)

# Decreto 43952: copiar la entrada que ya existe en otro capítulo
P = d.paragraphs
dec = next(p for p in P if p.text.startswith('Decreto Ejecutivo N.° 43952, Reglamento a la Ley Marco'))
# ubicar la lista del capítulo: desde el encabezado Referencias anterior a i136
i136 = next(i for i,p in enumerate(P) if i>i_lim and p.text.startswith('Procuraduría General de la República. (2026, 17 de agosto). Dictamen C-136-2026'))
ini = max(i for i in range(i136) if P[i].text.strip()=='Referencias')
ya = any(P[i].text.startswith('Decreto Ejecutivo N.° 43952') for i in range(ini, i136))
if not ya:
    j = next(i for i in range(ini+1, i136) if P[i].text and P[i].text.lower() > 'decreto ejecutivo')
    P[j]._p.addprevious(copy.deepcopy(dec._p))
    print('Decreto insertado antes de:', P[j].text[:60])
d.save(out)
print('ok', i_ancla, i_lim)
