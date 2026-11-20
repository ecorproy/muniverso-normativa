#!/usr/bin/env python3
"""Explora SINALEVI y lista los reglamentos municipales vigentes que aún no están en el repositorio.
Entrada: herramientas/exploracion_reglamentos.json = {"terminos": [...]}. Salida: herramientas/candidatos_reglamentos.json.
Solo lee listados de resultados (no descarga textos). Una búsqueda a la vez, con pausas."""
import json, os, sys, time
from datetime import date
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from descargar_normas import BASE, JS_TARJETAS, tarjeta, esperar, norm  # noqa: E402
from reglamentos_comun import REFORMA, RAIZ, inventario, destino  # noqa: E402

ENTRADA = os.path.join(RAIZ, "herramientas", "exploracion_reglamentos.json")
SALIDA = os.path.join(RAIZ, "herramientas", "candidatos_reglamentos.json")
JS_TOTAL = "() => { try { const lv = jQuery('#listView').data('kendoListView'); return lv ? lv.dataSource.total() : -1 } catch (e) { return -1 } }"
JS_PAGINA = """(n) => { try { const ds = jQuery('#listView').data('kendoListView').dataSource; ds.pageSize(400); ds.page(n); return ds.page(); } catch (e) { return -1 } }"""


def tarjetas(pg):
    """Todas las tarjetas del listado, página por página del control de resultados."""
    total = pg.evaluate(JS_TOTAL); out = {}
    paginas = max(1, -(-total // 400)) if total and total > 0 else 1
    for n in range(1, paginas + 1):
        if total and total > 0:
            pg.evaluate(JS_PAGINA, n); pg.wait_for_timeout(1500); esperar(pg, 15)
        for c in pg.evaluate(JS_TARJETAS): out[c["norma"]] = c
    return list(out.values()), total


class Navegador:
    """Un navegador que se reabre si SINALEVI corta la conexión."""
    def __init__(self, pw): self.pw = pw; self.abrir()
    def abrir(self):
        self.b = self.pw.chromium.launch(); self.pg = self.b.new_page(locale="es-CR")
    def reabrir(self):
        try: self.b.close()
        except Exception as ex: print("aviso: el navegador no cerró bien:", str(ex)[:80], flush=True)
        self.abrir()


def consultar(nav, t, desde="", hasta="", intentos=3):
    """Una búsqueda por nombre, con reintentos y espera creciente. Con años, SINALEVI filtra por fecha de la norma."""
    años = f"&radioFechas=1&AnnioDesde={desde}&AnnioHasta={hasta}" if desde else ""
    url = f"{BASE}/Resultados?TipoBusqueda=2&Pagina=1&Nombre={quote(t)}{años}&NormasHistoricas=false&CantidadResultados=-1"
    ultimo = None
    for i in range(intentos):
        try:
            nav.pg.goto(url, wait_until="domcontentloaded", timeout=90000); esperar(nav.pg, 40)
            return tarjetas(nav.pg)
        except Exception as ex:
            ultimo = ex; time.sleep(10 * (i + 1)); nav.reabrir()
    raise ultimo


LIMITE_TERMINO = 45 * 60  # segundos por término, para que una palabra ambigua no consuma toda la corrida


def explorar(nav, t, desde=None, hasta=None, log=None, t0=None):
    """Busca el término; si SINALEVI no responde (listados enormes con palabras ambiguas), parte el período en dos y vuelve
    a intentar, hasta un año a la vez. Devuelve todas las tarjetas, sin repetir."""
    t0 = t0 or time.time()
    if time.time() - t0 > LIMITE_TERMINO:
        if log is not None: log.append(f"{desde}-{hasta}: sin respuesta (tiempo agotado)")
        return []
    try:
        cs, total = consultar(nav, t, str(desde or ""), str(hasta or ""))
        if log is not None: log.append(f"{desde or 'todo'}-{hasta or ''}: {total}")
        return cs
    except Exception as ex:
        if desde is None: desde, hasta = 1800, date.today().year
        elif desde >= hasta:
            if log is not None: log.append(f"{desde}: sin respuesta ({str(ex)[:60]})")
            return []
        medio = (desde + hasta) // 2
        time.sleep(4)
        return explorar(nav, t, desde, medio, log, t0) + explorar(nav, t, medio + 1, hasta, log, t0)


def main():
    terminos = json.load(open(ENTRADA, encoding="utf-8"))["terminos"]
    ids, mapa, cantones = inventario()
    vistos, sin_ubicar, informe = {}, {}, []
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = Navegador(pw)
        for i, t in enumerate(terminos):
            if i: time.sleep(4)
            tramos = []
            cs = explorar(nav, t, log=tramos)
            n = 0
            for c in {c["norma"]: c for c in cs}.values():
                tj = tarjeta(c["tarjeta"])
                if not tj or not norm(tj["tipo"]).startswith("reglamento municipal") or tj["derogada"]: continue
                if c["norma"] in ids or c["norma"] in vistos: continue
                if REFORMA.match(tj["nombre"]) and "integral" not in tj["nombre"].lower(): continue  # solo textos consolidados
                dst = destino(tj.get("emisor"), mapa, cantones)
                if not dst: sin_ubicar[c["norma"]] = {**tj, "norma": c["norma"]}; continue
                vistos[c["norma"]] = {"norma": c["norma"], "version": c["version"], "numero": tj["numero"], "nombre": tj["nombre"], "fecha": tj["fecha"],
                                      "emisor": tj["emisor"], "provincia": dst[0], "carpeta": dst[1], "termino": t}; n += 1
            partido = len(tramos) > 1
            informe.append(f"{t}: {len(cs)} resultados{' en ' + str(len(tramos)) + ' tramos por año' if partido else ''}, {n} reglamentos municipales nuevos"
                           + ("; sin respuesta: " + ", ".join(x for x in tramos if 'sin respuesta' in x) if any('sin respuesta' in x for x in tramos) else ""))
            print(informe[-1], flush=True)
    lista = sorted(vistos.values(), key=lambda x: (x["provincia"], x["carpeta"], x["fecha"][-4:], x["nombre"]))
    json.dump({"total": len(lista), "sin_ubicar": list(sin_ubicar.values()), "busquedas": informe, "candidatos": lista},
              open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(lista), "reglamentos municipales vigentes que no están en el repositorio;", len(sin_ubicar), "sin ubicar")


if __name__ == "__main__":
    main()
