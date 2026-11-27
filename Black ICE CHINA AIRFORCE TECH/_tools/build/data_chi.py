# -*- coding: utf-8 -*-
"""内容数据表：中系飞机科技树（黑冰 / BIAD）

这是整个模组**唯一需要手工维护**的文件。改完运行：

    python _tools/build/make.py all

会自动重建科技文件、研究数组、图标引用、本地化、预览图并跑校验。

字段说明
--------
AIRFRAMES（作战飞机）
    key        内部键，决定科技 id：ad_chi_tech_<key>
    equip      BIAD 机体原型 id（必须真实存在，构建时会校验）
    en / zh    中英文名
    year       可研发年份
    x          列坐标（用 config.COLUMNS 里的数值：26 战斗机 / 30 截击 / 34 攻击 / 38 轰炸 / 42 支援）
    dy         同列同年有两架时用 0/1 错开
    mfr        厂牌分类（curtiss_air 等，必须在黑冰 technology_categories 中）
    prev       前置科技的 key（同类别内），构建时转成 path + dependencies
    desc_en / desc_zh  英文/中文描述

ENGINES / GUNS / ORDNANCE（配件）
    key        科技 id 后缀：ad_chi_tech_engine_<key> / _gun_ / _ord_
    modules    要解锁的模块 id 列表（构建时校验存在性）
    x/year/mfr/prev/desc_* 同上

坐标约定：x 为列（1 列 = 70px），y 由年份推出（每年 2 行）。
不要手写 y；构建脚本按 config.YEAR_BASE / YEAR_STEP 计算。
"""
from config import FOLDER, FLAG, YEAR_BASE, YEAR_STEP, COLUMNS

# year -> folder y coordinate (2 rows per year, as BIAD nation folders do)
YEAR_Y = {y: (y - YEAR_BASE) * YEAR_STEP for y in range(YEAR_BASE, YEAR_BASE + 13)}


def y(year, dy=0):
    return YEAR_Y[year] + dy


