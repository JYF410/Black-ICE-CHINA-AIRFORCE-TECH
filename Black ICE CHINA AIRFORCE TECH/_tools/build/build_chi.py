# -*- coding: utf-8 -*-
"""Generate the "Chinese Aircraft Tech Tree" submod for Black ICE / BIAD.

Outputs into the session workspace (mod root):
  descriptor.mod
  common/technologies/CHI_air.txt
  common/technology_tags/zz_CHI_air_technology.txt
  common/on_actions/zz_CHI_air_startup.txt
  interface/chi_air_technology.gfx
  interface/countrytechtreeview.gui      (patched copy of BIAD / tank-mod GUI)
  localisation/{english,simp_chinese}/chi_air_l_*.yml
  gfx/interface/techtree/techtree_china_air_tab.tga
  thumbnail.png
"""
import os
import re
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
DATA = os.path.join(TOOLS, "data")
sys.path.insert(0, HERE)
sys.path.insert(0, TOOLS)

import data_chi as D
from config import (
    MOD, BI, BIAD, TANK, MOD_LINK, MOD_FILE_NAME,
    FOLDER, FLAG, ARRAY_FLAG, ARRAY_EFFECT, LOG_MARKER, CHINESE_TAGS,
    SLOT, YEAR_BASE, YEAR_STEP, PIXEL_ORIGIN_X, PIXEL_ORIGIN_Y,
    CANVAS_W, CANVAS_H, COLUMNS,
    MOD_VERSION, MOD_NAME_CN, MOD_NAME_EN, SUPPORTED_VERSION, DEPENDENCIES,
)

TECH_DIR = os.path.join(MOD, "common", "technologies")

report = []


def log(*a):
    line = " ".join(str(x) for x in a)
    report.append(line)
    print(line)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


EQ = {e["id"]: e for e in load("equipment.json")}
MODS = {m["id"]: m for m in load("modules.json")}
LOC = load("loc.json")
SPRITES = load("sprites.json")
EN = dict(LOC.get("english", {}))

# Black ICE (parent mod) also provides tooltip / category localisation
BI = r"D:\Steam\steamapps\workshop\content\394360\1851181613"


def merge_bi_loc():
    line_re = re.compile(r'^\s*([A-Za-z0-9_.\-]+):(?:\d+)?\s+"(.*)"\s*$')
    d = os.path.join(BI, "localisation", "english")
    if not os.path.isdir(d):
        return
    for fn in os.listdir(d):
        if not fn.endswith(".yml"):
            continue
        with open(os.path.join(d, fn), encoding="utf-8-sig", errors="replace") as f:
            for line in f:
                m = line_re.match(line)
                if m:
                    EN.setdefault(m.group(1), m.group(2))


merge_bi_loc()


def load_technology_categories():
    """Read the authoritative category list from BIAD's technology_tags."""
    import cw_parse as C
    path = os.path.join(BIAD, "common", "technology_tags", "00_technology.txt")
    tree = C.parse_file(path)
    cats = tree.get("technology_categories")
    return set(C.scalars(cats))


TECH_CATEGORIES = load_technology_categories()

# archetype -> BIAD technology category
ARCH_CAT = {
    "fighter_equipment": "light_fighter",
    "fighter_alt_equipment": "light_fighter",
    "mr_fighter_equipment": "light_fighter",
    "interceptor_equipment": "light_fighter",
    "cv_fighter_equipment": "light_fighter",
    "cv_mr_fighter_equipment": "light_fighter",
    "fighter_navy_equipment": "light_fighter",
    "interceptor_navy_equipment": "light_fighter",
    "heavy_fighter_equipment": "cat_heavy_fighter",
    "night_fighter_equipment": "cat_heavy_fighter",
    "CAS_equipment": "cas_bomber",
    "cv_CAS_equipment": "cas_bomber",
    "twin_cas_equipment": "cas_bomber",
    "light_bomber_equipment": "tactical_bomber",
    "tac_bomber_equipment": "tactical_bomber",
    "fast_bomber_equipment": "tactical_bomber",
    "quad_engine_bomber_equipment": "cat_strategic_bomber",
    "nav_bomber_equipment": "naval_bomber",
    "nav_bomber_gb_equipment": "naval_bomber",
    "heavy_nav_bomber_equipment": "naval_bomber",
    "flying_boat_equipment": "naval_bomber",
    "jet_fighter_equipment": "jet_aircraft",
    "jet_mr_fighter_equipment": "jet_aircraft",
    "jet_cas_equipment": "jet_aircraft",
    "scout_plane_equipment": None,
    "transport_plane_equipment": None,
}

