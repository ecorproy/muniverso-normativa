import re,glob,os,sys,json
R='/home/claude/repo/main'
MES=['','enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre']
def meta(f):
    t=open(f,encoding='utf-8').read(4000); d={}
    for k in ['numero','nombre','fecha','fecha_norma','hora','expediente','enlace','ente_emisor','titulo','institucion','consultante']:
        m=re.search(r'(?m)^'+k+r':\s*"([^"]*)"',t); d[k]=m.group(1) if m else ''
    return d
def fdate(s):
    m=re.match(r'(\d{4})-(\d{2})-(\d{2})',s) or None
    if m: y,mo,da=m.groups()
    else:
        m=re.match(r'(\d{2})/(\d{2})/(\d{4})',s)
        if not m: return None
        da,mo,y=m.groups()
    return int(y),int(mo),int(da)
out=[]
sala="2007-010102 2020-009186 2026-018928 2026-027906 2008-017231 2018-012823 2025-012894 2023-005011 2024-032380 2009-015920 2024-014239 2024-032554 2020-009780 2021-024259 2026-013450 2026-025649 2026-016165 2020-021381 2025-029985 2016-002706 2013-014326 2023-021531 2021-001706 2022-006710 2020-011750 2025-014445 2022-023266 2023-001782 2025-035627 2026-020272 2026-014326 2026-015340 2011-015763 2020-013387 2026-014377 2014-017860 2020-008465 2025-041927 2025-019603 2024-017189 2006-016766 2007-005051 2025-037535 2025-034914 2026-014801 2024-021998 2008-005692 2008-016445 2025-000583 2011-007502 2002-003956 2007-011500 2025-022755 2023-027545 2009-000494 2003-005006 2004-000626 2007-009385 2026-014917 2025-016121 2026-032956 2008-016885 2013-002572 2016-011545 2020-020109 2026-031941 2026-010924 2022-004588 2026-034745 2018-011414 2023-027541 2023-012817 2026-010907 2025-030948".split()
miss=[]
for v in sorted(set(sala)):
    f=f'{R}/Jurisprudencia constitucional (Sala Constitucional)/Municipal/Sentencia {v}.md'
    if not os.path.exists(f): miss.append(v); continue
    d=meta(f); y,mo,da=fdate(d['fecha']); h=d['hora'].lstrip('0') if d['hora'] else ''
    h=re.sub(r'^:', '0:', h)
    hs=f', de las {h} horas' if h else ''
    exp=f' (Expediente {d["expediente"]})' if d['expediente'] else ''
    url=f' NexusPJ. {d["enlace"]}' if d['enlace'] else ' NexusPJ.'
    out.append(('B',f'Sala Constitucional de la Corte Suprema de Justicia. ({y}, {da} de {MES[mo]}). *Sentencia N.° {v}{hs}*{exp}.{url}'))
tca={'I 2002-000425':'Sección I','II 2003-000268':'Sección II','III 2009-002416':'Sección III','III 2011-000123':'Sección III','III 2011-000436':'Sección III','III 2012-000510':'Sección III','III 2015-000321':'Sección III','III 2016-000334':'Sección III','III 2023-000111':'Sección III','IV 2015-000082':'Sección IV','JI 2023-003972':None}
for k,sec in tca.items():
    f=f'{R}/Jurisprudencia contencioso administrativa (TCA)/Municipal/Sentencia TCA {k}.md'
    d=meta(f); y,mo,da=fdate(d['fecha']); h=d['hora'].lstrip('0'); n=k.split()[1]; yy,num=n.split('-'); num=str(int(num))
    org='Tribunal Contencioso Administrativo y Civil de Hacienda' if sec is None else f'Tribunal Contencioso Administrativo, {sec}'
    hs=f', de las {h} horas' if h else ''
    exp=f' (Expediente {d["expediente"]})' if d['expediente'] else ''
    out.append(('C',f'{org}. ({y}, {da} de {MES[mo]}). *Resolución N.° {num}-{yy}{hs}*{exp}. NexusPJ.'))
pgr="C-015-2013 C-136-2020 C-243-1997 C-082-2015 C-108-2021 C-189-2019 C-131-1997 C-078-2026 C-045-2012 C-205-2017 C-088-2017 C-009-2010 C-049-2026 C-213-2013 C-166-2014 C-179-2018 C-217-2015 C-236-2016 C-321-2019 C-089-2022 C-079-2022 C-285-2012 C-231-2014 C-064-2022 C-071-1987 C-107-2026 C-058-2013 C-043-2016 C-238-2020 C-185-2015 C-092-2024 C-166-2023 C-241-2016 C-067-2018 C-319-2015 C-015-2026 C-331-2011 C-345-2014 C-194-2024 C-089-2024 C-118-2021 C-127-2018 C-220-2015 C-045-2014 C-136-2002 C-180-2022 C-014-2018".split()
for p in sorted(set(pgr),key=lambda x:(x.split('-')[2],x)):
    fs=glob.glob(f'{R}/Jurisprudencia administrativa (PGR)/*/Dictamen {p}.md')
    if not fs: miss.append(p); continue
    d=meta(fs[0]); y,mo,da=fdate(d['fecha'])
    url=f' Sistema Costarricense de Información Jurídica. {d["enlace"]}' if d['enlace'] else ''
    out.append(('D',f'Procuraduría General de la República. ({y}, {da} de {MES[mo]}). *Dictamen {p}*.{url}'))
json.dump({'out':out,'miss':miss},open('/home/claude/refs/juris.json','w'),ensure_ascii=False)
print(len(out),'miss',miss)
for x in out[:3]+out[-3:]: print(x[1])