# --------------------------------------------------------------------------
# Airframes: reuses BlackICE Aircraft Designer prototypes (verified ids).
# --------------------------------------------------------------------------
# key, tech_id, equipment, EN name, ZH name, year, column-x, manufacturer cat,
# previous tech (chain), EN desc, ZH desc, icon override (optional)
AIRFRAMES = [
    dict(
        key="hawk3", equip="ad_curtiss_hawk3_mr_equipment_1",
        en="Curtiss Hawk III", zh="霍克 III",
        year=1935, x=COLUMNS["ftr"], mfr="curtiss_air", prev=None,
        desc_en="The Curtiss Hawk III was the backbone of the Chinese Air Force in 1937; its mixed armament and dive-bombing capability made it the most numerous Chinese fighter of the opening campaigns.",
        desc_zh="霍克 III 是 1937 年中国空军的主力机型，既可空战也能俯冲轰炸，是抗战初期装备数量最多的战斗机。",
    ),
    dict(
        key="hawk75m", equip="ad_curtiss_p36_equipment_1",
        en="Curtiss Hawk H-75M", zh="霍克 H-75M",
        year=1937, x=COLUMNS["ftr"], mfr="curtiss_air", prev="hawk3",
        desc_en="The Hawk H-75M was the export version of the Curtiss P-36; small numbers reached China after 1937 to replace combat losses.",
        desc_zh="霍克 H-75M 是 P-36 的出口型，中国空军在 1937 年后少量接收，用于补充战损。",
    ),
    dict(
        key="p40b", equip="ad_curtiss_p40_equipment_1",
        en="Curtiss P-40B Warhawk", zh="P-40B 战鹰",
        year=1941, x=COLUMNS["ftr"], mfr="curtiss_air", prev="hawk75m",
        desc_en="Delivered with the American Volunteer Group, the P-40B gave China a modern monoplane fighter with heavy .50 calibre armament.",
        desc_zh="随美国志愿航空队来华，P-40B 以 12.7 毫米重机枪和坚固结构为中国提供了现代化战斗机。",
    ),
    dict(
        key="p40e", equip="ad_curtiss_p40_equipment_2",
        en="Curtiss P-40E Warhawk", zh="P-40E 战鹰",
        year=1942, x=COLUMNS["ftr"], mfr="curtiss_air", prev="p40b",
        desc_en="Replacing the four-gun wing with six .50 calibre guns, the P-40E became the standard fighter of the Chinese-American Composite Wing.",
        desc_zh="P-40E 以六挺 12.7 毫米机枪取代早期的四挺配置，成为中美混合联队的标准战斗机。",
    ),
    dict(
        key="p47d", equip="ad_republic_p47d_equipment_1",
        en="Republic P-47D Thunderbolt", zh="P-47D 雷电",
        year=1943, x=COLUMNS["ftr"], mfr="republic_air", prev="p40e",
        desc_en="The heavy, tough Thunderbolt arrived late in the war and excelled at escorting bombers and strafing river traffic.",
        desc_zh="P-47D 结构坚固、火力凶猛，在战争后期承担护航与扫射日军内河运输的任务。",
    ),
    dict(
        key="p51d", equip="ad_northamerican_p51d_equipment_1",
        en="North American P-51D Mustang", zh="P-51D 野马",
        year=1944, x=COLUMNS["ftr"], mfr="north_american_air", prev="p47d",
        desc_en="The Mustang's laminar wing and Packard-Merlin engine made it the best long-range escort fighter available to Chinese squadrons.",
        desc_zh="层流翼设计与帕卡德-梅林发动机使 P-51D 成为中国空军最优秀的远程护航战斗机。",
    ),
    dict(
        key="la9", equip="ad_lagg_9_equipment_1",
        en="Lavochkin La-9", zh="拉-9",
        year=1946, x=COLUMNS["ftr"], mfr="lavochkin_air", prev="p51d",
        desc_en="All-metal La-9 fighters equipped the first post-war aviation regiments and later flew in Korea.",
        desc_zh="全金属结构的拉-9 装备了战后第一批航空团，并参加了后来的朝鲜战争。",
    ),
    dict(
        key="p80a", equip="ad_lockheed_p80_equipment_1",
        en="Lockheed P-80A Shooting Star", zh="P-80A 流星",
        year=1946, x=COLUMNS["ftr"], mfr="lockheed_air", prev="p51d",
        desc_en="First-generation jet fighters offered to the post-war Chinese Air Force; the P-80A set the standard for the new jet age.",
        desc_zh="战后中国空军接触到的第一代喷气战斗机，P-80A 为喷气时代确立了新标准。",
    ),
    dict(
        key="mig9", equip="ad_mig_9_fighter_equipment_1",
        en="Mikoyan-Gurevich MiG-9", zh="米格-9",
        year=1947, x=COLUMNS["ftr"], mfr="mikoyan_gurevich_air", prev="p80a",
        desc_en="The MiG-9 was the Soviet Union's first operational jet fighter and the type that began Chinese jet aviation.",
        desc_zh="米格-9 是苏联第一种服役的喷气战斗机，也是中国喷气航空兵的开端。",
    ),
    dict(
        key="ki45", equip="ad_kawasaki_ki_45_equipment_1",
        en="Kawasaki Ki-45 Toryu", zh="二式复战 屠龙",
        year=1945, x=COLUMNS["hvy_ftr"], mfr="kawasaki_air", prev=None,
        desc_en="The twin-engine Ki-45 Toryu served as the Japanese Army's heavy interceptor and night fighter over China.",
        desc_zh="二式复战「屠龙」是日本陆军的双发重型战斗机，在中国战场承担拦截与夜间作战任务。",
    ),
    dict(
        key="a5m", equip="ad_mitsubishi_a5m_equipment_1",
        en="Mitsubishi A5M", zh="九六式舰战",
        year=1937, x=COLUMNS["cv_ftr"], mfr="mitsubishi_air", prev=None,
        desc_en="The A5M was the Imperial Japanese Navy's first all-metal monoplane carrier fighter and entered combat over China in 1937.",
        desc_zh="九六式舰战是日本海军第一种全金属单翼舰载战斗机，1937 年投入中国战场。",
    ),
    dict(
        key="a6m2", equip="ad_mitsubishi_a6m_equipment_1",
        en="Mitsubishi A6M2 Zero", zh="零式舰战二一型",
        year=1941, x=COLUMNS["cv_ftr"], mfr="mitsubishi_air", prev="a5m",
        desc_en="Zero fighters recovered from crashed or captured examples were evaluated and flown against their former owners.",
        desc_zh="从坠毁或缴获的零式战机中修复的机体被用于评估，并反过来投入对日作战。",
    ),
    dict(
        key="a6m3", equip="ad_mitsubishi_a6m3_equipment_1",
        en="Mitsubishi A6M3 Zero", zh="零式舰战三二型",
        year=1945, x=COLUMNS["cv_ftr"], mfr="mitsubishi_air", prev="a6m2",
        desc_en="The A6M3 introduced a more powerful engine and clipped wings, and was still encountered over China as late as 1945.",
        desc_zh="零式舰战三二型换装更大功率发动机并缩短翼展，1945 年前仍在中国战场出现。",
    ),
    dict(
        key="hs123", equip="ad_hs_123_equipment_1",
        en="Henschel Hs 123", zh="亨舍尔 Hs 123",
        year=1935, x=COLUMNS["cas"], mfr="henschel_air", prev=None,
        desc_en="Twelve Hs 123 dive bombers were bought from Germany in 1937 and flew close-support sorties until 1941.",
        desc_zh="1937 年从德国购入的十二架 Hs 123 俯冲轰炸机一直执行近距支援任务到 1941 年。",
    ),
    dict(
        key="v11", equip="ad_vultee_a19_equipment_1",
        en="Vultee V-11", zh="伏尔梯 V-11",
        year=1937, x=COLUMNS["cas"], mfr="vultee_air", prev="hs123",
        desc_en="The Vultee V-11 was a 1930s American attack aircraft; China used it for ground attack in the opening campaigns (approximated with A-19 airframe data).",
        desc_zh="伏尔梯 V-11 是 1930 年代的美国攻击机，中国引进后在抗战初期用于对地攻击（以 A-19 机体数据近似）。",
    ),
    dict(
        key="v12d", equip="ad_vultee_a31_equipment_1",
        en="Vultee V-12D", zh="伏尔梯 V-12D",
        year=1938, x=COLUMNS["cas"], mfr="vultee_air", prev="v11",
        desc_en="The V-12D was an export development of the V-11; China received a small number for close support (approximated with A-31 airframe data).",
        desc_zh="伏尔梯 V-12D 是 V-11 的出口改进型，中国少量装备，用于近距支援（以 A-31 机体数据近似）。",
    ),
    dict(
        key="mosquito_fb26", equip="ad_mosquito_fsb_equipment_2",
        en="DH.98 Mosquito FB Mk.26", zh="蚊式 FB Mk.26",
        year=1945, x=COLUMNS["cas"], mfr="de_havilland_air", prev="v12d",
        desc_en="The Mosquito FB Mk.26 was the Canadian-built fighter-bomber variant with heavy ground-attack armament.",
        desc_zh="蚊式 FB Mk.26 是加拿大生产的战斗轰炸型，具备强大的对地火力。",
    ),
    dict(
        key="sb2m", equip="ad_sb_2m_bomber_equipment_1",
        en="Tupolev SB 2M", zh="图波列夫 SB 2M",
        year=1937, x=COLUMNS["l_bomber"], mfr="tupolev_air", prev=None,
        desc_en="Soviet SB bombers formed the core of the Chinese bomber force and raided bases in Formosa and Japan-held territory.",
        desc_zh="苏联 SB 轰炸机构成中国轰炸机部队的核心，曾空袭台湾与日占区基地。",
    ),
    dict(
        key="br20", equip="br20_bomber_equipment_1",
        en="Fiat BR.20 Cicogna", zh="菲亚特 BR.20 鹳",
        year=1939, x=COLUMNS["l_bomber"], mfr="fiat_air", prev="sb2m",
        desc_en="A small batch of Italian BR.20 bombers served with the Chinese Air Force in the late 1930s.",
        desc_zh="1930 年代末，少量意大利 BR.20 轰炸机在中国空军服役。",
    ),
    dict(
        key="he111a", equip="ad_he_111_bomber_equipment_1",
        en="Heinkel He 111A", zh="亨克尔 He 111A",
        year=1936, x=COLUMNS["tac_bomber"], mfr="heinkel_air", prev=None,
        desc_en="China bought early He 111 bombers in 1936; they flew the first long-range raids on Japanese positions.",
        desc_zh="1936 年中国购入早期型 He 111 轰炸机，执行了对日军目标的首次远程轰炸。",
    ),
    dict(
        key="db3", equip="ad_db_3_bomber_equipment_1",
        en="Ilyushin DB-3", zh="伊尔-4（DB-3）",
        year=1940, x=COLUMNS["tac_bomber"], mfr="ilyushin_air", prev="he111a",
        desc_en="The long-range DB-3 flew the famous leaflet raids over Japan in 1938 and remained China's heavy bomber.",
        desc_zh="DB-3 远程轰炸机执行了 1938 年著名的对日“纸弹”空袭，并长期担任中国空军唯一的远程轰炸力量。",
    ),
    dict(
        key="b25c", equip="ad_northamerican_b25_equipment_2",
        en="North American B-25C Mitchell", zh="B-25C 米切尔",
        year=1942, x=COLUMNS["tac_bomber"], mfr="north_american_air", prev="db3",
        desc_en="Lend-lease Mitchells equipped the Chinese-American Composite Wing's bomber squadrons.",
        desc_zh="租借法案提供的 B-25 米切尔装备了中美混合联队的轰炸机中队。",
    ),
    dict(
        key="tu2", equip="ad_tu_2_bomber_equipment_1",
        en="Tupolev Tu-2", zh="图-2",
        year=1943, x=COLUMNS["tac_bomber"], mfr="tupolev_air", prev="b25c",
        desc_en="The Tu-2 fast bomber became the mainstay of the post-war Chinese bomber force.",
        desc_zh="图-2 快速轰炸机成为战后中国轰炸机部队的中坚。",
    ),
    dict(
        key="g4m2", equip="ad_mitsubishi_g4m2_equipment_1",
        en="Mitsubishi G4M2", zh="一式陆攻二二型",
        year=1945, x=COLUMNS["tac_bomber"], mfr="mitsubishi_air", prev="tu2",
        desc_en="Captured G4M2 bombers were used for maritime patrol and transport duties at the end of the war.",
        desc_zh="战争末期缴获的一式陆攻被用于海上巡逻与运输任务。",
    ),
    dict(
        key="martin139", equip="ad_martin_b10_bomber_equipment_1",
        en="Martin 139WC (B-10)", zh="马丁 139WC",
        year=1936, x=COLUMNS["strat_bomber"], mfr="martin_air", prev=None,
        desc_en="The Martin 139WC (B-10) was the backbone of the Chinese bomber force in the 1930s and flew leaflet raids over Japan.",
        desc_zh="马丁 139WC（B-10）是中国空军 1930 年代的主力轰炸机，曾执行对日宣传轰炸任务。",
    ),
    dict(
        key="db3h", equip="ad_db_3_bomber_equipment_2",
        en="Ilyushin DB-3 (long range)", zh="DB-3 轰炸机",
        year=1939, x=COLUMNS["strat_bomber"], mfr="ilyushin_air", prev="martin139",
        desc_en="Long-range DB-3 bombers gave China a strategic strike capability before the Il-4 took over.",
        desc_zh="DB-3 远程轰炸机，中国空军用于远程打击，后由伊尔-4 接替。",
    ),
    dict(
        key="b24j", equip="ad_consolidated_b24_equipment_2",
        en="Consolidated B-24J Liberator", zh="B-24J 解放者",
        year=1944, x=COLUMNS["strat_bomber"], mfr="consolidated_air", prev="db3h",
        desc_en="Four-engine Liberators gave China a genuine strategic bombing capability against Japan's supply lines.",
        desc_zh="四发 B-24 解放者使中国第一次具备打击日军补给线的真正战略轰炸能力。",
    ),
    dict(
        key="pby5", equip="ad_consolidated_pby_equipment_2",
        en="Consolidated PBY-5 Catalina", zh="PBY-5 卡特琳娜",
        year=1942, x=COLUMNS["fly_bts"], mfr="consolidated_air", prev=None,
        desc_en="Catalina flying boats performed maritime patrol, search and rescue along the Yangtze and the southern coast.",
        desc_zh="卡特琳娜水上飞机在长江与华南沿海执行海上巡逻与搜救任务。",
    ),
    dict(
        key="ki15", equip="ad_mitsubishi_ki_15_scout_equipment_1",
        en="Mitsubishi Ki-15", zh="九七式司令部侦察机",
        year=1937, x=COLUMNS["recon"], mfr="mitsubishi_air", prev=None,
        desc_en="Fast reconnaissance aircraft bought from Japan before the war provided the Chinese Air Force's eyes.",
        desc_zh="战前从日本购入的高速侦察机，是中国空军重要的空中侦察力量。",
    ),
    dict(
        key="f5", equip="ad_lockheed_p38_scout_equipment_2",
        en="Lockheed F-5 Lightning", zh="F-5 闪电侦察机",
        year=1943, x=COLUMNS["recon"], mfr="lockheed_air", prev="ki15",
        desc_en="Photo-reconnaissance Lightning variants mapped Japanese dispositions across the China theatre.",
        desc_zh="F-5 照相侦察机为中国战区绘制了日军部署图。",
    ),
    dict(
        key="mosquito_pr", equip="ad_mosquito_scout_equipment_2",
        en="DH.98 Mosquito PR Mk IX", zh="蚊式 PR Mk IX",
        year=1944, x=COLUMNS["recon"], mfr="de_havilland_air", prev="f5",
        desc_en="High-altitude Mosquito reconnaissance aircraft flew deep missions over occupied China and Japan.",
        desc_zh="高空蚊式侦察机深入日占中国与日本本土执行侦察任务。",
    ),
    dict(
        key="c47", equip="douglas_c47_transport_equipment_1",
        en="Douglas C-47 Skytrain", zh="C-47 空中列车",
        year=1942, x=COLUMNS["trpt"], mfr="douglas_air", prev=None,
        desc_en="The C-47 became the backbone of the Hump airlift, hauling supplies over the Himalayas into China.",
        desc_zh="C-47 是“驼峰航线”的主力运输机，把物资从印度空运至中国。",
    ),
]