# techs are grouped into chains by (prefix, key)
AIRFRAME_KEYS = {a["key"] for a in D.AIRFRAMES}
ENGINE_KEYS = {e["key"] for e in D.ENGINES}
GUN_KEYS = {g["key"] for g in D.GUNS}
ORD_KEYS = {o["key"] for o in D.ORDNANCE}


def tech_id(kind, key):
    if kind == "air":
        return f"ad_chi_tech_{key}"
    return f"ad_chi_tech_{kind}_{key}"


def resolve_prev(kind, prev):
    if not prev:
        return None
    pool = {"air": AIRFRAME_KEYS, "engine": ENGINE_KEYS, "gun": GUN_KEYS, "ord": ORD_KEYS}[kind]
    if prev not in pool:
        raise SystemExit(f"unknown prev {prev} for kind {kind}")
    return tech_id(kind, prev)


def frame_config(equip):
    """frame_config module ids required by the prototype."""
    slots = EQ[equip]["slots"].get("ad_airforce_frame_config", [])
    return slots


def tex_of(sprite):
    t = SPRITES.get(sprite)
    if not t:
        return None
    t = t.replace("\\\\", "/").replace("//", "/")
    return t


def file_exists(tex):
    for root in (MOD, BIAD, TANK, r"D:\Steam\steamapps\workshop\content\394360\1851181613",
                 r"D:\Steam\steamapps\common\Hearts of Iron IV"):
        if os.path.isfile(os.path.join(root, *tex.split("/"))):
            return True
    return False


def icon_for_equipment(equip):
    for name in (f"GFX_{equip}_medium", f"GFX_{equip}"):
        t = tex_of(name)
        if t and file_exists(t):
            return t
    return None


# --- icon lookup for equipment techs: use the icon of the BIAD tech that
# --- unlocks the same module, else a generic module icon
def build_module_icon_map():
    mapping = {}
    techs = load("techs.json")
    for t in techs:
        for m in t["enable_equipment_modules"]:
            mapping.setdefault(m, t["id"])
    out = {}
    for m, tid in mapping.items():
        for cand in (f"GFX_{tid}_medium", f"GFX_{tid}"):
            tex = tex_of(cand)
            if tex and file_exists(tex):
                out[m] = tex
                break
    return out


MODULE_ICON = build_module_icon_map()

GENERIC_ENGINE = "gfx/interface/equipmentdesigner/planes/modules/modules/airplane_engine_1_1_icon.dds"
GENERIC_BOMB = "gfx/interface/equipmentdesigner/planes/modules/modules/airplane_bomb_1_icon.dds"
GENERIC_CANNON = "gfx/interface/equipmentdesigner/planes/modules/modules/airplane_cannon_1_1_icon.dds"


def equipment_icon(modules, fallback):
    for m in modules:
        if m in MODULE_ICON:
            return MODULE_ICON[m]
    return fallback


# ==========================================================================
# builders
# ==========================================================================
def fmt_modules(mods, indent="\t\t\t"):
    return "\n".join(f"{indent}{m}" for m in mods)


def ai_variant_effects():
    """Archetypes for which Black ICE defines ai_create_variant/<arch>."""
    import cw_parse as C
    path = os.path.join(BI, "common", "scripted_effects", "_ai_VARIANTS_scripted_effects.txt")
    tree = C.parse_file(path)
    node = tree.get("scripted_effects")
    if not isinstance(node, C.Node):
        return set()
    out = set()
    for k in node:
        if isinstance(k, str) and k.startswith("ai_create_variant/"):
            out.add(k.split("/", 1)[1])
    return out


