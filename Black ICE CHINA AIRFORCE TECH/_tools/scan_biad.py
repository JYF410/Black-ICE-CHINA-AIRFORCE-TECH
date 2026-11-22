# -*- coding: utf-8 -*-
"""Scan BlackICE Aircraft Designer for reusable data tables.

Outputs JSON/CSV into _tools/data so the Chinese tree can reference
existing (verified) equipment / module / tech ids.
"""
import os
import sys
import json
import csv
import re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cw_parse as C

BIAD = r"D:\Steam\steamapps\workshop\content\394360\3808452657"
OUT = os.path.join(HERE, "data")
os.makedirs(OUT, exist_ok=True)


def norm_name(v):
    return v if isinstance(v, str) else ""


def scan_equipment():
    rows = []
    eq_dir = os.path.join(BIAD, "common", "units", "equipment")
    for path in C.load_dir(eq_dir):
        fname = os.path.basename(path)
        tree = C.parse_file(path)
        eqs = tree.get("equipments")
        if not isinstance(eqs, C.Node):
            continue
        for eid, blk in eqs.items():
            if not isinstance(blk, C.Node):
                continue
            row = {
                "id": eid,
                "file": fname,
                "archetype": norm_name(blk.get("archetype")),
                "year": norm_name(blk.get("year")),
                "parent": norm_name(blk.get("parent")),
                "picture": norm_name(blk.get("picture")),
                "slots": {},
            }
            slots = blk.get("module_slots")
            if isinstance(slots, C.Node):
                for slot_name, slot in slots.items():
                    if not isinstance(slot, C.Node):
                        continue
                    cats = slot.get("allowed_module_categories")
                    if isinstance(cats, C.Node):
                        cat_list = list(cats.get("_items", []))
                    else:
                        cat_list = C.scalars(cats)
                    row["slots"][slot_name] = cat_list
            rows.append(row)
    return rows


def scan_equipment_raw_lists():
    """Second pass: regex-extract allowed_module_categories lists (inline lists
    are bare tokens, which the generic parser drops)."""
    eq_dir = os.path.join(BIAD, "common", "units", "equipment")
    out = {}
    block_re = re.compile(r"^\t([A-Za-z0-9_]+) = \{", re.M)
    for path in C.load_dir(eq_dir):
        text = open(path, encoding="utf-8-sig", errors="replace").read()
        # find equipment blocks by id
        for m in block_re.finditer(text):
            eid = m.group(1)
            start = m.end()
            # find matching close brace
            depth = 1
            i = start
            while i < len(text) and depth > 0:
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                i += 1
            body = text[start:i]
            slots = {}
            for sm in re.finditer(r"(\w+) = \{([^{}]*)\}", body):
                sname, sbody = sm.group(1), sm.group(2)
                if "allowed_module_categories" in sbody or sname in (
                    "module_slots",
                ):
                    cats = []
                    cm = re.search(r"allowed_module_categories = \{([^{}]*)\}", sbody)
                    if cm:
                        cats = [x for x in cm.group(1).split() if x]
                    slots[sname] = cats
            if slots:
                out.setdefault(os.path.basename(path), {})[eid] = slots
    return out


def scan_modules():
    rows = []
    mod_dir = os.path.join(BIAD, "common", "units", "equipment", "modules")
    for path in C.load_dir(mod_dir):
        fname = os.path.basename(path)
        tree = C.parse_file(path)
        mods = tree.get("equipment_modules")
        if not isinstance(mods, C.Node):
            continue
        for mid, blk in mods.items():
            if not isinstance(blk, C.Node):
                continue
            rows.append(
                {
                    "id": mid,
                    "file": fname,
                    "category": norm_name(blk.get("category")),
                    "gui_category": norm_name(blk.get("gui_category")),
                }
            )
    return rows


def scan_techs():
    rows = []
    tech_dir = os.path.join(BIAD, "common", "technologies")
    for path in C.load_dir(tech_dir):
        fname = os.path.basename(path)
        tree = C.parse_file(path)
        vars_ = C.collect_vars(tree)
        techs = tree.get("technologies")
        if not isinstance(techs, C.Node):
            continue
        for tid, blk in techs.items():
            if not isinstance(blk, C.Node):
                continue
            folder = blk.get("folder")
            fname_ = pos = None
            x = y = None
            if isinstance(folder, C.Node):
                fname_ = norm_name(folder.get("name"))
                pos = folder.get("position")
                if isinstance(pos, C.Node):
                    x = C.resolve(norm_name(pos.get("x")), vars_)
                    y = C.resolve(norm_name(pos.get("y")), vars_)
            rows.append(
                {
                    "id": tid,
                    "file": fname,
                    "folder": fname_,
                    "x": x,
                    "y": y,
                    "start_year": norm_name(blk.get("start_year")),
                    "research_cost": norm_name(blk.get("research_cost")),
                    "enable_equipments": C.scalars(blk.get("enable_equipments")),
                    "enable_equipment_modules": C.scalars(
                        blk.get("enable_equipment_modules")
                    ),
                    "small_layout": norm_name(blk.get("force_use_small_tech_layout")),
                    "categories": C.scalars(blk.get("categories")),
                }
            )
    return rows


def scan_loc():
    """Return {lang: {key: text}} for BIAD localisation."""
    out = {}
    loc_root = os.path.join(BIAD, "localisation")
    line_re = re.compile(r'^\s*([A-Za-z0-9_.\-]+):(?:\d+)?\s+"(.*)"\s*$')
    for lang in os.listdir(loc_root):
        d = os.path.join(loc_root, lang)
        if not os.path.isdir(d):
            continue
        table = {}
        for path in C.load_dir(d, "*.yml"):
            with open(path, encoding="utf-8-sig", errors="replace") as f:
                for line in f:
                    m = line_re.match(line)
                    if m:
                        table.setdefault(m.group(1), m.group(2))
        out[lang] = table
    return out


def main():
    equipment = scan_equipment()
    rawslots = scan_equipment_raw_lists()
    modules = scan_modules()
    techs = scan_techs()
    loc = scan_loc()

    # merge raw slot lists
    for row in equipment:
        f = row["file"]
        if f in rawslots and row["id"] in rawslots[f]:
            row["slots_raw"] = rawslots[f][row["id"]]

    def dump(name, data):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)

    dump("equipment.json", equipment)
    dump("modules.json", modules)
    dump("techs.json", techs)
    dump("loc.json", loc)

    print(f"equipment: {len(equipment)}")
    print(f"modules:   {len(modules)}")
    print(f"techs:     {len(techs)}")
    print("loc langs: " + ", ".join(f"{k}={len(v)}" for k, v in loc.items()))

    # human report: equipment grouped by file, with English names
    en = loc.get("english", {})
    by_file = {}
    for row in equipment:
        by_file.setdefault(row["file"], []).append(row)
    with open(os.path.join(OUT, "report_equipment.txt"), "w", encoding="utf-8") as f:
        for fname in sorted(by_file):
            f.write(f"\n### {fname}\n")
            for row in sorted(by_file[fname], key=lambda r: (r["year"], r["id"])):
                nm = en.get(row["id"], "")
                f.write(
                    f"{row['year']:>4} {row['id']:<45} {row['archetype']:<22} {nm}\n"
                )


if __name__ == "__main__":
    main()
