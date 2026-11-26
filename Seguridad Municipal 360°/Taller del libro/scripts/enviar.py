# enviar.py TEMA ID... : reemplaza cada ANCLA de cgr27/TEMA.json por el id dado (en orden) e imprime payload; sin ids, lista anclas buscables
import json, sys, re
o = json.load(open(f'/home/claude/art/cgr27/{sys.argv[1]}.json'))['ops']; ids = sys.argv[2:]
if not ids:
    for x in o:
        if 'ANCLA' in x: print(re.sub(r'\*', '', x['ANCLA'])[40:100])
    sys.exit()
for x in o:
    if 'ANCLA' in x:
        x.pop('ANCLA'); x['target'] = {"kind": "blocks", "ids": [ids.pop(0)]}
print(json.dumps({"ops": o}, ensure_ascii=False))