AI_VARIANTS = ai_variant_effects()


def tech_block(tid, start_year, cost, x, yy, equipments, modules, categories,
               leads_to=None, depends_on=None, small=False, tooltips=(),
               ai_archetype=None, ai_variant=None):
    for c in categories:
        if c not in TECH_CATEGORIES:
            raise SystemExit(f"{tid}: unknown technology category '{c}'")
    lines = [f"\t{tid} = {{"]
    if equipments:
        lines.append("\t\tenable_equipments = {")
        lines.append(fmt_modules(equipments))
        lines.append("\t\t}")
    if modules:
        lines.append("\t\tenable_equipment_modules = {")
        lines.append(fmt_modules(modules))
        lines.append("\t\t}")
    if leads_to:
        lines.append("\t\tpath = {")
        lines.append(f"\t\t\tleads_to_tech = {leads_to}")
        lines.append("\t\t\tresearch_cost_coeff = 1")
        lines.append("\t\t}")
    if depends_on:
        lines.append("\t\tdependencies = {")
        lines.append(f"\t\t\t{depends_on} = 1")
        lines.append("\t\t}")
    if small:
        lines.append("\t\tforce_use_small_tech_layout = yes")
    lines.append(f"\t\tresearch_cost = {cost}")
    lines.append(f"\t\tstart_year = {start_year}")
    lines.append("\t\tfolder = {")
    lines.append(f"\t\t\tname = {FOLDER}")
    lines.append(f"\t\t\tposition = {{ x = {x} y = {yy} }}")
    lines.append("\t\t}")
    lines.append("")
    lines.append("\t\tspecial_project_specialization = { specialization_air }")
    lines.append("")
    lines.append("\t\tai_will_do = {")
    lines.append("\t\t\tfactor = 1")
    lines.append("\t\t}")
    lines.append("\t\ton_research_complete = {")
    lines.append(f"\t\t\tset_temp_variable = {{ tech = token:{tid} }}")
    lines.append("\t\t\ton_air_tech_research_complete = yes")
    if ai_archetype and ai_variant and ai_archetype in AI_VARIANTS and len(equipments) == 1:
        lines.append("\t\t\tif = {")
        lines.append("\t\t\t\tlimit = {")
        lines.append("\t\t\t\t\tis_ai = yes")
        lines.append("\t\t\t\t}")
        lines.append(f"\t\t\t\tset_country_flag = ai_tech/{ai_archetype}")
        lines.append(f"\t\t\t\tset_temp_variable = {{ selected_variant = token:{ai_variant} }}")
        lines.append(f"\t\t\t\tai_create_variant/{ai_archetype} = yes")
        lines.append("\t\t\t}")
    tt = ["tech_category_tt", "air_equipment_tt"] + [t for t in tooltips if t]
    seen = []
    for t in tt:
        if t in EN and t not in seen:
            seen.append(t)
    for t in seen:
        lines.append(f"\t\t\tcustom_effect_tooltip = {t}")
    lines.append("\t\t}")
    lines.append("")
    lines.append("\t\tcategories = {")
    for c in categories:
        lines.append(f"\t\t\t{c}")
    lines.append("\t\t}")
    lines.append("\t}")
    return "\n".join(lines)


