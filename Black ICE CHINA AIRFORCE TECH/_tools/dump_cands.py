import json, os
D = r"D:\Steam\steamapps\workshop\content\394360\中系飞机科技树\_tools\data"
eq = {e["id"]: e for e in json.load(open(os.path.join(D, "equipment.json"), encoding="utf-8"))}
mods = json.load(open(os.path.join(D, "modules.json"), encoding="utf-8"))
loc = json.load(open(os.path.join(D, "loc.json"), encoding="utf-8"))
en = loc["english"]
bycat = {}
for m in mods:
    bycat.setdefault(m["category"], []).append(m["id"])
cands = [l.strip() for l in open(os.path.join(D, "cands.txt"), encoding="utf-8") if l.strip()]
out = []
for cid in cands:
    e = eq.get(cid)
    if not e:
        out.append(f"!! {cid} MISSING")
        continue
    pp = e["slots"].get("ad_airforce_powerplant", [])
    fc = e["slots"].get("ad_airforce_frame_config", [])
    wpn = e["slots"].get("ad_airforce_body_weapon", [])
    out.append(f"{cid}\t{e['archetype']}\t{e['year']}\tpp={pp}\tfc={fc}\tEN={en.get(cid,'')}")
    for cat in pp:
        ms = bycat.get(cat, [])
        out.append("    [" + cat + "] " + " | ".join(f"{m}({en.get(m,'')})" for m in ms))
    for cat in wpn:
        ms = bycat.get(cat, [])
        if ms:
            out.append("    W[" + cat + "] " + " | ".join(ms))
open(os.path.join(D, "cands_report.txt"), "w", encoding="utf-8").write("\n".join(out))
print("ok", len(cands))
