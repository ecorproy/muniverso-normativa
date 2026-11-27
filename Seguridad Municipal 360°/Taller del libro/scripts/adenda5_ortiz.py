import sys, copy
from docx import Document
f_in,f_out=sys.argv[1],sys.argv[2]
d=Document(f_in); P=d.paragraphs
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
idx=lambda s: next(i for i,p in enumerate(P) if p.text.startswith(s))
# 1. mover los seis párrafos de familias después de la leyenda de la figura 10
i0=idx('La clasificación de la figura 9 tiene también un efecto jurídico')
i5=idx('En uno y otro caso, los deberes realmente desempeñados')
assert i5-i0==5
seis=[P[k]._p for k in range(i0,i5+1)]
cap10=next(p for p in P if p.style.name=='Image Caption' and p.text.startswith('Figura 10.'))
assert P[i0-1].text.startswith('Los mismos autores proponen') and P[i5+1].text.startswith('De ese mismo deber')
ant=cap10._p
for el in seis:
    ant.addnext(el); ant=el
# 2. párrafo nuevo después de los seis
def nuevo(base_p, texto):
    el=copy.deepcopy(base_p)
    rs=el.findall(W+'r')
    for r in rs[1:]: el.remove(r)
    t=rs[0].find(W+'t'); t.text=texto; t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    return el
B=('La misma lógica alcanza a cada persona servidora. Ortíz-Fernandez et al. (2024) revisaron treinta estudios publicados entre 2011 y 2022 sobre gestión por procesos y recogen, entre las ventajas del enfoque, que "Cada empleado entiende su papel en cada proceso y sabe cómo contribuir para lograr los objetivos de la organización" (Aval, 2018, como se citó en Ortíz-Fernandez et al., 2024, p. 13). Es lo que la jefatura procura cuando distribuye a cada persona entre los procesos, proyectos, productos y servicios de la dependencia (Ley 10159, art. 29). '
   'La mejora tiene también sus responsables: "La responsabilidad de mejorar un proceso recae en sus participantes directos, pero siempre con la colaboración de toda la organización" (Domingo y Fernandez-Baca, 2016, como se citó en Ortíz-Fernandez et al., 2024, p. 13). El Código Municipal formula ese deber para cada servidor, que debe sugerir ante la instancia correspondiente lo que considere adecuado para el mejor desempeño de sus labores (CM, art. 156). '
   'La revisión advierte que la mayoría de las instituciones muestran una fuerte resistencia a esta transformación (Flores-Rueda et al., 2020, como se citó en Ortíz-Fernandez et al., 2024, p. 9), y recoge que la herramienta ha demostrado su eficacia tanto en empresas privadas como en organizaciones públicas (Aranda et al., 2018, como se citó en Ortíz-Fernandez et al., 2024, p. 9). '
   'Los autores proponen no ver la gestión por procesos como una tarea aislada, "sino como una mentalidad que impulsa el día a día de la empresa" (Ortíz-Fernandez et al., 2024, p. 8). En una municipalidad ese día a día no se mide por la rentabilidad, que es lo que la revisión encuentra en las empresas (Ortíz-Fernandez et al., 2024, p. 19), sino por el producto que recibe cada persona del cantón.')
eb=nuevo(seis[-1],B); seis[-1].addnext(eb)
# 3. párrafo nuevo después de «Queda el orden de las palabras…»
P=d.paragraphs
q=P[idx('Queda el orden de las palabras')]
A=('La literatura más reciente sobre gestión por procesos confirma ese orden. La revisión sistemática de Ortíz-Fernandez et al. (2024) recoge una definición en la que el proceso termina en lo que se entrega: es "una secuencia de actividades o pasos interconectados que, al llevarse a cabo, conducen a un resultado o a la generación de un producto específico" (Moyado, 2011, como se citó en Ortíz-Fernandez et al., 2024, p. 18). '
   'En la misma línea, un proceso combina eventos, actividades y decisiones que, en conjunto, "resultan en un producto final que agrega valor a los clientes de una organización" (Dumas et al., 2012, como se citó en Ortíz-Fernandez et al., 2024, p. 18). '
   'Entre los rasgos del enfoque, la revisión destaca "la búsqueda constante del propósito y beneficiario del trabajo realizado" (Medina et al., 2019, como se citó en Ortíz-Fernandez et al., 2024, p. 12). En el gobierno local, el beneficiario es la persona del cantón, y lo que recibe es el producto.')
ea=nuevo(q._p,A); q._p.addnext(ea)
# 4. referencia
P=d.paragraphs
med=next(p for p in P if p.text.startswith('Medina León, A., Nogueira Rivera') and P.index(p)>idx('Queda el orden'))
r=copy.deepcopy(med._p); rs=r.findall(W+'r'); ts=[x.find(W+'t') for x in rs]
ts[0].text='Ortíz-Fernandez, J., Baldeón-Tovar, M., Medina-Pelaiza, L., Ortíz-Huamán, C., & Godiño-Poma, M. (2024). Gestión por procesos en las empresas. Una revisión sistémica.'
ts[2].text='Gestionar: Revista de Empresa y Gobierno, 4'
ts[3].text='(1), 7-22. https://doi.org/10.35622/j.rg.2024.01.001'
for t in ts: t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
med._p.addnext(r)
d.save(f_out); print('ok')
