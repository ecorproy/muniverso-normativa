#!/bin/bash
# Uso: armar.sh N  -> /home/claude/docx/finalN/Seguridad Municipal 360°.docx
set -e; N=$1; cd /home/claude/docx
python3 -I /home/claude/indices/indices.py >/dev/null
cp libro.md libro_build.md
printf '\n\n' >> libro_build.md; cat /home/claude/indices/indices.md >> libro_build.md
python3 -I /home/claude/docx_scripts/figuras.py libro_build.md
mkdir -p final$N
pandoc libro_build.md -f markdown-smart -o b$N.docx --reference-doc=ref.docx --toc --toc-depth=2
python3 -I /home/claude/docx_scripts/post.py b$N.docx p$N.docx
python3 -I /home/claude/docx_scripts/portada.py p$N.docx "final$N/Seguridad Municipal 360°.docx" /home/claude/docx/logo360.png
