# -*- coding: utf-8 -*-
"""Static validation for the Chinese aircraft tech tree submod.

Checks structure, references, icons, localisation and GUI wiring, using the
same parser used to mine the parent mods.
"""
import os
import re
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'build'))
import cw_parse as C
try:
    from config import HIDE_GENERIC_AIR, REQUEST_GATE
except Exception:
    HIDE_GENERIC_AIR = True
    REQUEST_GATE = False

MOD = r"D:\Steam\steamapps\workshop\content\394360\中系飞机科技树"
BIAD = r"D:\Steam\steamapps\workshop\content\394360\3808452657"
TANK = r"D:\Steam\steamapps\workshop\content\394360\3463196432"
BI = r"D:\Steam\steamapps\workshop\content\394360\1851181613"
VANILLA = r"D:\Steam\steamapps\common\Hearts of Iron IV"

PARENTS = [BIAD, TANK, BI, VANILLA]
ROOTS = [MOD] + PARENTS

errors = []
warns = []
infos = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warns.append(msg)


def info(msg):
    infos.append(msg)


def read(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def brace_balance(text):
    depth = 0
    min_depth = 0
    for ch in text:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            min_depth = min(min_depth, depth)
    return depth, min_depth


# --------------------------------------------------------------------------
# collect reference sets from parent mods
# --------------------------------------------------------------------------
def collect_equipment_and_modules():
    eq, mods = set(), set()
    for root in PARENTS:
        base = os.path.join(root, "common", "units", "equipment")
        if not os.path.isdir(base):
            continue
        for dirpath, _, files in os.walk(base):
            for fn in files:
                if not fn.endswith(".txt"):
                    continue
                tree = C.parse_file(os.path.join(dirpath, fn))
                for key, target in (("equipments", eq), ("equipment_modules", mods)):
                    node = tree.get(key)
                    if isinstance(node, C.Node):
                        target.update(k for k in node if isinstance(k, str))
    return eq, mods


def collect_techs(root, out):
    d = os.path.join(root, "common", "technologies")
    if not os.path.isdir(d):
        return
    for fn in os.listdir(d):
        if not fn.endswith(".txt"):
            continue
        tree = C.parse_file(os.path.join(d, fn))
        node = tree.get("technologies")
        if isinstance(node, C.Node):
            for k in node:
                if isinstance(k, str) and not k.startswith("@"):
                    out.setdefault(k, os.path.join(d, fn))


def collect_categories(root, out):
    d = os.path.join(root, "common", "technology_tags")
    if not os.path.isdir(d):
        return
    for fn in os.listdir(d):
        if not fn.endswith(".txt"):
            continue
        tree = C.parse_file(os.path.join(d, fn))
        node = tree.get("technology_categories")
        out.update(C.scalars(node))


def collect_loc():
    table = {}
    for root in ROOTS:
        base = os.path.join(root, "localisation")
        if not os.path.isdir(base):
            continue
        for lang in os.listdir(base):
            d = os.path.join(base, lang)
            if not os.path.isdir(d):
                continue
            for dirpath, _, files in os.walk(d):
                for fn in files:
                    if not fn.endswith(".yml"):
                        continue
                    txt = read(os.path.join(dirpath, fn))
                    for line in txt.splitlines():
                        m = re.match(r'^\s*([A-Za-z0-9_.\-]+):(?:\d+)?\s+"', line)
                        if m:
                            table.setdefault(lang, set()).add(m.group(1))
    return table


def collect_sprites():
    table = set()
    for root in ROOTS:
        base = os.path.join(root, "interface")
        if not os.path.isdir(base):
            continue
        for dirpath, _, files in os.walk(base):
            for fn in files:
                if not fn.lower().endswith(".gfx"):
                    continue
                txt = read(os.path.join(dirpath, fn))
                table.update(re.findall(r'name\s*=\s*"?(GFX_[A-Za-z0-9_]+)"?', txt))
    return table


def file_in_roots(rel):
    rel = rel.replace("\\\\", "/").replace("\\", "/").replace("//", "/")
    for root in ROOTS:
        if os.path.isfile(os.path.join(root, *rel.split("/"))):
            return True
    return False


# --------------------------------------------------------------------------
def main():
    tech_file = os.path.join(MOD, "common", "technologies", "CHI_air.txt")
    tags_file = os.path.join(MOD, "common", "technology_tags", "zz_CHI_air_technology.txt")
    oa_file = os.path.join(MOD, "common", "on_actions", "zz_CHI_air_startup.txt")
    gfx_file = os.path.join(MOD, "interface", "chi_air_technology.gfx")
    gui_file = os.path.join(MOD, "interface", "countrytechtreeview.gui")
    loc_en = os.path.join(MOD, "localisation", "english", "chi_air_l_english.yml")
    loc_zh = os.path.join(MOD, "localisation", "simp_chinese", "chi_air_l_simp_chinese.yml")

    for p in (tech_file, tags_file, oa_file, gfx_file, gui_file, loc_en, loc_zh):
        if not os.path.isfile(p):
            err(f"缺少文件 / missing file: {p}")
    if errors:
        return

    # ---- syntax -------------------------------------------------------
    for p in (tech_file, tags_file, oa_file, gfx_file, gui_file):
        depth, neg = brace_balance(read(p))
        if depth != 0 or neg < 0:
            err(f"括号不配对 / unbalanced braces ({depth}): {os.path.basename(p)}")
    if "guiTypes" not in read(gui_file):
        err("GUI 文件不以 guiTypes 开头 / gui does not start with guiTypes")

    # ---- collect references ------------------------------------------
    equipment, modules = collect_equipment_and_modules()
    known_techs = {}
    for root in PARENTS:
        collect_techs(root, known_techs)
    our_techs = {}
    collect_techs(MOD, our_techs)
    all_techs = set(known_techs) | set(our_techs)

    categories = set()
    for root in PARENTS:
        collect_categories(root, categories)

    loc = collect_loc()
    sprites = collect_sprites()

    for k in our_techs:
        if k in known_techs:
            err(f"科技 id 与父模组冲突 / tech id collides with parent mod: {k}")

    # ---- parse our techs ---------------------------------------------
    tree = C.parse_file(tech_file)
    vars_ = C.collect_vars(tree)
    techs = tree.get("technologies")
    if not isinstance(techs, C.Node):
        err("technologies 根节点缺失 / no technologies root")
        return

    positions = {}
    folder_names = set()
    count = 0
    for tid, blk in techs.items():
        if not isinstance(blk, C.Node):
            continue
        count += 1
        folder = blk.get("folder")
        fname = None
        if isinstance(folder, C.Node):
            fname = folder.get("name")
            pos = folder.get("position")
            if isinstance(pos, C.Node):
                x = C.resolve(pos.get("x"), vars_)
                yy = C.resolve(pos.get("y"), vars_)
                key = (x, yy)
                if key in positions:
                    err(f"科技位置重叠 / tech position collision: {tid} 与 {positions[key]} at {key}")
                positions[key] = tid
            else:
                err(f"{tid}: 缺少 position / missing position")
        else:
            err(f"{tid}: 缺少 folder / missing folder block")
        if fname:
            folder_names.add(fname)

        equip_list = C.scalars(blk.get("enable_equipments"))
        for e in equip_list:
            if e not in equipment:
                err(f"{tid}: enable_equipments 引用了不存在的装备 / unknown equipment: {e}")
        mod_list = C.scalars(blk.get("enable_equipment_modules"))
        for m in mod_list:
            if m not in modules:
                err(f"{tid}: enable_equipment_modules 引用了不存在的模块 / unknown module: {m}")
        if not equip_list and not mod_list:
            warn(f"{tid}: 没有解锁任何装备或模块 / unlocks nothing")

        path = blk.get("path")
        if isinstance(path, C.Node):
            nxt = path.get("leads_to_tech")
            if isinstance(nxt, str) and nxt not in all_techs:
                err(f"{tid}: path.leads_to_tech 指向不存在的科技 / unknown tech: {nxt}")
        deps = blk.get("dependencies")
        if isinstance(deps, C.Node):
            for d in deps:
                if d.startswith("_"):
                    continue
                if d not in all_techs:
                    err(f"{tid}: dependencies 指向不存在的科技 / unknown tech: {d}")

        cats = C.scalars(blk.get("categories"))
        if not cats:
            warn(f"{tid}: 没有 categories / no categories")
        for c in cats:
            if c not in categories:
                err(f"{tid}: 未定义的科技分类 / unknown category: {c}")

        # localisation
        for lang in ("english", "simp_chinese"):
            if tid not in loc.get(lang, set()):
                err(f"{tid}: 缺少 {lang} 主键 / missing {lang} name key")
        if tid + "_desc" not in loc.get("simp_chinese", set()):
            warn(f"{tid}: 缺少中文描述键 / missing zh desc key")

        # icon sprite
        if f"GFX_{tid}_medium" not in sprites:
            err(f"{tid}: 缺少图标 sprite / missing icon sprite GFX_{tid}_medium")

        # gui gridbox
        if f'name = "{tid}_tree"' not in read(gui_file):
            err(f"{tid}: GUI 中缺少 gridbox / missing gridbox {tid}_tree")
        # 小格科技（发动机/枪炮/挂载）还需要 _small_tree 才会用 72×72 模板
        if tid.startswith(("ad_chi_tech_engine_", "ad_chi_tech_gun_", "ad_chi_tech_ord_")):
            if f'name = "{tid}_small_tree"' not in read(gui_file):
                err(f"{tid}: 小格科技缺少 gridbox / missing gridbox {tid}_small_tree")

    # ---- required-slot coverage (can the plane actually be built?) ------
    # For every airframe tech we need:
    #   * its required frame_config module unlocked by itself
    #   * at least one module of each required slot category unlocked by a
    #     tech in our own folder (powerplant is the critical one)
    our_modules = {}
    for tid, blk in techs.items():
        if not isinstance(blk, C.Node):
            continue
        for m in C.scalars(blk.get("enable_equipment_modules")):
            if m in modules:
                our_modules[m] = tid
    module_category = {}
    for root in PARENTS:
        base = os.path.join(root, "common", "units", "equipment", "modules")
        if not os.path.isdir(base):
            continue
        for fn in os.listdir(base):
            if not fn.endswith(".txt"):
                continue
            t = C.parse_file(os.path.join(base, fn))
            node = t.get("equipment_modules")
            if isinstance(node, C.Node):
                for mid, mb in node.items():
                    if isinstance(mb, C.Node) and isinstance(mb.get("category"), str):
                        module_category.setdefault(mid, mb.get("category"))

    eq_slots = {}
    for root in PARENTS:
        base = os.path.join(root, "common", "units", "equipment")
        if not os.path.isdir(base):
            continue
        for dirpath, _, files in os.walk(base):
            for fn in files:
                if not fn.endswith(".txt"):
                    continue
                t = C.parse_file(os.path.join(dirpath, fn))
                node = t.get("equipments")
                if not isinstance(node, C.Node):
                    continue
                for eid, eb in node.items():
                    if not isinstance(eb, C.Node):
                        continue
                    slots = eb.get("module_slots")
                    if isinstance(slots, C.Node):
                        slot_info = {}
                        for sname, sb in slots.items():
                            if isinstance(sb, C.Node):
                                cats = C.scalars(sb.get("allowed_module_categories"))
                                required = sb.get("required")
                                slot_info[sname] = (cats, required == "yes")
                        eq_slots.setdefault(eid, slot_info)

    slot_checks = 0
    for tid, blk in techs.items():
        if not isinstance(blk, C.Node):
            continue
        for eid in C.scalars(blk.get("enable_equipments")):
            slots = eq_slots.get(eid, {})
            for sname, (cats, required) in slots.items():
                if not required or not cats:
                    continue
                slot_checks += 1
                ok = False
                for m in our_modules:
                    if module_category.get(m) in cats:
                        ok = True
                        break
                if not ok:
                    err(f"{tid}: 必需槽位 {sname} 无可用模块（{eid} 需要 {cats}，本树未解锁）")

    info(f"科技总数 / techs: {count}")
    info(f"必需槽位覆盖检查 / required slot checks: {slot_checks}")

    # ---- graph sanity: unique successors, reachability, no cycles -------
    path_edges = []          # (source_tech, next_tech) declared by path blocks
    deps_graph = {}
    for tid, blk in techs.items():
        if not isinstance(blk, C.Node):
            continue
        deps_graph.setdefault(tid, [])
        path = blk.get("path")
        if isinstance(path, C.Node):
            nxt = path.get("leads_to_tech")
            if isinstance(nxt, str):
                path_edges.append((tid, nxt))
        deps = blk.get("dependencies")
        if isinstance(deps, C.Node):
            for d in deps:
                if not d.startswith("_"):
                    deps_graph.setdefault(tid, []).append(d)

    # every tech should be pointed to at most once by path blocks
    pointed = {}
    for src, nxt in path_edges:
        pointed.setdefault(nxt, []).append(src)
    for target, sources in pointed.items():
        if len(sources) > 1:
            err(f"path 冲突 / several techs lead to {target}: {sources}")

    # reachability over both path edges and dependency edges
    edges = {t: set() for t in deps_graph}
    for src, nxt in path_edges:
        edges.setdefault(src, set()).add(nxt)
    for tid, ds in deps_graph.items():
        for d in ds:
            edges.setdefault(d, set()).add(tid)
    roots = [t for t, ds in deps_graph.items() if not ds]
    seen = set()
    stack = list(roots)
    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        stack.extend(edges.get(t, ()))
    orphans = [t for t in deps_graph if t not in seen]
    if orphans:
        warn(f"无法从起始科技到达 / unreachable techs: {len(orphans)}: {sorted(orphans)[:8]}")
    # cycle detection (dfs)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {t: WHITE for t in deps_graph}
    cycle = []

    def dfs(node, path):
        color[node] = GRAY
        for dep in deps_graph.get(node, []):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                cycle.append(path + [dep])
                return True
            if color[dep] == WHITE and dfs(dep, path + [dep]):
                return True
        color[node] = BLACK
        return False

    for t in list(deps_graph):
        if color[t] == WHITE and dfs(t, [t]):
            break
    if cycle:
        err(f"前置关系存在环 / dependency cycle: {cycle[0]}")
    info(f"起始科技 / root techs: {len(roots)}")

    # ---- 每个 folder 需要 item / small_item 模板 -------------------------
    # 引擎按 "techtree_<folder>_item" / "techtree_<folder>_small_item" 建科技格子；
    # 缺了会刷 "Undefined GUI_TYPE ... Failed to create containerWindowType"，
    # 表现是科研界面闪烁一下打不开。
    gui_text = read(gui_file)
    if len(folder_names) == 1:
        _folder = next(iter(folder_names))
        for suffix in ("_item", "_small_item"):
            tpl = f"techtree_{_folder}{suffix}"
            pos_tpl = gui_text.find(f'name = "{tpl}"')
            if pos_tpl < 0:
                err(f"缺少科技条目模板 / missing tech item template: {tpl}")
            else:
                d = gui_text[:pos_tpl].count("{") - gui_text[:pos_tpl].count("}")
                if d != 2:
                    err(f"{tpl}: 模板必须是 guiTypes 下的顶层 containerWindowType（当前 name 深度 {d}）")

    # ---- gridbox 必须是 folder 容器的直接子节点 -------------------------
    # 放进 techtree_stripes 里引擎找不到，会刷 "Found no grid box for tech"，
    # 表现是科技页空白（甚至看起来没打开）。
    gui_text = read(gui_file)
    if len(folder_names) == 1:
        _folder = next(iter(folder_names))
        anchor = gui_text.find(f'name = "{_folder}"')
        if anchor >= 0:
            folder_depth = gui_text[:anchor].count("{") - gui_text[:anchor].count("}")
            for tid, blk in techs.items():
                if not isinstance(blk, C.Node):
                    continue
                pos = gui_text.find(f'name = "{tid}_tree"')
                if pos < 0:
                    continue
                depth = gui_text[:pos].count("{") - gui_text[:pos].count("}")
                if depth != folder_depth + 1:
                    err(f"{tid}: gridbox 层级不对 / gridbox is nested too deep "
                        f"(depth {depth}, expected {folder_depth + 1}) — 必须直接放在 {_folder} 下")
                    break

    # ---- 「+」请求页 / 解锁链路 ----------------------------------------
    req_folder = "chinaair_request_folder"
    if not REQUEST_GATE:
        req_folder = ""  # 请求页方案已关闭，跳过相关检查
    tags_txt = read(os.path.join(MOD, "common", "technology_tags", "zz_CHI_air_technology.txt"))
    if "trm_armour_chi_folder" in tags_txt and "has_country_flag = CHI_armor" not in tags_txt:
        err("technology_tags 里坦克文件夹缺少 CHI_armor 判定")
    if req_folder:
        if f"{req_folder} = {{" not in tags_txt:
            err(f"technology_tags 缺少请求页 / missing folder {req_folder}")
        if f'name = "{req_folder}"' not in gui_text:
            err(f"{req_folder}: GUI 中缺少请求页容器")
        if f'name = "{req_folder}_tab"' not in gui_text:
            err(f"{req_folder}: GUI 中缺少「+」页签按钮")
        req_gui = os.path.join(MOD, "common", "scripted_guis", "CHI_air_request.txt")
        if not os.path.isfile(req_gui):
            err("缺少请求页 scripted GUI / missing CHI_air_request.txt")
        else:
            rg = read(req_gui)
            if f'window_name = "{req_folder}"' not in rg:
                err("请求页 scripted GUI 的 window_name 与容器名不一致")
            if "set_country_flag = CHI_air" not in rg:
                err("请求页 scripted GUI 没有授予 CHI_air 标志")
            if "CHI_air_request_ready" not in rg:
                err("请求页 scripted GUI 没有引用 CHI_air_request_ready 条件")
    if REQUEST_GATE:
        trig = read(os.path.join(MOD, "common", "scripted_triggers", "zz_CHI_air_triggers.txt"))
        if "CHI_air_request_ready" not in trig:
            err("zz_CHI_air_triggers.txt 缺少 CHI_air_request_ready")

    # ---- 一次性提示事件（与坦克子模同款） ------------------------------
    ev_file = os.path.join(MOD, "events", "zz_CHI_air_tip.txt")
    if os.path.isfile(ev_file):
        ev = read(ev_file)
        for needle in ("add_namespace = CHI_air_unlock", "id = CHI_air_unlock.1", "is_triggered_only = yes"):
            if needle not in ev:
                err(f"提示事件文件缺少 / event file missing '{needle}'")
        for suffix in ("t", "d", "a"):
            key = f"CHI_air_unlock.1.{suffix}"
            for lang in ("english", "simp_chinese"):
                if key not in loc.get(lang, set()):
                    err(f"缺少提示事件本地化键 / missing {lang} key: {key}")
        # 解锁事件由请求页触发；请求页方案关闭时跳过
        if REQUEST_GATE:
            oa = read(os.path.join(MOD, "common", "scripted_guis", "CHI_air_request.txt"))
            if "CHI_air_unlock.1" not in oa:
                err("请求页未触发解锁事件 / request gui does not fire CHI_air_unlock.1")

    # ---- Black ICE research arrays + scripted GUI registration ---------
    eff_file = os.path.join(MOD, "common", "scripted_effects", "zz_CHI_air_research_arrays.txt")
    oa_arr = os.path.join(MOD, "common", "on_actions", "zz_CHI_air_array_gen.txt")
    sg_file = os.path.join(MOD, "common", "scripted_guis", "BI_tech_queue_china_air.txt")
    for p in (eff_file, oa_arr, sg_file):
        if not os.path.isfile(p):
            err(f"缺少研究界面注册文件 / missing registration file: {os.path.basename(p)}")
    if os.path.isfile(eff_file):
        txt = read(eff_file)
        depth, neg = brace_balance(txt)
        if depth != 0 or neg < 0:
            err("研究数组注册文件括号不配对 / unbalanced braces in research arrays")
        missing = []
        for tid, blk in techs.items():
            if not isinstance(blk, C.Node):
                continue
            if f"global.chinaair_folder = token:{tid}" not in txt:
                missing.append(tid)
            for key in ("tech_x@", "tech_y@", "tech_cost@", "tech_date@"):
                if f"{key}{tid} " not in txt:
                    err(f"{tid}: 研究数组缺少 {key} / missing {key}")
        if missing:
            err(f"未注册进 global.chinaair_folder 的科技: {len(missing)} 个，例如 {missing[:5]}")
        # pixel bounds: the folder container is 4000x2600
        for m_px, m_py in re.findall(r"tech_x@\w+ = (\d+) \}\s*\n\s*set_variable = \{ global\.tech_y@\w+ = (\d+)", txt):
            if not (0 <= int(m_px) <= 4000) or not (0 <= int(m_py) <= 2600):
                err(f"研究数组坐标越界 / tech position out of container: x={m_px} y={m_py}")
        info(f"研究数组条目 / research array techs: {txt.count('global.chinaair_folder = token:')}")
    if os.path.isfile(sg_file):
        sg = read(sg_file)
        depth, neg = brace_balance(sg)
        if depth != 0 or neg < 0:
            err("scripted GUI 括号不配对 / unbalanced braces in scripted GUI")
        if 'parent_window_name = "chinaair_folder"' not in sg:
            err("scripted GUI 未挂到 chinaair_folder / missing parent_window_name")
        if "BI_tech_queue_chinaair_folder = {" not in sg:
            err("scripted GUI 缺少文件夹块 / missing BI_tech_queue_chinaair_folder block")
        if "global.chinaair_folder" not in sg:
            err("scripted GUI 未引用 global.chinaair_folder 数组")
        if "luftwaffe" in sg:
            err("scripted GUI 仍残留 luftwaffe 引用 / leftover luftwaffe reference")

    # ---- folder wiring -------------------------------------------------
    if len(folder_names) != 1:
        err(f"科技使用了多个 folder / techs use several folders: {sorted(folder_names)}")
    else:
        folder = folder_names.pop()
        if f'name = "{folder}"' not in read(gui_file):
            err(f"GUI 缺少文件夹容器 / missing GUI container for folder {folder}")
        if f'name = "{folder}_tab"' not in read(gui_file):
            err(f"GUI 缺少标签按钮 / missing tab button {folder}_tab")
        if f"GFX_{folder}_tab" not in sprites:
            err(f"缺少标签页 sprite / missing tab sprite GFX_{folder}_tab")
        txt = read(tags_file)
        if folder not in txt:
            err(f"technology_tags 未声明 {folder}")
        if HIDE_GENERIC_AIR and "air_techs_folder" not in txt:
            err("technology_tags 未重定义 air_techs_folder（中国会出现两个空军页）")

    # ---- gfx texture files exist --------------------------------------
    gfx_txt = read(gfx_file)
    for name, tex in re.findall(r'name\s*=\s*"?(GFX_[A-Za-z0-9_]+)"?[\s\S]{0,80}?textureFile\s*=\s*"([^"]+)"', gfx_txt, re.I):
        if not file_in_roots(tex):
            err(f"sprite {name}: 贴图文件不存在 / texture missing: {tex}")

    # ---- loc keys used by GUI / tags ----------------------------------
    for key in ("SLOT_chinaair_folder", "chinaair_folder"):
        if key not in loc.get("simp_chinese", set()):
            warn(f"缺少本地化键 / missing loc key: {key}")

    # ---- duplicate tab / container insertion --------------------------
    gui_txt = read(gui_file)
    if gui_txt.count('name = "chinaair_folder_tab"') != 1:
        err("GUI 中标签按钮数量不等于 1 / tab button count != 1")
    if gui_txt.count('name = "chinaair_folder"') != 1:
        err("GUI 中文件夹容器数量不等于 1 / folder container count != 1")

    # ---- report --------------------------------------------------------
    print("=" * 70)
    print(f"error: {len(errors)}   warn: {len(warns)}   info: {len(infos)}")
    for tag, items in (("ERROR", errors), ("WARN", warns), ("INFO", infos)):
        for m in items:
            print(f"[{tag}] {m}")
    print("=" * 70)
    with open(os.path.join(HERE, "data", "validate_report.txt"), "w", encoding="utf-8") as f:
        f.write(f"error: {len(errors)} warn: {len(warns)} info: {len(infos)}\n")
        for tag, items in (("ERROR", errors), ("WARN", warns), ("INFO", infos)):
            for m in items:
                f.write(f"[{tag}] {m}\n")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