def validate_data():
    """数据表自检：在生成任何文件之前拦住低级错误。"""
    problems = []
    tables = (("air", D.AIRFRAMES), ("engine", D.ENGINES), ("gun", D.GUNS), ("ord", D.ORDNANCE))
    all_keys = set()
    for kind, table in tables:
        seen = set()
        for item in table:
            key = item["key"]
            if key in seen:
                problems.append(f"{kind}: 重复 key {key}")
            seen.add(key)
            all_keys.add((kind, key))
            if item["x"] not in COLUMNS.values():
                problems.append(f"{kind}.{key}: 列 x={item['x']} 不在 config.COLUMNS 中")
            if not (YEAR_BASE <= item["year"] <= YEAR_BASE + 12):
                problems.append(f"{kind}.{key}: 年份 {item['year']} 超出 {YEAR_BASE}..{YEAR_BASE + 12}")
            prev = item.get("prev")
            if prev:
                same = {"air": D.AIRFRAMES, "engine": D.ENGINES, "gun": D.GUNS, "ord": D.ORDNANCE}[kind]
                if prev not in {o["key"] for o in same}:
                    problems.append(f"{kind}.{key}: prev={prev} 不在同类数据表中")
                if prev == key:
                    problems.append(f"{kind}.{key}: prev 指向自己")
            for field in ("en", "zh", "mfr"):
                if not item.get(field):
                    problems.append(f"{kind}.{key}: 缺少字段 {field}")
    if problems:
        for p in problems:
            log("DATA ERROR:", p)
        raise SystemExit(f"数据表有 {len(problems)} 处错误，已中止生成")
    log(f"data check ok: {len(D.AIRFRAMES)} aircraft, {len(D.ENGINES)} engines, "
        f"{len(D.GUNS)} guns, {len(D.ORDNANCE)} ordnance")


def emit_technologies():
    validate_data()
    out = []
    out.append("# 中系飞机科技树 / Chinese Aircraft Tech Tree")
    out.append("# 黑冰（Black ICE）+ BlackICE Aircraft Designer 子模组")
    out.append("# 位置说明：x 为列，y 为年份行（每年 2 行，1935 = 0）")
    out.append("technologies = {")
    for year in range(YEAR_BASE, YEAR_BASE + 13):
        out.append(f"\t@{year} = {(year - YEAR_BASE) * YEAR_STEP}")
    out.append("")

    used_cells = {}

    def cell(x, year, dy=None):
        taken = {k[2] for k in used_cells if k[0] == x and k[1] == year}
        if dy is None:
            for cand in (0, 1):
                if cand not in taken:
                    dy = cand
                    break
            else:
                raise SystemExit(f"no free row for x={x} year={year}")
        if dy in taken:
            raise SystemExit(f"duplicate cell x={x} year={year} dy={dy}")
        used_cells[(x, year, dy)] = True
        return (year - YEAR_BASE) * YEAR_STEP + dy

    # ---- airframes -------------------------------------------------------
    out.append("\t####################################################################")
    out.append("\t##  作战飞机")
    out.append("\t####################################################################")
    for a in D.AIRFRAMES:
        tid = tech_id("air", a["key"])
        equip = a["equip"]
        if equip not in EQ:
            raise SystemExit(f"missing equipment {equip}")
        mods = frame_config(equip)
        arch = EQ[equip]["archetype"]
        cats = [a["mfr"]]
        arch_cat = ARCH_CAT.get(arch)
        if arch_cat:
            cats.append(arch_cat)
        cats.append("air_equipment")
        yy = cell(a["x"], a["year"], a.get("dy"))
        nxt = next((b for b in D.AIRFRAMES if b["prev"] == a["key"]), None)
        leads = tech_id("air", nxt["key"]) if nxt else None
        dep = resolve_prev("air", a["prev"])
        tooltip = (arch_cat + "_tt") if arch_cat else None
        out.append(tech_block(tid, a["year"], 1.05, a["x"], yy, [equip], mods, cats,
                              leads_to=leads, depends_on=dep, tooltips=(tooltip, a["mfr"] + "_tt"),
                              ai_archetype=arch,
                              ai_variant=equip[3:] if equip.startswith("ad_") else equip))

    # ---- engines ---------------------------------------------------------
    out.append("\t####################################################################")
    out.append("\t##  航空发动机")
    out.append("\t####################################################################")
    chains = {}
    for e in D.ENGINES:
        chains.setdefault(e["x"], []).append(e)
    for x in sorted(chains):
        for e in chains[x]:
            tid = tech_id("engine", e["key"])
            for m in e["modules"]:
                if m not in MODS:
                    raise SystemExit(f"missing module {m}")
            yy = cell(e["x"], e["year"])
            nxt = next((o for o in chains[x] if o["prev"] == e["key"]), None)
            leads = tech_id("engine", nxt["key"]) if nxt else None
            dep = resolve_prev("engine", e["prev"])
            out.append(tech_block(tid, e["year"], 1.0, e["x"], yy, None, e["modules"],
                                  ["air_equipment", "ad_air_component"],
                                  leads_to=leads, depends_on=dep, small=True))

    # ---- guns ------------------------------------------------------------
    out.append("\t####################################################################")
    out.append("\t##  航空枪炮")
    out.append("\t####################################################################")
    for g in D.GUNS:
        tid = tech_id("gun", g["key"])
        for m in g["modules"]:
            if m not in MODS:
                raise SystemExit(f"missing module {m}")
        yy = cell(g["x"], g["year"])
        nxt = next((o for o in D.GUNS if o["prev"] == g["key"]), None)
        leads = tech_id("gun", nxt["key"]) if nxt else None
        dep = resolve_prev("gun", g["prev"])
        out.append(tech_block(tid, g["year"], 0.75, g["x"], yy, None, g["modules"],
                              ["air_equipment", "ad_air_component"],
                              leads_to=leads, depends_on=dep, small=True))

    # ---- ordnance --------------------------------------------------------
    out.append("\t####################################################################")
    out.append("\t##  航空炸弹与火箭")
    out.append("\t####################################################################")
    for o in D.ORDNANCE:
        tid = tech_id("ord", o["key"])
        for m in o["modules"]:
            if m not in MODS:
                raise SystemExit(f"missing module {m}")
        yy = cell(o["x"], o["year"])
        nxt = next((q for q in D.ORDNANCE if q["prev"] == o["key"]), None)
        leads = tech_id("ord", nxt["key"]) if nxt else None
        dep = resolve_prev("ord", o["prev"])
        out.append(tech_block(tid, o["year"], 0.6, o["x"], yy, None, o["modules"],
                              ["air_equipment", "ad_air_component"],
                              leads_to=leads, depends_on=dep, small=True))

    out.append("}")
    path = os.path.join(TECH_DIR, "CHI_air.txt")
    os.makedirs(TECH_DIR, exist_ok=True)
    write_text(path, "\n".join(out) + "\n")
    log(f"technologies: {len(D.AIRFRAMES) + len(D.ENGINES) + len(D.GUNS) + len(D.ORDNANCE)} techs -> {path}")
    return used_cells


