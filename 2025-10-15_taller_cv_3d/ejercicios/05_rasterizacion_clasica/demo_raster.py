# demo_raster.py
from raster_core import *

W, H = 800, 500
img = make_canvas(W, H)

# Líneas
line_bresenham(img, 50, 60, 350, 300, (255, 160, 90))
line_bresenham(img, 350, 80, 70, 400, (90, 200, 255))
line_bresenham(img, 400, 250, 760, 250, (180, 255, 120))

# Círculos
circle_midpoint(img, 600, 130, 80, (255, 230, 90))
circle_midpoint(img, 600, 130, 40, (255, 90, 180))

# Triángulos (scanline)
fill_triangle_scanline(img, (120,120), (220,320), (40,300), (120, 200, 255))
fill_triangle_scanline(img, (480,320), (700,450), (630,230), (255,150,150))

save_png(img, 'out/raster_demo.png')
print('Guardado: out/raster_demo.png')
