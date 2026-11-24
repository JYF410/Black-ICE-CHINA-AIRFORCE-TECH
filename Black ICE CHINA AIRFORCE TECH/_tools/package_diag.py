# -*- coding: utf-8 -*-
"""生成两套排查包（都只写工作区的 _install/，不影响游戏目录）

A. update_game_files.zip        —— 当前构建（v0.1.4：不隐藏通用空军页、文件夹只认 CHI_air 标志）
B. update_game_files_diagB.zip  —— 把 UI 集成本身全部退回原始状态：
      * countrytechtreeview.gui 换回未修改的坦克子模版本（没有中国空军页/页签/条目模板）
      * technology_tags 置空（不重定义任何文件夹）
      * scripted_guis 置空（不挂中国空军的科技队列块）
   其余（科技文件、研究数组、on_actions）保留。
   用途：如果 B 能正常打开科技树而 A 不行，问题就在 UI 集成；如果 B 也不行，
   说明问题不在这些 UI 文件（可能是别的模组更新或数组/on_actions）。

用法：python _tools/package_diag.py
"""
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build")
TANK = r"D:\Steam\steamapps\workshop\content\394360\3463196432"
OUT_A = os.path.join(ROOT, "_install", "update_game_files.zip")
OUT_B = os.path.join(ROOT, "_install", "update_game_files_diagB.zip")
DIRS = ["common", "interface", "gfx", "localisation", "history", "events"]


def collect():
    for d in DIRS:
        base = os.path.join(ROOT, d)
        for dirpath, _, files in os.walk(base):
            for fn in files:
                p = os.path.join(dirpath, fn)
                yield p, os.path.relpath(p, ROOT).replace(os.sep, "/")
    info = os.path.join(ROOT, "build_info.txt")
    if os.path.isfile(info):
        yield info, "build_info.txt"


def write_zip(path, overrides=None):
    overrides = overrides or {}
    seen = set()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for p, rel in collect():
            if rel in overrides:
                z.writestr(rel, overrides[rel])
                seen.add(rel)
            else:
                z.write(p, rel)
        for rel, text in overrides.items():
            if rel not in seen:
                z.writestr(rel, text)
    print(f"{path}  {os.path.getsize(path)} bytes")


def main():
    os.makedirs(os.path.dirname(OUT_A), exist_ok=True)
    write_zip(OUT_A)

    base_gui = os.path.join(TANK, "interface", "countrytechtreeview.gui")
    with open(base_gui, encoding="utf-8-sig", errors="replace") as f:
        plain_gui = f.read()
    write_zip(
        OUT_B,
        {
            "interface/countrytechtreeview.gui": plain_gui,
            "common/technology_tags/zz_CHI_air_technology.txt": "technology_folders = {\n}\n",
            "common/scripted_guis/BI_tech_queue_china_air.txt": "scripted_gui = {\n}\n",
        },
    )


if __name__ == "__main__":
    main()
