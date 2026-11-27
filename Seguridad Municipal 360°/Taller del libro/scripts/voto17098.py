p='/home/claude/libro/cap04/src/cap04.md'; t=open(p,encoding='utf-8').read().split('\n\n')
i=[k for k,x in enumerate(t) if x.startswith('Esa división coincide con el mapa de procesos')]; assert len(i)==1
nuevo=('La decisión sobre el apoyo tiene, en el mismo voto, un argumento para mirar la planilla entera. En razones adicionales, la magistrada Picado Brenes se apartó de la división en grupos y sostuvo que '
 '"todo el personal que labora en las municipalidades, desde el puesto más humilde hasta el cargo jerárquico más alto, es absolutamente indispensable para el ejercicio de la función pública local" [[V:2021-017098:considerando XIII]]. '
 'Su ejemplo coincide con el de este libro: sin la labor de quienes recogen la basura o hacen la limpieza, el Concejo y la Alcaldía no podrían cumplir las metas propuestas en beneficio de los intereses locales [[V:2021-017098:considerando XIII]]. '
 'Son razones de una magistrada y no la regla del voto, que sigue siendo la de los grupos. Pero el Concejo y la Alcaldía, cuando deciden sobre el apoyo, pueden tomarlas como motivo para incluir en la familia municipal a todo el personal que sostiene los servicios.')
t.insert(i[0]+1,nuevo)
a='La rectoría del Poder Ejecutivo no alcanza a fijar cómo evalúa una municipalidad a su personal.'
j=[k for k,x in enumerate(t) if a in x]; assert len(j)==1
t[j[0]]=t[j[0]].replace(a,a+' La magistrada Picado Brenes, en razones adicionales a ese voto, dio el motivo de fondo: "Absurdo sería pretender que los intereses locales sean determinados por las corporaciones municipales, pero su atención y cumplimiento sean llevados a cabo por personas que sirven en función de directrices, reglamentos y disposiciones que provienen de un ente centralizado" [[V:2021-017098:considerando XIII]].')
open(p,'w',encoding='utf-8').write('\n\n'.join(t)); print('ok')
