#!/usr/bin/env python3
"""
Descarga normas de SINALEVI a Markdown etiquetado para el repositorio muniverso-normativa.

Para cada nombre del catálogo:
  1. Búsqueda selectiva oficial por nombre (si no hay resultados, búsqueda sencilla). Se exige título idéntico;
     si no lo hay, la entrada queda «PARA REVISAR» con los candidatos y NO se descarga.
  2. Ficha sin param2 → SINALEVI redirige a la última versión; se confirma «Versión de la Norma: N de N».
  3. Texto de #divVista, limpio (sin «Ficha Artículo», botones ni menú); ficha de la norma (#botonFicha) para
     fecha de versión, ente emisor y vigencia; notas de vigencia («recobra vigencia», «anulado», «inconstitucional»).
  4. Archivo .md con etiqueta. Si la norma ya está en el repositorio, se reutiliza su nombre de archivo.
Ritmo: una norma a la vez, con pausas, para no sobrecargar el sitio.

Uso:  python descargar_normas.py catalogo_220.txt --desde 1 --hasta 20 --repo ../muniverso-normativa --salida lote_01
"""
import argparse, json, os, re, sys, time, unicodedata
from datetime import date
from urllib.parse import quote
from playwright.sync_api import sync_playwright

BASE = "https://sinalevi.go.cr/ResultadosNormativa"
MESES = {m: i + 1 for i, m in enumerate("enero febrero marzo abril mayo junio julio agosto setiembre octubre noviembre diciembre".split())}
MESES["septiembre"] = 9
MATERIAS = {"I": "constitucional", "II": "administrativo", "III": "municipal", "IV": "laboral", "V": "laboral", "VI": "internacional",
            "VII": "seguridad-social", "VIII": "hacienda", "IX": "tributario", "X": "ambiental", "XI": "electoral", "XII": "social",
            "XIII": "servicios-publicos", "XIV": "penal"}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9ñ ]", " ", s)).strip()


VACIAS = {"de", "la", "el", "los", "las", "y", "del", "a", "al", "en", "para", "por", "e"}


def clave_titulo(s):
    """Título comparable: sin «Ley de…» inicial ni artículos o preposiciones."""
    n = re.sub(r"^(ley|codigo)\b", "", norm(s)).strip()
    return " ".join(w for w in n.split() if w not in VACIAS)


def leer_catalogo(ruta):
    entradas, seccion = [], None
    for linea in open(ruta, encoding="utf-8"):
        m = re.match(r"\s*([IVX]+)\.\s", linea)
        if m and not re.match(r"\s*\d", linea):
            seccion = m.group(1); continue
        m = re.match(r"\s*(\d+)\.\s+(.+?)\s*$", linea)
        if m:
            nombre = m.group(2).rstrip(".")
            derogada = "(derogada)" in nombre.lower()
            nombre = re.sub(r"\s*\((derogada|referencia histórica a verificar)\)", "", nombre, flags=re.I).strip()
            entradas.append({"n": int(m.group(1)), "nombre": nombre, "seccion": seccion, "materia": MATERIAS.get(seccion, ""), "derogada": derogada})
    return entradas


JS_TARJETAS = """() => [...document.querySelectorAll('[onclick*="abrirTexto"]')].map(b => {
  const m = (b.getAttribute('onclick')||'').match(/'(\\d+)'\\s*,\\s*'(\\d+)'/); if (!m) return null;
  let e = b, t = '';
  for (let i = 0; i < 12 && e; i++) { t = e.innerText || ''; if (/Ente Emisor/.test(t) && (t.match(/ del \\d/g)||[]).length === 1) break; e = e.parentElement; }
  return {norma: m[1], version: m[2], tarjeta: t.replace(/\\s+/g,' ').trim().slice(0,500)}; }).filter(Boolean)"""
JS_AMPLIAR = """() => { try { const lv = jQuery('#listView').data('kendoListView'); if (!lv) return 0; const ds = lv.dataSource, t = ds.total();
  if (t > ds.pageSize()) ds.pageSize(Math.min(t, 600)); return t; } catch (e) { return -1; } }"""
RE_TARJ = re.compile(r"(?:^|\s|\d\.\s)([A-ZÁÉÍÓÚ][\wÁÉÍÓÚáéíóúñ ]{1,40}?)\s*:\s*(\d+(?:\s*-\s*[A-Z]{1,6})?)\s+del\s+(\d{1,2}/\d{1,2}/\d{4})")


