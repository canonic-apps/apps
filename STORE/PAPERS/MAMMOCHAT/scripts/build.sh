#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TEX_DIR="$ROOT/tex"
MAIN_TEX="$TEX_DIR/main.tex"
OUT_PDF="$ROOT/manuscript.pdf"

if [ ! -f "$MAIN_TEX" ]; then
  echo "Missing $MAIN_TEX" >&2
  exit 1
fi

if ! command -v latexmk >/dev/null 2>&1; then
  echo "latexmk not found; install TeX Live with latexmk." >&2
  exit 1
fi

if grep -q "backend=biber" "$TEX_DIR/preamble.tex" && ! command -v biber >/dev/null 2>&1; then
  echo "biber not found; install biber for biblatex backend." >&2
  exit 1
fi

pushd "$TEX_DIR" >/dev/null
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
popd >/dev/null

cp "$TEX_DIR/main.pdf" "$OUT_PDF"
echo "Built: $OUT_PDF"
