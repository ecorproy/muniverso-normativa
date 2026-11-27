import re,glob,os,unicodedata,sys
def norm(s): s=unicodedata.normalize('NFC',s); return re.sub(r'\s+',' ',re.sub(r'[“”«»"]','',s)).strip().lower()
idx={}
for root in ['/home/claude/repo/main','/home/claude/libro/fuentes']:
    for f in glob.glob(root+'/**/*.md',recursive=True):
        idx.setdefault(os.path.basename(f),f)
def fuente(m):
    p=m.split(':')
    if p[0]=='V': return idx.get(f'Sentencia {p[1]}.md')
    if p[0]=='VT': return idx.get(f'Sentencia {p[2]}.md')
    if p[0]=='D': return idx.get(f'Dictamen {p[1]}.md')
    return None
HEAD=re.compile(r'(?mi)^\s*(?:\*\*)?\s*(?:(?:considerando|apartado)\s+)?([IVXL]{1,6})\s*(?:\*\*)?\s*[\.\-–—)°º:]|^\s*(?:\*\*)?(por tanto|resultando|considerando|conclusi[oó]n(?:es)?)\b')
out=[]
for f in sorted(glob.glob('/home/claude/libro/*/chk_A/zz_informe.txt')):
    t=open(f).read(); sec=re.search(r'UBICACIONES VERIFICADAS A MANO \(\d+\):\n(.*?)\n\n',t,re.S)
    if not sec: continue
    for line in sec.group(1).split('\n'):
        m=re.match(r'\s*\[(.+?)\] (.+?): "(.*)" \(segmentador',line)
        if not m: continue
        arch,mac,q=m.groups(); src=fuente(mac)
        cit=mac.split(':')[-1]
        if not src: out.append((arch,mac,q,'(sin resolver fuente: revisar a mano)')); continue
        raw=open(src,encoding='utf-8').read(); n=norm(raw); qq=norm(q)[:45]
        i=n.find(qq)
        if i<0: out.append((arch,mac,q,'NO HALLADA')); continue
        # map back approx: find in raw by ratio
        pos=int(i*len(raw)/max(1,len(n)))
        heads=[(h.start(),(h.group(1) or h.group(2))) for h in HEAD.finditer(raw[:pos+200])]
        last=[h for h in heads if h[0]<=pos+50][-3:]
        out.append((arch,mac,q,'antes: '+' > '.join(x[1] for x in last)))
for o in out: print(f'{o[0]} | {o[1]} | {o[2][:40]} | {o[3]}')
