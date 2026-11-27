import sys
p=sys.argv[1]; t=open(p,encoding='utf-8').read()
if 'Ortíz-Fernandez et al., 2024' in t: print('ya estaba'); sys.exit()
F="/home/claude/libro/fuentes/doctrina/ortiz_fernandez_2024_pag.txt"
REF="Ortíz-Fernandez, J., Baldeón-Tovar, M., Medina-Pelaiza, L., Ortíz-Huamán, C., & Godiño-Poma, M. (2024). Gestión por procesos en las empresas. Una revisión sistémica. *Gestionar: Revista de Empresa y Gobierno*, *4*(1), 7-22. https://doi.org/10.35622/j.rg.2024.01.001"
lin=[f"    'Ortíz-Fernandez et al., 2024': dict(file='{F}',\n        ref='{REF}'),"]
for a in ['Moyado, 2011','Dumas et al., 2012','Medina et al., 2019','Aval, 2018','Domingo y Fernandez-Baca, 2016','Flores-Rueda et al., 2020','Aranda et al., 2018']:
    lin.append(f"    '{a}, como se citó en Ortíz-Fernandez et al., 2024': dict(file='{F}', alias='Ortíz-Fernandez et al., 2024',\n        ref='{REF}'),")
anc="    'Leiva Poveda, 2016': dict("
assert t.count(anc)==1
t=t.replace(anc,'\n'.join(lin)+'\n'+anc)
open(p,'w',encoding='utf-8').write(t); print('ok')