def tarjeta(t):
    m = RE_TARJ.search(t)
    if not m: return None
    resto = t[m.end():].replace("Ver descriptores", " ").strip()
    nombre = re.split(r"\(Derogad|\(Anulad|Ente Emisor", resto)[0].strip()
    em = re.search(r"Ente Emisor:\s*(.+?)(?:\s+Art[ií]culo\s+\d|\s+Ficha|$)", resto)
    return {"tipo": m.group(1).strip(), "numero": re.sub(r"\s+", "", m.group(2)), "fecha": m.group(3), "nombre": nombre,
            "emisor": em.group(1).strip() if em else None, "derogada": bool(re.search(r"\((Derogad|Anulad)", resto))}


def esperar(pg, maximo=25):
    try: pg.wait_for_load_state("networkidle", timeout=maximo * 1000)
    except Exception: pass
    prev, t0 = None, time.time()
    while time.time() - t0 < maximo:
        t = pg.evaluate("document.body ? document.body.innerText.length : 0")
        if prev == t and t > 300: return True
        prev = t; pg.wait_for_timeout(500)
    return False


def buscar(pg, e):
    """Devuelve (candidato elegido o None, lista de candidatos, mecanismo)."""
    urls = []
    if norm(e["nombre"]).startswith("constitucion politica"):
        urls.append(("selectiva por tipo", f"{BASE}/Resultados?TipoBusqueda=2&Pagina=1&ListaTipoNorma=1&NormasHistoricas=true&CantidadResultados=-1"))
    urls += [("selectiva por nombre", f"{BASE}/Resultados?TipoBusqueda=2&Pagina=1&Nombre={quote(e['nombre'])}&NormasHistoricas=true&CantidadResultados=-1"),
             ("sencilla", f"https://sinalevi.go.cr/BusquedaSimple/Resultados?pagina=1&radioBtnGroup=1&opcionSelected=1&textBuscar={quote(e['nombre'])}&textAnnio=&selectedBuscarEn=F&TipoNorma=&cantidadResultados=-1")]
    sin_ley = re.sub(r"^(Ley|Código)\s+(de\s+(la\s+|los\s+|las\s+|el\s+)?|del\s+|para\s+|sobre\s+(el\s+|la\s+)?|contra\s+(el\s+|la\s+)?)?", "", e["nombre"]).strip()
    if sin_ley and sin_ley != e["nombre"]:
        urls.insert(-1, ("selectiva por nombre (sin «Ley de»)", f"{BASE}/Resultados?TipoBusqueda=2&Pagina=1&Nombre={quote(sin_ley)}&NormasHistoricas=true&CantidadResultados=-1"))
    todos = []
    objetivo = norm(re.sub(r"\s+de la República de Costa Rica$", "", e["nombre"], flags=re.I))
    for mec, u in urls:
        pg.goto(u, wait_until="domcontentloaded", timeout=40000); esperar(pg, 20)
        if pg.evaluate(JS_AMPLIAR) > 10: pg.wait_for_timeout(1200)
        cands = []
        for c in pg.evaluate(JS_TARJETAS):
            tj = tarjeta(c["tarjeta"])
            if tj: cands.append({**c, **tj})
        todos += [c for c in cands if c["norma"] not in {x["norma"] for x in todos}]
        objetivo_c = clave_titulo(objetivo)
        exactos = [c for c in cands if norm(c["nombre"]) == objetivo or clave_titulo(c["nombre"]) == objetivo_c]
        if norm(e["nombre"]).startswith(("ley", "codigo")):   # se pidió una ley: no sirven reglamentos ni circulares
            exactos = [c for c in exactos if norm(c["tipo"]) == "ley"] or exactos
        if exactos:
            vivos = [c for c in exactos if not c["derogada"]]
            if e["derogada"]: vivos = [c for c in exactos if c["derogada"]] or exactos
            if len(vivos) > 1 and objetivo == "constitucion politica":
                vivos = sorted(vivos, key=lambda c: c["fecha"][-4:], reverse=True)[:1]
            if len(vivos) > 1:   # preferir ley sobre otros tipos
                leyes = [c for c in vivos if norm(c["tipo"]) == "ley"]
                vivos = leyes if len(leyes) == 1 else vivos
            if len(vivos) == 1: return vivos[0], todos, mec
            return None, vivos, mec + " (varias coincidencias exactas)"
    return None, todos, "sin coincidencia exacta"


