import json, os, collections
D = r"D:\Steam\steamapps\workshop\content\394360\中系飞机科技树\_tools\data"
techs = json.load(open(os.path.join(D, "techs.json"), encoding="utf-8"))
eq = {e["id"]: e for e in json.load(open(os.path.join(D, "equipment.json"), encoding="utf-8"))}
m = collections.defaultdict(collections.Counter)
for t in techs:
    if t["folder"] not in ("usair_folder", "luftwaffe_folder", "japanair_folder", "sovietair_folder", "britishair_folder"):
        continue
    cats = [c for c in t["categories"] if not c.endswith("_air") and c not in ("air_equipment", "ad_air_component")]
    for e in t["enable_equipments"]:
        arch = eq.get(e, {}).get("archetype")
        if arch:
            m[arch][tuple(sorted(cats))] += 1
for arch in sorted(m):
    print(arch, "->", m[arch].most_common(3))
