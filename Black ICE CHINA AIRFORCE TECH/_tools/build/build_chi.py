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
    SLOT, YEAR_BASE, YEAR_STEP, DY_STEP, PIXEL_ORIGIN_X, PIXEL_ORIGIN_Y,
    CANVAS_W, CANVAS_H, COLUMNS, GRIDBOX_X, GRIDBOX_Y, LAYOUT_SHIFT_X, ITEM_POS_LARGE, ITEM_POS_SMALL,
    DAYS_LARGE_DX, DAYS_LARGE_DY, DAYS_SMALL_DX, DAYS_SMALL_DY, ARROW_LARGE_DX, ARROW_LARGE_DY, ARROW_SMALL_DX, ARROW_SMALL_DY,
    MOD_VERSION, MOD_NAME_CN, MOD_NAME_EN, SUPPORTED_VERSION, DEPENDENCIES,
    HIDE_GENERIC_AIR, AVAILABLE_BY_FLAG_ONLY,
    TIP_EVENT_ENABLED, TIP_EVENT_ID, TIP_EVENT_NAMESPACE, TIP_FLAG,
    TAB_TEXTURE, TAB_FRAMES, REQUEST_FOLDER, CANDIDATE_FLAG, REQUEST_GATE,
    TANK_FOLDER, TANK_FLAG, ARMOR_TT_FIX,
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
        return (year - YEAR_BASE) * YEAR_STEP + dy * DY_STEP

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
    """生成 technology_folders 覆盖。

    重点（0.3.0）：中系判定改用 original_tag，让「显示中国空军页 / 隐藏通用空军页」
    在**读档那一帧**就已经成立——BIAD 对德意日美英法苏就是这么做的（写在国家历史里）。
    之前用 on_startup 挂标志，科技视图在标志生效前就建好了，于是隐藏通用页会导致
    科研界面闪一下就关。
    """
    tags_or = "\n".join(f"\t\t\t\t\toriginal_tag = {t}" for t in CHINESE_TAGS)

    if REQUEST_GATE:
        gate = f"\t\t\thas_country_flag = {FLAG}"
        request_block = f"""
	{REQUEST_FOLDER} = {{
		ledger = air
		available = {{
			has_country_flag = {CANDIDATE_FLAG}
			NOT = {{ has_country_flag = {FLAG} }}
		}}
	}}"""
    else:
        gate = f"""\t\t\tOR = {{
\t\t\t\thas_country_flag = {FLAG}
{tags_or}
\t\t\t}}"""
        request_block = ""

    # 坦克子模文件夹：哪怕坦克子模没启用也注册一份（条件相同），
    # 这样 gui 里它的页签是「未解锁」而不是「文件夹不存在」，不会留下死页签。
    # 0.4.7 起改为「标志 或 四条条件」，满足条件即自动解锁（不再依赖请求面板点击）。
    tank_block = f"""
	{TANK_FOLDER} = {{
		ledger = army
		available = {{
			# 静态判定：装着坦克子模就一直可见。
			# 动态条件（工厂/国策/科技）会让文件夹可用性在游戏中途翻转，
			# 实测会直接把黑冰科研界面弄崩，所以不再用条件解锁。
			# 静态判定：original_tag 在读档那一刻就成立，不会中途翻转
			OR = {{
				original_tag = CHI
				original_tag = PRC
			}}
		}}
	}}"""

    hide_block = ""
    if HIDE_GENERIC_AIR:
        hide_block = f"""
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
{tags_or}
				}}
			}}
		}}
	}}"""

    import config as _cfg
    if getattr(_cfg, "GUI_MINIMAL", False):
        # 诊断模式：只保留坦克文件夹，不注册中国空军页（否则会 Window not found）
        text = f"""# 诊断模式：只注册坦克文件夹
technology_folders = {{
{tank_block}
}}
"""
        path = os.path.join(MOD, "common", "technology_tags", "zz_CHI_air_technology.txt")
        write_text(path, text)
        log("technology_tags (MINIMAL) ->", path)
        return

    text = f"""# 中系飞机科技树 / Chinese Aircraft Tech Tree
# REQUEST_GATE={REQUEST_GATE}，HIDE_GENERIC_AIR={HIDE_GENERIC_AIR}
# 中系判定用 original_tag，保证读档时状态一致（见函数注释）
technology_folders = {{
	{FOLDER} = {{
		ledger = air
		available = {{
{gate}
		}}
	}}{request_block}{hide_block}
}}
"""
    path = os.path.join(MOD, "common", "technology_tags", "zz_CHI_air_technology.txt")
    write_text(path, text)
    log("technology_tags ->", path, f"(hide_generic={HIDE_GENERIC_AIR}, tag_based=True)")