def buscar_numero(pg, tipo, numero):
    """Resolución indicada por el usuario: búsqueda selectiva por número, exigiendo el tipo."""
    pg.goto(f"{BASE}/Resultados?TipoBusqueda=2&Pagina=1&Numero={numero.split('-')[0]}&NormasHistoricas=true&CantidadResultados=-1", wait_until="domcontentloaded", timeout=40000)
    esperar(pg, 20)
    if pg.evaluate(JS_AMPLIAR) > 10: pg.wait_for_timeout(1500)
    cands = [dict(c, **tj) for c in pg.evaluate(JS_TARJETAS) for tj in [tarjeta(c["tarjeta"])] if tj]
    tipo_ok = lambda c: norm(c["tipo"]) == norm(tipo) or norm(c["tipo"]).startswith(norm(tipo))
    ok = [c for c in cands if tipo_ok(c) and norm(c["numero"]) == norm(numero)] or [c for c in cands if tipo_ok(c) and c["numero"].split("-")[0] == numero]
    return (ok[0] if len(ok) == 1 else None), cands, f"indicada por el usuario ({tipo} {numero})"


JS_NOTAS = r"""() => { const t = (document.querySelector('#divVista')||document.body).innerText;
 const re = /[^\n]*(recobr\w*\s+(?:su\s+)?vigencia|declar\w*\s+inconstitucional|inconstitucionalidad|anulad[oa]s?\s+(?:por|mediante)|se\s+anul\w*)[^\n]*/gi;
 const out = [], vistos = {}; let m; const inicio = t.search(/\n\s*Art[ií]culo\s*1\b/i);
 while ((m = re.exec(t)) && out.length < 80) { const l = m[0].replace(/\s+/g,' ').trim(); if (l.length < 15 || vistos[l]) continue; vistos[l] = 1;
  if(!(/Nota de Sinalevi/i.test(l)||/\(\s*(As[ií]|Anulad|Declarad|Mediante|Esta norma|Por resoluci|Derogad)/i.test(l)||/Sala Constitucional\s*(N[°º.]|Voto|mediante|en\s+(su\s+)?resoluci)/i.test(l)))continue;if(/^\(?\s*Corregido mediante Fe de Erratas/i.test(l))continue;
  let art = null; const p = l.match(/^\(?\s*Art[ií]culo\s+(\d+(?:\s*(?:bis|ter))?)/i);
  if (p) art = p[1]; else if (inicio >= 0 && m.index > inicio) { const prev = t.slice(Math.max(0, m.index - 30000), m.index); const rr = /\n\s*Art[ií]culo\s+(\d+(?:\s*(?:bis|ter))?)/gi; let x; while ((x = rr.exec(prev))) art = x[1]; }
  out.push({a: art, t: l.slice(0, 600)}); }
 return out; }"""


