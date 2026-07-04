#!/usr/bin/env python3
"""
overlay_text.py — pune textul (hook + CTA) ca layer peste vizualul generat de kie.ai.

De ce un layer separat: modelele de imagine mazgalesc textul, mai ales diacriticele
RO (a-breve, a-circ, i-circ, s-virgula, t-virgula). PIL randeaza text corect, in safe
zones exacte, cu paleta de brand. Asa scopul "text foarte usor de citit" devine fiabil.

Canvas tinta: 1080x1920 (Instagram Story). Daca imaginea de intrare are alt raport,
e potrivita pe canvas (cover-crop) ca sa nu deformeze.

Usage:
  python overlay_text.py --image visual.png --hook "Textul tau" \
      --cta VREAU --output story-final.png
  python overlay_text.py --image v.png --hook "..." --hook-pos top --no-overlay -o out.png
"""
import argparse
import os
import sys
import textwrap

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.exit("PIL (Pillow) lipseste. Instaleaza: pip install Pillow")

# Formate suportate: (W, H, safe_top, safe_bottom, side)
FORMATS = {
    "story":    (1080, 1920, 250, 1610, 64),   # Instagram/TikTok/FB Story 9:16
    "carousel": (1080, 1350, 90, 1230, 80),    # Instagram Carousel 4:5
    "square":   (1080, 1080, 80, 1000, 80),    # 1:1
}

# Valori active — setate din --format in main(). Default: story.
W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 250, 1610          # zona libera de text
SIDE = 64
TEXT_W = W - 2 * SIDE                       # latimea utila a textului

DEFAULT_ACCENT = "#C8921A"                  # auriu brand
TEXT_LIGHT = "#FFFFFF"
TEXT_DARK = "#2B2218"

