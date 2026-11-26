# revisar.py tNN...: «Cómo hace», arranque de la conclusión y oraciones sospechosas con contexto, sin macros
import re,sys,glob,os,subprocess
R='/home/claude/repo/360/Seguridad Municipal 360°/Taller del libro/Capítulos'
def L(s): return re.sub(r'\[\[[^\]]*\]\]','§',s)
for n in sys.argv[1:]:
    d=f'/home/claude/art/{n}/src' if os.path.isdir(f'/home/claude/art/{n}/src') else f'{R}/{n}/src'
    t=open(glob.glob(f'{d}/*.md')[0],encoding='utf-8').read()
    i=t.find('## Cómo hace'); j=t.find('## Lo que hoy'); k=t.find('## Conclusión')
    print(f'##### {n}\n'+L(t[i:j]).strip()); print('-- concl:', L(t[k+14:k+700]).replace('\n',' ')[:650])
    out=subprocess.run(['python3','-I','/home/claude/mis_scripts/senales3.py',n],capture_output=True,text=True).stdout
    out+=subprocess.run(['python3','-I','/home/claude/mis_scripts/senales2.py',n],capture_output=True,text=True).stdout
    vistos=set()
    for ln in out.splitlines():
        s=ln.split(': ',1)[1][:60] if ': ' in ln else ''
        if not s or s in vistos: continue
        vistos.add(s)
        if t[i:j].find(s[:30])>=0 and i>=0: continue
        print('*', ln.split(': ',1)[1][:300])
