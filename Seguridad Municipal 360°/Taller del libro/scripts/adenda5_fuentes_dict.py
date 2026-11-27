import sys
dest=sys.argv[1]
items=[
 ('/mnt/user-data/uploads/c9c4ec68-attachment.txt','C-136-2026','17/08/2026','Gerencia General de la Asamblea Legislativa','Asamblea Legislativa','Empleo público','Familia legislativa y rectoría de Mideplán (Ley 10159, arts. 6, 13 y 26); voto 2021-017098; sistemas de selección','25548'),
 ('/mnt/user-data/uploads/6ae851d3-attachment.txt','C-078-2025','21/04/2025','Ministro de Obras Públicas y Transportes','Ministerio de Obras Públicas y Transportes','Empleo público','Transitorio IX de la Ley 10159 y familia policial (art. 13 inciso c)','24934'),
 ('/mnt/user-data/uploads/b69f71ad-attachment.txt','C-016-2024','12/02/2024','Directora Ejecutiva de la Secretaría Técnica de la Autoridad Presupuestaria','Secretaría Técnica de la Autoridad Presupuestaria','Empleo público','Competencias de la Autoridad Presupuestaria tras la Ley 10159; manuales de puestos (art. 33); Dirección de Confianza (art. 37)','24246'),
]
for src,num,fecha,cons,inst,mat,temas,param in items:
    body=open(src,encoding='utf-8').read().strip()
    fm=(f'---\nnumero: "{num}"\ntipo: "Dictamen de la Procuraduría General de la República"\nfecha: "{fecha}"\nconsultante: "{cons}"\ninstitucion: "{inst}"\nmateria: "{mat}"\ntemas: "{temas}"\n'
        f'enlace: "https://sinalevi.go.cr/ResultadosPronunciamiento/Informacion?param1={param}&param2=0"\ndescargado: "2026-11-26"\nfuente: "Texto de SINALEVI aportado por Edward Cortés García el 26 de noviembre de 2026"\n---\n# Dictamen {num}\n\n')
    open(f'{dest}/Dictamen {num}.md','w',encoding='utf-8').write(fm+body+'\n')
print('ok')
