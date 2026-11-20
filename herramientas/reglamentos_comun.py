"""Utilidades compartidas para los reglamentos municipales: qué hay ya en el repositorio y a qué carpeta va cada ente emisor."""
import os, re
from descargar_normas import norm

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGL = os.path.join(RAIZ, "Reglamentos municipales")


def inventario():
    """Ids de SINALEVI ya descargados y mapa ente emisor → (provincia, carpeta), tomado de los archivos existentes."""
    ids, mapa, cantones = set(), {}, {}
    for r, _, fs in os.walk(REGL):
        rel = os.path.relpath(r, REGL).split(os.sep)
        if len(rel) >= 2: cantones.setdefault(norm(rel[1]), (rel[0], rel[1]))
        for f in fs:
            if not f.endswith(".md"): continue
            t = open(os.path.join(r, f), encoding="utf-8").read(1500)
            p = re.search(r"param1=(\d+)", t); e = re.search(r'^ente_emisor: "([^"]*)"', t, re.M)
            if p: ids.add(p.group(1))
            if e and len(rel) >= 2: mapa.setdefault(norm(e.group(1)), (rel[0], rel[1]))
    return ids, mapa, cantones


def destino(emisor, mapa, cantones):
    """Provincia y carpeta para un ente emisor, o None si no se puede ubicar con certeza."""
    e = norm(emisor or "")
    if not e: return None
    if e in mapa: return mapa[e]
    m = re.match(r"(?:municipalidad|concejo municipal) (?:del? )?(?:canton (?:central )?(?:de )?)?(.+)$", e)
    if m and m.group(1) in cantones: return cantones[m.group(1)]
    if e.startswith("concejo municipal de distrito"):
        for k, v in cantones.items():
            if k.startswith("concejo municipal de distrito") and k.split()[-1] == e.split()[-1]: return v
    return None


def archivo(nombre, fecha, prov, carpeta):
    base = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", re.sub(r"\s+", " ", nombre)).strip(" .")[:150] or "Reglamento"
    anio = (fecha or "")[-4:]
    d = os.path.join(REGL, prov, carpeta); os.makedirs(d, exist_ok=True)
    ruta = os.path.join(d, f"{base} ({anio}).md"); k = 2
    while os.path.exists(ruta):
        ruta = os.path.join(d, f"{base} ({anio}) ({k}).md"); k += 1
    return ruta
