# blocks.py VIEW_FILE [show]  -> mapa de bloques del documento: id, hash, tipo, inicio del texto, por sección
import sys, re, json
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
m = re.search(r"<doc[^>]*rev='(\d+)'", s)
rev = m.group(1) if m else '?'
# bloques de primer nivel: paragraph / blockquote / list / table
pat = re.compile(r"<(paragraph|blockquote|list|table|pending)\b([^>]*)>(.*?)</\1>", re.S)
out = []
for mm in pat.finditer(s):
    kind, attrs, inner = mm.group(1), mm.group(2), mm.group(3)
    idm = re.search(r"id='([^']+)'", attrs); hm = re.search(r"\bh='([^']+)'", attrs); hd = re.search(r"heading='(\d)'", attrs)
    txt = re.sub(r'<[^>]+>', '', inner)
    txt = txt.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'")
    out.append(dict(id=idm.group(1) if idm else None, h=hm.group(1) if hm else None, kind=kind, heading=int(hd.group(1)) if hd else 0, text=txt, pos=mm.start()))
json.dump(dict(rev=rev, blocks=out), open('/home/claude/export/blocks.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('rev', rev, '| bloques', len(out), '| caracteres', len(s))
if len(sys.argv) > 2:
    for b in out:
        if b['heading']:
            print(f"{b['id']:>24} h={b['h']} H{b['heading']} {b['text'][:80]}")
