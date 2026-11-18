"""Lectura diaria de La Gaceta y sus Alcances (Imprenta Nacional) para mantener al día las leyes del repositorio.

1. Detecta las leyes sancionadas en la edición del día (DECRETO LEGISLATIVO N.º …) y las leyes que esas leyes reforman,
   adicionan o derogan.
2. Las agrega a la cola herramientas/leyes_pendientes.json.
3. Para cada ley pendiente consulta SINALEVI (una consulta a la vez, con pausas). Si hay una versión más reciente que la
   del repositorio, reescribe el archivo .md; si la ley no existe en el repositorio, la crea en
   «Leyes y decretos nacionales/<Materia>/Ley N.md».
4. Si SINALEVI todavía no incorpora la ley o la reforma, la deja pendiente y la reintenta los días siguientes (15 días).

Uso: python herramientas/gaceta_diaria.py            (edición de hoy)
     GACETA_HTML=archivo.html ALCANCE_TXT=a.txt ...   (pruebas con archivos locales)
"""
import io, json, os, re, sys, time, unicodedata, urllib.request
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descargar_normas import buscar_numero, descargar, limpiar, ultima_reforma  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NACIONALES = os.path.join(RAIZ, "Leyes y decretos nacionales")
COLA = os.path.join(RAIZ, "herramientas", "leyes_pendientes.json")
BASE = "https://www.imprentanacional.go.cr"
MAX_DIARIO, MAX_INTENTOS = int(os.environ.get("MAX_DIARIO", 12)), 15


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def bajar(url, intentos=4):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Muniverso; lectura diaria de La Gaceta)"})
    for i in range(intentos):
        try:
            return urllib.request.urlopen(req, timeout=90).read()
        except Exception:
            if i == intentos - 1: raise
            time.sleep(30 * (i + 1))


def texto_html(h):
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</div>|</li>", "\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    import html as _h
    return re.sub(r"[ \t\xa0]+", " ", _h.unescape(h))


def texto_pdf(datos):
    from pypdf import PdfReader
    return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(datos)).pages)


def edicion():
    """Devuelve (fecha, [(fuente, texto legislativo)])."""
    if os.environ.get("GACETA_HTML"):
        html = open(os.environ["GACETA_HTML"], encoding="utf-8", errors="replace").read()
    else:
        html = bajar(BASE + "/gaceta/").decode("utf-8", errors="replace")
    f = re.search(r"/pub/(\d{4})/(\d{2})/(\d{2})/COMP_", html)
    fecha = f"{f.group(3)}/{f.group(2)}/{f.group(1)}" if f else date.today().strftime("%d/%m/%Y")
    piezas = []
    # Diario: solo la sección PODER LEGISLATIVO (h1 hasta el siguiente h1).
    partes = re.split(r"(?is)<h1[^>]*>", html)
    for p in partes:
        cab = norm(texto_html(p.split("</h1>")[0]))
        if "poder legislativo" in re.sub(r"\s+", " ", cab):
            piezas.append(("La Gaceta", texto_html(p)))
    # Alcances: el HTML es solo índice; el texto está en el PDF.
    if os.environ.get("ALCANCE_TXT"):
        for a in os.environ["ALCANCE_TXT"].split(os.pathsep):
            piezas.append((os.path.basename(a), open(a, encoding="utf-8").read()))
    else:
        for ruta, nombre in dict.fromkeys(re.findall(r"ViewAlcance\.aspx\?url=(/pub/[^'\"]+?)\.html['\"][^>]*>([^<]+)</a>", html)):
            try:
                piezas.append((texto_html(nombre).strip(), texto_pdf(bajar(BASE + ruta + ".pdf"))))
            except Exception as ex:
                print("No se pudo leer", nombre, ex)
    return fecha, piezas