def limpiar(texto):
    lineas, out = texto.replace("\xa0", " ").splitlines(), []
    for l in lineas:
        s = l.strip()
        if re.fullmatch(r"Ficha Art[ií]culo\s*\S*", s) or s in ("Anterior", "Siguiente", "-Usted está en la última versión de la norma-", "Ir a la última versión"):
            continue
        if re.match(r"Versi[oó]n de la Norma:", s): continue
        out.append(s)
    md = "\n".join(out)
    md = re.sub(r"(?m)^((?:ART[IÍ]CULO|Art[ií]culo)\s+\d+[^\s.]*\s*(?:bis|ter|quater)?\s*[.ºo°]*\s*[-–—.:]*)", r"**\1**", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return unir_lineas(md)


def unir_lineas(md):
    """Une líneas partidas a mitad de frase (texto de origen con saltos duros), sin tocar títulos ni párrafos."""
    bloques = md.split("\n\n")
    for _ in range(2):
        out = [bloques[0]]
        for b in bloques[1:]:
            prev = out[-1].rstrip()
            sig = b.lstrip()
            sigue = re.match(r"[a-záéíóúñ(0-9]", sig) and not re.match(r"\d{1,3}\s*[.)-]\s", sig)
            # Tras una palabra funcional («de», «del», «la»…) la frase sigue aunque empiece con mayúscula («Código Penal»).
            sigue = sigue or (re.search(r"\b(de|del|la|el|los|las|y|en|por|a|al|con|que|su|sus)$", prev, re.I) and not sig.startswith(("**", "#")))
            if prev and not re.search(r"[.:;)\]»”\"]$|\*\*$", prev) and sigue:
                out[-1] = prev + " " + b.lstrip()
            else:
                out.append(b)
        bloques = out
    return "\n\n".join(bloques)


def ultima_reforma(texto, propio):
    mejor = None
    for m in re.finditer(r"\(As[ií] (?:reformad|adicionad|modificad|derogad|corrid)[^)]*?ley\s*N[°º.]*\s*([\d.]+)\s+del?\s+(\d{1,2})\s+de\s+(\w+)\s+del?\s+(\d{4})", texto, re.I):
        num = m.group(1).replace(".", ""); mes = MESES.get(m.group(3).lower())
        if num == propio or not mes: continue
        f = (int(m.group(4)), mes, int(m.group(2)))
        if not mejor or f > mejor[0]: mejor = (f, num)
    return f"Ley {mejor[1]} del {mejor[0][0]:04d}-{mejor[0][1]:02d}-{mejor[0][2]:02d}" if mejor else ""


def descargar(pg, c):
    pg.goto(f"{BASE}/Informacion?param1={c['norma']}&param3=1", wait_until="domcontentloaded", timeout=40000)
    t0 = time.time()
    while "param2=" not in pg.url and time.time() - t0 < 15: pg.wait_for_timeout(300)
    esperar(pg, 30)
    vista = pg.evaluate("(document.querySelector('#divVista')||{}).innerText || ''")
    v = re.search(r"Versi[oó]n de la Norma:\s*(\d+)\s+de\s+(\d+)", vista)
    ultima = bool(re.search(r"Usted est[aá] en la [uú]ltima versi[oó]n", vista)) and v and v.group(1) == v.group(2)
    url = pg.url.split("&param5")[0].split("#")[0]
    notas = pg.evaluate(JS_NOTAS)
    ficha = ""
    try:
        pg.evaluate("document.querySelector('#botonFicha').click()"); pg.wait_for_timeout(1500); esperar(pg, 15)
        ficha = pg.evaluate("(document.querySelector('#divVista')||document.body).innerText")
    except Exception: pass
    fv = re.search(r"Versi[oó]n de la Norma:\s*\d+ de \d+ del (\d{2}/\d{2}/\d{4})", ficha)
    vig = re.search(r"Fecha de vigencia desde:\s*(\d{2}/\d{2}/\d{4})", ficha)
    derog = bool(re.search(r"^\s*\((Derogad[oa]|Anulad[oa])\)\s*$", ficha, re.M)) or c["derogada"]
    return {"vista": vista, "version": f"{v.group(1)} de {v.group(2)}" if v else "", "ultima": bool(ultima), "url": url, "notas": notas,
            "fecha_version": fv.group(1) if fv else "", "vigencia_desde": vig.group(1) if vig else "", "derogada": derog,
            "ficha_ok": bool(re.search(r"Datos Generales", ficha) and re.search(r"Versi[oó]n de la Norma", ficha))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("catalogo"); ap.add_argument("--desde", type=int, default=1); ap.add_argument("--hasta", type=int, default=20)
    ap.add_argument("--repo", default=""); ap.add_argument("--salida", default="lote"); ap.add_argument("--estado", default="estado_descargas.json")
    ap.add_argument("--chromium", default=os.environ.get("CHROMIUM", ""))
    ap.add_argument("--elegir", action="append", default=[], help="Resolución manual: N:TIPO:NUMERO, p. ej. 15:Ley:9822")
    a = ap.parse_args()
    os.makedirs(a.salida, exist_ok=True)
    estado = json.load(open(a.estado)) if os.path.exists(a.estado) else {"hechas": {}}
    repo = {}
    if a.repo:
        for f in os.listdir(a.repo):
            if f.endswith(".md"):
                m = re.search(r'^numero:\s*"([^"]+)"', open(os.path.join(a.repo, f), encoding="utf-8").read(3000), re.M)
                if m: repo[norm(m.group(1))] = f
    informe = []
    entradas = [e for e in leer_catalogo(a.catalogo) if a.desde <= e["n"] <= a.hasta]
    solo = {int(x) for x in os.environ.get("SOLO", "").split(",") if x}
    if solo: entradas = [e for e in entradas if e["n"] in solo]
    with sync_playwright() as pw:
        b = pw.chromium.launch(**({"executable_path": a.chromium} if a.chromium else {}))
        pg = b.new_page(locale="es-CR")
        for e in entradas:
            clave = norm(e["nombre"])
            if clave in estado["hechas"]:
                informe.append({**e, "resultado": "REPETIDA", "detalle": f"ya procesada como {estado['hechas'][clave]}"}); print(f"{e['n']:>3}. REPETIDA  {e['nombre']}"); continue
            try:
                manual = next((x.split(":") for x in a.elegir if x.split(":")[0] == str(e["n"])), None)
                if manual:
                    c, cands, mec = buscar_numero(pg, manual[1], manual[2])
                else:
                    c, cands, mec = buscar(pg, e)
                if not c:
                    informe.append({**e, "resultado": "PARA REVISAR", "detalle": mec, "candidatos": [f"{x['tipo']} {x['numero']} ({x['fecha']}): {x['nombre']}{' (Derogado)' if x['derogada'] else ''}" for x in cands[:6]]})
                    print(f"{e['n']:>3}. REVISAR   {e['nombre']} — {mec}"); time.sleep(2); continue
                d = descargar(pg, c)
                if not d["ultima"] or len(d["vista"]) < 500:
                    informe.append({**e, "resultado": "PARA REVISAR", "detalle": f"no se confirmó la última versión ({d['version']})"}); print(f"{e['n']:>3}. REVISAR   {e['nombre']} — versión no confirmada"); continue
                tipo = c["tipo"]; numero = c["numero"]
                etiqueta_num = "Constitución Política" if norm(tipo).startswith("constitucion") else f"{tipo} {numero}"
                archivo = repo.get(norm(etiqueta_num)) or (f"{etiqueta_num}.md" if not norm(tipo).startswith("constitucion") else "Constitución Política.md")
                cuerpo = limpiar(d["vista"])
                recobra = any(re.search(r"recobr\w*\s+(su\s+)?vigencia", n["t"], re.I) for n in d["notas"])
                # Convención de SINALEVI: las derogadas llevan «(Derogado)». Ficha cargada sin esa marca → vigente.
                estado_j = ("derogada, con artículos que recobraron vigencia" if recobra else "derogada") if d["derogada"] else ("vigente" if d["ficha_ok"] else "no indicado")
                fm = ["---", f'numero: "{etiqueta_num}"', f'nombre: "{c["nombre"]}"', f'materia: "{e["materia"]}"', f'estado: "{estado_j}"',
                      f'version_sinalevi: "{d["version"]}"', f'fecha_version: "{d["fecha_version"]}"', f'ultima_reforma: "{ultima_reforma(d["vista"], numero)}"',
                      f'ente_emisor: "{c["emisor"] or ""}"', f'fecha_norma: "{c["fecha"]}"', f'enlace: "{d["url"]}"', f'descargado: "{date.today().isoformat()}"', "---", ""]
                notas_md = ""
                if d["notas"]:
                    notas_md = "\n\n## Notas de SINALEVI sobre vigencia\n\n" + "\n".join(f"- {('Artículo ' + n['a']) if n['a'] else 'Nota general'}: {n['t']}" for n in d["notas"])
                open(os.path.join(a.salida, archivo), "w", encoding="utf-8").write("\n".join(fm) + cuerpo + notas_md + "\n")
                estado["hechas"][clave] = archivo
                nuevo = archivo not in repo.values()
                informe.append({**e, "resultado": "NUEVA" if nuevo else "ACTUALIZADA", "archivo": archivo, "norma": f"{etiqueta_num} — {c['nombre']}",
                                "version": d["version"], "fecha_version": d["fecha_version"], "estado": estado_j, "mecanismo": mec, "notas": len(d["notas"]), "enlace": d["url"]})
                print(f"{e['n']:>3}. {'NUEVA     ' if nuevo else 'ACTUALIZ. '} {archivo} · {d['version']} · {estado_j} · notas {len(d['notas'])}")
            except Exception as ex:
                informe.append({**e, "resultado": "ERROR", "detalle": str(ex)[:200]}); print(f"{e['n']:>3}. ERROR     {e['nombre']} — {str(ex)[:120]}")
            json.dump(estado, open(a.estado, "w"), ensure_ascii=False, indent=1)
            time.sleep(2.5)   # pausa entre normas
        b.close()
    json.dump(informe, open(os.path.join(a.salida, "_informe.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
