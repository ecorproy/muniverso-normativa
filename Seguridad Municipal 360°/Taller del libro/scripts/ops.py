import json,sys
d=json.load(open(f'/home/claude/art/limpieza/{sys.argv[1]}.json'))['ops']
if len(sys.argv)>2: d=d[-int(sys.argv[2]):]
print(json.dumps({"ops":d},ensure_ascii=True))
