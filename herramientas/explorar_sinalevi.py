#!/usr/bin/env python3
"""Explora SINALEVI con búsquedas selectivas por nombre y lista las leyes vigentes que aún no están en el repositorio.
Entrada: herramientas/exploracion.json = {"terminos": ["Ley General", ...]}. Salida: herramientas/candidatos.json.
Solo lee los listados de resultados (no descarga textos). Una búsqueda a la vez, con pausas."""
import json, os, re, sys, time
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from descargar_normas import BASE, JS_TARJETAS, JS_AMPLIAR, tarjeta, esperar, norm  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(RAIZ, "herramientas", "exploracion.json")
SALIDA = os.path.join(RAIZ, "herramientas", "candidatos.json")


def en_repo():
    nums = set()
    for carpeta in ("Leyes y decretos nacionales", "Leyes locales"):
        for r, _, fs in os.walk(os.path.join(RAIZ, carpeta)):
            for f in fs:
                if f.endswith(".md"):
                    m = re.search(r'^numero:\s*"([^"]+)"', open(os.path.join(r, f), encoding="utf-8").read(400), re.M)
                    if m: nums.add(m.group(1))
    return nums


def main():
    terminos = json.load(open(ENTRADA, encoding="utf-8"))["terminos"]
    ya = en_repo(); vistos = {}
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
        for i, t in enumerate(terminos):
            if i: time.sleep(4)
            try:
                pg.goto(f"{BASE}/Resultados?TipoBusqueda=2&Pagina=1&Nombre={quote(t)}&NormasHistoricas=false&CantidadResultados=-1", wait_until="domcontentloaded", timeout=60000)
                esperar(pg, 30)
                if pg.evaluate(JS_AMPLIAR) > 10: pg.wait_for_timeout(2500)
                n = 0
                for c in pg.evaluate(JS_TARJETAS):
                    tj = tarjeta(c["tarjeta"])
                    if not tj or norm(tj["tipo"]) != "ley" or tj["derogada"]: continue
                    clave = f"Ley {tj['numero'].split('-')[0]}"
                    if clave in ya or clave in vistos: continue
                    vistos[clave] = {"numero": tj["numero"], "nombre": tj["nombre"], "fecha": tj["fecha"], "emisor": tj.get("emisor"), "termino": t}; n += 1
                print(f"{t}: {n} nuevas", flush=True)
            except Exception as ex:
                print(f"{t}: error {str(ex)[:120]}", flush=True)
    json.dump(sorted(vistos.values(), key=lambda x: int(re.sub(r'\D', '', x["numero"]) or 0)), open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(vistos), "leyes vigentes que no están en el repositorio")


if __name__ == "__main__":
    main()
