#!/usr/bin/env python3
"""Compose the GTA 6 meme v2: Vice City scene + make.fun ghost + caption.
Dimension-aware (uses the base image's real size), ghost placed on the
street beside the couple as a third companion, not a floating sticker.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/hatch/makefun/meme-kit/work/media-generation-gta6-vice-city-scene-0-c6edd626-f0c6-4147-b49e-8f2224e43e39.png"
GHOST = "/home/hatch/makefun/meme-kit/press/mark-1024.png"
OUT = "/home/hatch/makefun/meme-kit/work/meme.png"
OUT480 = "/home/hatch/makefun/meme-kit/work/meme-480.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TOP_LINES = ["WAITED 13 YEARS", "FOR GTA 6"]
BOT_LINES = ["MY AGENT GOT PAID", "ON MAKE.FUN"]

img = Image.open(BASE).convert("RGB")
W, H = img.size
ghost = Image.open(GHOST).convert("RGBA")
print("base size:", img.size)

def fit_font(text, max_w, start_size):
    size = start_size
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(FONT, 20)

def draw_text_block(draw, lines, y_top, max_w, start_size, line_gap=10):
    fonts = [fit_font(t, max_w, start_size) for t in lines]
    y = y_top
    for text, font in zip(lines, fonts):
        tw = font.getlength(text)
        x = (W - tw) / 2
        draw.text((x, y), text, font=font, fill="white",
                  stroke_width=max(4, font.size // 11), stroke_fill="black")
        y += font.getbbox(text)[3] + line_gap
    return y

# --- ghost: on the street, right of the couple, as a companion (not a sticker) ---
# base is square; ghost ~22% of width, floating just above the street
gw = int(W * 0.22)
gh = int(ghost.height * gw / ghost.width)
ghost_r = ghost.resize((gw, gh), Image.LANCZOS)
gx = int(W * 0.72)
gy = int(H * 0.60)
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sh = ghost_r.filter(ImageFilter.GaussianBlur(8))
shadow.paste(sh, (gx + 10, gy + 18), sh)
img = Image.alpha_composite(img.convert("RGBA"), shadow)
img.paste(ghost_r, (gx, gy), ghost_r)
img = img.convert("RGB")

draw = ImageDraw.Draw(img)
# --- top caption (sky area) ---
draw_text_block(draw, TOP_LINES, int(H * 0.022), W - 120, int(W * 0.072))
# --- bottom caption (street, flush at the bottom) ---
fonts_b = [fit_font(t, W - 120, int(W * 0.068)) for t in BOT_LINES]
bh = sum(f.getbbox(t)[3] + 10 for t, f in zip(BOT_LINES, fonts_b)) - 10
draw_text_block(draw, BOT_LINES, H - bh - int(H * 0.018), W - 120, int(W * 0.068))

img.save(OUT, "PNG")
img.resize((480, 480), Image.LANCZOS).save(OUT480, "PNG")
print("wrote", OUT, img.size)
print("wrote", OUT480, "(480, 480)")