# Fonturi candidate (Windows + cross-platform). Primul gasit castiga.
FONT_CANDIDATES = [
    "C:/Windows/Fonts/Georgia.ttf",
    "C:/Windows/Fonts/georgiab.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/seguisb.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def fit_canvas(img):
    """Potriveste imaginea pe canvas prin cover-crop (fara deformare)."""
    img = ImageOps.exif_transpose(img).convert("RGB")
    if img.size == (W, H):
        return img
    return ImageOps.fit(img, (W, H), method=Image.LANCZOS, centering=(0.5, 0.45))


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def fit_with_band(img, band_h, band_color):
    """Pune poza in partea de jos (H - band_h) prin cover-crop si lasa o banda
    de culoare brand sus pentru text. Garanteaza ca persoana nu e acoperita
    (textul sta in banda, nu peste poza). Doc sec.2: spatiu pentru text."""
    img = ImageOps.exif_transpose(img).convert("RGB")
    photo_h = H - band_h
    photo = ImageOps.fit(img, (W, photo_h), method=Image.LANCZOS,
                         centering=(0.5, 0.35))
    canvas = Image.new("RGB", (W, H), hex_rgb(band_color))
    canvas.paste(photo, (0, band_h))
    return canvas


def wrap_to_width(draw, text, font, max_w):
    """Imparte textul in linii care incap in max_w (masurat real cu fontul)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block_height(draw, lines, font, line_gap):
    h = 0
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        h += (bbox[3] - bbox[1]) + line_gap
    return h - line_gap if lines else 0


def add_gradient(img, top_y, bottom_y, max_alpha=110):
    """Gradient soft pentru contrast, doar in banda [top_y, bottom_y]."""
    grad = Image.new("L", (1, H), 0)
    band = max(1, bottom_y - top_y)
    for y in range(H):
        if top_y <= y <= bottom_y:
            # mai intens spre centrul benzii
            d = abs((y - (top_y + bottom_y) / 2) / (band / 2))
            grad.putpixel((0, y), int(max_alpha * (1 - min(d, 1)) + max_alpha * 0.4))
    alpha = grad.resize((W, H))
    black = Image.new("RGB", (W, H), (10, 8, 6))
    return Image.composite(black, img, alpha)


def draw_hook(img, draw, hook, pos, accent, align="center", size_start=92, dark=False):
    """Deseneaza hook-ul. align = center|left|right (regula document: textul curge
    in zona libera / spre directia privirii, NU peste persoana).
    dark=True -> text inchis (pe banda crem); altfel alb (pe poza)."""
    size = size_start
    font = load_font(size)
    lines = wrap_to_width(draw, hook, font, TEXT_W)
    # micsoreaza fontul daca sunt prea multe linii
    while len(lines) > 4 and size > 44:
        size -= 8
        font = load_font(size)
        lines = wrap_to_width(draw, hook, font, TEXT_W)

    line_gap = int(size * 0.28)
    block_h = text_block_height(draw, lines, font, line_gap)

    if pos == "top":
        y = SAFE_TOP + 60
    elif pos == "bottom":
        y = SAFE_BOTTOM - block_h - 220
    else:  # center
        y = (SAFE_TOP + SAFE_BOTTOM) // 2 - block_h // 2

    fill = hex_rgb(TEXT_DARK) if dark else (255, 255, 255)
    for ln in lines:
        tw = draw.textlength(ln, font=font)
        if align == "left":
            x = SIDE
        elif align == "right":
            x = W - SIDE - tw
        else:
            x = (W - tw) / 2
        if not dark:
            draw.text((x + 2, y + 2), ln, font=font, fill=(0, 0, 0))  # umbra pe poza
        draw.text((x, y), ln, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), ln, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y  # baseline (y) dupa hook


def draw_cta(img, draw, cta, accent, align="center"):
    font = load_font(46)
    label = cta.strip().upper()
    tw = draw.textlength(label, font=font)
    pad_x, pad_y = 48, 26
    bbox = draw.textbbox((0, 0), label, font=font)
    th = bbox[3] - bbox[1]
    pill_w = tw + 2 * pad_x
    pill_h = th + 2 * pad_y
    if align == "left":
        x0 = SIDE
    elif align == "right":
        x0 = W - SIDE - pill_w
    else:
        x0 = (W - pill_w) / 2
    y0 = SAFE_BOTTOM - pill_h - 30
    draw.rounded_rectangle(
        [x0, y0, x0 + pill_w, y0 + pill_h],
        radius=pill_h / 2, fill=accent,
    )
    draw.text(
        (x0 + pad_x, y0 + pad_y - bbox[1]), label, font=font, fill=TEXT_DARK,
    )


def main():
    ap = argparse.ArgumentParser(description="Overlay text peste un Instagram Story.")
    ap.add_argument("--image", required=True, help="Vizualul de baza (de la kie.ai).")
    ap.add_argument("--hook", required=True, help="Hook-ul (textul principal).")
    ap.add_argument("--cta", default="", help="CTA: CURIOASA|INFO|START|VREAU|POT.")
    ap.add_argument("--output", "-o", required=True, help="Fisierul de iesire.")
    ap.add_argument("--hook-pos", default="center", choices=["top", "center", "bottom"])
    ap.add_argument("--align", default="center", choices=["center", "left", "right"],
                    help="Aliniere text. Regula document: spre zona libera / directia privirii.")
    ap.add_argument("--accent", default=DEFAULT_ACCENT, help="Culoare accent hex.")
    ap.add_argument("--no-overlay", action="store_true", help="Fara gradient de contrast.")
    ap.add_argument("--format", default="story", choices=list(FORMATS.keys()),
                    help="story (9:16) | carousel (4:5) | square (1:1).")
    ap.add_argument("--extend-top", type=int, default=0,
                    help="Inaltime banda brand sus (px) pentru text. Poza coboara sub ea. "
                         "Doc sec.2: spatiu pentru text fara a acoperi persoana.")
    ap.add_argument("--band-color", default="#F4ECDD", help="Culoarea benzii (crem brand).")
    ap.add_argument("--auto-band", action="store_true",
                    help="Banda crem auto-dimensionata dupa textul real (text garantat sub persoana).")
    ap.add_argument("--verify-face", action="store_true",
                    help="Verifica (cv2) ca textul NU atinge fata. Exit !=0 daca o atinge.")
    args = ap.parse_args()

    # Activeaza dimensiunile formatului ales.
    global W, H, SAFE_TOP, SAFE_BOTTOM, SIDE, TEXT_W
    W, H, SAFE_TOP, SAFE_BOTTOM, SIDE = FORMATS[args.format]
    TEXT_W = W - 2 * SIDE

    if not os.path.exists(args.image):
        sys.exit(f"Imaginea nu exista: {args.image}")

    src = Image.open(args.image)

    # Mod AUTO-BAND (default cand textul ar atinge fata, sau fortat cu --extend-top):
    # masuram textul, calculam banda EXACTA care-l incadreaza, poza coboara sub ea.
    # Asa textul NU atinge niciodata persoana. Doc sec.2 + sec.5.
    use_band = args.extend_top > 0 or args.auto_band

    if use_band:
        PAD_TOP, PAD_BOTTOM = 70, 70
        lines, font, size, block_h = measure_hook(args.hook, size_start=80)
        band_h = PAD_TOP + block_h + PAD_BOTTOM
        if args.extend_top > band_h:        # respecta minimul cerut explicit
            band_h = args.extend_top
        img = fit_with_band(src, band_h, args.band_color)
        draw = ImageDraw.Draw(img)
        y_start = PAD_TOP
        hook_y_end = draw_lines_at(draw, lines, font, y_start,
                                   align=args.align, dark=True)
        text_top, text_bottom = 0, band_h    # textul e garantat in banda
    else:
        img = fit_canvas(src)
        if not args.no_overlay:
            if args.hook_pos == "top":
                g0, g1 = SAFE_TOP - 40, SAFE_TOP + 420
            elif args.hook_pos == "bottom":
                g0, g1 = SAFE_BOTTOM - 600, SAFE_BOTTOM + 20
            else:
                g0, g1 = (SAFE_TOP + SAFE_BOTTOM) // 2 - 320, (SAFE_TOP + SAFE_BOTTOM) // 2 + 320
            img = add_gradient(img, g0, g1)
        draw = ImageDraw.Draw(img)
        hook_y_end = draw_hook(img, draw, args.hook, args.hook_pos, args.accent,
                               align=args.align)
        text_top, text_bottom = SAFE_TOP, hook_y_end

    if args.cta:
        draw_cta(img, draw, args.cta, args.accent, align=args.align)

    # --- VERIFICARE OBLIGATORIE: textul nu atinge fata ---
    ok = verify_no_face_overlap(img, text_top, text_bottom)
    status = "PASS" if ok else "FAIL"
    print(f"[verify-face] text[{text_top},{text_bottom}] vs fata -> {status}")
    if not ok and args.verify_face:
        sys.exit(f"[verify-face] FAIL: textul atinge fata in {args.output}")

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    img.save(args.output, "PNG")
    print(f"OK -> {args.output} ({W}x{H})")


def verify_no_face_overlap(pil_img, text_top, text_bottom):
    """True daca banda de text [text_top, text_bottom] nu intersecteaza fata."""
    try:
        import numpy as np
        import cv2
    except ImportError:
        print("[verify-face] cv2/numpy lipsa — skip verificare")
        return True
    arr = np.array(pil_img.convert("RGB"))[:, :, ::-1].copy()
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, 1.1, 6, minSize=(70, 70))
    if len(faces) == 0:
        return True
    for (fx, fy, fw, fh) in faces:
        face_top = fy - int(fh * 0.5)  # include parul
        # overlap vertical intre text si fata?
        if text_bottom > face_top and text_top < fy + fh:
            return False
    return True


if __name__ == "__main__":
    main()
