import json,collections,os
D=r"D:\Steam\steamapps\workshop\content\394360\中系飞机科技树\_tools\data"
techs=json.load(open(os.path.join(D,"techs.json"),encoding="utf-8"))
c=collections.Counter()
for t in techs:
    if t["folder"] in ("usair_folder","luftwaffe_folder","japanair_folder","sovietair_folder","britishair_folder"):
        for cat in t["categories"]:
            if not cat.endswith("_air"):
                c[cat]+=1
print("\n".join(f"{k}: {v}" for k,v in c.most_common(40)))
# per archetype sample from enable_equipments
