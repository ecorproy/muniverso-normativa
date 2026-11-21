#!/usr/bin/env python3
"""Todos los dictámenes de la PGR que citan una norma: inventario año por año en SINALEVI y descarga del texto.

Lee herramientas/pedido_pgr_norma.json:
  {"carpeta": "22 Empleo público (Ley Marco y Ley de Salarios)",
   "consultas": [{"q": "10159", "desde": 2022, "exige": "regex que el texto debe cumplir"}, ...]}
Para cada consulta y cada año desde «desde» hasta hoy, busca en el texto completo de los pronunciamientos (solo dictámenes),
recorre todas las páginas y anota el id. Después baja cada dictamen que no esté ya en la biblioteca y lo guarda si su texto
cumple «exige» (para descartar coincidencias de número que no son la ley). Una petición a la vez, con pausas. Reanudable:
el avance queda en herramientas/pgr_norma_estado.json; si se agota el tiempo, la próxima corrida sigue donde quedó.
"""
import json
import os
import re
import time
from datetime import date
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEDIDO = os.path.join(RAIZ, "herramientas", "pedido_pgr_norma.json")
ESTADO = os.path.join(RAIZ, "herramientas", "pgr_norma_estado.json")
INFORME = os.path.join(RAIZ, "herramientas", "ultimo_pgr_norma.md")
PGR = os.path.join(RAIZ, "Jurisprudencia administrativa (PGR)")
LIMITE = float(os.environ.get("MINUTOS", "270")) * 60
T0 = time.time()

TARJETA = re.compile(r"\n\s*\d+\.\s+(Dictamen|Opinión Jurídica|Pronunciamiento[^:]*):\s*([^\n]+?)\s+del\s+(\d\d/\d\d/\d{4})\s*\n"
                     r"(?:Ver descriptores\s*\n)?\s*(?:Consultante:\s*([^\n]*)\n)?\s*(?:Institución:\s*([^\n]*)\n)?")
IDS = "()=>[...document.querySelectorAll('[onclick]')].map(e=>e.getAttribute('onclick')).filter(s=>/obtenerTextoCompleto\\(\\d+,0\\)/.test(s)).map(s=>s.match(/\\d+/)[0])"


def tiempo():
    return time.time() - T0 < LIMITE