# 同列同年有多架时自动错行，避免重叠
_seen = {}
for _a in sorted(AIRFRAMES, key=lambda a: (a["x"], a["year"])):
    _slot = (_a["x"], _a["year"])
    _a["dy"] = _seen.get(_slot, 0)
    _seen[_slot] = _a["dy"] + 1

# --------------------------------------------------------------------------
# Engines.  modules: exact equipment-module ids (validated against BIAD)
# --------------------------------------------------------------------------
ENGINES = []

# --------------------------------------------------------------------------
# Guns / cannons
# --------------------------------------------------------------------------
GUNS = []

# --------------------------------------------------------------------------
# Bombs / rockets / ordnance
# --------------------------------------------------------------------------
ORDNANCE = []


# --------------------------------------------------------------------------
# 配件列坐标统一由 COLUMNS 推导，方便整体平移/调间距
# --------------------------------------------------------------------------
_X_TO_ROLE = {
    0: "engine_usa", 2: "engine_usa_multi", 4: "engine_sov", 6: "engine_sov_multi",
    8: "engine_jap", 12: "engine_other", 16: "gun", 20: "ordnance", 22: "ordnance_2",
}
for _t in ENGINES:
    _t["x"] = COLUMNS[_X_TO_ROLE[_t["x"]]]
for _t in GUNS:
    _t["x"] = COLUMNS["gun"]
for _t in ORDNANCE:
    _t["x"] = COLUMNS["ordnance_2" if _t["key"] in ("ao10", "rs82") else "ordnance"]
