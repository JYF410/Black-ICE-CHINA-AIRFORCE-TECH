# -*- coding: utf-8 -*-
"""Ad-hoc probe over the extracted BIAD data."""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


EQ = {e["id"]: e for e in load("equipment.json")}
MOD = load("modules.json")
LOC = load("loc.json")
EN = LOC.get("english", {})
ZH = LOC.get("simp_chinese", {})

TECH = {t["id"]: t for t in load("techs.json")}


def mods_by_cat(cat):
    return [m for m in MOD if m["category"] == cat]


def show_eq(eid):
    e = EQ.get(eid)
    if not e:
        print(f"!! {eid} NOT FOUND")
        return
    print(f"\n=== {eid} | {e['archetype']} | {e['year']} | {e['file']}")
    print("  EN:", EN.get(eid, "?"))
    print("  ZH:", ZH.get(eid, "?"))
    for slot, cats in (e.get("slots") or {}).items():
        if not cats:
            print(f"  slot {slot}: (inherit)")
            continue
        print(f"  slot {slot}: {cats}")
        for c in cats:
            ms = mods_by_cat(c)
            if ms:
                print(f"     [{c}] " + ", ".join(
                    f"{m['id']}({EN.get(m['id'],'?')})" for m in ms[:6]
                ) + (" ..." if len(ms) > 6 else ""))


def show_cats(prefix):
    cats = sorted({m["category"] for m in MOD})
    for c in cats:
        if prefix in c:
            ms = mods_by_cat(c)
            print(f"\n[{c}] {len(ms)} modules")
            for m in ms[:20]:
                print(f"   {m['id']:<40} {EN.get(m['id'],'')}")


def show_tech(tid):
    t = TECH.get(tid)
    print(t)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "eq"
    args = sys.argv[2:]
    if mode == "eq":
        for a in args:
            show_eq(a)
    elif mode == "cat":
        for a in args:
            show_cats(a)
    elif mode == "tech":
        for a in args:
            show_tech(a)
