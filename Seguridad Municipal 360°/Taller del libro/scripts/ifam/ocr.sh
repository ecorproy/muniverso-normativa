#!/bin/bash
cd /tmp/ifam/ocr24
for p in $(seq 1 295); do
  [ -f p$p.txt ] && continue
  pdftoppm -f $p -l $p -r 150 -gray -png /tmp/ifam/idx2024.pdf img$p >/dev/null 2>&1
  f=$(ls img$p*.png 2>/dev/null | head -1)
  tesseract "$f" p$p -l spa >/dev/null 2>&1
  rm -f img$p*.png
done
echo DONE > done.flag
