import copy,sys,json
from docx import Document
from docx.shared import Cm
f=sys.argv[1]; d=Document(f)
R='/home/claude/recursos/png/'
info=json.load(open('/home/claude/temas_heads.json',encoding='utf-8'))
H12=('Heading 1','Heading 2'); H123=('Heading 1','Heading 2','Heading 3')
P=d.paragraphs
modelo=P[[i for i,p in enumerate(P) if p.style.name=='Image Caption' and p.text.startswith('Figura 1.')][0]-1]
def imagen(after_p,png,alt,ancho=16):
    d.add_picture(png,width=Cm(ancho))
    np_=d.paragraphs[-1]._p
    np_.getparent().remove(np_)
    ppr=modelo._p.pPr
    if ppr is not None:
        old=np_.pPr
        if old is not None: np_.remove(old)
        np_.insert(0,copy.deepcopy(ppr))
    for dp in np_.xpath('.//wp:docPr'): dp.set('descr',alt); dp.set('title',alt)
    after_p._p.addnext(np_)
def rango(texto,niveles=H12):
    ps=d.paragraphs
    hs=[k for k,p in enumerate(ps) if p.style.name in niveles and p.text.strip()==texto]
    assert len(hs)==1,(texto,len(hs)); h=hs[0]
    e=next((k for k in range(h+1,len(ps)) if ps[k].style.name in niveles),len(ps)); return ps,h,e
def fin_seccion(ps,h,e,inicio):
    k=[i for i in range(h,e) if ps[i].style.name=='Heading 3' and ps[i].text.startswith(inicio)]; assert len(k)==1,(inicio,len(k))
    j=next((i for i in range(k[0]+1,e) if ps[i].style.name in H123),e)
    return ps[j-1]
n=0
# capítulos
for tit,c in [('1. La red','cap01'),('2. Lo local en el artículo 169','cap02'),('3. El concepto','cap03'),('4. La persona en el centro','cap04'),('Conclusión. Volver al núcleo','conclusion')]:
    ps,h,e=rango(tit,('Heading 1',)); imagen(ps[h],R+f'{c}_mapa.png',f'Mapa del capítulo: {tit}'); n+=1
for start,png,alt in [('Del artículo 169 y de sus lectores queda una regla','cap02_sintesis.png','Lo esencial: la regla que deja el artículo 169'),('Lo local es todo interés y todo servicio','cap03_sintesis.png','Lo esencial: qué es lo local')]:
    ps=d.paragraphs; k=[i for i,p in enumerate(ps) if p.text.startswith(start)]; assert len(k)==1,start
    imagen(ps[k[0]],R+png,alt); n+=1
# cuadrantes
for q,tit in enumerate(['Cuadrante I. Vida','Cuadrante II. Dignidad','Cuadrante III. Protección especial','Cuadrante IV. Bienestar y entorno'],1):
    ps,h,e=rango(tit,('Heading 1',)); imagen(ps[h],R+f'cuadrante_{q}.png',f'Portada del {tit}'); n+=1
# temas
GRAF={'t04':'La tabla de datos que acompaña el índice de 2025 contesta','t29':'La tabla de datos que acompaña el índice de 2025 baja','t10':'Las respuestas de 2025 muestran cuánto falta'}
for num in range(1,37):
    t=f't{num:02d}'; tit=info[t]['title']; nom=tit.split('. ',1)[1]
    ps,h,e=rango(tit)
    lista_after=fin_seccion(ps,h,e,'Cómo hace')
    caso_after=fin_seccion(ps,h,e,'El caso')
    graf_after=None
    if t in GRAF:
        k=[i for i in range(h,e) if ps[i].text.startswith(GRAF[t])]; assert len(k)==1,t; graf_after=ps[k[0]]
    if graf_after is not None: imagen(graf_after,R+f'{t}_grafico.png',f'Tema {num}: gráfico con datos del IGSM 2025'); n+=1
    imagen(lista_after,R+f'{t}_lista.png',f'Tema {num}. {nom}: revise en su municipalidad'); n+=1
    imagen(caso_after,R+f'{t}_caso.png',f'Tema {num}. {nom}: el caso, paso a paso'); n+=1
    imagen(ps[h],R+f'{t}_mapa.png',f'Tema {num}. {nom}: mapa del tema'); n+=1
d.save(f); print('imágenes insertadas:',n)
