# -*- coding: utf-8 -*-
"""Generate tab sprite (TGA, 2 frames) and workshop thumbnail (PNG)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from config import MOD
FONT_CN = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_EN = r"C:\Windows\Fonts\msyhbd.ttc"


def load_font(path, size):
    for p in (path, r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def tab_frame(active):
    W, H = 182, 61
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # slanted tab shape
    skew = 10
    poly = [(skew, 2), (W - 2, 2), (W - 2, H - 1), (2, H - 1), (skew, 2)]
    top = (58, 74, 96, 255) if not active else (86, 108, 132, 255)
    bot = (32, 42, 56, 255) if not active else (48, 62, 82, 255)
    # gradient fill
    for yy in range(H):
        t = yy / (H - 1)
        col = tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)) + (255,)
        d.line([(0, yy), (W, yy)], fill=col)
    # mask the gradient into the tab shape
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(skew, 1), (W - 1, 1), (W - 1, H - 1), (1, H - 1)], fill=255)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.paste(img, (0, 0), mask)
    d = ImageDraw.Draw(base)
    # borders
    edge = (150, 172, 196, 255) if active else (96, 112, 132, 255)
    d.line([(skew, 1), (W - 2, 1)], fill=edge, width=2)
    d.line([(W - 2, 1), (W - 2, H - 2)], fill=edge, width=2)
    d.line([(1, H - 2), (W - 2, H - 2)], fill=(20, 26, 36, 255), width=2)
    # star + text
    f_cn = load_font(FONT_CN, 22)
    f_en = load_font(FONT_EN, 9)
    text = "中国空军"
    tb = d.textbbox((0, 0), text, font=f_cn)
    tw = tb[2] - tb[0]
    d.text(((W - tw) / 2 + 4, 8), text, font=f_cn,
           fill=(255, 236, 200, 255) if active else (226, 232, 240, 255))
    sub = "CHINESE  AIR  FORCE"
    sb = d.textbbox((0, 0), sub, font=f_en)
    d.text(((W - (sb[2] - sb[0])) / 2 + 2, 38), sub, font=f_en,
           fill=(190, 202, 218, 255) if active else (150, 162, 180, 255))
    # small roundel top-left
    d.ellipse([12, 12, 26, 26], fill=(190, 40, 40, 255), outline=(30, 30, 30, 255))
    d.ellipse([16, 16, 22, 22], fill=(250, 250, 250, 255))
    return base


def make_tab():
    a = tab_frame(False)
    b = tab_frame(True)
    out = Image.new("RGBA", (364, 61), (0, 0, 0, 0))
    out.paste(a, (0, 0))
    out.paste(b, (182, 0))
    path = os.path.join(MOD, "gfx", "interface", "techtree", "techtree_china_air_tab.tga")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path, format="TGA")
    return path


def make_thumbnail():
    W = H = 512
    img = Image.new("RGB", (W, H), (14, 22, 34))
    d = ImageDraw.Draw(img)
    # subtle gradient + stripes
    for yy in range(H):
        t = yy / H
        col = (int(14 + 26 * t), int(22 + 34 * t), int(34 + 44 * t))
        d.line([(0, yy), (W, yy)], fill=col)
    for i in range(0, W, 48):
        d.line([(i, 0), (i - 200, H)], fill=(22, 32, 46))
    # frame
    d.rectangle([8, 8, W - 9, H - 9], outline=(120, 140, 164), width=2)
    f_big = load_font(FONT_CN, 52)
    f_mid = load_font(FONT_CN, 26)
    f_small = load_font(FONT_CN, 17)
    f_en = load_font(FONT_EN, 15)
    title = "中系飞机科技树"
    b = d.textbbox((0, 0), title, font=f_big)
    d.text(((W - (b[2] - b[0])) / 2, 92), title, font=f_big, fill=(246, 226, 180))
    sub = "BLACK ICE  ·  CHINESE AIRCRAFT TREE"
    b = d.textbbox((0, 0), sub, font=f_en)
    d.text(((W - (b[2] - b[0])) / 2, 168), sub, font=f_en, fill=(150, 172, 196))
    d.line([(80, 204), (W - 80, 204)], fill=(120, 100, 70), width=2)

    lines = ["1936  霍克 III", "1938  伊-16 · 九七式战", "1941  P-40 · B-25",
             "1944  P-51D · 图-2", "1947  米格-9"]
    for i, line in enumerate(lines):
        b = d.textbbox((0, 0), line, font=f_mid)
        d.text(((W - (b[2] - b[0])) / 2, 224 + i * 38), line, font=f_mid,
               fill=(214, 222, 234) if i % 2 == 0 else (186, 198, 214))
    foot = "科技标签页 · 76 项科技 · 中英双语"
    b = d.textbbox((0, 0), foot, font=f_small)
    d.text(((W - (b[2] - b[0])) / 2, 430), foot, font=f_small, fill=(140, 156, 176))
    # roundel
    d.ellipse([36, 36, 96, 96], fill=(178, 38, 38), outline=(240, 240, 240), width=3)
    d.ellipse([56, 56, 76, 76], fill=(240, 240, 240))
    path = os.path.join(MOD, "thumbnail.png")
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    print(make_tab())
    print(make_thumbnail())
