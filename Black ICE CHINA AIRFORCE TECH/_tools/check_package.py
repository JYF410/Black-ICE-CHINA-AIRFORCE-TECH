import os
import tempfile
import zipfile

ROOT = r"D:\Steam\steamapps\workshop\content\394360\中系飞机科技树"
ZIP = os.path.join(ROOT, "_install", "update_game_files.zip")

z = zipfile.ZipFile(ZIP)
print("zip entries:", len(z.infolist()))
for i in z.infolist():
    print(f"  {i.filename:60} {i.file_size}")

tmp = tempfile.mkdtemp()
z.extract("interface/countrytechtreeview.gui", tmp)
gui = os.path.join(tmp, "interface", "countrytechtreeview.gui")
t = open(gui, encoding="utf-8", errors="replace").read()
i = t.find('name = "chinaair_folder"')
fd = t[:i].count("{") - t[:i].count("}")
g = t.find('name = "ad_chi_tech_hawk3_tree"')
gd = t[:g].count("{") - t[:g].count("}")
print(f"extracted gui: folder depth={fd}, gridbox depth={gd}, "
      f"{'OK' if gd == fd + 1 else 'WRONG'}")
