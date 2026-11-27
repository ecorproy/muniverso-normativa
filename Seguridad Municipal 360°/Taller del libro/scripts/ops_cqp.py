import sys,json,re
t=sys.argv[1]; spec=json.loads(sys.argv[2])
A='/home/claude/art/'
parts=open(A+f'{t}/out/{t}.md',encoding='utf-8').read().split('\n\n')
body='\n\n'.join(parts)
refs=open(A+f'{t}/out/zz_referencias.md',encoding='utf-8').read().split('\n\n')
i=body.index('## Con qué se paga'); j=body.index('\n## Cómo hace',i)
sec=body[i:j].strip()
pre='m4fycn3amtm'
ops=[]
for s in spec:
    if s['k']=='sec':
        ops.append({"op":"insert","target":{"kind":"blocks","ids":[pre+s['id']]},"side":"before","source":{"as":"markdown","from":{"kind":"inline","content":sec}}})
    elif s['k']=='ref':
        txt=[r.strip() for r in refs if r.strip().startswith(s['start'])]; assert len(txt)==1,(s,len(txt))
        ops.append({"op":"insert","target":{"kind":"blocks","ids":[pre+s['id']]},"side":"after","source":{"as":"markdown","from":{"kind":"inline","content":txt[0]}}})
    elif s['k']=='refs':
        txts=[]
        for st in s['starts']:
            tt=[r.strip() for r in refs if r.strip().startswith(st)]; assert len(tt)==1,(st,len(tt)); txts.append(tt[0])
        ops.append({"op":"insert","target":{"kind":"blocks","ids":[pre+s['id']]},"side":"after","source":{"as":"markdown","from":{"kind":"inline","content":'\n\n'.join(txts)}}})
    elif s['k']=='rep':
        txt=[p.strip() for p in parts if p.strip().startswith(s['start'])]; assert len(txt)==1,(s,len(txt))
        ops.append({"op":"replace","target":{"kind":"blocks","ids":[pre+s['id']]},"ifHash":s['h'],"with":{"as":"markdown","from":{"kind":"inline","content":txt[0]}}})
print(json.dumps({"ops":ops},ensure_ascii=True))
