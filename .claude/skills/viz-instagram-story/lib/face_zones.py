#!/usr/bin/env python3
"""
face_zones.py — masoara unde e fata/persoana intr-o imagine adusa la formatul tinta,
si raporteaza benzile LIBERE (fara fata) disponibile pentru text.

Scop: sa NU mai plasam text "pe incredere". Inainte de overlay, stim cifrele:
unde e fata, cat spatiu liber e sus/jos, si daca textul incape fara sa atinga fata.

Folosit de overlay_text.py (--avoid-face) si ca tool de verificare standalone.
"""
import sys
import json

import numpy as np
from PIL import Image, ImageOps

try:
    import cv2
except ImportError:
    cv2 = None

FORMATS = {
    "story":    (1080, 1920, 250, 1610, 64),
    "carousel": (1080, 1350, 90, 1230, 80),
    "square":   (1080, 1080, 80, 1000, 80),
}


def fit_canvas(img, W, H):
    img = ImageOps.exif_transpose(img).convert("RGB")
    if img.size == (W, H):
        return img
    return ImageOps.fit(img, (W, H), method=Image.LANCZOS, centering=(0.5, 0.45))


def detect_face(pil_img):
    """Returneaza (x, y, w, h) al celei mai mari fete, sau None."""
    if cv2 is None:
        return None
    arr = np.array(pil_img)[:, :, ::-1].copy()  # RGB -> BGR
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6,
                                     minSize=(70, 70))
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    return (int(x), int(y), int(w), int(h))


def analyze(path, fmt="carousel", hair_pad_ratio=0.6):
    W, H, safe_top, safe_bottom, side = FORMATS[fmt]
    img = fit_canvas(Image.open(path), W, H)
    face = detect_face(img)

    res = {"path": path, "format": fmt, "canvas": [W, H],
           "safe_top": safe_top, "safe_bottom": safe_bottom}
    if face is None:
        res["face"] = None
        res["note"] = "fara fata detectata — text poate merge oriunde in safe area"
        res["top_band"] = [safe_top, safe_bottom]
        res["bottom_band"] = [safe_top, safe_bottom]
        return res

    fx, fy, fw, fh = face
    # extinde in sus pentru par/frunte, in jos pentru barbie
    obstacle_top = max(0, fy - int(fh * hair_pad_ratio))
    obstacle_bottom = min(H, fy + fh + int(fh * 0.3))
    res["face"] = [fx, fy, fw, fh]
    res["face_center_x"] = fx + fw // 2
    res["obstacle_v"] = [obstacle_top, obstacle_bottom]

    # banda libera sus = de la safe_top pana la inceputul obstacolului
    top_band = [safe_top, max(safe_top, obstacle_top - 30)]
    # banda libera jos = de la finalul obstacolului pana la safe_bottom
    bottom_band = [min(safe_bottom, obstacle_bottom + 30), safe_bottom]
    res["top_band"] = top_band
    res["top_band_h"] = top_band[1] - top_band[0]
    res["bottom_band"] = bottom_band
    res["bottom_band_h"] = bottom_band[1] - bottom_band[0]

    # pe ce parte e fata (pentru aliniere text spre partea libera)
    cx = fx + fw // 2
    res["free_side"] = "left" if cx > W / 2 else "right"
    return res


if __name__ == "__main__":
    fmt = "carousel"
    args = [a for a in sys.argv[1:]]
    if "--format" in args:
        i = args.index("--format")
        fmt = args[i + 1]
        args = args[:i] + args[i + 2:]
    out = [analyze(p, fmt) for p in args]
    print(json.dumps(out, indent=2, ensure_ascii=False))
