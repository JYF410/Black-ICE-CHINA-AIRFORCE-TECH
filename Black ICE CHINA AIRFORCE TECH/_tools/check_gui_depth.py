import sys

def check(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    i = t.find('name = "chinaair_folder"')
    fd = t[:i].count("{") - t[:i].count("}")
    g = t.find('name = "ad_chi_tech_hawk3_tree"')
    gd = t[:g].count("{") - t[:g].count("}")
    print(f"{path}\n  folder name depth={fd} gridbox name depth={gd} "
          f"({'OK' if gd == fd + 1 else 'WRONG — 在子容器里，引擎找不到'})")

for p in sys.argv[1:]:
    check(p)
