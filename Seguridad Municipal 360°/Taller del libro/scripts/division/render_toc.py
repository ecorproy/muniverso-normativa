"""Abre un DOCX en LibreOffice, actualiza los índices (TOC) y exporta PDF, sin tocar el DOCX."""
import sys,subprocess,time,uno,os
from com.sun.star.beans import PropertyValue
def P(n,v): p=PropertyValue(); p.Name=n; p.Value=v; return p
src,pdf=os.path.abspath(sys.argv[1]),os.path.abspath(sys.argv[2])
proc=subprocess.Popen(['soffice','--headless','--invisible','--norestore','--accept=socket,host=localhost,port=2002;urp;'])
ctx=None
for _ in range(60):
    try:
        local=uno.getComponentContext(); res=local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',local)
        ctx=res.resolve('uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext'); break
    except Exception: time.sleep(1)
smgr=ctx.ServiceManager; desk=smgr.createInstanceWithContext('com.sun.star.frame.Desktop',ctx)
doc=desk.loadComponentFromURL(uno.systemPathToFileUrl(src),'_blank',0,(P('Hidden',True),))
ix=doc.getDocumentIndexes(); print('índices',ix.getCount())
for i in range(ix.getCount()): ix.getByIndex(i).update()
doc.refresh()
doc.storeToURL(uno.systemPathToFileUrl(pdf),(P('FilterName','writer_pdf_Export'),))
doc.close(True); 
try: desk.terminate()
except Exception: pass
proc.wait(timeout=60)
