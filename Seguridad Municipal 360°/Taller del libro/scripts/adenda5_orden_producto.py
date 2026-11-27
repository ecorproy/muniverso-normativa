import sys
from docx import Document
f=sys.argv[1]
d=Document(f); P=d.paragraphs
def para(start):
    return next(p for p in P if p.text.startswith(start))
a=para('Ninguna de las dos leyes define qué es un proceso'); assert len(a.runs)==1
old='La definición termina donde termina el servicio prestado: en alguien que recibe.'
assert old in a.runs[0].text
a.runs[0].text=a.runs[0].text.replace(old,'La definición termina donde termina el producto: en alguien que lo recibe.')
b=para('Queda la palabra en la que este libro insiste'); assert len(b.runs)==1
b.runs[0].text=('Queda el orden de las palabras, en el que este libro insiste. La ley enumera los procesos, proyectos, productos y servicios de la dependencia (Ley 2166, art. 48), pero la cadena del trabajo corre en otro orden: el proceso ordena la labor, el proyecto la concentra en una meta con plazo, el servicio es la prestación que ejecuta la dependencia y el producto es lo que recibe la persona. '
 'La propia norma lo deja ver cuando vincula el registro diario de cada persona servidora a "dichos procesos, proyectos y productos" (Ley 2166, art. 48) (Ley 10159, art. 29) y omite los servicios: lo que se registra es lo que llega a término. '
 'Leída conforme a la regla del artículo 10 de la Ley General de la Administración Pública (LGAP, art. 10), con el mandato de servir a cada administrado del artículo 114 (LGAP, art. 114) y con la finalidad de la Ley Marco, que es "asegurar la eficiencia y eficacia en la prestación de los bienes y servicios públicos" (Ley 10159, art. 1), la meta individual de una persona servidora municipal debería medirse por el producto que llegó efectivamente a las personas del cantón: la basura recogida, la acera construida, la solicitud resuelta en plazo. '
 'Un oficio archivado es una actividad interna, y solo cuenta cuando el expediente termina en un producto que una persona recibió. La pregunta que ordena la evaluación es qué recibió la persona. '
 'Es la misma pregunta que la gestión por procesos pone en su definición, cuando pide reordenar el trabajo buscando por qué y para quién se hace (Medina León et al., 2009, p. 70).')
d.save(f); print('ok')
