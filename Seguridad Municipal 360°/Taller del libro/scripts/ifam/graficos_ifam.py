import csv,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':13,'axes.edgecolor':'#6B7480','axes.labelcolor':'#1E2A38','xtick.color':'#1E2A38','ytick.color':'#1E2A38'})
R=list(csv.DictReader(open('/home/claude/ifam/ifam2025.csv',encoding='utf-8')))
def cab(fig,t,sub,fuente,ytop=0.965,ysub=0.94,yf=0.012):
    fig.text(0.04,ytop,t,fontsize=19,fontweight='bold',color='#1E2A38',va='top')
    fig.text(0.04,ysub,sub,fontsize=13,style='italic',color='#44505F',va='top')
    fig.text(0.04,yf,fuente,fontsize=10,style='italic',color='#6B7480')
# Conclusión: presupuesto por habitante
C=[r for r in R if r['codigo'].count('.')==1]
d=sorted([(float(r['pres2024'])/float(r['poblacion']),r['nombre']) for r in C])
import statistics as st; med=st.median(v for v,_ in d)
fig,ax=plt.subplots(figsize=(8,14.5),dpi=230); fig.subplots_adjust(left=0.29,right=0.9,top=0.905,bottom=0.075)
cols=['#9E2A2B' if n=='Alajuelita' else '#4F7942' if n=='Belén' else ('#B5543A' if v<med else '#1F4E79') for v,n in d]
ax.barh([n for _,n in d],[v/1000 for v,_ in d],color=cols,height=0.72)
ax.axvline(med/1000,color='#B07A12',lw=2,ls='--'); ax.text(med/1000+8,22,f'Mediana: {med/1000:,.0f} mil colones'.replace(',','.'),color='#B07A12',fontsize=12,va='top',fontweight='bold')
for i,(v,n) in enumerate(d):
    if n in ('Belén','Alajuelita'): ax.text(v/1000+6,i,f'{v/1000:,.0f} mil'.replace(',','.'),va='center',fontsize=12,fontweight='bold',color='#1E2A38')
ax.tick_params(axis='y',labelsize=12); ax.set_ylim(-0.7,len(d)-0.3)
ax.set_xlabel('Miles de colones por habitante')
for s in ('top','right'): ax.spines[s].set_visible(False)
cab(fig,'Presupuesto municipal por habitante','Presupuesto total 2024 de cada cantón entre su población.\nAzul: sobre la mediana; terracota: bajo ella.',
    'Fuente: IFAM, Índice Municipal de Costa Rica 2025 (fichas cantonales).\nElaboración propia. Sin concejos municipales de distrito.',yf=0.004)
fig.savefig('/home/claude/recursos/png/conclusion_grafico.png'); plt.close(fig)
# Tema 32: estado del plan regulador
cats=[('Vigente','Vigente','#4F7942'),('Actualizando','Actualizando','#2F86AE'),('Creando','Creando','#B07A12'),('Donado','Donado','#5B4B8A'),('SIN','Sin plan','#9E2A2B')]
cnt={k:sum(1 for r in R if (r['plan'] in ('SIN','Sin PR') if k=='SIN' else r['plan']==k)) for k,_,_ in cats}
fig,ax=plt.subplots(figsize=(11,5.6),dpi=190); fig.subplots_adjust(left=0.17,right=0.95,top=0.74,bottom=0.17)
labs=[l for _,l,_ in cats]; vals=[cnt[k] for k,_,_ in cats]
ax.barh(labs,vals,color=[c for *_,c in cats],height=0.62)
for i,v in enumerate(vals): ax.text(v+0.6,i,str(v),va='center',fontsize=14,fontweight='bold',color='#1E2A38')
ax.invert_yaxis(); ax.set_xlim(0,40); ax.set_xlabel('Territorios municipales (84 cantones y 7 concejos municipales de distrito)')
for s in ('top','right'): ax.spines[s].set_visible(False)
cab(fig,'¿En qué estado está el plan regulador?','Cómo lo registran las fichas cantonales de 2025, con datos de MIDEPLAN.',
    'Fuente: IFAM, Índice Municipal de Costa Rica 2025 (fichas cantonales). «Sin plan»: Carrillo y los 7 concejos municipales de distrito.',ytop=0.95,ysub=0.87,yf=0.025)
fig.savefig('/home/claude/recursos/png/t32_grafico.png'); plt.close(fig)
print(cnt, round(med))
