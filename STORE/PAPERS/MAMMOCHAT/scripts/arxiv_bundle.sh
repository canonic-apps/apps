#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TEX_DIR="$ROOT/tex"
OUT_DIR="$ROOT/arxiv"
STAGE_DIR="$OUT_DIR/stage"
ZIP_PATH="$OUT_DIR/mammochat-arxiv.zip"

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"

cp "$TEX_DIR"/main.tex "$STAGE_DIR/"
cp "$TEX_DIR"/preamble.tex "$STAGE_DIR/"
cp "$TEX_DIR"/*.tex "$STAGE_DIR/"
cp "$TEX_DIR"/refs.bib "$STAGE_DIR/"

if [ -f "$TEX_DIR/mCODE_STU2.png" ]; then
  cp "$TEX_DIR/mCODE_STU2.png" "$STAGE_DIR/"
fi

if [ -f "$TEX_DIR/main.bbl" ]; then
  cp "$TEX_DIR/main.bbl" "$STAGE_DIR/"
fi

python3 - <<PY
from pathlib import Path
path = Path("$STAGE_DIR") / "preamble.tex"
text = path.read_text()
if "backend=biber" in text:
    path.write_text(text.replace("backend=biber", "backend=bibtex"))
PY

python3 - <<PY
from pathlib import Path
import zipfile

stage = Path("$STAGE_DIR")
zip_path = Path("$ZIP_PATH")
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(stage.rglob("*")):
        if path.is_file():
            zf.write(path, path.relative_to(stage))
print(f"Created {zip_path}")
PY
