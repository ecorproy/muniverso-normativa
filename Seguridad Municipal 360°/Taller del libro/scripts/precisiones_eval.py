"""Precisiones de la evaluación de final64: destinatarias de los servicios, capacidad y coordinación, fuentes empíricas."""
B='/home/claude/libro'
def rd(c): return open(f'{B}/{c}/src/{c}.md',encoding='utf-8').read()
def wr(c,s): open(f'{B}/{c}/src/{c}.md','w',encoding='utf-8').write(s)
def rep(s,a,b):
    if b in s: return s
    assert s.count(a)==1,a[:60]; return s.replace(a,b)
s=rd('cap03')
s=rep(s,'El municipio lo forman los vecinos residentes; los servicios locales llegan a todo el que está en el cantón.',
 'El municipio lo forman los vecinos residentes; los servicios locales tienen como destinatarias potenciales a todas las personas que habitan el cantón o se encuentran en él, sin perjuicio de los requisitos que el ordenamiento establezca para acceder a determinadas prestaciones.')
s=rep(s,'que entonces consiste en procurarla y coordinar,',
 'que entonces consiste en procurarla y, mientras tanto, coordinar para que el servicio llegue, sin que la coordinación la libere de lo que le toca prestar,')
s=rep(s,'del Índice de Cumplimiento para la Mejora Pública 2026.',
 'del Índice de Cumplimiento para la Mejora Pública 2026. Los completan otras mediciones públicas, que se citan en los temas donde se usan: el Índice Municipal de Costa Rica del Instituto de Fomento y Asesoría Municipal, en sus ediciones de 2024 y 2025; el Índice de Competitividad Nacional 2026; el Índice Cantonal de Seguridad Ciudadana 2025, del Observatorio de la Violencia; el índice cantonal de desarrollo sostenible 2020-2022, del Ministerio de Planificación Nacional y Política Económica, y el capítulo ambiental del Informe Estado de la Nación 2026.')
wr('cap03',s)
s=rd('conclusion')
s=rep(s,'y los servicios locales llegan a todo el que está en el cantón.',
 'y los servicios locales tienen como destinatarias potenciales a todas las personas que están en el cantón, sin perjuicio de los requisitos que la ley fije para prestaciones como las becas o las ayudas temporales.')
wr('conclusion',s)
print('ok')
