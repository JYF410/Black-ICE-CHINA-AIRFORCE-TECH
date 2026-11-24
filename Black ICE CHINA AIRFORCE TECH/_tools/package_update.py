# -*- coding: utf-8 -*-
"""把工作区里「游戏需要的那部分」打成一个 zip，方便覆盖已发布的副本。

背景：Paradox 启动器发布时会复制一份到工坊目录（例如
D:/Steam/steamapps/workshop/content/394360/3844078670），游戏加载的是那份副本。
工作区改了代码但没重新发布，游戏看到的仍是旧文件。

用法：
    python _tools/package_update.py
产物：
    _install/update_game_files.zip
内容（不含 descriptor.mod / 封面 / 文档 / _tools，避免覆盖你在启动器里改的名字和版本）：
    common/ interface/ gfx/ localisation/ history/ build_info.txt
"""
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "_install", "update_game_files.zip")
DIRS = ["common", "interface", "gfx", "localisation", "history", "events"]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    count = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for d in DIRS:
            base = os.path.join(ROOT, d)
            for dirpath, _, files in os.walk(base):
                for fn in files:
                    p = os.path.join(dirpath, fn)
                    rel = os.path.relpath(p, ROOT)
                    z.write(p, rel)
                    count += 1
        info = os.path.join(ROOT, "build_info.txt")
        if os.path.isfile(info):
            z.write(info, "build_info.txt")
            count += 1
    print(f"{OUT}\n  {count} files, {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