RE_NUEVA = re.compile(r"DECRETO\s+LEGISLATIVO\s+N[.°º ]*((?:\d ?){3,5})", re.I)
RE_LEY = re.compile(r"\bLey\s+(?:N[.°º]*\s*|número\s+)?(\d{3,5})\b", re.I)
RE_ACCION = re.compile(r"(?:refórm|reform|adici[oó]n|der[oó]g|modif)\w*\s+(?:el|los|la|las|un|una|del?)?\s*"
                       r"(?:inciso|p[aá]rrafo|art[ií]culo|cap[ií]tulo|t[ií]tulo|transitorio|numeral|ley)", re.I)
RE_FIN_BLOQUE = re.compile(r"\n\s*(PROYECTOS|PODER EJECUTIVO|DECRETOS|ACUERDOS|DOCUMENTOS VARIOS|REGLAMENTOS)\s*\n")


def leyes(piezas):
    nuevas, reformadas = {}, {}
    for fuente, txt in piezas:
        marcas = list(RE_NUEVA.finditer(txt))
        for i, m in enumerate(marcas):
            fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(txt)
            corte = RE_FIN_BLOQUE.search(txt, m.end(), fin)
            bloque = txt[max(0, m.start() - 400): corte.start() if corte else fin]
            numero = m.group(1).replace(" ", "")
            nuevas[numero] = fuente
            for r in RE_LEY.finditer(bloque):
                previo = bloque[max(0, r.start() - 160): r.start()]
                previo = previo[previo.rfind(". ") + 1:]
                if RE_ACCION.search(previo) and r.group(1) != numero:
                    reformadas.setdefault(r.group(1), f"Ley {numero}")
    for n in nuevas: reformadas.pop(n, None)
    return nuevas, reformadas


def archivo_existente(numero):
    for carpeta, _, archivos in os.walk(NACIONALES):
        for a in archivos:
            if a == f"Ley {numero}.md": return os.path.join(carpeta, a)
    for carpeta, _, archivos in os.walk(NACIONALES):
        for a in archivos:
            if a.endswith(".md"):
                with open(os.path.join(carpeta, a), encoding="utf-8") as fh:
                    if f'numero: "Ley {numero}"' in fh.read(400): return os.path.join(carpeta, a)
    return None


def front(ruta):
    with open(ruta, encoding="utf-8") as fh:
        t = fh.read(3000)
    return dict(re.findall(r'(?m)^(\w+):\s*"(.*)"\s*$', t.split("\n---", 1)[0]))


MATERIAS = [("Municipal", r"municip|cantonal|patente"), ("Laboral", r"trabaj|laboral|salari|empleo"),
            ("Tributario", r"impuest|tribut|fiscal|\brenta\b"), ("Hacienda pública", r"presupuest|hacienda|deuda|credito publico"),
            ("Ambiental", r"ambient|forestal|agua|residu|biodivers|mineri"), ("Penal", r"\bpenal|delit|\bpenas?\b"),
            ("Electoral", r"electoral|partido"), ("Seguridad social", r"seguro social|pension|salud"),
            ("Familia", r"famili|\bnin[oa]s?\b|\bnine[zs]|adolesc|matrimon"), ("Agrario", r"agrari|agricol|ganad|pesca"),
            ("Comercial", r"comerci|consumidor|competencia|financ|banc|mora"),
            ("Internacional", r"convenio|tratado|acuerdo|protocolo|aprobacion"), ("Constitucional", r"constituci")]


def materia(nombre):
    t = norm(nombre)
    return next((m for m, r in MATERIAS if re.search(r, t)), "Administrativo")


