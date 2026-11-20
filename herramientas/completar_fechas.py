#!/usr/bin/env python3
"""Completa la fecha de la norma (fecha_norma) en los archivos que no la tienen, tomándola de la ficha de SINALEVI.
Entrada: herramientas/completar_fechas.json = [{"archivo": ruta, "tipo": "Ley", "numero": "30"}].
Solo agrega la línea fecha_norma; no toca el texto. Una búsqueda a la vez, con pausas. Informe en herramientas/ultimas_fechas.md."""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from descargar_normas import buscar_numero  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(RAIZ, "herramientas", "completar_fechas.json")
INFORME = os.path.join(RAIZ, "herramientas", "ultimas_fechas.md")


def main():
    pedidos = json.load(open(ENTRADA, encoding="utf-8")) if os.path.exists(ENTRADA) else []
    if not pedidos: print("Sin pedidos"); return
    from playwright.sync_api import sync_playwright
    informe, quedan = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
        for i, p in enumerate(pedidos):
            if i: time.sleep(4)
            ruta = os.path.join(RAIZ, p["archivo"])
            try:
                elegido, cands, _ = buscar_numero(pg, p["tipo"], p["numero"])
            except Exception as ex:
                elegido, cands = None, []; informe.append(f"- {p['archivo']}: error {str(ex)[:100]}")
            fecha = (elegido or {}).get("fecha", "")
            if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha or ""):
                quedan.append(dict(p, intentos=p.get("intentos", 0) + 1)) if p.get("intentos", 0) < 2 else None
                informe.append(f"- {p['archivo']}: sin coincidencia única ({len(cands)} candidatos)"); continue
            t = open(ruta, encoding="utf-8").read()
            if "\nfecha_norma:" in t.split("\n---", 2)[0] + "\n---": informe.append(f"- {p['archivo']}: ya tenía fecha"); continue
            t = t.replace("\n---", f'\nfecha_norma: "{fecha}"\n---', 1) if t.startswith("---") else t
            open(ruta, "w", encoding="utf-8").write(t)
            informe.append(f"- {p['archivo']}: {fecha} · {elegido.get('nombre', '')[:80]}"); print(informe[-1], flush=True)
    json.dump(quedan, open(ENTRADA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(INFORME, "w", encoding="utf-8").write("# Fechas completadas desde SINALEVI\n\n" + "\n".join(informe) + "\n")


if __name__ == "__main__":
    main()
