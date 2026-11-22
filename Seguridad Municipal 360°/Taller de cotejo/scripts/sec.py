# sec.py DESDE_ID HASTA_ID(excl)  -> ids de los bloques de ese tramo (según /home/claude/export/blocks.json)
import json, sys
d = json.load(open('/home/claude/export/blocks.json', encoding='utf-8'))
P = 'm3z97wxmbms'
full = lambda i: i if i.startswith(P) else P + i
bl = d['blocks']; ids = [full(b['id']) for b in bl]
a = ids.index(full(sys.argv[1])); b = ids.index(full(sys.argv[2])) if len(sys.argv) > 2 and sys.argv[2] != 'END' else len(ids)
print('rev', d['rev'], '| bloques', b - a)
print(json.dumps(ids[a:b]))
for x in bl[a:b]:
    print('  ', x['id'], x['h'], x['kind'], ('H%d ' % x['heading'] if x['heading'] else '') + x['text'][:60])
