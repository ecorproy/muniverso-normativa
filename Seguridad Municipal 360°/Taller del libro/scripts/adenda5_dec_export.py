import sys,json,base64,hashlib
j=json.load(open(sys.argv[1]))
txt=[x['text'] for x in j if x['type']=='text' and 'bytes_b64' in x['text']][0]
d=json.loads(txt)
b=base64.b64decode(d['data']['bytes_b64'])
open(sys.argv[2],'wb').write(b)
print('rev',d['rev'],'bytes',len(b),'sha',hashlib.sha256(b).hexdigest())
