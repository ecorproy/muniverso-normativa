#!/usr/bin/env bash
# paginas.sh CAPITULO.md [REFERENCIAS.md]: páginas con pandoc (a .docx) y LibreOffice (a PDF), formato por defecto
set -e
d=$(mktemp -d); b=$(basename "$1" .md)
if [ -n "${2:-}" ]; then cat "$1" <(echo) "$2" > "$d/$b.md"; else cp "$1" "$d/$b.md"; fi
pandoc "$d/$b.md" -o "$d/$b.docx"
soffice --headless --convert-to pdf --outdir "$d" "$d/$b.docx" >/dev/null 2>&1
echo "páginas: $(pdfinfo "$d/$b.pdf" | awk '/^Pages/{print $2}') | palabras: $(wc -w < "$d/$b.md")"
