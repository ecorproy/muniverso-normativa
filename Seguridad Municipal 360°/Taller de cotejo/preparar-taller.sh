#!/usr/bin/env bash
# Rearma el taller de cotejo de Seguridad Municipal 360° en una sesión nueva.
# Uso:  bash "preparar-taller.sh"
# No borra nada: si una carpeta ya existe, la deja como está.
set -u

BASE=/home/claude
REPO=https://github.com/ecorproy/muniverso-normativa.git
UP=/mnt/user-data/uploads

echo "== carpetas"
mkdir -p "$BASE"/{scripts,art/src,art/src3,art/out3,refs,cgr,export,icn,pdf,pele,madero,tocq,repo}

echo "== repositorio"
if [ ! -d "$BASE/repo/main/.git" ]; then
  git clone --filter=blob:none "$REPO" "$BASE/repo/main" || echo "  !! no se pudo clonar main"
fi
if [ ! -d "$BASE/repo/360/.git" ]; then
  git clone --filter=blob:none -b seguridad-municipal-360 "$REPO" "$BASE/repo/360" || echo "  !! no se pudo clonar la rama 360"
fi

T="$BASE/repo/360/Seguridad Municipal 360°/Taller de cotejo"
if [ ! -d "$T" ]; then echo "!! no aparece el taller en el clon; se detiene aquí"; exit 1; fi

echo "== programas y bitácora"
cp "$T"/scripts/*.py "$BASE/scripts/"
cp "$T/NOTAS.md" "$BASE/art/NOTAS.md"
cp "$T/overrides.json" "$BASE/art/overrides.json"
cp "$T/all.md" "$BASE/art/src3/all.md"
cp "$T"/refs/* "$BASE/refs/"
cp "$T"/articulo-src/*.md "$BASE/art/src/" 2>/dev/null

echo "== textos de la Contraloría"
for f in "$BASE/repo/360/Seguridad Municipal 360°/Criterios CGR"/*" - texto extraído.txt"; do
  [ -e "$f" ] || continue
  b=$(basename "$f"); cp "$f" "$BASE/cgr/${b% - texto extraído.txt}.txt"
done
ls "$BASE/cgr" | sed 's/^/  /'

echo "== Informe ICN 2026 (está en el repositorio)"
icn="$BASE/repo/360/Seguridad Municipal 360°/Referencias externas/Informe ICN 2026 (CPC) - texto extraído.txt"
[ -e "$icn" ] && cp "$icn" "$BASE/icn/icn.txt" && echo "  icn.txt listo"

echo "== obras ajenas con enlace abierto"
# Tocqueville, La democracia en América (edición en línea citada en el libro)
if [ ! -s "$BASE/tocq/tocq.txt" ]; then
  curl -sS -L --max-time 180 -o "$BASE/tocq/tocq.pdf" \
    "https://www.suneo.mx/literatura/subidas/Alexis%20de%20Tocqueville%20La%20Democracia%20en%20America.pdf" \
    && pdftotext -layout "$BASE/tocq/tocq.pdf" "$BASE/tocq/tocq.txt" \
    && echo "  tocq.txt listo (la página del archivo es la que se cita)" \
    || echo "  !! no se pudo bajar Tocqueville"
fi
# Madero Gómez (2023), SciELO México, acceso abierto
if [ ! -s "$BASE/madero/madero_pag.txt" ]; then
  curl -sS -L --max-time 180 -o "$BASE/madero/madero.pdf" \
    "https://www.scielo.org.mx/pdf/cya/v68n1/0186-1042-cya-68-01-235.pdf" \
    && pdftotext -layout "$BASE/madero/madero.pdf" "$BASE/madero/madero.txt" \
    && python3 -I -c "
t=open('$BASE/madero/madero.txt',encoding='utf-8').read().split(chr(12))
open('$BASE/madero/madero_pag.txt','w',encoding='utf-8').write(chr(12)*234+chr(12).join(t[:25]))" \
    && echo "  madero_pag.txt listo (páginas 235-259 de la revista)" \
    || echo "  !! no se pudo bajar Madero Gómez"
fi

echo "== obras que hay que volver a aportar como archivo adjunto"
# Pele (2015): el PDF se aportó adjunto. Si vuelve a estar en uploads, se procesa.
p=$(ls "$UP"/*KANT_Y_LA_DIGNIDAD_HUMANA*.pdf 2>/dev/null | head -1)
if [ -n "${p:-}" ] && [ ! -s "$BASE/pele/pele_pag.txt" ]; then
  cp "$p" "$BASE/pele/pele.pdf"
  pdftotext -layout "$BASE/pele/pele.pdf" "$BASE/pele/pele.txt"
  python3 -I -c "
import re
t=open('$BASE/pele/pele.txt',encoding='utf-8').read().split(chr(12))[:32]
d=lambda x: re.sub(r'(\w)-\s*\n\s*(\w)',r'\1\2',x)
open('$BASE/pele/pele_pag.txt','w',encoding='utf-8').write(chr(12)*14+chr(12).join(p+chr(10)+d(p) for p in t))"
  echo "  pele_pag.txt listo (páginas 15-46 de la revista)"
elif [ ! -s "$BASE/pele/pele_pag.txt" ]; then
  echo "  falta: Pele, A. (2015). Kant y la dignidad humana. Adjuntar el PDF y volver a correr."
fi
[ -s "$BASE/pdf/iso.txt" ]   || echo "  falta: ISO 18091:2019 (norma de pago, no se guarda aquí). Adjuntar la vista previa."
[ -s "$BASE/pdf/cabos.txt" ] || echo "  falta: Observatorio Ciudadano Integral de Los Cabos (2020). Adjuntar el PDF."

echo
echo "Listo. Para cotejar: exportar el documento en markdown y correr"
echo "  python3 -I $BASE/scripts/chk.py <archivo exportado>"
