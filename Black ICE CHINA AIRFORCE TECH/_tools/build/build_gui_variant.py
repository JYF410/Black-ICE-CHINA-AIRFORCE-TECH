# -*- coding: utf-8 -*-
"""Also produce a BIAD-based (tank-mod-free) GUI copy for users who do not run
the Chinese tank tech submod. It is written outside interface/ so the game never
loads it; rename it to countrytechtreeview.gui to use.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_chi as B


def main():
    sprites = B.emit_gfx.__wrapped__ if hasattr(B.emit_gfx, "__wrapped__") else None
    # rebuild the sprite list the same way emit_gfx does
    sprites = []
    for a in B.D.AIRFRAMES:
        tex = B.icon_for_equipment(a["equip"]) or \
            "gfx/interface/technologies/air/GENERIC/ALLIES_fighter_p40_warhawk_1.dds"
        sprites.append((B.tech_id("air", a["key"]), tex))
    for e in B.D.ENGINES:
        sprites.append((B.tech_id("engine", e["key"]), B.equipment_icon(e["modules"], B.GENERIC_ENGINE)))
    for g in B.D.GUNS:
        sprites.append((B.tech_id("gun", g["key"]), B.equipment_icon(g["modules"], B.GENERIC_CANNON)))
    for o in B.D.ORDNANCE:
        sprites.append((B.tech_id("ord", o["key"]), B.equipment_icon(o["modules"], B.GENERIC_BOMB)))

    out = os.path.join(B.MOD, "_install", "countrytechtreeview.gui.biad_base")
    B.emit_gui(sprites,
               base_override=os.path.join(B.BIAD, "interface", "countrytechtreeview.gui"),
               out_path=out)
    print(out)


if __name__ == "__main__":
    main()