def guardar(estado):
    json.dump(estado, open(ESTADO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


PAGINADOR = """(n)=>{
  const cands=[...document.querySelectorAll('a,button,li,span')].filter(e=>e.innerText&&e.innerText.trim()===String(n)&&e.offsetParent!==null);
  const enPag=cands.filter(e=>e.closest('.pagination,.paginacion,.pager,nav,ul'));
  const el=(enPag[0]||cands[0]); if(!el) return false; el.scrollIntoView(); el.click(); return true; }"""
TOTAL = re.compile(r"Resultados para[^\n(]*\((\d[\d.,]*)\)|(\d[\d.,]*)\s+resultados", re.I)


def leer_resultados(pg):
    t = pg.evaluate("()=>document.body.innerText")
    ids = pg.evaluate(IDS)
    tarjetas = TARJETA.findall(t)
    if len(tarjetas) != len(ids):
        raise RuntimeError(f"{len(tarjetas)} tarjetas y {len(ids)} enlaces")
    m = TOTAL.search(t)
    total = int(re.sub(r"[.,]", "", m.group(1) or m.group(2))) if m else None
    return list(zip(tarjetas, ids)), total


TOPE = 1000  # cantidadResultados: SINALEVI devuelve como máximo esa cantidad, de 10 en 10 por página


def busqueda(pg, q, anio, diag):
    """Todos los resultados de una búsqueda: página 1 por dirección y las siguientes con clic en el paginador."""
    u = (f"https://sinalevi.go.cr/BusquedaSimple/Resultados?pagina=1&radioBtnGroup=2&opcionSelected=2&textBuscar={quote(q)}"
         f"&textAnnio={anio}&selectedBuscarEn=T&TipoNorma=&TipoPronunciamiento=&ClaseAsunto=&cantidadResultados={TOPE}")
    for intento in range(3):
        try:
            pg.goto(u, timeout=120000, wait_until="domcontentloaded")
            for _ in range(60):
                pg.wait_for_timeout(1000)
                t = pg.evaluate("()=>document.body.innerText")
                if "Resultados para" in t or "No se encontraron" in t:
                    break
            pg.wait_for_timeout(1500)
            todos, total = leer_resultados(pg)
            if not diag.get("paginador"):
                diag["paginador"] = pg.evaluate("()=>{const p=document.querySelector('.pagination,.paginacion,.pager,nav ul');return p?p.outerHTML.slice(0,600):'(sin contenedor de paginación)'}")
            n = 2
            while n <= TOPE // 10 + 1:
                antes = {i for _, i in todos[-10:]}
                if not pg.evaluate(PAGINADOR, n):
                    break
                for _ in range(30):
                    pg.wait_for_timeout(1000)
                    try:
                        r, _ = leer_resultados(pg)
                    except RuntimeError:
                        continue
                    if r and {i for _, i in r} != antes:
                        break
                else:
                    break
                r, _ = leer_resultados(pg)
                nuevos = [x for x in r if x[1] not in {i for _, i in todos}]
                if not nuevos:
                    break
                todos += nuevos
                n += 1
                time.sleep(2)
            return todos, total, n - 1
        except Exception as ex:
            print(f"  reintento {intento + 1} «{q}» {anio}: {str(ex)[:120]}", flush=True)
            time.sleep(20 * (intento + 1))
    return None, None, 0


def texto(pg, i):
    url = f"https://sinalevi.go.cr/ResultadosPronunciamiento/Informacion?param1={i}&param2=0"
    pg.goto(url, timeout=120000, wait_until="domcontentloaded")
    for _ in range(40):
        pg.wait_for_timeout(1000)
        t = pg.evaluate("()=>document.body.innerText")
        if "Texto del pronunciamiento" in t and len(t) > 1500:
            break
    t = pg.evaluate("()=>document.body.innerText")
    a = t.rfind("Texto del pronunciamiento")
    b = t.rfind("Poder Judicial\nHacienda")
    return url, t[a + len("Texto del pronunciamiento"): b if b > a else None].strip()


def ya_en_biblioteca():
    vistos = set()
    for base, _, archivos in os.walk(PGR):
        for f in archivos:
            m = re.match(r"Dictamen (C-\d+-\d{4})\.md$", f)
            if m:
                vistos.add(m.group(1))
    return vistos


def main():
    pedido = json.load(open(PEDIDO, encoding="utf-8"))
    estado = json.load(open(ESTADO, encoding="utf-8")) if os.path.exists(ESTADO) else {"busquedas": {}, "inv": {}, "bajados": {}, "descartados": {}}
    hoy = date.today().year
    diag = {}
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(locale="es-CR")
        # 1. Inventario
        for c in pedido["consultas"]:
            for anio in range(c["desde"], hoy + 1):
                clave = f"{c['q']}|{anio}"
                if clave in estado["busquedas"] or not tiempo():
                    continue
                r, total_sinalevi, paginas = busqueda(pg, c["q"], anio, diag)
                time.sleep(3)
                if r is None:
                    estado["busquedas"][clave] = "sin respuesta"
                else:
                    dict_n = 0
                    for (tipo, num, fecha, cons, inst), i in r:
                        if tipo != "Dictamen":
                            continue
                        dict_n += 1
                        if i not in estado["inv"]:
                            num = num.strip().replace(" ", "")
                            estado["inv"][i] = {"numero": f"C-{num.zfill(3)}-{fecha[-4:]}", "fecha": fecha, "consultante": cons.strip(),
                                                "institucion": inst.strip(), "consultas": [c["q"]]}
                        elif c["q"] not in estado["inv"][i]["consultas"]:
                            estado["inv"][i]["consultas"].append(c["q"])
                    completo = f" · INCOMPLETO: llegó al tope de {TOPE}" if len(r) >= TOPE else ""
                    estado["busquedas"][clave] = f"{len(r)} resultados ({dict_n} dictámenes) en {paginas} página(s){completo}"
                print(f"«{c['q']}» {anio}: {estado['busquedas'].get(clave)}", flush=True)
                guardar(estado)
        # 2. Descarga
        exige = [re.compile(c["exige"], re.I) for c in pedido["consultas"]]
        presentes = ya_en_biblioteca()
        carpeta = os.path.join(PGR, pedido["carpeta"])
        os.makedirs(carpeta, exist_ok=True)
        for i, v in sorted(estado["inv"].items(), key=lambda kv: kv[1]["fecha"][-4:] + kv[1]["fecha"][3:5] + kv[1]["fecha"][:2], reverse=True):
            if i in estado["bajados"] or i in estado["descartados"] or not tiempo():
                continue
            if v["numero"] in presentes:
                estado["bajados"][i] = "ya estaba"
                continue
            try:
                url, c = texto(pg, i)
                time.sleep(3)
                if len(c) < 500:
                    raise RuntimeError("texto vacío")
            except Exception as ex:
                print(f"  {v['numero']}: {str(ex)[:120]}", flush=True)
                try:
                    nav.close()
                except Exception as ex2:
                    print(f"  cierre: {ex2}", flush=True)
                nav = pw.chromium.launch()
                pg = nav.new_page(locale="es-CR")
                continue
            if not any(e.search(c) for e in exige):
                estado["descartados"][i] = "no cita la norma"
                guardar(estado)
                continue
            cuerpo = re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t\u00a0]+\n", "\n", c))
            q = lambda s: str(s or "").replace('"', "'")
            fm = ["---", f'numero: "{v["numero"]}"', 'tipo: "Dictamen de la Procuraduría General de la República"', f'fecha: "{v["fecha"]}"',
                  f'consultante: "{q(v["consultante"])}"', f'institucion: "{q(v["institucion"])}"', f'materia: "{pedido["materia"]}"',
                  f'temas: "{q("; ".join(v["consultas"]))}"', f'enlace: "{url}"', f'descargado: "{date.today().isoformat()}"', "---", ""]
            open(os.path.join(carpeta, f"Dictamen {v['numero']}.md"), "w", encoding="utf-8").write("\n".join(fm) + f"# Dictamen {v['numero']}\n\n" + cuerpo + "\n")
            estado["bajados"][i] = v["numero"]
            presentes.add(v["numero"])
            print(f"  bajado {v['numero']}", flush=True)
            guardar(estado)
        nav.close()
    guardar(estado)
    faltan = [v["numero"] for i, v in estado["inv"].items() if i not in estado["bajados"] and i not in estado["descartados"]]
    sin = [k for k, v in estado["busquedas"].items() if v.startswith("sin respuesta") or "INCOMPLETO" in v]
    nuevos = sum(1 for v in estado["bajados"].values() if v != "ya estaba")
    open(INFORME, "w", encoding="utf-8").write(
        f"# Dictámenes de la PGR por norma · {date.today().isoformat()}\n\n"
        f"Inventario: {len(estado['inv'])} dictámenes. Bajados nuevos: {nuevos}. Ya estaban: {len(estado['bajados']) - nuevos}. "
        f"Descartados (no citan la norma): {len(estado['descartados'])}. Pendientes: {len(faltan)}.\n\n"
        + "## Búsquedas\n\n" + "\n".join(f"- {k}: {v}" for k, v in sorted(estado["busquedas"].items())) + "\n\n"
        + f"## Paginador de SINALEVI\n\n```\n{diag.get('paginador', '(no se leyó)')}\n```\n\n"
        + ("## Sin respuesta (se reintenta en la próxima corrida)\n\n" + "\n".join(f"- {k}" for k in sin) + "\n" if sin else ""))
    for k in sin:
        estado["busquedas"].pop(k)
    guardar(estado)
    print(f"Inventario {len(estado['inv'])}; bajados nuevos {nuevos}; pendientes {len(faltan)}", flush=True)


if __name__ == "__main__":
    main()
