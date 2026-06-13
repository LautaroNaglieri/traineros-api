# Generador de la presentación y los diagramas

Pipeline (sin dependencias externas más allá de draw.io desktop y PowerPoint):

1. `build_drawio.py` → genera los archivos **.drawio** reales (mxGraph) en
   `../diagramas/drawio/`. Son editables en draw.io / diagrams.net.
2. Render a PNG con el **draw.io desktop** (ya instalado):
   ```
   "C:\Program Files\draw.io\draw.io.exe" --export --format png --scale 2 \
       --border 24 --output ../diagramas/<nombre>.png ../diagramas/drawio/<nombre>.drawio --no-sandbox
   ```
   (o correr `render_drawio.sh`).
3. `build_pptx.py` → arma `../TrainerOS_TFI_Fase1-2.pptx` embebiendo esos PNG en las
   diapositivas de diagrama; las demás diapositivas son formas nativas editables.
4. `export_png.py` (opcional) → exporta cada slide a PNG con PowerPoint para verificar.
   Nota: PowerPoint COM abre desde C:\Temp (no desde el Desktop sincronizado con OneDrive).
