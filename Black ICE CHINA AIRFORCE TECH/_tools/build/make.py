# -*- coding: utf-8 -*-
"""中系飞机科技树 —— 一键构建入口

用法：
    python _tools/build/make.py all        # 内容 + 数组 + 图标 + 预览 + 校验（默认）
    python _tools/build/make.py content    # 只重建 common/（科技、标签、GUI、gfx、本地化）
    python _tools/build/make.py arrays     # 只重建研究数组与 scripted GUI 注册
    python _tools/build/make.py art        # 只重绘标签页按钮与封面
    python _tools/build/make.py preview    # 只重绘 docs/科技树预览.png
    python _tools/build/make.py validate   # 只跑静态校验

设计原则：
  * data_chi.py 是唯一的内容数据源；
  * 其余文件全部由脚本生成，不要手改（手改会在下次 make 时被覆盖）；
  * 每次构建结束自动跑校验，非 0 时返回非 0 退出码。
"""
import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, HERE)
sys.path.insert(0, TOOLS)


def run_content():
    import build_chi
    build_chi.main()


def run_arrays():
    import build_arrays
    build_arrays.main()


def run_art():
    import make_art
    print(make_art.make_tab())
    print(make_art.make_thumbnail())


def run_preview():
    import make_preview
    make_preview.main()


def run_validate():
    import validate
    return validate.main()


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "all"
    steps = {
        "content": [run_content],
        "arrays": [run_arrays],
        "art": [run_art],
        "preview": [run_preview],
        "all": [run_content, run_arrays, run_art, run_preview],
        "validate": [],
    }
    if cmd not in steps:
        print(__doc__)
        return 2
    for step in steps[cmd]:
        print(f"\n=== {step.__name__} ===")
        step()
    print("\n=== validate ===")
    return run_validate()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