def write_text(path, text, bom=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = text.encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    with open(path, "wb") as f:
        f.write(data)


def emit_technology_tags():
    tag_or = "\n".join(f"\t\t\t\toriginal_tag = {t}" for t in CHINESE_TAGS)
    tag_or_not = "\n".join(f"\t\t\t\t\toriginal_tag = {t}" for t in CHINESE_TAGS)
    text = f"""# 中系飞机科技树 / Chinese Aircraft Tech Tree
# 中国（含中共及内战分裂政权）显示专属空军科技标签页，
# 同时把黑冰通用空军页对中国隐藏，避免出现两个空军页。
# 判定方式：{FLAG} 标志（on_startup 设置）或 original_tag，双重保险。
technology_folders = {{
	{FOLDER} = {{
		ledger = air
		available = {{
			OR = {{
				has_country_flag = {FLAG}
{tag_or}
			}}
		}}
	}}
	air_techs_folder = {{
		ledger = air
		available = {{
			NOT = {{
				OR = {{
					has_country_flag = GER_air
					has_country_flag = ITA_air
					has_country_flag = JAP_air
					has_country_flag = USA_air
					has_country_flag = ENG_air
					has_country_flag = FRA_air
					has_country_flag = SOV_air
					has_country_flag = {FLAG}
{tag_or_not}
				}}
			}}
		}}
	}}
}}
"""
    path = os.path.join(MOD, "common", "technology_tags", "zz_CHI_air_technology.txt")
    write_text(path, text)
    log("technology_tags ->", path)


def emit_on_actions():
    tag_or = "\n".join(f"\t\t\t\t\t\toriginal_tag = {t}" for t in CHINESE_TAGS)
    text = f"""# 中系飞机科技树 / Chinese Aircraft Tech Tree
# 开局给中国（含中共）挂上 {FLAG} 标志，科技树标签页据此显示。
on_actions = {{
	on_startup = {{
		effect = {{
			every_country = {{
				limit = {{
					OR = {{
{tag_or}
					}}
				}}
				set_country_flag = {FLAG}
				log = "{LOG_MARKER}: {FLAG} granted to [THIS.GetTag]"
			}}
		}}
	}}
}}
"""
    path = os.path.join(MOD, "common", "on_actions", "zz_CHI_air_startup.txt")
    write_text(path, text)
    log("on_actions ->", path)


def emit_scripted_triggers():
    tag_or = "\n".join(f"\t\t\toriginal_tag = {t}" for t in CHINESE_TAGS)
    text = f"""# 中系飞机科技树 / Chinese Aircraft Tech Tree
# 供其它模组、事件、AI 复用的触发器（AUTO-GENERATED）
scripted_triggers = {{
	# 这个国家是否算"中系"（含内战分裂政权，用 original_tag）
	CHI_is_chinese_country = {{
		OR = {{
{tag_or}
		}}
	}}

	# 这个国家是否拥有中国空军科技页
	CHI_has_chinese_air_tree = {{
		OR = {{
			has_country_flag = {FLAG}
			CHI_is_chinese_country = yes
		}}
	}}
}}
"""
    path = os.path.join(MOD, "common", "scripted_triggers", "zz_CHI_air_triggers.txt")
    write_text(path, text)
    log("scripted_triggers ->", path)


def emit_gfx():
    """Register one <techid>_medium icon per tech plus the tab sprite."""
    sprites = []
    missing = []
    for a in D.AIRFRAMES:
        tex = icon_for_equipment(a["equip"])
        if not tex:
            missing.append(a["equip"])
            tex = "gfx/interface/technologies/air/GENERIC/ALLIES_fighter_p40_warhawk_1.dds"
        sprites.append((tech_id("air", a["key"]), tex))
    for e in D.ENGINES:
        sprites.append((tech_id("engine", e["key"]), equipment_icon(e["modules"], GENERIC_ENGINE)))
    for g in D.GUNS:
        sprites.append((tech_id("gun", g["key"]), equipment_icon(g["modules"], GENERIC_CANNON)))
    for o in D.ORDNANCE:
        sprites.append((tech_id("ord", o["key"]), equipment_icon(o["modules"], GENERIC_BOMB)))
    if missing:
        log("WARN missing airframe icon:", ", ".join(missing))

    lines = ["spriteTypes = {", ""]
    lines.append("\t### 中国空军科技树标签页按钮（2 帧：常态 / 选中）")
    lines.append("\tspriteType = {")
    lines.append(f'\t\tname = "GFX_{FOLDER}_tab"')
    lines.append('\t\ttextureFile = "gfx/interface/techtree/techtree_china_air_tab.tga"')
    lines.append("\t\tnoOfFrames = 2")
    lines.append("\t}")
    lines.append("")
    lines.append("\t### 科技图标：直接引用原版 / 黑冰 / BIAD 已有的机种与配件图标")
    for tid, tex in sprites:
        lines.append("\tspriteType = {")
        lines.append(f'\t\tname = "GFX_{tid}_medium"')
        lines.append(f'\t\ttextureFile = "{tex}"')
        lines.append("\t}")
        lines.append("\tspriteType = {")
        lines.append(f'\t\tname = "GFX_{tid}"')
        lines.append(f'\t\ttextureFile = "{tex}"')
        lines.append("\t}")
    lines.append("}")
    path = os.path.join(MOD, "interface", "chi_air_technology.gfx")
    write_text(path, "\n".join(lines) + "\n")
    log(f"gfx: {len(sprites)} tech icons -> {path}")
    return sprites


# ==========================================================================
# GUI patch
# ==========================================================================
def find_block(text, anchor_regex, open_kind="containerWindowType"):
    """Find the { ... } block whose body contains anchor_regex; return (start, end)
    where start is the index of the opening keyword and end is index after '}'."""
    m = re.search(anchor_regex, text)
    if not m:
        return None
    # walk back to the nearest "containerWindowType = {" before anchor
    start = text.rfind(open_kind, 0, m.start())
    if start < 0:
        return None
    brace = text.index("{", start)
    depth = 1
    i = brace + 1
    while i < len(text) and depth:
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return (start, i)


def gui_folder_container(sprites):
    year_labels = []
    for year in range(YEAR_BASE, YEAR_BASE + 13):
        yv = (year - YEAR_BASE) * YEAR_STEP
        year_labels.append(
            f"""				instantTextBoxType = {{
					name = "china_air_year_{year}"
					position = {{ x = 1700 y = {140 + yv * SLOT} }}
					textureFile = ""
					font = "hoi_36header"
					borderSize = {{ x = 0 y = 0 }}
					text = "{year}"
					maxWidth = 220
					maxHeight = 140
					vertical_alignment = centre
					format = left
					orientation = "UPPER_LEFT"
				}}"""
        )
    grid = []
    for tid, _tex in sprites:
        grid.append(
            f"""				gridboxtype = {{
					name = "{tid}_tree"
					position = {{ x = 190 y = 172 }}
					slotsize = {{ width = 70 height = 70 }}
					format = "UP"
				}}"""
        )
    body = f"""
		containerWindowType = {{
			name = "{FOLDER}"
			position = {{ x=@TECH_X_OFFSET y=47 }}
			size = {{ width = 100%% height = 100%% }}
			margin = {{ top = 13 left = 13 bottom = 24 right = 25}}
			drag_scroll = {{ left middle }}
			verticalScrollbar = "right_vertical_slider"
			horizontalScrollbar = "bottom_horizontal_slider"
			smooth_scrolling = yes
			scroll_wheel_factor = @TECH_TABS_SCROLL_WHEEL_FACTOR

			background = {{
				name = "Background"
				quadTextureSprite = "GFX_tiled_window_2b_border"
			}}

			containerWindowType = {{
				name = "techtree_stripes"
				position = {{ x= 0 y= 0 }}
				size = {{
					width = {CANVAS_W} height = {CANVAS_H}
					min = {{ width = 100% height = 100% }}
				}}
				clipping = no

				background = {{
					name = "Background"
					quadTextureSprite = "GFX_techtree_stripes"
				}}

				iconType = {{
					name = "china_air_techtree_bg"
					spriteType = "GFX_air_techtree_bg"
					position = {{ x = 0 y = 0 }}
					allwaystransparent = yes
				}}

{chr(10).join(year_labels)}

{chr(10).join(grid)}
			}}
		}}
"""
    return body


def read_gui_lines(path):
    """Read a .gui preserving every line, decoding mixed UTF-8 / GBK comments
    line by line (some submods ship GBK comments)."""
    raw = open(path, "rb").read()
    out = []
    for chunk in raw.split(b"\n"):
        for enc in ("utf-8", "gb18030"):
            try:
                out.append(chunk.decode(enc))
                break
            except UnicodeDecodeError:
                continue
        else:
            out.append(chunk.decode("utf-8", "replace"))
    return out


def emit_gui(sprites, base_override=None, out_path=None):
    base = base_override or os.path.join(TANK, "interface", "countrytechtreeview.gui")
    base_name = "中国坦克科技子模"
    if base_override:
        base_name = "BlackICE Aircraft Designer（备用底稿）"
    if not os.path.isfile(base):
        base = os.path.join(BIAD, "interface", "countrytechtreeview.gui")
        base_name = "BlackICE Aircraft Designer"
    lines = read_gui_lines(base)
    text = "\n".join(lines)
    log(f"GUI base: {base_name} ({len(lines)} lines)")

    # 1) tab button: insert on its own line right before the closing brace of folder_tabs
    tabs = find_block(text, r'name = "folder_tabs"')
    if not tabs:
        raise SystemExit("folder_tabs container not found")
    close = tabs[1] - 1
    if text[close] != "}":
        raise SystemExit("could not locate folder_tabs closing brace")
    line_start = text.rfind("\n", 0, close) + 1
    button = (
        '\t\t\tbuttonType = {\n'
        '\t\t\t\tposition = { x=880 y = 0 }\n'
        f'\t\t\t\tname = "{FOLDER}_tab"\n'
        '\t\t\t\tquadTextureSprite = "GFX_chinaair_folder_tab"\n'
        '\t\t\t\tframe = 1\n'
        '\t\t\t\tclicksound = click_default\n'
        '\t\t\t}\n'
    )
    text = text[:line_start] + button + text[line_start:]

    # 2) folder container: insert on its own line right after the usair_folder block
    anchor = find_block(text, r'name = "usair_folder"')
    if not anchor:
        raise SystemExit("usair_folder container not found")
    insert_at = anchor[1]
    line_start = text.find("\n", insert_at)
    if line_start < 0:
        line_start = len(text)
    text = text[:line_start + 1] + gui_folder_container(sprites) + "\n" + text[line_start + 1:]

    path = out_path or os.path.join(MOD, "interface", "countrytechtreeview.gui")
    write_text(path, text)
    log("GUI ->", path)


# ==========================================================================
# localisation
# ==========================================================================
def loc_lines(lang):
    out = []
    for a in D.AIRFRAMES:
        tid = tech_id("air", a["key"])
        if lang == "english":
            out.append(f' {tid}:0 "{a["en"]}"')
            out.append(f' {tid}_desc:0 "{a["desc_en"]}"')
        else:
            out.append(f' {tid}:0 "{a["zh"]}"')
            out.append(f' {tid}_desc:0 "{a["desc_zh"]}"')
    for kind, table, key in (
        ("engine", D.ENGINES, "modules"),
        ("gun", D.GUNS, "modules"),
        ("ord", D.ORDNANCE, "modules"),
    ):
        for item in table:
            tid = tech_id(kind, item["key"])
            first = item[key][0]
            if first in EN:
                out.append(f' {tid}:0 "${first}$"')
            else:
                name = item["en"] if lang == "english" else item["zh"]
                out.append(f' {tid}:0 "{name}"')
            desc = item["desc_en"] if lang == "english" else item["desc_zh"]
            out.append(f' {tid}_desc:0 "{desc}"')
    if lang == "english":
        out.append(f' SLOT_{FOLDER}:0 "§YChinese Air Force§!\\n"')
        out.append(f' {FOLDER}:0 "Chinese Air Force"')
        out.append(f' {FOLDER}_tab:0 "Chinese Air Force"')
    else:
        out.append(f' SLOT_{FOLDER}:0 "§Y中国空军§!\\n"')
        out.append(f' {FOLDER}:0 "中国空军"')
        out.append(f' {FOLDER}_tab:0 "中国空军"')
    return out


def emit_loc():
    for lang, folder in (("english", "english"), ("simp_chinese", "simp_chinese")):
        lines = [f"l_{lang}:" if lang != "simp_chinese" else "l_simp_chinese:", ""]
        lines += loc_lines(lang)
        path = os.path.join(MOD, "localisation", folder, f"chi_air_l_{lang}.yml")
        write_text(path, "\n".join(lines) + "\n", bom=True)
        log("loc ->", path)


def emit_descriptor():
    deps = "\n".join(f'\t"{d}"' for d in DEPENDENCIES)
    text = f"""version="{MOD_VERSION}"
tags={{
	"Technologies"
	"Military"
	"Historical"
}}
name="{MOD_NAME_CN} {MOD_NAME_EN}"
picture="thumbnail.png"
dependencies={{
{deps}
}}
supported_version="{SUPPORTED_VERSION}"
"""
    path = os.path.join(MOD, "descriptor.mod")
    write_text(path, text)
    log("descriptor ->", path)


def main():
    used = None
    try:
        used = emit_technologies()
    finally:
        if used is not None:
            log(f"grid cells used: {len(used)}")
    emit_technology_tags()
    emit_on_actions()
    emit_scripted_triggers()
    sprites = emit_gfx()
    emit_gui(sprites)
    emit_loc()
    emit_descriptor()
    path = os.path.join(DATA, "build_report.txt")
    write_text(path, "\n".join(report) + "\n")
    log("report ->", path)


if __name__ == "__main__":
    main()
