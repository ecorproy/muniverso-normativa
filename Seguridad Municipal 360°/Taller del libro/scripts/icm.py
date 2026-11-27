B='/home/claude/libro/'
def edit(f,a,b,mode='replace'):
    t=open(B+f,encoding='utf-8').read(); assert t.count(a)==1,(f,a[:40])
    t=t.replace(a,b if mode=='replace' else a+b); open(B+f,'w',encoding='utf-8').write(t)
# cap04: párrafo nuevo después del planificador
t=open(B+'cap04/src/cap04.md',encoding='utf-8').read().split('\n\n')
i=[k for k,x in enumerate(t) if x.startswith('La cadena necesita quien la arme')]; assert len(i)==1
nuevo=('La Contraloría General de la República mide una cadena parecida en su propio terreno. Su Índice de Cumplimiento para la Mejora Pública evalúa cómo atiende cada institución las disposiciones y órdenes que le gira en sus productos de fiscalización [[O:ICM:p. 1]]. '
 'La mitad del puntaje es la eficacia, que califica cada disposición según su grado de avance [[O:ICM-F1:p. 1]]. '
 'Un 30 % es la eficiencia, que compara el plazo original previsto por el órgano contralor con el tiempo que la institución empleó en atender la disposición [[O:ICM-F2:p. 1]]. '
 'El resto se reparte en partes iguales entre las prácticas de estrategia y gestión de datos y las de cultura y liderazgo, que cada institución autoevalúa [[O:ICM-F3:p. 1]] [[O:ICM-F4:p. 1]]. '
 'Entre esas prácticas están designar a una persona que coordine internamente el seguimiento e informe a sus superiores sobre el estado de cada producto [[O:ICM-BP:p. 3]], y que las disposiciones de la Contraloría "se incorporan en instrumentos de planificación institucional, asegurando su atención prioritaria" [[O:ICM-BP:p. 4]]. '
 'Es la tarea del planificador aplicada a un deber concreto: llevarlo al plan, con plazo y responsable. La eficiencia del índice, además, es la medida que este libro propone para la meta individual: el plazo previsto frente al plazo real.')
t.insert(i[0]+1,nuevo); open(B+'cap04/src/cap04.md','w',encoding='utf-8').write('\n\n'.join(t))
# conclusión
edit('conclusion/src/conclusion.md','un reglamento, un equipo, una partida.','un reglamento, un equipo, una partida. El Índice de Cumplimiento para la Mejora Pública de la Contraloría mide otra cosa: con qué eficacia y en qué plazo atiende la institución las disposiciones del órgano contralor [[O:ICM:p. 1]]. Cumplir una disposición puede mejorar un servicio, pero el índice registra el cumplimiento.')
# capítulo 3, fuentes
edit('cap03/src/cap03.md','Los indicadores municipales vienen del Índice de Gestión de Servicios Municipales 2025 de la Contraloría.','Los indicadores municipales vienen del Índice de Gestión de Servicios Municipales 2025 de la Contraloría, y la medición del cumplimiento de sus disposiciones, del Índice de Cumplimiento para la Mejora Pública 2026.')
print('ok')
