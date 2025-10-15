# raster_core.py
import numpy as np
from PIL import Image

def make_canvas(w, h, bg=(20, 22, 26)):
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = bg
    return img

def save_png(img, path):
    Image.fromarray(img).save(path)

def _set_px(img, x, y, color):
    h, w = img.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        img[y, x] = color

# ---------- LÍNEA: Bresenham ----------
def line_bresenham(img, x0, y0, x1, y1, color=(255,255,255)):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)
    err = dx // 2
    ystep = 1 if y0 < y1 else -1
    y = y0

    for x in range(x0, x1 + 1):
        if steep: _set_px(img, y, x, color)
        else:     _set_px(img, x, y, color)
        err -= dy
        if err < 0:
            y += ystep
            err += dx

# ---------- CÍRCULO: Punto medio ----------
def circle_midpoint(img, cx, cy, r, color=(255,255,0)):
    x, y = r, 0
    d = 1 - r
    def plot_symm(x, y):
        _set_px(img, cx + x, cy + y, color)
        _set_px(img, cx - x, cy + y, color)
        _set_px(img, cx + x, cy - y, color)
        _set_px(img, cx - x, cy - y, color)
        _set_px(img, cx + y, cy + x, color)
        _set_px(img, cx - y, cy + x, color)
        _set_px(img, cx + y, cy - x, color)
        _set_px(img, cx - y, cy - x, color)

    while x >= y:
        plot_symm(x, y)
        y += 1
        if d <= 0:
            d += 2*y + 1
        else:
            x -= 1
            d += 2*(y - x) + 1

# ---------- TRIÁNGULO: Scanline ----------
def _edge_interp(x0, y0, x1, y1):
    if y1 == y0:
        return []
    inv_slope = (x1 - x0) / (y1 - y0)
    x = x0
    pts = []
    y_start, y_end = (y0, y1) if y0 < y1 else (y1, y0)
    x_start = x0 if y0 < y1 else x1
    x = x_start
    for y in range(y_start, y_end + 1):
        pts.append((y, x))
        x += inv_slope
    return pts

def fill_triangle_scanline(img, p0, p1, p2, color=(120,200,255)):
    # ordenar por y (p0.y <= p1.y <= p2.y)
    pts = sorted([p0, p1, p2], key=lambda p: p[1])
    (x0, y0), (x1, y1), (x2, y2) = pts

    if y1 == y2:  # triángulo "plano arriba"
        _fill_flat_top(img, (x0,y0), (x1,y1), (x2,y2), color)
    elif y0 == y1:  # triángulo "plano abajo"
        _fill_flat_bottom(img, (x0,y0), (x1,y1), (x2,y2), color)
    else:
        # dividir el triángulo general en dos planos
        # x = x0 + (y1 - y0)*(x2 - x0)/(y2 - y0)
        x_s = x0 + ( (y1 - y0) * (x2 - x0) ) / (y2 - y0)
        _fill_flat_bottom(img, (x0,y0), (x1,y1), (x_s,y1), color)
        _fill_flat_top(img, (x1,y1), (x_s,y1), (x2,y2), color)

def _fill_flat_bottom(img, v0, v1, v2, color):
    (x0,y0),(x1,y1),(x2,y2) = v0,v1,v2
    invslope1 = (x1 - x0) / (y1 - y0) if (y1 - y0)!=0 else 0
    invslope2 = (x2 - x0) / (y2 - y0) if (y2 - y0)!=0 else 0
    curx1, curx2 = x0, x0
    for y in range(int(y0), int(y2)+1):
        x_start, x_end = sorted([int(round(curx1)), int(round(curx2))])
        for x in range(x_start, x_end+1):
            _set_px(img, x, y, color)
        curx1 += invslope1
        curx2 += invslope2

def _fill_flat_top(img, v0, v1, v2, color):
    (x0,y0),(x1,y1),(x2,y2) = v0,v1,v2
    invslope1 = (x2 - x0) / (y2 - y0) if (y2 - y0)!=0 else 0
    invslope2 = (x2 - x1) / (y2 - y1) if (y2 - y1)!=0 else 0
    curx1, curx2 = x2, x2
    for y in range(int(y2), int(y0)-1, -1):
        x_start, x_end = sorted([int(round(curx1)), int(round(curx2))])
        for x in range(x_start, x_end+1):
            _set_px(img, x, y, color)
        curx1 -= invslope1
        curx2 -= invslope2