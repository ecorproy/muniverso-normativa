import re,sys,unicodedata
from docx import Document
L='/home/claude/libro/'
d=Document(sys.argv[1]); ps=d.paragraphs
def pl(t): return re.sub(r'\s+',' ',unicodedata.normalize('NFC',re.sub(r'[\*\[\]]','',t))).strip()
def titulo(c):
    return open(L+c+'/chk_A/'+('all' if c=='cap02' else c)+'.md',encoding='utf-8').read().split('\n',1)[0].lstrip('# ').strip()
caps=[('intro','Heading 1'),('cap01','Heading 1'),('cap02','Heading 1'),('cap03','Heading 1'),('cap04','Heading 1'),('conclusion','Heading 1'),('anexos','Heading 1')]+[(f't{i:02d}','Heading 2') for i in range(1,37)]
tot_m=tot_e=0
for c,niv in caps:
    md=open(L+c+'/chk_A/'+('all' if c=='cap02' else c)+'.md',encoding='utf-8').read()
    t=titulo(c)
    h=[i for i,p in enumerate(ps) if p.style.name==niv and pl(p.text)==pl(t)]
    if len(h)!=1: print(c,'título no hallado:',t[:50],len(h)); continue
    h=h[0]
    e=next((k for k in range(h+1,len(ps)) if ps[k].style.name=='Heading 1' or (niv=='Heading 2' and ps[k].style.name=='Heading 2' and ps[k].paragraph_format.page_break_before)),len(ps))
    W=[pl(ps[k].text) for k in range(h+1,e) if ps[k].text.strip()]
    Wset=set(W)
    blocks=[]
    for b in md.split('\n\n'):
        b=b.strip()
        if re.match(r'^[A-Z][a-z]{2} \d{1,2}, \d{4} · @',b): continue
        if not b or b.startswith('[[') or b.startswith('<?') or b.startswith('# ') or b.startswith('|') or b.startswith('!['): continue
        if b.startswith('## ') or b.startswith('### '): b=b.split(' ',1)[1]
        if b.startswith('> '): b=b[2:]
        for sub in (b.split('\n') if b.startswith('- ') or re.match(r'^\d+\. ',b) else [b]):
            sub=re.sub(r'^(- |\d+\. )','',sub.strip())
            if sub: blocks.append(pl(sub))
    zz=[pl(x) for x in open(L+c+'/chk_A/zz_referencias.md',encoding='utf-8').read().split('\n\n') if x.strip() and not x.startswith('#')]
    blocks+=zz+['Referencias']
    miss=[b for b in blocks if b not in Wset]
    Bset=set(blocks)
    extra=[w for w in W if w not in Bset]
    tot_m+=len(miss); tot_e+=len(extra)
    if miss or extra:
        print(f'== {c}: faltan {len(miss)}, sobran {len(extra)}')
        for m in miss[:6]: print('   - FALTA:',m[:150])
        for x in extra[:6]: print('   + SOBRA:',x[:150])
print('TOTAL faltan',tot_m,'sobran',tot_e)
