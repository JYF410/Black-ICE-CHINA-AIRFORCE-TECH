# -*- coding: utf-8 -*-
"""Render a layout preview of the Chinese air tech tree (PNG, for docs)."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data_chi as D

from config import MOD
FONT = r"C:\Windows\Fonts\msyh.ttc"
FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"

COL_W, ROW_H = 172, 46
LEFT, TOP = 190, 96
from config import COLUMNS
LABELS = {
    "engine_usa": "美制发动机", "engine_usa_multi": "美制多发/喷气",
    "engine_sov": "苏制单发", "engine_sov_multi": "苏制多发/喷气",
    "engine_jap": "日制发动机", "engine_other": "德英发动机",
    "gun": "航空枪炮", "ordnance": "航空炸弹", "ordnance_2": "火箭/特种炸弹",
    "ftr": "战斗机", "hvy_ftr": "重型战斗机", "cv_ftr": "舰载战斗机",
    "cas": "近距支援机", "l_bomber": "轻型轰炸机", "tac_bomber": "中型轰炸机",
    "strat_bomber": "重型轰炸机", "fly_bts": "水上飞机", "recon": "侦察机", "trpt": "运输机",
}
COLS = {COLUMNS[k]: v for k, v in LABELS.items()}
COLOR = {
    0: (52, 84, 120), 2: (52, 84, 120), 4: (110, 62, 52), 6: (110, 62, 52),
    8: (118, 108, 54), 12: (70, 96, 70), 16: (92, 74, 110), 20: (108, 86, 60),
    26: (58, 108, 74), 30: (58, 96, 116), 34: (120, 78, 48), 38: (96, 62, 96),
    42: (72, 76, 116),
}


def font(size, bold=False):
    for p in ((FONT_B if bold else FONT), r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    items = []
    for a in D.AIRFRAMES:
        items.append(("air", a["key"], a["zh"], a["year"], a["x"], a.get("dy") or 0, a["prev"]))
    for kind, table in (("engine", D.ENGINES), ("gun", D.GUNS), ("ord", D.ORDNANCE)):
        for t in table:
            items.append((kind, t["key"], t["zh"], t["year"], t["x"], 0, t["prev"]))

    xs = sorted({i[4] for i in items})
    col_index = {x: i for i, x in enumerate(xs)}
    years = sorted({i[3] for i in items})
    W = LEFT + COL_W * len(xs) + 60
    H = TOP + ROW_H * ((years[-1] - years[0]) * 2 + 2) + 80
    img = Image.new("RGB", (W, H), (18, 24, 34))
    d = ImageDraw.Draw(img)
    f_head = font(15, True)
    f_cell = font(12)
    f_year = font(13, True)
    f_title = font(24, True)
    f_small = font(11)

    d.text((24, 20), "黑冰 · 中系飞机科技树 Chinese Aircraft Tech Tree", font=f_title, fill=(240, 228, 200))
    d.text((24, 54), "1920×auto 预览 · 列 = 科技分支，行 = 年份（每年 2 行）", font=f_small, fill=(150, 164, 184))

    # column headers
    for x, idx in col_index.items():
        cx = LEFT + idx * COL_W + COL_W / 2
        label = COLS.get(x, str(x))
        tb = d.textbbox((0, 0), label, font=f_head)
        d.text((cx - (tb[2] - tb[0]) / 2, TOP - 34), label, font=f_head, fill=(214, 224, 238))

    # year grid
    for year in years:
        yy = TOP + (year - years[0]) * 2 * ROW_H
        d.line([(24, yy + ROW_H - 1), (W - 40, yy + ROW_H - 1)], fill=(36, 46, 60))
        d.text((24, yy + ROW_H - 18), str(year), font=f_year, fill=(150, 164, 184))

    pos = {}
    for kind, key, zh, year, x, dy, prev in items:
        idx = col_index[x]
        cx = LEFT + idx * COL_W + 4
        cy = TOP + (year - years[0]) * 2 * ROW_H + dy * ROW_H + 2
        pos[(kind, key)] = (cx, cy, COL_W - 10, ROW_H - 6)

    # arrows first so the boxes cover the lines
    for kind, key, zh, year, x, dy, prev in items:
        if not prev:
            continue
        a = pos.get((kind, prev))
        b = pos.get((kind, key))
        if not a or not b:
            continue
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        if ay == by:
            d.line([(ax + aw, ay + ah / 2), (bx, by + bh / 2)], fill=(210, 200, 160), width=2)
        else:
            mid = by - 6
            d.line([(ax + aw / 2, ay + ah), (ax + aw / 2, mid), (bx + bw / 2, mid)], fill=(210, 200, 160), width=2)
            d.line([(bx + bw / 2, mid), (bx + bw / 2, by)], fill=(210, 200, 160), width=2)
            d.polygon([(bx + bw / 2 - 4, by - 2), (bx + bw / 2 + 4, by - 2), (bx + bw / 2, by + 4)],
                      fill=(210, 200, 160))

    # boxes on top of the arrows
    for kind, key, zh, year, x, dy, prev in items:
        cx, cy, w, h = pos[(kind, key)]
        base = COLOR.get(x, (70, 70, 70))
        d.rounded_rectangle([cx, cy, cx + w, cy + h], radius=5, fill=base, outline=(200, 210, 224))
        name = zh
        if len(name) > 12:
            name = name[:12] + "…"
        d.text((cx + 7, cy + 5), name, font=f_cell, fill=(245, 245, 245))
        d.text((cx + 7, cy + 21), f"{year}", font=f_small, fill=(210, 214, 222))

    out_dir = os.path.join(MOD, "docs")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "科技树预览.png")
    img.save(path)
    print(path, img.size)


if __name__ == "__main__":
    main()
