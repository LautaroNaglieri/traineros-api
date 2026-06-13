#!/usr/bin/env bash
# Renderiza los .drawio a PNG con el draw.io desktop.
set -e
DRAWIO="/c/Program Files/draw.io/draw.io.exe"
DIR="$(cd "$(dirname "$0")/../diagramas" && pwd)"
for name in fase1_monolito_3capas fase2a_microservicios_tradicionales \
            fase2b_microservicios_modernos evolucion_3_arquitecturas; do
  "$DRAWIO" --export --format png --scale 2 --border 24 \
    --output "$DIR/$name.png" "$DIR/drawio/$name.drawio" --no-sandbox >/dev/null 2>&1
  echo "render $name"
done
