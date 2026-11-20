#!/usr/bin/env python3
"""Explora SINALEVI y lista los reglamentos municipales vigentes que aún no están en el repositorio.
Entrada: herramientas/exploracion_reglamentos.json = {"terminos": [...]}. Salida: herramientas/candidatos_reglamentos.json.
Solo lee listados de resultados (no descarga textos). Una búsqueda a la vez, con pausas."""
import json, os, sys, time
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


def main():
    terminos = json.load(open(ENTRADA, encoding="utf-8"))["terminos"]
    ids, mapa, cantones = inventario()
    vistos, sin_ubicar, informe = {}, {}, []
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
        for i, t in enumerate(terminos):
            if i: time.sleep(4)
            try:
                pg.goto(f"{BASE}/Resultados?TipoBusqueda=2&Pagina=1&Nombre={quote(t)}&NormasHistoricas=false&CantidadResultados=-1", wait_until="domcontentloaded", timeout=90000)
                esperar(pg, 40)
                cs, total = tarjetas(pg); n = 0
                for c in cs:
                    tj = tarjeta(c["tarjeta"])
                    if not tj or not norm(tj["tipo"]).startswith("reglamento municipal") or tj["derogada"]: continue
                    if c["norma"] in ids or c["norma"] in vistos: continue
                    if REFORMA.match(tj["nombre"]) and "integral" not in tj["nombre"].lower(): continue  # solo textos consolidados
                    dst = destino(tj.get("emisor"), mapa, cantones)
                    if not dst: sin_ubicar[c["norma"]] = {**tj, "norma": c["norma"]}; continue
                    vistos[c["norma"]] = {"norma": c["norma"], "version": c["version"], "numero": tj["numero"], "nombre": tj["nombre"], "fecha": tj["fecha"],
                                          "emisor": tj["emisor"], "provincia": dst[0], "carpeta": dst[1], "termino": t}; n += 1
                informe.append(f"{t}: {total} resultados, {n} reglamentos municipales nuevos")
                print(informe[-1], flush=True)
            except Exception as ex:
                informe.append(f"{t}: error {str(ex)[:120]}"); print(informe[-1], flush=True)
                try: b.close()
                except Exception: pass
                b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
    lista = sorted(vistos.values(), key=lambda x: (x["provincia"], x["carpeta"], x["fecha"][-4:], x["nombre"]))
    json.dump({"total": len(lista), "sin_ubicar": list(sin_ubicar.values()), "busquedas": informe, "candidatos": lista},
              open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(lista), "reglamentos municipales vigentes que no están en el repositorio;", len(sin_ubicar), "sin ubicar")


if __name__ == "__main__":
    main()
