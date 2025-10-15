# demo_geom.py
import cv2, imageio
from pathlib import Path
from geom_metrics import load_gray, binarize, analyze_contours, draw_annotations

IN = Path('data/figuras.png')   # <- tu imagen
OUT_DIR = Path('out'); OUT_DIR.mkdir(exist_ok=True, parents=True)

# 1) Cargar y preprocesar
gray = load_gray(IN)
bgr  = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# 2) Tres binarizaciones para comparar
bw_fixed = binarize(gray, method='fixed', thr=128)
bw_otsu  = binarize(gray, method='otsu')
bw_adapt = binarize(gray, method='adaptive', block=31, C=5)

# 3) Analizar contornos
inv, contours = analyze_contours(bw_otsu)

# 4) Dibujar resultados
annot = draw_annotations(bgr, contours)

# 5) Guardar imágenes
cv2.imwrite(str(OUT_DIR/'gray.png'), gray)
cv2.imwrite(str(OUT_DIR/'bw_fixed.png'), bw_fixed)
cv2.imwrite(str(OUT_DIR/'bw_otsu.png'), bw_otsu)
cv2.imwrite(str(OUT_DIR/'bw_adapt.png'), bw_adapt)
cv2.imwrite(str(OUT_DIR/'annot.png'), annot)

# 6) GIF: original -> binaria -> anotada
frames = [
    cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
    cv2.cvtColor(bw_otsu, cv2.COLOR_GRAY2BGR),
    annot
]
# BGR->RGB para imageio
frames = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames]
imageio.mimsave(OUT_DIR/'pipeline.gif', frames, duration=[0.8, 0.8, 1.4])

print('Guardado en out/: gray.png, bw_*.png, annot.png, pipeline.gif')
