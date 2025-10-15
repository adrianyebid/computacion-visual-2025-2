# geom_metrics.py
import cv2
import numpy as np
from pathlib import Path

def load_gray(path):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    return img

def binarize(img_gray, method='otsu', block=21, C=5, thr=128):
    if method == 'otsu':
        _, bw = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == 'fixed':
        _, bw = cv2.threshold(img_gray, thr, 255, cv2.THRESH_BINARY)
    elif method == 'adaptive':
        bw = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, block, C)
    else:
        raise ValueError('method inválido')
    return bw

def analyze_contours(bw):
    inv = bw
    white_ratio = (bw > 0).mean()
    if white_ratio > 0.5:
        inv = cv2.bitwise_not(bw)

    contours, _ = cv2.findContours(inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return inv, contours

def classify_shape(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    n = len(approx)
    label = f'{n}-lados'
    if n == 3: label = 'Triángulo'
    elif n == 4:
        x,y,w,h = cv2.boundingRect(approx)
        ar = w/float(h)
        label = 'Cuadrado' if 0.95 <= ar <= 1.05 else 'Rectángulo'
    elif n == 5: label = 'Pentágono'
    elif n > 5: label = 'Círculo/aprox.'
    return label, approx

def draw_annotations(src_bgr, contours):
    out = src_bgr.copy()
    for i, cnt in enumerate(contours, 1):
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        else:
            cx, cy = 0, 0

        label, approx = classify_shape(cnt)
        x,y,w,h = cv2.boundingRect(cnt)

        cv2.drawContours(out, [cnt], -1, (0,255,255), 2)
        cv2.circle(out, (cx,cy), 3, (0,0,255), -1)
        cv2.rectangle(out, (x,y), (x+w, y+h), (255,0,0), 1)
        cv2.putText(out, f'#{i} {label}', (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50,220,50), 1, cv2.LINE_AA)
        cv2.putText(out, f'A={area:.1f}  P={peri:.1f}', (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200,200,255), 1, cv2.LINE_AA)
    return out
