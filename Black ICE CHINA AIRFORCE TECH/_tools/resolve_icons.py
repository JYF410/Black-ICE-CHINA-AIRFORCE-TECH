# -*- coding: utf-8 -*-
"""Resolve icon texture paths for planes/modules from BIAD + Black ICE .gfx files."""
import os, re, json, sys

BIAD = r"D:\Steam\steamapps\workshop\content\394360\3808452657"
BI = r"D:\Steam\steamapps\workshop\content\394360\1851181613"
VANILLA = r"D:\Steam\steamapps\common\Hearts of Iron IV"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

ROOTS = [BIAD, BI, VANILLA]

sprite_re = re.compile(
    r'name\s*=\s*"?(GFX_[A-Za-z0-9_]+)"?[\s\S]{0,400}?texturefile\s*=\s*"([^"]+)"',
    re.IGNORECASE,
)


def scan_gfx(root):
    table = {}
    idir = os.path.join(root, "interface")
    if not os.path.isdir(idir):
        return table
    for dirpath, _, files in os.walk(idir):
        for fn in files:
            if not fn.lower().endswith(".gfx"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                text = open(p, encoding="utf-8-sig", errors="replace").read()
            except OSError:
                continue
            for m in sprite_re.finditer(text):
                name, tex = m.group(1), m.group(2)
                tex = tex.replace("\\\\", "/").replace("\\", "/").replace("//", "/")
                table.setdefault(name, tex)
    return table


def path_exists(tex):
    for root in ROOTS:
        p = os.path.join(root, *tex.split("/"))
        if os.path.isfile(p):
            return root
    return None


def main():
    table = {}
    for root in ROOTS:
        for k, v in scan_gfx(root).items():
            table.setdefault(k, v)
    # index alternative: sprite name -> texture (BI may define same names)
    with open(os.path.join(DATA, "sprites.json"), "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False, indent=1)
    print("sprites:", len(table))

    ids = [l.strip() for l in open(os.path.join(DATA, "icon_targets.txt"), encoding="utf-8") if l.strip()]
    out = []
    for i in ids:
        cands = [f"GFX_{i}_medium", f"GFX_{i}", f"GFX_tech_{i}_medium"]
        found = None
        for c in cands:
            if c in table:
                found = (c, table[c], path_exists(table[c]) or "MISSING")
                break
        out.append(f"{i}\t{found}")
    open(os.path.join(DATA, "icon_resolve.txt"), "w", encoding="utf-8").write("\n".join(out))
    print("resolved:", sum(1 for l in out if "None" not in l), "/", len(out))


if __name__ == "__main__":
    main()
