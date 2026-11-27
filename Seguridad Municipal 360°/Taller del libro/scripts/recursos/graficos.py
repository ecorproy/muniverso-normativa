import openpyxl,collections,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':13,'axes.edgecolor':'#6B7480','axes.labelcolor':'#1E2A38','xtick.color':'#1E2A38','ytick.color':'#1E2A38'})
X='/home/claude/repo/360/Seguridad Municipal 360°/Criterios CGR/IGSM 2025 - tabla de datos (sitio web).xlsx'
wb=openpyxl.load_workbook(X,data_only=True); ws=wb['Distrit.Cobert y Recurso, Vulne']
rows=[r for r in ws.iter_rows(min_row=2,values_only=True) if r[0]]
NIV=['Mayor','Medio','Bajo','Muy bajo']; ET=['Desarrollo\nmayor','Desarrollo\nmedio','Desarrollo\nbajo','Desarrollo\nmuy bajo']
FUENTE='Fuente: CGR, tabla de datos del IGSM 2025 (hoja de distritos); clasificación según el índice de desarrollo social 2023 de Mideplán.'
def cab(fig,t,sub):
    fig.text(0.04,0.95,t,fontsize=19,fontweight='bold',color='#1E2A38',va='top')
    fig.text(0.04,0.885,sub,fontsize=13,style='italic',color='#44505F',va='top')
    fig.text(0.04,0.03,FUENTE,fontsize=10,style='italic',color='#6B7480')
# Tema 29: cobertura de la recolección por nivel de desarrollo
ct=collections.Counter((r[2],r[3]) for r in rows)
cats=[('Total','Cobertura total','#4F7942'),('Parcial','Cobertura parcial','#E9C878'),('Administración no cuenta con la información','Sin información','#9E2A2B')]
fig,ax=plt.subplots(figsize=(11,6.2),dpi=190); fig.subplots_adjust(left=0.17,right=0.97,top=0.78,bottom=0.2)
left=[0]*4
for k,lab,c in cats:
    v=[ct[(n,k)] for n in NIV]; tot=[sum(ct[(n,kk)] for kk,_,_ in cats) for n in NIV]
    p=[100*a/b for a,b in zip(v,tot)]
    ax.barh(ET,p,left=left,color=c,label=lab,height=0.62,edgecolor='white')
    for i,(pp,a) in enumerate(zip(p,v)):
        if pp>7: ax.text(left[i]+pp/2,i,f'{a}',ha='center',va='center',color='white' if c!='#E9C878' else '#1E2A38',fontsize=13,fontweight='bold')
        elif a>0: ax.text(left[i]+pp/2,i-0.42,f'{a}',ha='center',va='bottom',color='#1E2A38',fontsize=12,fontweight='bold')
    left=[a+b for a,b in zip(left,p)]
for i,n in enumerate(NIV):
    ax.text(101,i,f'{sum(ct[(n,k)] for k,_,_ in cats)} distritos',va='center',fontsize=11,color='#44505F')
ax.invert_yaxis(); ax.set_xlim(0,118); ax.set_xticks([0,25,50,75,100]); ax.set_xticklabels(['0 %','25 %','50 %','75 %','100 %'])
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.legend(ncol=3,loc='upper left',bbox_to_anchor=(0,1.13),frameon=False,fontsize=12)
cab(fig,'Recolección de residuos ordinarios: ¿llega a cada distrito?','Distritos según la cobertura que informó la municipalidad (números dentro de las barras).')
fig.savefig('/home/claude/recursos/png/t29_grafico.png'); plt.close(fig)
# Tema 10: falta de información según desarrollo
fig,ax=plt.subplots(figsize=(11,5.6),dpi=190); fig.subplots_adjust(left=0.1,right=0.97,top=0.76,bottom=0.24)
p=[100*ct[(n,'Administración no cuenta con la información')]/sum(ct[(n,k)] for k,_,_ in cats) for n in NIV]
b=ax.bar(ET,p,color=['#DCE8F4','#9DBAD8','#E3A48F','#9E2A2B'],edgecolor='#1E2A38',width=0.6)
for i,n in enumerate(NIV):
    a=ct[(n,'Administración no cuenta con la información')]; t=sum(ct[(n,k)] for k,_,_ in cats)
    ax.text(i,p[i]+2,f'{a} de {t}',ha='center',fontsize=13,fontweight='bold',color='#1E2A38')
ax.set_ylim(0,85); ax.set_yticks([0,20,40,60,80]); ax.set_yticklabels(['0 %','20 %','40 %','60 %','80 %'])
for s in ('top','right'): ax.spines[s].set_visible(False)
cab(fig,'Donde menos se sabe a quién se sirve','Distritos en que la municipalidad no cuenta con la información de cobertura de la recolección.')
fig.savefig('/home/claude/recursos/png/t10_grafico.png'); plt.close(fig)
# Tema 4: policía y vigilancia por nivel de desarrollo
fig,ax=plt.subplots(figsize=(11,6),dpi=190); fig.subplots_adjust(left=0.1,right=0.97,top=0.76,bottom=0.22)
import numpy as np
x=np.arange(4); w=0.36
for j,(col,lab,c) in enumerate([(17,'Policía municipal','#1F4E79'),(19,'Vigilancia con soluciones tecnológicas','#2F86AE')]):
    v=[sum(1 for r in rows if r[2]==n and r[col]=='SI') for n in NIV]; t=[sum(1 for r in rows if r[2]==n) for n in NIV]
    p=[100*a/bb for a,bb in zip(v,t)]
    ax.bar(x+(j-0.5)*w,p,w,color=c,label=lab)
    for i in range(4): ax.text(x[i]+(j-0.5)*w,p[i]+1.5,f'{v[i]} de {t[i]}',ha='center',fontsize=11,color='#1E2A38')
ax.set_xticks(x); ax.set_xticklabels(ET); ax.set_ylim(0,95); ax.set_yticks([0,25,50,75]); ax.set_yticklabels(['0 %','25 %','50 %','75 %'])
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.legend(frameon=False,loc='upper right',fontsize=12)
cab(fig,'Protección municipal según el desarrollo del distrito','Distritos con cobertura de cada servicio, según la tabla de la Contraloría.')
fig.savefig('/home/claude/recursos/png/t04_grafico.png'); plt.close(fig)
print('ok')