def emit_on_actions():
    tag_or = "\n".join(f"\t\t\t\t\t\toriginal_tag = {t}" for t in CHINESE_TAGS)
    text = f"""# 中系飞机科技树 / Chinese Aircraft Tech Tree
# 解锁不再由 on_startup 自动授予：玩家需在「+」请求页提交申请并满足条件，
# 由 common/scripted_guis/CHI_air_request.txt 授予 {FLAG}。
# 这里只留一条日志方便确认模组已加载。
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
				set_country_flag = CHI_armor
				log = "{LOG_MARKER} v{MOD_VERSION}: China air tree loaded for [THIS.GetTag]"
			}}
			# 一次性提示：装甲科技页首次打开可能缺图标/连线，需存档读档一次
			every_country = {{
				limit = {{
					is_player = yes
					NOT = {{ has_country_flag = CHI_armor_tip_shown }}
					OR = {{
						original_tag = CHI
						original_tag = PRC
					}}
				}}
				set_country_flag = CHI_armor_tip_shown
				news_event = {{ id = CHI_air_unlock.2 days = 1 }}
			}}
		}}
	}}
}}
"""
    path = os.path.join(MOD, "common", "on_actions", "zz_CHI_air_startup.txt")
    write_text(path, text)
    log("on_actions ->", path)


def emit_events():
    if not TIP_EVENT_ENABLED:
        return
    text = f"""# 中系飞机科技树 / Chinese Aircraft Tech Tree
# 「飞机科技研究权已获得」解锁事件（AUTO-GENERATED）
# 与坦克科技子模同款原因：黑冰科研界面会缓存布局，
# 首次打开新科技页时科技之间的连线/箭头可能不显示，存档再读档一次即可。
add_namespace = {TIP_EVENT_NAMESPACE}

country_event = {{
	id = {TIP_EVENT_ID}
	title = {TIP_EVENT_ID}.t
	desc = {TIP_EVENT_ID}.d
	is_triggered_only = yes
	option = {{
		name = {TIP_EVENT_ID}.a
	}}
}}

# 带图片的版本：走 news_event 窗口（黑冰的普通事件窗口没有可用的图片控件）
news_event = {{
	id = CHI_air_unlock.2
	title = CHI_air_unlock.2.t
	desc = CHI_air_unlock.2.d
	picture = GFX_chi_armor_tip
	is_triggered_only = yes
	fire_only_once = yes
	option = {{
		name = CHI_air_unlock.2.a
	}}
}}
"""
    path = os.path.join(MOD, "events", "zz_CHI_air_tip.txt")
    write_text(path, text)
    log("events ->", path)


