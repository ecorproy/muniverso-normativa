#!/usr/bin/env bash
# Rearma el taller del libro Seguridad Municipal 360° en una sesión nueva.
# Requisito: haber corrido antes "Taller de cotejo/preparar-taller.sh", que clona la rama main y esta rama
# y deja en /home/claude/scripts los programas base que usa hacer_build_libro.py.
# Uso:  bash "preparar-libro.sh"
# Prueba en otra carpeta:  BASE=/tmp/prueba bash "preparar-libro.sh"  (necesita BASE/repo con los dos clones)
# No borra nada: copia encima de lo que haya.
set -u
BASE=${BASE:-/home/claude}
T="$BASE/repo/360/Seguridad Municipal 360°/Taller del libro"
M="$BASE/repo/main"
[ -d "$T" ] || { echo "!! no aparece el taller del libro en $T"; exit 1; }
[ -d "$M" ] || { echo "!! no aparece el clon de main en $M"; exit 1; }

echo "== programas"
mkdir -p "$BASE/mis_scripts"
cp "$T"/scripts/*.py "$T"/scripts/*.sh "$BASE/mis_scripts/"
ls "$BASE/mis_scripts" | wc -l | sed 's/^/  archivos: /'

echo "== bitácora y notas"
mkdir -p "$BASE/libro/fuentes/sala1" "$BASE/libro/fuentes/tca" "$BASE/libro/fuentes/votos" "$BASE/libro/fuentes/dictamenes"
cp "$T/Bitácora del taller.md" "$BASE/libro/estado_taller.md"
cp "$T"/notas/* "$BASE/libro/"

echo "== fuentes que el verificador busca en /home/claude/libro/fuentes"
cp "$T"/fuentes/* "$BASE/libro/fuentes/"
cp "$M/Leyes y decretos nacionales/Ambiental/Ley 10939.md" "$BASE/libro/fuentes/"
cp "$M/Leyes y decretos nacionales/Municipal/Ley 10594.md" "$BASE/libro/fuentes/"
cp "$M/Leyes y decretos nacionales/Ambiental/Decreto Ejecutivo 42075.md" "$BASE/libro/fuentes/"
cp "$M/Leyes y decretos nacionales/Municipal/Reglamento de Construcciones INVU (2018).md" "$BASE/libro/fuentes/"
cp "$M/Jurisprudencia de casación (Sala Primera)/Municipal/"Sentencia\ Sala\ Primera\ *.md "$BASE/libro/fuentes/sala1/"
cp "$M/Jurisprudencia contencioso administrativa (TCA)/Municipal/"Sentencia\ TCA\ *.md "$BASE/libro/fuentes/tca/"
ls "$BASE/libro/fuentes" | wc -l | sed 's/^/  archivos y carpetas: /'

echo "== capítulos"
for d in "$T"/Capítulos/*/; do
  n=$(basename "$d")
  mkdir -p "$BASE/libro/$n"
  cp -r "$d". "$BASE/libro/$n/"
done
ls "$BASE/libro" | grep -E '^(cap|t)[0-9]' | tr '\n' ' '; echo

echo "== verificador"
if [ "$BASE" = /home/claude ]; then
  mkdir -p /home/claude/art
  python3 -I /home/claude/mis_scripts/hacer_build_libro.py
else
  echo "  prueba en $BASE: no se genera build_libro.py, que usa rutas fijas"
fi

echo "== obras de doctrina que no se guardan en el repositorio"
[ -s "$BASE/libro/fuentes/perez_pag.txt" ] || echo "  falta: Pérez Hernández, Tabares Neyra y Díaz Legón (2019). Adjuntar el PDF si hay que volver a verificar el capítulo 2."
[ -s "$BASE/libro/fuentes/wilches_pag.txt" ] || echo "  falta: Wilches-Chaux (2007). Adjuntar el PDF si hay que volver a verificar el capítulo 2."

echo "Listo. Ejemplo:"
echo "  cd /home/claude/art && SRC=/home/claude/libro/t36/src OUT=/home/claude/libro/t36/out python3 -I /home/claude/mis_scripts/build_libro.py"
