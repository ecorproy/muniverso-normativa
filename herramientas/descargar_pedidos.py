#!/usr/bin/env python3
"""Descarga desde SINALEVI las normas pedidas en herramientas/pedidos_descarga.json y las guarda en el repositorio.

Cada pedido: {"tipo": "Ley" | "Decreto Ejecutivo" | ..., "numero": "7130", "carpeta": "Civil",
              "estado": (opcional, sustituye al de la ficha), "articulos_vigentes": (opcional, p. ej. "709-818,825-870")}
Una norma a la vez y con pausas, igual que la descarga diaria. Los pedidos resueltos salen de la lista;
los que fallan quedan con el motivo para el siguiente intento. Resultado en herramientas/ultimo_pedido.md.
"""
import json, os, sys, time
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from descargar_normas import buscar_numero, descargar, limpiar, ultima_reforma  # noqa: E402
from gaceta_diaria import materia  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NACIONALES = os.path.join(RAIZ, "Leyes y decretos nacionales")
PEDIDOS = os.path.join(RAIZ, "herramientas", "pedidos_descarga.json")
INFORME = os.path.join(RAIZ, "herramientas", "ultimo_pedido.md")


def existente(etiqueta):
    for carpeta, _, archivos in os.walk(NACIONALES):
        for a in archivos:
            if a.endswith(".md"):
                with open(os.path.join(carpeta, a), encoding="utf-8") as fh:
                    if f'numero: "{etiqueta}"' in fh.read(400): return os.path.join(carpeta, a)
    return None


def bajar(pg, p):
    tipo, numero = p["tipo"], p["numero"]
    etiqueta = f"{tipo} {numero}"
    elegido, cands, _ = buscar_numero(pg, tipo, numero)
    if not elegido:
        return False, "sin coincidencia única en SINALEVI: " + "; ".join(f"{c.get('tipo')} {c.get('numero')} {c.get('nombre', '')[:60]}" for c in cands[:6])
    d = descargar(pg, elegido)
    if len(d["vista"]) < 300: return False, "texto vacío"
    if p.get("solo_vigentes") and d["derogada"]:
        return None, f"descartada: SINALEVI la marca derogada ({elegido['nombre']})"
    if not p.get("carpeta"): p["carpeta"] = materia(elegido["nombre"])
    q = lambda s: str(s or "").replace('"', "'")
    estado = p.get("estado") or ("derogada" if d["derogada"] else ("vigente" if d["ficha_ok"] else "no indicado"))
    ruta = existente(etiqueta) or os.path.join(NACIONALES, p.get("carpeta", "Administrativo"), f"{etiqueta}.md")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fm = ["---", f'numero: "{etiqueta}"', f'nombre: "{q(elegido["nombre"])}"', f'materia: "{q(p.get("carpeta", "Administrativo")).lower()}"',
          f'estado: "{q(estado)}"', f'version_sinalevi: "{d["version"]}"', f'fecha_version: "{d["fecha_version"]}"',
          f'ultima_reforma: "{ultima_reforma(d["vista"], numero)}"', f'ente_emisor: "{q(elegido.get("emisor"))}"',
          f'fecha_norma: "{elegido["fecha"]}"', f'enlace: "{d["url"]}"', f'descargado: "{date.today().isoformat()}"']
    if p.get("articulos_vigentes"): fm.append(f'articulos_vigentes: "{p["articulos_vigentes"]}"')
    fm += ["---", ""]
    notas = ("\n\n## Notas de SINALEVI sobre vigencia\n\n" + "\n".join(
        f"- {('Artículo ' + n['a']) if n['a'] else 'Nota general'}: {n['t']}" for n in d["notas"])) if d["notas"] else ""
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write("\n".join(fm) + limpiar(d["vista"]) + notas + "\n")
    return True, f"{os.path.relpath(ruta, RAIZ)} · {elegido['nombre']} · versión {d['version']} ({'última' if d['ultima'] else 'revisar versión'})"


def main():
    pedidos = json.load(open(PEDIDOS, encoding="utf-8")) if os.path.exists(PEDIDOS) else []
    if not pedidos: print("Sin pedidos"); return
    from playwright.sync_api import sync_playwright
    informe, quedan = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
        for i, p in enumerate(pedidos):
            if i: time.sleep(5)
            try:
                ok, det = bajar(pg, p)
            except Exception as ex:
                ok, det = False, f"error: {str(ex)[:160]}"
                try: b.close()
                except Exception: pass
                b = pw.chromium.launch(); pg = b.new_page(locale="es-CR")
            etiqueta = 'descargada' if ok else ('descartada' if ok is None else 'PENDIENTE')
            print(f"{p['tipo']} {p['numero']}: {etiqueta} · {det}", flush=True)
            informe.append(f"- {p['tipo']} {p['numero']}: {etiqueta} · {det}")
            if ok is False: quedan.append(dict(p, ultimo=det))
    json.dump(quedan, open(PEDIDOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(INFORME, "w", encoding="utf-8").write(f"# Descarga de normas pedidas · {date.today().isoformat()}\n\n" + "\n".join(informe) + "\n")


if __name__ == "__main__":
    main()