def actualizar(pg, numero):
    """Devuelve (estado, detalle). estado: 'actualizada' | 'nueva' | 'pendiente'."""
    elegido, cands, _ = buscar_numero(pg, "Ley", numero)
    if not elegido:
        return "pendiente", "SINALEVI aún no la incorpora"
    d = descargar(pg, elegido)
    if len(d["vista"]) < 300: return "pendiente", "texto vacío"
    ruta = archivo_existente(numero)
    previo = front(ruta) if ruta else {}
    if previo.get("version_sinalevi") and previo["version_sinalevi"] == d["version"]:
        return "pendiente", f"SINALEVI sigue en la versión {d['version']}"
    estado = "derogada" if d["derogada"] else ("vigente" if d["ficha_ok"] else "no indicado")
    q = lambda s: str(s or "").replace('"', "'")
    nombre = previo.get("nombre") or elegido["nombre"]
    mat = previo.get("materia") or materia(nombre).lower()
    if not ruta:
        ruta = os.path.join(NACIONALES, materia(nombre), f"Ley {numero}.md")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
    cuerpo = limpiar(d["vista"])
    fm = ["---", f'numero: "Ley {numero}"', f'nombre: "{q(nombre)}"', f'materia: "{q(mat)}"', f'estado: "{estado}"',
          f'version_sinalevi: "{d["version"]}"', f'fecha_version: "{d["fecha_version"]}"',
          f'ultima_reforma: "{ultima_reforma(d["vista"], numero)}"', f'ente_emisor: "{q(elegido.get("emisor"))}"',
          f'fecha_norma: "{elegido["fecha"]}"', f'enlace: "{d["url"]}"', f'descargado: "{date.today().isoformat()}"', "---", ""]
    notas = ("\n\n## Notas de SINALEVI sobre vigencia\n\n" + "\n".join(
        f"- {('Artículo ' + n['a']) if n['a'] else 'Nota general'}: {n['t']}" for n in d["notas"])) if d["notas"] else ""
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write("\n".join(fm) + cuerpo + notas + "\n")
    return ("actualizada" if previo else "nueva"), f"{os.path.relpath(ruta, RAIZ)} · versión {d['version']}"


def main():
    cola = json.load(open(COLA, encoding="utf-8")) if os.path.exists(COLA) else {}
    fecha, piezas = edicion()
    nuevas, reformadas = leyes(piezas)
    print(f"La Gaceta del {fecha}: {len(piezas)} textos legislativos · leyes nuevas {sorted(nuevas)} · reformadas {sorted(reformadas)}")
    for n, f in nuevas.items(): cola.setdefault(n, {"motivo": f"Publicada en {f} ({fecha})", "desde": fecha, "intentos": 0})
    for n, por in reformadas.items(): cola.setdefault(n, {"motivo": f"Reformada por la {por} ({fecha})", "desde": fecha, "intentos": 0})
    if os.environ.get("SOLO_DETECTAR"):
        print(json.dumps(cola, ensure_ascii=False, indent=1)); return

    informe = []
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
        for i, n in enumerate(sorted(cola, key=lambda k: cola[k]["intentos"])):
            if i >= MAX_DIARIO: break
            if i: time.sleep(4)
            try:
                estado, det = actualizar(pg, n)
            except Exception as ex:
                estado, det = "pendiente", f"error: {str(ex)[:120]}"
                try: b.close()
                except Exception: pass
                b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
            print(f"Ley {n}: {estado} · {det}", flush=True)
            if estado == "pendiente":
                cola[n]["intentos"] += 1; cola[n]["ultimo"] = det
                if cola[n]["intentos"] >= MAX_INTENTOS:
                    informe.append(f"- Ley {n}: se dejó de intentar tras {MAX_INTENTOS} días ({det})"); cola.pop(n)
            else:
                informe.append(f"- Ley {n} {estado}: {det} — {cola[n]['motivo']}"); cola.pop(n)
        b.close()
    with open(COLA, "w", encoding="utf-8") as fh:
        json.dump(cola, fh, ensure_ascii=False, indent=1, sort_keys=True)
    if informe:
        with open(os.path.join(RAIZ, "herramientas", "ultimo_informe.md"), "w", encoding="utf-8") as fh:
            fh.write(f"# Actualización del {datetime.now():%Y-%m-%d}\n\n" + "\n".join(informe) + "\n")
    print("\n".join(informe) or "Sin cambios hoy.")


if __name__ == "__main__":
    main()
