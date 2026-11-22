# refplan.py -> plan de inserción/borrado de referencias a partir de blocks.json (mapa fresco) y refs_delta.json (chk)
import json,re,unicodedata
def norm(t):
    t = unicodedata.normalize('NFC', t).replace('\\', '')
    t = re.sub(r'[*_#>]', '', t)
    return re.sub(r'\s+', ' ', t).strip()
B=json.load(open('/home/claude/export/blocks.json',encoding='utf-8'))
bl=B['blocks']
k=[i for i,b in enumerate(bl) if b['heading'] and b['text'].strip()=='Referencias'][0]
refs=bl[k+1:]
D=json.load(open('/home/claude/export/refs_delta.json',encoding='utf-8'))
gen=D['gen']; add=set(norm(x) for x in D['add']); rem=[norm(x) for x in D['rem']]
docmap={norm(b['text']):b for b in refs}
miss=[g for g in gen if norm(g) not in docmap and norm(g) not in add]
print('rev',B['rev'],'| refs en doc',len(refs),'| gen',len(gen),'| gen sin bloque ni add:',len(miss))
plan=[]; prev=bl[k]['id']; cur=None
for g in gen:
    n=norm(g)
    if n in add:
        if cur is None:
            cur=[prev,[]]; plan.append(cur)
        cur[1].append(g)
    else:
        b=docmap.get(n)
        if b: prev=b['id']
        cur=None
pref='m3z97wxmbms'
ops=[]
for a,ts in plan:
    aid=a if a.startswith(pref) else pref+a
    ops.append({"op":"insert","target":{"kind":"blocks","ids":[aid]},"side":"after","source":{"as":"markdown","from":{"kind":"inline","content":"\n\n".join(ts)}}})
    print('AFTER',aid,'->',[t[:60] for t in ts])
for b in refs:
    if norm(b['text']) in rem:
        bid=b['id'] if b['id'].startswith(pref) else pref+b['id']
        ops.append({"op":"delete","target":{"kind":"blocks","ids":[bid]},"ifHash":b['h'],"ifRev":int(B['rev'])})
        print('DELETE',bid,b['text'][:70])
order_doc=[norm(b['text']) for b in refs if norm(b['text']) not in rem]
order_gen=[norm(g) for g in gen if norm(g) not in add]
print('orden doc == orden gen (sin cambios):', order_doc==order_gen)
json.dump({"ops":ops},open('/home/claude/export/refs_ops.json','w',encoding='utf-8'),ensure_ascii=True)
print('ops:',len(ops),'| bytes payload:',len(json.dumps({"ops":ops})))
