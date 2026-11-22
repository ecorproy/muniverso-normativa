import re,glob,json
R='/home/claude/repo/main/Leyes y decretos nacionales'
MES=['','enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre']
nums="5412 10141 2391 10412 8533 7794 8892 9078 9329 9976 8488 9047 10009 704 5395 7600 7801 9095 8220 9097 8422 8968 10216 6587 10254 9137 9220 7739 10476 7552 8261 10359 7935 10192 8688 3859 9145 1634 10595 8839 7554 6043 7451 10199 4240 7555 10234 6227 10159 2166 4574".split()
out=[];miss=[]
for n in nums:
    fs=[f for f in glob.glob(f'{R}/*/Ley {n}.md')+glob.glob(f'{R}/*/Ley {n}.md.md')]
    if not fs: miss.append(n); continue
    t=open(fs[0],encoding='utf-8').read(3000)
    g=lambda k:(re.search(r'(?m)^'+k+r':\s*"([^"]*)"',t) or [None,''])[1]
    fn=g('fecha_norma'); m=re.match(r'(\d{2})/(\d{2})/(\d{4})',fn)
    if not m: miss.append(n+'(fecha)'); continue
    da,mo,y=map(int,m.groups())
    url=g('enlace')
    out.append((y,f'Asamblea Legislativa de la República de Costa Rica. ({y}). *{g("nombre")}* (Ley N.° {n}). Sistema Costarricense de Información Jurídica.'+(f' {url}' if url else '')))
out.sort()
json.dump({'out':[o[1] for o in out],'miss':miss},open('/home/claude/refs/leyes.json','w'),ensure_ascii=False)
print(len(out),miss)
for o in out: print(o[1][:140])
