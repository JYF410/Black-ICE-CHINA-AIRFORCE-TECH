# -*- coding: utf-8 -*-
"""生成可编辑的科技树布局图（PPTX）。

用途：不用进游戏就能预览 / 拖拽调整科技条目的相对位置。
每个科技 = 一个圆角矩形（形状名 = 科技 key，方便以后反查），
连线 = 连接符（连接到形状，移动方块时线会跟着走）。

坐标换算：列 = 科技文件夹的 x（黑冰网格，1 格 = 70px），行 = 年份（每年 2 行）+ dy。
PPT 里每列固定 COL_W 英寸、每行固定 ROW_H 英寸，便于拖动对齐。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data_chi as D

from config import MOD, YEAR_BASE, YEAR_STEP

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# 版面
COL_W = 2.20          # 每列宽（英寸）
ROW_H = 0.48          # 每行高（英寸）
X0 = 0.55             # 左边距
Y0 = 0.95             # 表头上方留白
BOX_W = 2.05
BOX_H = 0.40

# 列标题与配色（与 PNG 预览一致）
COLS = {
    0: ("美制发动机", (52, 84, 120)),
    2: ("美制多发/喷气", (52, 84, 120)),
    4: ("苏制单发", (110, 62, 52)),
    6: ("苏制多发/喷气", (110, 62, 52)),
    8: ("日制发动机", (118, 108, 54)),
    12: ("德英发动机", (70, 96, 70)),
    16: ("航空枪炮", (92, 74, 110)),
    20: ("炸弹火箭", (108, 86, 60)),
    26: ("战斗机", (58, 108, 74)),
    30: ("截击机", (58, 96, 116)),
    32: ("重型战斗机", (74, 78, 124)),
    34: ("攻击机", (120, 78, 48)),
    36: ("侦察机", (86, 90, 100)),
    38: ("轻型轰炸机", (96, 62, 96)),
    40: ("中型轰炸机", (66, 84, 120)),
    42: ("重型轰炸机", (72, 76, 116)),
    44: ("运输机", (110, 96, 60)),
    46: ("水上飞机", (54, 104, 112)),
    48: ("喷气战斗机", (120, 66, 62)),
}


def build_items():
    items = []
    for a in D.AIRFRAMES:
        items.append(dict(kind="air", key=a["key"], zh=a["zh"], en=a["en"],
                          year=a["year"], x=a["x"], dy=a.get("dy") or 0, prev=a.get("prev")))
    for kind, table in (("engine", D.ENGINES), ("gun", D.GUNS), ("ord", D.ORDNANCE)):
        for t in table:
            items.append(dict(kind=kind, key=t["key"], zh=t["zh"], en=t.get("en", ""),
                              year=t["year"], x=t["x"], dy=0, prev=t.get("prev")))
    return items


def main():
    items = build_items()

    # 与构建脚本一致：同列同年按顺序自动占位（dy 为空时取第一个空位）
    used = {}
    for it in items:
        key = (it["x"], it["year"])
        dy = it["dy"]
        if dy is None:
            dy = 0
            while (key, dy) in used:
                dy += 1
        while (key, dy) in used:
            dy += 1
        it["dy"] = dy
        used[(key, dy)] = True

    xs = sorted({i["x"] for i in items})
    col_idx = {x: i for i, x in enumerate(xs)}
    years = sorted({i["year"] for i in items})

    prs = Presentation()
    prs.slide_width = Inches(X0 * 2 + COL_W * len(xs) + 0.4)
    prs.slide_height = Inches(Y0 + ROW_H * ((years[-1] - years[0]) * 2 + 2) + 0.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(18, 24, 34)
    bg.line.fill.background()
    bg.name = "背景"
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)

    # 标题
    title = slide.shapes.add_textbox(Inches(0.25), Inches(0.10), Inches(9), Inches(0.4))
    tf = title.text_frame
    tf.text = "黑冰 · 中系飞机科技树 · 可编辑布局（拖动方块调整位置）"
    tf.paragraphs[0].font.size = Pt(16)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(240, 228, 200)

    sub = slide.shapes.add_textbox(Inches(0.25), Inches(0.45), Inches(16), Inches(0.3))
    tf = sub.text_frame
    tf.text = ("列 = 机种类别（与黑冰 @FTR/@INT/@CAS/@TACT_BOMBER/@STRAT_BOMBERS/@TRPT 对应）；"
               "行 = 年份（每年 2 行）。形状名即科技 key，便于回填坐标。")
    tf.paragraphs[0].font.size = Pt(9)
    tf.paragraphs[0].font.color.rgb = RGBColor(150, 164, 184)

    # 列标题
    for x in xs:
        label, _ = COLS.get(x, (str(x), (70, 70, 70)))
        left = X0 + col_idx[x] * COL_W
        tb = slide.shapes.add_textbox(Inches(left + 0.05), Inches(Y0 - 0.5), Inches(COL_W - 0.1), Inches(0.32))
        tf = tb.text_frame
        tf.word_wrap = False
        tf.text = label
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(10)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(214, 224, 238)

    # 年份行
    for year in years:
        yy = Y0 + (year - years[0]) * 2 * ROW_H
        lb = slide.shapes.add_textbox(Inches(0.05), Inches(yy), Inches(0.45), Inches(ROW_H * 2))
        tf = lb.text_frame
        tf.text = str(year)
        tf.paragraphs[0].font.size = Pt(9)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(150, 164, 184)
        # 年份分隔线
        ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                        Inches(X0), Inches(yy + ROW_H * 2),
                                        Inches(prs.slide_width.inches - 0.2), Inches(yy + ROW_H * 2))
        ln.line.color.rgb = RGBColor(36, 46, 60)
        ln.line.width = Pt(0.75)

    # 科技方块
    shapes = {}
    for it in items:
        ci = col_idx[it["x"]]
        left = X0 + ci * COL_W + (COL_W - BOX_W) / 2
        top = Y0 + (it["year"] - years[0]) * 2 * ROW_H + it["dy"] * ROW_H + 0.02
        shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                     Inches(left), Inches(top), Inches(BOX_W), Inches(BOX_H))
        shp.name = f'{it["kind"]}:{it["key"]}'
        shp.adjustments[0] = 0.12
        _, color = COLS.get(it["x"], ("", (70, 70, 70)))
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGBColor(*color)
        shp.line.color.rgb = RGBColor(200, 210, 224)
        shp.line.width = Pt(0.75)
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left = Pt(2)
        tf.margin_right = Pt(2)
        tf.margin_top = Pt(0)
        tf.margin_bottom = Pt(0)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.text = it["zh"]
        tf.paragraphs[0].font.size = Pt(8)
        tf.paragraphs[0].font.color.rgb = RGBColor(245, 245, 245)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = str(it["year"])
        p2.font.size = Pt(6.5)
        p2.font.color.rgb = RGBColor(210, 214, 222)
        p2.alignment = PP_ALIGN.CENTER
        shapes[(it["kind"], it["key"])] = shp

    # 连线（连接到形状上，拖动方块时会跟随）
    for it in items:
        prev = it.get("prev")
        if not prev:
            continue
        a = shapes.get((it["kind"], prev))
        b = shapes.get((it["kind"], it["key"]))
        if a is None or b is None:
            continue
        cx = a.left + a.width // 2
        ax, ay = a.left + a.width // 2, a.top + a.height
        bx, by = b.left + b.width // 2, b.top
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, ax, ay, bx, by)
        conn.line.color.rgb = RGBColor(210, 200, 160)
        conn.line.width = Pt(1.25)
        try:
            conn.begin_connect(a, 2)  # bottom
            conn.end_connect(b, 0)    # top
        except Exception:
            pass

    # 第二页：使用说明
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    tb = slide2.shapes.add_textbox(Inches(0.6), Inches(0.6), Inches(20), Inches(8))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = [
        "怎么用这份 PPT 调整科技树布局",
        "",
        "1. 每个方块 = 一个科技；方块的名字（选中后在“选择窗格”里可见）就是科技 key，例如 air:p40e、engine_r1820。",
        "2. 直接拖动方块即可改位置；连线是“连接符”，已挂在方块上，移动方块时箭头会跟着走。",
        "3. 横轴 = 机种类别（列），纵轴 = 年份（每年 2 行）；同列同年有多架时，上下错半行。",
        "4. 调好后把这份 PPT 发回，我按方块所在列/年份把坐标写回 data_chi.py（或你直接告诉我要移动哪几架）。",
        "",
        "列与黑冰列变量的对应关系：",
        "  战斗机 = @FTR；截击机 = @INT；重型战斗机 = @HVY_FTR / @MR；攻击机 = @CAS；",
        "  侦察机 = @RECON；轻型轰炸机 = @L_BOMBER；中型轰炸机 = @TACT_BOMBER；",
        "  重型轰炸机 = @STRAT_BOMBERS；运输机 = @TRPT；水上飞机 = @FLY_BTS；喷气战斗机 = @JET_FTR。",
        "",
        "注意：PPT 只用于“看和摆”，不会影响游戏；游戏里最终位置由 common/technologies/CHI_air.txt 的 folder position 决定。",
    ]
    tf.text = lines[0]
    for ln in lines[1:]:
        para = tf.add_paragraph()
        para.text = ln
    for para in tf.paragraphs:
        para.font.size = Pt(12)
        para.font.color.rgb = RGBColor(230, 234, 240)
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.bold = True

    out_dir = os.path.join(MOD, "docs")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "科技树布局_可编辑.pptx")
    prs.save(path)
    print(path, prs.slide_width, prs.slide_height, "shapes:", len(slide.shapes))


if __name__ == "__main__":
    main()
