"""Extrae, por unidad, cada fuente citada (macro o doctrina manual), sus localizadores,
formas completa y abreviada, y el texto de su referencia."""
import os,sys,re,json
os.environ['SRC']='/tmp/none'; os.environ['OUT']='/tmp/bl_out'; os.environ['CITA']='corta'
sys.path.insert(0,'/home/claude/division')
import bl_mod as B
L='/home/claude/libro/'
UNIDADES=['intro','cap01','cap02','cap03','cap04']+[f't{i:02d}' for i in range(1,37)]+['conclusion','anexos']
def tomo(u): return 'I' if u in ('intro','cap01','cap02','cap03','cap04') or (u[0]=='t' and int(u[1:])<=18) else 'II'
def etiqueta(u):
    if u=='intro': return 'introducción'
    if u.startswith('cap'): return 'capítulo '+str(int(u[3:]))
    if u[0]=='t': return 'tema '+str(int(u[1:]))
    return {'conclusion':'conclusión','anexos':'anexos'}[u]
ref_de={}   # id de fuente -> (clave cited, texto)
def ident(macro):
    p=[x.strip() for x in macro.replace('!','').split(':')]
    if p[0]=='CP': return 'CP'
    if p[0]=='VT': return 'V:'+p[2]
    return p[0]+':'+p[1]
def referencia(macro):
    i=ident(macro)
    if i not in ref_de:
        B.cited.clear()
        try: B.expand_larga(macro.replace('!',''))
        except Exception as e: ref_de[i]=('?', f'ERROR {e}'); return ref_de[i]
        it=list(B.cited.items())
        ref_de[i]=(it[-1][0], it[-1][1][1]) if it else ('?','')
    return ref_de[i]
apar=[]   # filas: fuente, unidad, localizador, forma
for u in UNIDADES:
    src=os.path.join(L,u,'src'); f=[x for x in os.listdir(src) if x.endswith('.md')][0]
    txt=open(os.path.join(src,f),encoding='utf-8').read()
    B.vistos.clear()
    for m in re.finditer(B.MACRO_RE,txt):
        for mac in [x for x in m.group(1).split('|') if x.strip()]:
            mac=mac.strip(); p=[x.strip() for x in mac.replace('!','').split(':')]
            loc=p[1] if p[0]=='CP' else (p[3] if p[0]=='VT' else (p[2] if len(p)>2 else ''))
            k,refx=referencia(mac)
            larga=B.expand_larga(mac.replace('!',''))
            forma=B.expand_corta(mac.replace('!',''),larga)
            apar.append(dict(fuente=ident(mac),clave=k,unidad=u,tomo=tomo(u),loc=loc,forma=forma,textual='!' in mac))
    # doctrina y documentos sin macro
    for k,v in B.MANUAL.items():
        if '('+k in txt or k in txt:
            kk=v.get('alias',k); ident_m='M:'+kk
            ref_de.setdefault(ident_m,('M'+kk,v['ref']))
            for mm in re.finditer(r'\('+re.escape(k)+r'((?:, [^()]*)?)\)',txt):
                apar.append(dict(fuente=ident_m,clave='M'+kk,unidad=u,tomo=tomo(u),loc=mm.group(1).lstrip(', '),forma='('+k+mm.group(1)+')',textual=False))
            if not re.search(r'\('+re.escape(k),txt):
                apar.append(dict(fuente=ident_m,clave='M'+kk,unidad=u,tomo=tomo(u),loc='',forma=k,textual=False))
json.dump(dict(apariciones=apar,referencias={k:v[1] for k,v in ref_de.items()},etiquetas={u:etiqueta(u) for u in UNIDADES}),open('fuentes.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(apar),'apariciones;',len(ref_de),'fuentes')
print('errores',[ (k,v) for k,v in ref_de.items() if v[1].startswith('ERROR') or not v[1]][:10])