def emit_request_gui():
    """「+」请求页的 scripted GUI：按钮点击后授予 CHI_air 并触发解锁事件。"""
    path = os.path.join(MOD, "common", "scripted_guis", "CHI_air_request.txt")
    if not REQUEST_GATE:
        # 关掉请求页时必须删除旧文件，否则它会引用不存在的窗口
        if os.path.isfile(path):
            os.remove(path)
            log("request gui -> removed (REQUEST_GATE=False)")
        return
    text = f"""# 中系飞机科技树 / Chinese Aircraft Tech Tree
# 「+」请求页交互（AUTO-GENERATED）
scripted_gui = {{
	CHI_air_request = {{
		context_type = player_context

		window_name = "{REQUEST_FOLDER}"

		effects = {{
			request_air_click = {{
				if = {{
					limit = {{ CHI_air_request_ready = yes }}
					set_country_flag = {FLAG}
					country_event = {{ id = {TIP_EVENT_ID} }}
				}}
			}}
		}}

		triggers = {{
			request_air_click_enabled = {{
				CHI_air_request_ready = yes
			}}
		}}
	}}
}}
"""
    write_text(path, text)
    log("request gui ->", path)


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

	# 天数(dx/dy)位置：用「有无解锁装备」区分大小格，与黑冰自己的判定一致。
	# 箭头(add_to_queue)无法用变量覆盖，只能靠 PIXEL_ORIGIN_X/Y 整体平移。
	CHI_air_time_estimate = {{
		if = {{
			limit = {{ check_variable = {{ global.tech_unlocks@var:v^num > 0 }} }}
			set_temp_variable = {{ dx = {{ value = global.tech_x@var:v  add = {DAYS_LARGE_DX} }} }}
			set_temp_variable = {{ dy = {{ value = global.tech_y@var:v  add = {DAYS_LARGE_DY} }} }}
		}}
		else = {{
			set_temp_variable = {{ dx = {{ value = global.tech_x@var:v  add = {DAYS_SMALL_DX} }} }}
			set_temp_variable = {{ dy = {{ value = global.tech_y@var:v  add = {DAYS_SMALL_DY} }} }}
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

    # 页签贴图：使用自制 DDS（gfx/interface/techtree/techtree_chiair_tab.dds），缺文件直接报错
    if not os.path.isfile(os.path.join(MOD, TAB_TEXTURE)):
        raise SystemExit(
            f"缺少页签贴图 {TAB_TEXTURE}。请把自制 DDS 放到 gfx/interface/techtree/ 下，"
            "或修改 config.TAB_TEXTURE。"
        )
    log("tab icon ->", TAB_TEXTURE)
    lines.append("\t### 中国空军科技树标签页按钮（2 帧：常态 / 选中）")
    lines.append("\tspriteType = {")
    lines.append(f'\t\tname = "GFX_{FOLDER}_tab"')
    lines.append(f'\t\ttextureFile = "{TAB_TEXTURE}"')
    lines.append(f"\t\tnoOfFrames = {TAB_FRAMES}")
    lines.append("\t}")

    # 本文件夹的小格条目背景：引擎按 GFX_technology_<folder>_small_*_item_bg 取图，
    # 不注册就会出现"小格科技没有底框/图标"（条目像消失了一样）。
    lines.append("\t### 小格条目背景（按文件夹命名）")
    for state in ("unavailable", "available", "researched"):
        lines.append("\tspriteType = {")
        lines.append(f'\t\tname = "GFX_technology_{FOLDER}_small_{state}_item_bg"')
        lines.append(f'\t\ttextureFile = "gfx/interface/techtree/tech_trm_{state}_item_bg.dds"')
        lines.append("\t}")
    lines.append("\tframeAnimatedSpriteType = {")
    lines.append(f'\t\tname = "GFX_technology_{FOLDER}_small_currently_researching_item_bg"')
    lines.append('\t\ttexturefile = "gfx/interface/techtree/tech_trm_researching_anim_strip.dds"')
    lines.append("\t\tnoOfFrames = 9")
    lines.append('\t\tloadType = "INGAME"')
    lines.append("\t\ttransparencecheck = yes")
    lines.append("\t\tanimation_rate_fps = 15")
    lines.append("\t\tlooping = yes")
    lines.append("\t\tplay_on_show = yes")
    lines.append("\t\tpause_on_loop = 0.0")
    lines.append("\t}")
    for state in ("unavailable", "available"):
        lines.append("\tspriteType = {")
        lines.append(f'\t\tname = "GFX_technology_{FOLDER}_special_project_small_{state}_item_bg"')
        lines.append(f'\t\ttextureFile = "gfx/interface/techtree/technology_special_project_small_{state}_item_bg.dds"')
        lines.append("\t}")
    lines.append("")

    # 事件配图（坦克科技树使用提示）
    lines.append("\t### 事件配图")
    lines.append("\tspriteType = {")
    lines.append('\t\tname = "GFX_chi_armor_tip"')
    lines.append('\t\ttexturefile = "gfx/event_pictures/chi_armor_tip.dds"')
    lines.append("\t}")
    lines.append("")
    # 不注册 GFX_chi_tank_folder_tab：该 sprite 由坦克子模提供。
    # 我们重复定义同名 sprite 可能与坦克子模的 gfx 冲突（实测坦克页图标会消失），故移除。
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


def extract_container(text, name):
    """Return the whole `containerWindowType = { ... }` block whose name is `name`."""
    marker = f'name = "{name}"'
    i = text.find(marker)
    if i < 0:
        raise SystemExit(f"container '{name}' not found in source GUI")
    start = text.rfind("containerWindowType", 0, i)
    brace = text.index("{", start)
    depth = 1
    j = brace + 1
    while j < len(text) and depth:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
        j += 1
    return text[start:j]


COLUMN_HEADERS = [
    # (列 key, 中文, 英文)
    ("engine_usa",       "美制发动机",        "US inline engines"),
    ("engine_usa_multi", "美制多发/喷气",     "US multi & jet"),
    ("engine_sov",       "苏制单发",          "Soviet inline"),
    ("engine_sov_multi", "苏制多发/喷气",     "Soviet multi & jet"),
    ("engine_jap",       "日制发动机",        "Japanese engines"),
    ("engine_other",     "德英发动机",        "German & British"),
    ("gun",              "航空枪炮",          "Guns"),
    ("ordnance",         "航空炸弹",          "Bombs"),
    ("ordnance_2",       "火箭/特种炸弹",     "Rockets"),
    ("ftr",              "战斗机",            "Fighters"),
    ("hvy_ftr",          "重型战斗机",        "Heavy fighters"),
    ("cv_ftr",           "舰载战斗机",        "Carrier fighters"),
    ("cas",              "近距支援机",        "Close support"),
    ("l_bomber",         "轻型轰炸机",        "Light bombers"),
    ("tac_bomber",       "中型轰炸机",        "Medium bombers"),
    ("strat_bomber",     "重型轰炸机",        "Heavy bombers"),
    ("fly_bts",          "水上飞机",          "Flying boats"),
    ("recon",            "侦察机",            "Reconnaissance"),
    ("trpt",             "运输机",            "Transports"),
]


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
    header_labels = []
    SMALL_COLS = {"engine_usa", "engine_usa_multi", "engine_sov", "engine_sov_multi",
                  "engine_jap", "engine_other", "gun", "ordnance", "ordnance_2"}
    for key, zh, _en in COLUMN_HEADERS:
        # 标题中心对齐该列第一个图标的中心：
        # 小格（72×72）中心在锚点左侧约 36px，大格（203×84）约 101px
        hx = 190 + LAYOUT_SHIFT_X + 35 + COLUMNS[key] * SLOT - 120
        header_labels.append(
            f"""				instantTextBoxType = {{
					name = "china_air_col_{key}"
					position = {{ x = {hx} y = 55 }}
					textureFile = ""
					font = "hoi_18mbs"
					borderSize = {{ x = 0 y = 2 }}
					text = "CHI_air_col_{key}"
					maxWidth = 240
					maxHeight = 40
					format = centre
					orientation = "UPPER_LEFT"
				}}"""
        )

    grid = []
    # 小格科技（发动机/枪炮/挂载）需要额外的 <tech>_small_tree 格子，
    # 引擎才会用 72×72 的 small_item 模板渲染（与坦克子模的弹药科技一致）。
    small_tids = {tech_id("engine", t["key"]) for t in D.ENGINES}
    small_tids |= {tech_id("gun", t["key"]) for t in D.GUNS}
    small_tids |= {tech_id("ord", t["key"]) for t in D.ORDNANCE}
    for tid, _tex in sprites:
        # 格子名的后缀决定用哪套条目模板：_small_tree → 72×72 小格，_tree → 203×84 大格。
        # 黑冰自己的小格科技（如 tech_trm_ammo_chi_apcr）就只有一个 <tech>_small_tree。
        grid_name = f"{tid}_tree"
        slot_w, slot_h = (70, 70)
        grid.append(
            f"""			gridboxtype = {{
				name = "{grid_name}"
				position = {{ x = {GRIDBOX_X} y = {GRIDBOX_Y} }}
				slotsize = {{ width = {slot_w} height = {slot_h} }}
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
{chr(10).join(header_labels)}
			}}

			# gridbox 必须是 folder 容器的直接子节点（与 BIAD 国家空军树一致），
			# 放进 techtree_stripes 里引擎会找不到，报 "Found no grid box for tech"。
{chr(10).join(grid)}
		}}
"""
    return body


def gui_request_container():
    """「+」请求页：解锁前取代正片页，里面只有一个申请按钮。"""
    return f"""
		containerWindowType = {{
			name = "{REQUEST_FOLDER}"
			position = {{ x=@TECH_X_OFFSET y=47 }}
			size = {{ width = 100%% height = 100%% }}
			margin = {{ top = 13 left = 13 bottom = 24 right = 25}}

			background = {{
				name = "Background"
				quadTextureSprite = "GFX_tiled_window_2b_border"
			}}

			containerWindowType = {{
				name = "techtree_stripes"
				position = {{ x= 0 y= 0 }}
				size = {{ width = 1400 height = 900 min = {{ width = 100% height = 100% }} }}
				clipping = no

				background = {{
					name = "Background"
					quadTextureSprite = "GFX_techtree_stripes"
				}}

				instantTextBoxType = {{
					name = "request_title"
					position = {{ x = 300 y = 180 }}
					font = "hoi_36header"
					text = "CHI_air_request_title"
					maxWidth = 800
					maxHeight = 60
					format = left
				}}

				instantTextBoxType = {{
					name = "request_desc"
					position = {{ x = 300 y = 260 }}
					font = "hoi_16mbs"
					text = "CHI_air_request_desc"
					maxWidth = 820
					maxHeight = 220
					format = left
				}}

				buttonType = {{
					name = "request_air"
					position = {{ x = 300 y = 520 }}
					spriteType = "GFX_button_150x34"
					buttonfont = "hoi_18mbs"
					buttontext = "CHI_air_request_button"
					pdx_tooltip = "CHI_air_request_tooltip"
					clicksound = click_default
				}}
			}}
		}}
"""


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


def shift_folder_tabs(text):
    """不动页签位置。

    0.6.2 起开局就给中国挂 CHI_armor，坦克子模自己的 BI_research_tabs 覆盖会把
    「请求装甲 +」对 CHI 隐藏，所以 340 那一格空出来给坦克页签，不需要再挤别的页签。
    """
    return text


def emit_gui(sprites, base_override=None, out_path=None):
    base = base_override or os.path.join(TANK, "interface", "countrytechtreeview.gui")
    base_name = "中国坦克科技子模"
    if base_override:
        base_name = "BlackICE Aircraft Designer（备用底稿）"
    if not os.path.isfile(base):
        base = os.path.join(BIAD, "interface", "countrytechtreeview.gui")
        base_name = "BlackICE Aircraft Designer"
    lines = read_gui_lines(base)
    import config as _cfg
    if getattr(_cfg, "GUI_MINIMAL", False):
        # 诊断模式：原样输出坦克子模的 gui（不插入我们的页签/文件夹/模板）
        text = "\n".join(lines)
        path = out_path or os.path.join(MOD, "interface", "countrytechtreeview.gui")
        write_text(path, text)
        log("GUI (MINIMAL, no insertions) ->", path)
        return
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
    if REQUEST_GATE:
        button += (
            '\t\t\tbuttonType = {\n'
            '\t\t\t\tposition = { x=880 y = 0 }\n'
            f'\t\t\t\tname = "{REQUEST_FOLDER}_tab"\n'
            '\t\t\t\tquadTextureSprite = "GFX_techtree_tabs"\n'
            '\t\t\t\tframe = 2\n'
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
    extra = "\n" + gui_request_container() if REQUEST_GATE else ""
    text = (
        text[:line_start + 1]
        + gui_folder_container(sprites)
        + extra
        + "\n"
        + text[line_start + 1:]
    )

    # 3) per-folder tech item templates.
    # 引擎按 "techtree_<folder>_item" / "techtree_<folder>_small_item" 取模板；
    # 缺了会报 "Undefined GUI_TYPE ... Failed to create containerWindowType"，
    # 科技页表现为闪烁一下就打不开。模板是 guiTypes 下的顶层 containerWindowType。
    item_src = os.path.join(BIAD, "interface", "countrytechtreeview.gui")
    item_text = "\n".join(read_gui_lines(item_src))
    blocks = []
    for suffix in ("_item", "_small_item"):
        name = f"techtree_luftwaffe_folder{suffix}"
        blocks.append(extract_container(item_text, name))
    templates = "\n\n".join(
        b.replace("techtree_luftwaffe_folder", f"techtree_{FOLDER}") for b in blocks
    )
    # 条目模板的位置偏移（大格/小格分开调）
    lx, ly = ITEM_POS_LARGE
    sx, sy = ITEM_POS_SMALL
    templates = templates.replace("position = { x=-66 y=-7 }", f"position = {{ x={lx} y={ly} }}", 1)
    templates = templates.replace("position = { x=0 y=0 }", f"position = {{ x={sx} y={sy} }}", 1)
    # insert before the final closing brace (end of guiTypes)
    last = text.rstrip().rfind("}")
    text = text[:last] + templates + "\n" + text[last:]

    text = shift_folder_tabs(text)
    path = out_path or os.path.join(MOD, "interface", "countrytechtreeview.gui")
    write_text(path, text)
    log("GUI ->", path, f"(+2 item templates: techtree_{FOLDER}_item / _small_item)")


# ==========================================================================
# localisation
# ==========================================================================
def loc_lines(lang):
    out = []
    # 科研面板顶端的列标题
    for key, zh, en in COLUMN_HEADERS:
        text = en if lang == "english" else zh
        out.append(f' CHI_air_col_{key}:0 "{text}"')
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
    if TIP_EVENT_ENABLED:
        if lang == "english":
            out.append(f' {TIP_EVENT_ID}.t:0 "Aircraft Research Rights Acquired"')
            out.append(
                f' {TIP_EVENT_ID}.d:0 "The Republic of China has secured its own aircraft research '
                f'programme. A new \\"Chinese Air Force\\" page is now available in the research screen.\\n\\n'
                f'Because the Black ICE research interface caches its layout, the connection lines '
                f'(arrows) between technologies may not appear the first time you open it. Please save '
                f'the game and load it again once - the lines and icon positions will then display correctly."'
            )
            out.append(f' {TIP_EVENT_ID}.a:0 "Understood."')
            out.append(' CHI_air_request_title:0 "Request Aircraft Research Assistance"')
            out.append(
                ' CHI_air_request_desc:0 "Our air force has no independent research programme yet. '
                'If we can show a real industrial base - or a sufficiently determined government - '
                'our allies and advisors will help us set one up.\\n\\n'
                'Requirements (any one):\\n'
                '  - at least 2 aircraft assembly plants, or\\n'
                '  - at least 2 engine assembly plants, or\\n'
                '  - the ruling party follows an absolutist / despotic ideology."'
            )
            out.append(' CHI_air_request_button:0 "Submit the request"')
            out.append(
                ' CHI_air_request_tooltip:0 "Once the requirements are met, this unlocks the '
                'Chinese Air Force tech tree. Remember to save and reload once so the tech tree '
                'draws its connection lines."'
            )
            out.append(f' SLOT_{REQUEST_FOLDER}:0 "§YRequest Air Research§!\\n"')
        else:
            out.append(f' {TIP_EVENT_ID}.t:0 "飞机科技研究权已获得"')
            out.append(
                f' {TIP_EVENT_ID}.d:0 "中华民国已经获得独立的航空科技研究权，科研界面中新增了'
                f'「中国空军」科技页。\\n\\n由于黑冰的科研界面会缓存布局，第一次打开该页时，'
                f'科技之间的连线（箭头）可能不显示。请先保存游戏并重新载入一次，连线与图标位置'
                f'就会恢复正常。"'
            )
            out.append(f' {TIP_EVENT_ID}.a:0 "明白了。"')
            out.append(' CHI_air_request_title:0 "申请航空科技研究权"')
            out.append(
                ' CHI_air_request_desc:0 "我们的空军还没有独立的研究体系。只要能证明我们拥有'
                '像样的工业基础——或者足够坚定的政府——盟国与顾问就会帮我们建立起来。\\n\\n'
                '满足以下任意一项即可申请：\\n'
                '  · 至少 2 座飞机装配厂，或\\n'
                '  · 至少 2 座发动机装配厂，或\\n'
                '  · 当前执政党奉行专制主义 / 专制统治意识形态。"'
            )
            out.append(' CHI_air_request_button:0 "提交申请"')
            out.append(
                ' CHI_air_request_tooltip:0 "满足条件后提交，即可解锁中国空军科技树。'
                '解锁后记得先存档再读档一次，科技连线才会正常绘制。"'
            )
            out.append(f' SLOT_{REQUEST_FOLDER}:0 "§Y申请航空科技研究权§!\\n"')
    out.append(
        ' CHI_ARMOR_REQ_TT:0 "需要其中之一：\\n'
        '· 坦克装配厂 ≥2 且发动机装配厂 ≥2\\n'
        '· 已完成「早期拖拉机」研究\\n'
        '· 已完成国策「中国装甲部队」\\n'
        '· 已完成国策「聘请苏联设计商」"'
        if lang == "simp_chinese"
        else ' CHI_ARMOR_REQ_TT:0 "Requires any one of:\\n'
        '· at least 2 tank assembly plants AND at least 2 engine assembly plants\\n'
        '· researched Early Tractors\\n'
        '· completed focus Chinese Armoured Forces\\n'
        '· completed focus Hire Soviet Designers"'
    )
    if lang == "simp_chinese":
        out.append(' CHI_armor_unlock.1.t:0 "中国坦克科技树使用提示"')
        out.append(
            ' CHI_armor_unlock.1.d:0 "£chi_armor_tip\\n\\n「中国空军」与「中国坦克」科技页已经可用。'
            '\\n\\n由于黑冰的科研界面会缓存布局，第一次打开这些科技页时，'
            '图标、名字与科技之间的连线可能不显示。请先保存游戏并重新载入一次，之后就会恢复正常。"'
        )
        out.append(' CHI_armor_unlock.1.a:0 "明白了。"')
        out.append(' CHI_air_unlock.2.t:0 "中国坦克科技树使用提示"')
        out.append(
            ' CHI_air_unlock.2.d:0 "「中国空军」与「中国坦克」科技页已经可用。'
            '\\n\\n由于黑冰的科研界面会缓存布局，第一次打开这些科技页时，'
            '图标、名字与科技之间的连线可能不显示。请先保存游戏并重新载入一次，之后就会恢复正常。"'
        )
        out.append(' CHI_air_unlock.2.a:0 "明白了。"')
    else:
        out.append(' CHI_armor_unlock.1.t:0 "Chinese Armour Tech Tree - Usage Notes"')
        out.append(
            ' CHI_armor_unlock.1.d:0 "£chi_armor_tip\\n\\nThe \\"Chinese Air Force\\" and \\"Chinese Armour\\" technology '
            'pages are available.\\n\\nBecause the Black ICE research interface caches its layout, '
            'the first time you open them the icons, names and connection lines may be missing. '
            'Please save the game and load it again once; after that they display correctly."'
        )
        out.append(' CHI_armor_unlock.1.a:0 "Understood."')
        out.append(' CHI_air_unlock.2.t:0 "Chinese Armour Tech Tree - Usage Notes"')
        out.append(
            ' CHI_air_unlock.2.d:0 "The \"Chinese Air Force\" and \"Chinese Armour\" technology '
            'pages are available.\\n\\nBecause the Black ICE research interface caches its layout, '
            'the first time you open them the icons, names and connection lines may be missing. '
            'Please save the game and load it again once; after that they display correctly."'
        )
        out.append(' CHI_air_unlock.2.a:0 "Understood."')
        out.append(' CHI_air_unlock.2.t:0 "Chinese Armour Tech Tree - Usage Notes"') if False else None
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


def emit_armor_tt_fix():
    """（已停用）曾用于覆盖 BI 的 BI_request_armor_tab。

    黑冰"请求装甲"面板里那面本国旗其实是页签按钮，点击路径在不同版本里不稳定，
    直接改面板风险太高。现在改为「文件夹可用性 OR 四条条件」自动解锁，
    不再需要点击任何旗帜；这里保留函数只负责清理旧文件。
    """
    path = os.path.join(MOD, "common", "scripted_guis", "zz_CHI_air_armor_request.txt")
    if os.path.isfile(path):
        os.remove(path)
        log("armor panel patch -> removed (auto-unlock mode)")
    return


def _emit_armor_tt_fix_unused():
    """覆盖 BI 的 BI_request_armor_tab：把 CHI 专属条件包进 hidden_trigger。

    黑冰那句 `ROOT = { tag = CHI has_completed_focus = KMT_request_american_tanks }`
    会出现在所有捐赠国图标的提示文字里（REQUEST_ARMOR_TOOLTIP = [!flag_click_enabled]），
    看起来像"每个国家都要求中国完成那个国策"。包一层 hidden_trigger 后逻辑不变、提示不再显示。
    """
    path = os.path.join(MOD, "common", "scripted_guis", "zz_CHI_air_armor_request.txt")
    if not ARMOR_TT_FIX:
        if os.path.isfile(path):
            os.remove(path)
            log("armor tt fix -> removed (ARMOR_TT_FIX=False)")
        return

    src = os.path.join(BI, "common", "scripted_guis", "BI_research_tabs_scripted_gui.txt")
    with open(src, encoding="utf-8-sig", errors="replace") as fh:
        text = fh.read()
    marker = "BI_request_armor_tab = {"
    i = text.find(marker)
    if i < 0:
        raise SystemExit("BI_request_armor_tab not found in BI sources")
    brace = text.index("{", i)
    depth, j = 1, brace + 1
    while j < len(text) and depth:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
        j += 1
    block = text[i:j]

    import re as _re
    pattern = _re.compile(
        r"NOT\s*=\s*\{\s*AND\s*=\s*\{\s*tag\s*=\s*USA\s*"
        r"ROOT\s*=\s*\{\s*tag\s*=\s*CHI\s*has_completed_focus\s*=\s*KMT_request_american_tanks\s*\}\s*\}\s*\}",
        _re.S,
    )
    m = pattern.search(block)
    if not m:
        log("WARN armor tt: CHI clause not found, 覆盖文件仍会生成但不改动")
        fixed = block
    else:
        fixed = block[:m.start()] + "NOT = {\n\t\t\t\t\t\t\t\t\thidden_trigger = {\n\t\t\t\t\t\t\t\t\t\tAND = {\n\t\t\t\t\t\t\t\t\t\t\ttag = USA\n\t\t\t\t\t\t\t\t\t\t\tROOT = { tag = CHI has_completed_focus = KMT_request_american_tanks }\n\t\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t}" + block[m.end():]
        log("armor tt fix: CHI clause wrapped in hidden_trigger")

    # ---- 中国自己那面旗（entry 版）：只看四条解锁条件；别国旗仍走黑冰原版 ----
    def _inner2(text, key):
        k = text.find(key)
        b = text.index("{", k)
        d, q = 1, b + 1
        while q < len(text) and d:
            if text[q] == "{":
                d += 1
            elif text[q] == "}":
                d -= 1
            q += 1
        return b + 1, q - 1

    t0, t1 = _inner2(fixed, "flag_click_enabled = {")
    original_enabled = fixed[t0:t1]
    chi_enabled = (
        "\n\t\t\t\tif = {\n"
        "\t\t\t\t\tlimit = {\n"
        "\t\t\t\t\t\tROOT = { tag = CHI }\n"
        "\t\t\t\t\t\ttag = CHI\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t\tROOT = {\n"
        "\t\t\t\t\t\tcustom_trigger_tooltip = {\n"
        "\t\t\t\t\t\t\ttooltip = CHI_ARMOR_REQ_TT\n"
        "\t\t\t\t\t\t\tOR = {\n"
        "\t\t\t\t\t\t\t\tAND = { tank_assembly > 1 engine_assembly > 1 }\n"
        "\t\t\t\t\t\t\t\thas_tech = early_tractors\n"
        "\t\t\t\t\t\t\t\thas_completed_focus = KMT_chinese_panzers\n"
        "\t\t\t\t\t\t\t\thas_completed_focus = KMT_hire_soviet_designer\n"
        "\t\t\t\t\t\t\t}\n"
        "\t\t\t\t\t\t}\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t}\n"
        "\t\t\t\telse = {\n"
        + original_enabled +
        "\n\t\t\t\t}\n\t\t\t"
    )
    fixed = fixed[:t0] + chi_enabled + fixed[t1:]
    log("armor tt fix: CHI self entry uses 4 conditions, others BI original")

    # ---- 中国点自己的旗帜（=请求页签图标）时直接授予 CHI_armor ----
    # 这一格不是捐赠国条目，而是 request_armor 按钮（显示本国国旗），
    # 它的点击效果是 request_armor_click，不是 flag_click。所以在这里分流。
    def _inner(text, key):
        k = text.find(key)
        b = text.index("{", k)
        d, q = 1, b + 1
        while q < len(text) and d:
            if text[q] == "{":
                d += 1
            elif text[q] == "}":
                d -= 1
            q += 1
        return b + 1, q - 1

    s0, e0 = _inner(fixed, "request_armor_click = {")
    original_click = fixed[s0:e0]
    chi_click = (
        "\n\t\t\t\tif = {\n"
        "\t\t\t\t\tlimit = {\n"
        "\t\t\t\t\t\tROOT = {\n"
        "\t\t\t\t\t\t\ttag = CHI\n"
        "\t\t\t\t\t\t\tOR = {\n"
        "\t\t\t\t\t\t\t\tAND = { tank_assembly > 1 engine_assembly > 1 }\n"
        "\t\t\t\t\t\t\t\thas_tech = early_tractors\n"
        "\t\t\t\t\t\t\t\thas_completed_focus = KMT_chinese_panzers\n"
        "\t\t\t\t\t\t\t\thas_completed_focus = KMT_hire_soviet_designer\n"
        "\t\t\t\t\t\t\t}\n"
        "\t\t\t\t\t\t}\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t\tROOT = {\n"
        "\t\t\t\t\t\tset_country_flag = CHI_armor\n"
        "\t\t\t\t\t\tlog = \"CHI_ARMOR_TRIGGERED by [THIS.GetTag]\"\n"
        "\t\t\t\t\t\tcountry_event = CHI_armor_unlock.1\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t}\n"
        "\t\t\t\telse = {\n"
        + original_click +
        "\n\t\t\t\t}\n\t\t\t"
    )
    fixed = fixed[:s0] + chi_click + fixed[e0:]
    log("armor tt fix: CHI tab click grants CHI_armor (4 conditions)")

    # 若“旗帜”其实是 donor 条目（不同 BI 版本布局不同），flag_click 也分流一次：
    s1, e1 = _inner(fixed, "flag_click = {")
    original_flag_click = fixed[s1:e1]
    chi_flag_click = (
        "\n\t\t\t\tif = {\n"
        "\t\t\t\t\tlimit = {\n"
        "\t\t\t\t\t\tROOT = {\n"
        "\t\t\t\t\t\t\ttag = CHI\n"
        "\t\t\t\t\t\t\tOR = {\n"
        "\t\t\t\t\t\t\t\tAND = { tank_assembly > 1 engine_assembly > 1 }\n"
        "\t\t\t\t\t\t\t\thas_tech = early_tractors\n"
        "\t\t\t\t\t\t\t\thas_completed_focus = KMT_chinese_panzers\n"
        "\t\t\t\t\t\t\t\thas_completed_focus = KMT_hire_soviet_designer\n"
        "\t\t\t\t\t\t\t}\n"
        "\t\t\t\t\t\t}\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t\tROOT = {\n"
        "\t\t\t\t\t\tset_country_flag = CHI_armor\n"
        "\t\t\t\t\t\tlog = \"CHI_ARMOR_TRIGGERED via flag_click by [THIS.GetTag]\"\n"
        "\t\t\t\t\t\tcountry_event = CHI_armor_unlock.1\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t}\n"
        "\t\t\t\telse = {\n"
        + original_flag_click +
        "\n\t\t\t\t}\n\t\t\t"
    )
    fixed = fixed[:s1] + chi_flag_click + fixed[e1:]
    log("armor tt fix: CHI flag click also grants CHI_armor")

    out = "scripted_gui = {\n" + fixed + "\n}\n"
    write_text(path, out)
    log("armor tt fix ->", path)


def emit_armor_tab_hide():
    """（停用）曾用于对中系隐藏「请求装甲 +」。
    隐藏后 + 的容器仍会挡住 340 格的坦克页签，实测反而更糟，改回移动页签的方案。
    """
    path = os.path.join(MOD, "common", "scripted_guis", "zz_CHI_air_armor_hide.txt")
    if os.path.isfile(path):
        os.remove(path)
        log("armor tab hide -> removed")
    return


def _emit_armor_tab_hide_unused():
    """对中系隐藏黑冰的「请求外国装甲科技」+ 页签。

    该 + 按钮固定在 (345,6)、宽约 182，正好压住 340 那一格的页签。
    中国已经有自己的坦克页（静态可见），这个请求入口是多余的，隐藏它让坦克页签露出来。
    """
    path = os.path.join(MOD, "common", "scripted_guis", "zz_CHI_air_armor_hide.txt")
    src = os.path.join(BI, "common", "scripted_guis", "BI_research_tabs_scripted_gui.txt")
    with open(src, encoding="utf-8-sig", errors="replace") as fh:
        text = fh.read()
    marker = "BI_request_armor_tab = {"
    i = text.find(marker)
    if i < 0:
        raise SystemExit("BI_request_armor_tab not found")
    brace = text.index("{", i)
    depth, j = 1, brace + 1
    while j < len(text) and depth:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
        j += 1
    block = text[i:j]

    import re as _re
    # 在 visible 的 NOT OR 列表里加 tag = CHI，令中国看不到这个页签
    block2, n = _re.subn(
        r"(visible\s*=\s*\{\s*NOT\s*=\s*\{)",
        r"\1\n\t\t\t\ttag = CHI",
        block,
        count=1,
    )
    if n == 0:
        log("WARN armor tab hide: visible block not matched")
    write_text(path, "scripted_gui = {\n" + block2 + "\n}\n")
    log("armor tab hide ->", path)


def emit_legacy_stubs():
    """把历史遗留的覆盖文件全部改写成空 scripted_gui。

    压缩包解压不会删除已存在的文件：老版本留下的 zz_CHI_air_armor_request.txt /
    zz_CHI_air_armor_hide.txt / CHI_air_request.txt 会一直留在工坊副本里，
    引用已不存在的窗口或旧逻辑，导致科研界面打不开。这里每次构建都用空块覆盖它们。
    """
    for name in ("CHI_air_request.txt", "zz_CHI_air_armor_request.txt", "zz_CHI_air_armor_hide.txt"):
        path = os.path.join(MOD, "common", "scripted_guis", name)
        write_text(path, "# 已停用（占位文件，防止旧副本残留生效）\nscripted_gui = {\n}\n")
        log("legacy stub ->", name)


def emit_armor_unlock_event():
    text = """# 中系飞机科技树 / Chinese Aircraft Tech Tree
# 中国点击「请求外国装甲科技」后获得装甲研究权的通知（AUTO-GENERATED）
add_namespace = CHI_armor_unlock

country_event = {
	id = CHI_armor_unlock.1
	title = CHI_armor_unlock.1.t
	desc = CHI_armor_unlock.1.d
	is_triggered_only = yes
	option = {
		name = CHI_armor_unlock.1.a
	}
}
"""
    path = os.path.join(MOD, "events", "zz_CHI_armor_unlock.txt")
    write_text(path, text)
    log("armor unlock event ->", path)


def emit_build_info():
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"""中系飞机科技树 / Chinese Aircraft Tech Tree — build info
version : {MOD_VERSION}
built   : {now}
folder  : {FOLDER}
techs   : {len(D.AIRFRAMES) + len(D.ENGINES) + len(D.GUNS) + len(D.ORDNANCE)}
          aircraft {len(D.AIRFRAMES)} / engines {len(D.ENGINES)} / guns {len(D.GUNS)} / ordnance {len(D.ORDNANCE)}
gui     : countrytechtreeview.gui 已插入 {FOLDER} 容器 + 76 个直接子级 gridbox

提示：如果游戏加载的副本里这个文件的版本/时间与工作区不一致，
说明加载的是旧副本（例如工坊目录 3844078670），需要更新发布或覆盖文件。
"""
    path = os.path.join(MOD, "build_info.txt")
    write_text(path, text)
    log("build_info ->", path, f"(v{MOD_VERSION})")


def main():
    used = None
    try:
        used = emit_technologies()
    finally:
        if used is not None:
            log(f"grid cells used: {len(used)}")
    emit_technology_tags()
    emit_on_actions()
    emit_events()
    emit_request_gui()
    emit_armor_tt_fix()
    emit_armor_unlock_event()
    emit_legacy_stubs()
    emit_scripted_triggers()
    sprites = emit_gfx()
    emit_gui(sprites)
    emit_loc()
    emit_descriptor()
    emit_build_info()
    path = os.path.join(DATA, "build_report.txt")
    write_text(path, "\n".join(report) + "\n")
    log("report ->", path)


if __name__ == "__main__":
    main()
