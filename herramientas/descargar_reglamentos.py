#!/usr/bin/env python3
"""Descarga los reglamentos municipales pedidos en herramientas/pedidos_reglamentos.json y los guarda en
Reglamentos municipales/<provincia>/<cantón>/<nombre> (<año>).md, con la misma ficha que los demás.
Una norma a la vez, con pausas. Se detiene antes del límite de tiempo de la acción; lo que falta queda en la lista
y la acción programada lo retoma. Resultado en herramientas/ultimo_pedido_reglamentos.md."""
import json, os, sys, time
from datetime import date
sys.path.insert(0, os.path.dirname(__file__))
from descargar_normas import descargar, limpiar  # noqa: E402
from reglamentos_comun import RAIZ, inventario, archivo  # noqa: E402

PEDIDOS = os.path.join(RAIZ, "herramientas", "pedidos_reglamentos.json")
INFORME = os.path.join(RAIZ, "herramientas", "ultimo_pedido_reglamentos.md")
LIMITE = float(os.environ.get("MINUTOS", "250")) * 60


def bajar(pg, p, ids):
    if p["norma"] in ids: return None, "ya estaba en el repositorio"
    d = descargar(pg, {"norma": p["norma"], "derogada": False})
    if len(d["vista"]) < 300: return False, "texto vacío"
    if d["derogada"]: return None, "descartada: SINALEVI la marca derogada"
    q = lambda s: str(s or "").replace('"', "'")
    ruta = archivo(p["nombre"], p["fecha"], p["provincia"], p["carpeta"])
    canton = p["carpeta"]
    fm = ["---", f'numero: "Reglamento municipal {q(p["numero"])} ({p["fecha"]})"', f'nombre: "{q(p["nombre"])}"', 'materia: "municipal"',
          f'canton: "{q(canton)}"', f'estado: "{"vigente" if d["ficha_ok"] else "no indicado"}"', f'version_sinalevi: "{d["version"]}"',
          f'fecha_version: "{d["fecha_version"]}"', f'ente_emisor: "{q(p["emisor"])}"', f'fecha_norma: "{p["fecha"]}"', f'enlace: "{d["url"]}"',
          f'descargado: "{date.today().isoformat()}"', "---", ""]
    notas = ("\n\n## Notas de SINALEVI sobre vigencia\n\n" + "\n".join(
        f"- {('Artículo ' + n['a']) if n['a'] else 'Nota general'}: {n['t']}" for n in d["notas"])) if d["notas"] else ""
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write("\n".join(fm) + limpiar(d["vista"]) + notas + "\n")
    ids.add(p["norma"])
    return True, f"{os.path.relpath(ruta, RAIZ)} · versión {d['version']}"


def main():
    pedidos = json.load(open(PEDIDOS, encoding="utf-8")) if os.path.exists(PEDIDOS) else []
    if not pedidos: print("Sin pedidos"); return
    ids, _, _ = inventario()
    from playwright.sync_api import sync_playwright
    t0, informe, quedan = time.time(), [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
        for i, p in enumerate(pedidos):
            if time.time() - t0 > LIMITE: quedan += pedidos[i:]; break
            if i: time.sleep(4)
            try:
                ok, det = bajar(pg, p, ids)
            except Exception as ex:
                ok, det = False, f"error: {str(ex)[:160]}"
                try: b.close()
                except Exception: pass
                b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
            if ok is False and p.get("intentos", 0) < 2: quedan.append(dict(p, intentos=p.get("intentos", 0) + 1, ultimo=det))
            et = "descargado" if ok else ("omitido" if ok is None else "PENDIENTE")
            informe.append(f"- {p['carpeta']} · {p['nombre'][:90]}: {et} · {det}"); print(informe[-1], flush=True)
    json.dump(quedan, open(PEDIDOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hechos = sum(1 for l in informe if ": descargado" in l)
    open(INFORME, "w", encoding="utf-8").write(f"# Reglamentos municipales pedidos · {date.today().isoformat()}\n\n{hechos} descargados en esta corrida; quedan {len(quedan)}.\n\n" + "\n".join(informe) + "\n")


if __name__ == "__main__":
    main()
