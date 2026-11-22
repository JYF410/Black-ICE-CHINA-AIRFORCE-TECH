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
from config import FOLDER, FLAG, YEAR_BASE, YEAR_STEP

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
    # ---------------- fighters (x=26) ----------------
    dict(
        key="hawk3", equip="ad_curtiss_hawk3_mr_equipment_1",
        en="Curtiss Hawk III", zh="霍克 III",
        year=1936, x=26, mfr="curtiss_air", prev=None,
        desc_en="The Curtiss Hawk III was the backbone of the Chinese Air Force in 1937; its mixed armament and dive-bombing capability made it the most numerous Chinese fighter of the opening campaigns.",
        desc_zh="霍克 III 是 1937 年中国空军的主力机型，既可空战也能俯冲轰炸，是抗战初期装备数量最多的战斗机。",
    ),
    dict(
        key="i152", equip="ad_i_152_equipment_1",
        en="Polikarpov I-15bis", zh="伊-15 比斯",
        year=1937, x=26, mfr="polikarpov_air", prev="hawk3",
        desc_en="Soviet I-15bis biplanes arrived with the 1937 aid packages and bore the brunt of the fighting over Wuhan and Chongqing.",
        desc_zh="苏联援华的伊-15 比斯双翼机随 1937 年援助抵达，在武汉、重庆上空承担了繁重的空战任务。",
    ),
    dict(
        key="i16t10", equip="ad_i_16_equipment_3",
        en="Polikarpov I-16 Type 10", zh="伊-16 10 型",
        year=1938, x=26, mfr="polikarpov_air", prev="i152",
        desc_en="The I-16 Type 10 monoplane gave Chinese pilots a fast, heavily armed fighter able to challenge Japanese bombers over the interior.",
        desc_zh="伊-16 10 型单翼战斗机让中国飞行员第一次拥有足以拦截日军轰炸机的速度与火力。",
    ),
    dict(
        key="i16t24", equip="ad_i_16_equipment_4",
        en="Polikarpov I-16 Type 24", zh="伊-16 24 型",
        year=1940, x=26, mfr="polikarpov_air", prev="i16t10",
        desc_en="The Type 24 was the definitive I-16: four ShKAS, a strengthened wing and a more powerful M-62 engine.",
        desc_zh="24 型是伊-16 系列的成熟版本：四挺 ShKAS 机枪、加强机翼与功率更大的 M-62 发动机。",
    ),
    dict(
        key="p40b", equip="ad_curtiss_p40_equipment_1",
        en="Curtiss P-40B Warhawk", zh="P-40B 战鹰",
        year=1941, x=26, mfr="curtiss_air", prev="i16t24",
        desc_en="Delivered with the American Volunteer Group, the P-40B gave China a modern monoplane fighter with heavy .50 calibre armament.",
        desc_zh="随美国志愿航空队来华，P-40B 以 12.7 毫米重机枪和坚固结构为中国提供了现代化战斗机。",
    ),
    dict(
        key="p40e", equip="ad_curtiss_p40_equipment_2",
        en="Curtiss P-40E Warhawk", zh="P-40E 战鹰",
        year=1942, x=26, mfr="curtiss_air", prev="p40b",
        desc_en="Replacing the four-gun wing with six .50 calibre guns, the P-40E became the standard fighter of the Chinese-American Composite Wing.",
        desc_zh="P-40E 以六挺 12.7 毫米机枪取代早期的四挺配置，成为中美混合联队的标准战斗机。",
    ),
    dict(
        key="p47d", equip="ad_republic_p47d_equipment_1",
        en="Republic P-47D Thunderbolt", zh="P-47D 雷电",
        year=1943, x=26, mfr="republic_air", prev="p40e",
        desc_en="The heavy, tough Thunderbolt arrived late in the war and excelled at escorting bombers and strafing river traffic.",
        desc_zh="P-47D 结构坚固、火力凶猛，在战争后期承担护航与扫射日军内河运输的任务。",
    ),
    dict(
        key="p51d", equip="ad_northamerican_p51d_equipment_1",
        en="North American P-51D Mustang", zh="P-51D 野马",
        year=1944, x=26, mfr="north_american_air", prev="p47d",
        desc_en="The Mustang's laminar wing and Packard-Merlin engine made it the best long-range escort fighter available to Chinese squadrons.",
        desc_zh="层流翼设计与帕卡德-梅林发动机使 P-51D 成为中国空军最优秀的远程护航战斗机。",
    ),
    dict(
        key="p80a", equip="ad_lockheed_p80_equipment_1",
        en="Lockheed P-80A Shooting Star", zh="P-80A 流星",
        year=1946, x=26, mfr="lockheed_air", prev="p51d",
        desc_en="First-generation jet fighters offered to the post-war Chinese Air Force; the P-80A set the standard for the new jet age.",
        desc_zh="战后中国空军接触到的第一代喷气战斗机，P-80A 为喷气时代确立了新标准。",
    ),
    # ---------------- interceptors / late fighters (x=30) ----------------
    dict(
        key="ki27", equip="ad_nakajima_ki_27_equipment_1",
        en="Nakajima Ki-27", zh="九七式战斗机",
        year=1938, x=30, mfr="nakajima_air", prev=None,
        desc_en="Captured and repaired Ki-27 airframes were pressed into Chinese service for training and local patrols.",
        desc_zh="缴获修复的九七式战斗机被编入中国空军，用于训练与局部巡逻。",
    ),
    dict(
        key="i153", equip="ad_i_153_equipment_1",
        en="Polikarpov I-153", zh="伊-153 海鸥",
        year=1939, x=30, mfr="polikarpov_air", prev="ki27",
        desc_en="The gull-winged Chaika was the last Soviet biplane fighter supplied to China and fought on into 1941.",
        desc_zh="海鸥翼的伊-153 是苏联援助中国的最后一种双翼战斗机，一直使用到 1941 年。",
    ),
    dict(
        key="ki43", equip="ad_nakajima_ki_43_equipment_1",
        en="Nakajima Ki-43 Hayabusa", zh="一式战斗机二型",
        year=1941, x=30, mfr="nakajima_air", prev="i153",
        desc_en="Lightly built and extremely manoeuvrable, the Hayabusa was the Japanese Army's main fighter and a prized capture.",
        desc_zh="一式战以轻巧灵活著称，是日本陆军航空队的主力战斗机，也是中国空军重点搜集的缴获机型。",
    ),
    dict(
        key="a6m2", equip="ad_mitsubishi_a6m_equipment_1",
        en="Mitsubishi A6M2 Zero", zh="零式舰战二一型",
        year=1942, x=30, mfr="mitsubishi_air", prev="ki43",
        desc_en="Zero fighters recovered from crashed or captured examples were evaluated and flown against their former owners.",
        desc_zh="从坠毁或缴获的零式战机中修复的机体被用于评估，并反过来投入对日作战。",
    ),
    dict(
        key="ki61", equip="ad_kawasaki_ki_61_equipment_1",
        en="Kawasaki Ki-61 Hien", zh="三式战斗机一型",
        year=1943, x=30, mfr="kawasaki_air", prev="a6m2",
        desc_en="The liquid-cooled Hien was the only Japanese inline-engine fighter of the war; captured examples were carefully studied.",
        desc_zh="三式战是战争中唯一采用液冷直列发动机的日军战斗机，缴获机体被仔细研究。",
    ),
    dict(
        key="ki84", equip="ad_nakajima_ki_84_equipment_1",
        en="Nakajima Ki-84 Hayate", zh="四式战斗机一型",
        year=1944, x=30, mfr="nakajima_air", prev="ki61",
        desc_en="Fast and heavily armed, the Hayate was the best Japanese Army fighter to reach China and a valuable late-war prize.",
        desc_zh="四式战速度快、火力强，是投入中国战场的最优秀日本陆军战斗机，也是战争后期的重要战利品。",
    ),
    dict(
        key="la9", equip="ad_lagg_9_equipment_1",
        en="Lavochkin La-9", zh="拉-9",
        year=1946, x=30, mfr="lavochkin_air", prev="ki84",
        desc_en="All-metal La-9 fighters equipped the first post-war aviation regiments and later flew in Korea.",
        desc_zh="全金属结构的拉-9 装备了战后第一批航空团，并参加了后来的朝鲜战争。",
    ),
    dict(
        key="mig9", equip="ad_mig_9_fighter_equipment_1",
        en="Mikoyan-Gurevich MiG-9", zh="米格-9",
        year=1947, x=30, mfr="mikoyan_gurevich_air", prev="la9",
        desc_en="The MiG-9 was the Soviet Union's first operational jet fighter and the type that began Chinese jet aviation.",
        desc_zh="米格-9 是苏联第一种服役的喷气战斗机，也是中国喷气航空兵的开端。",
    ),
    # ---------------- attackers / CAS (x=34) ----------------
    dict(
        key="gamma2e", equip="ad_northrop_gamma_2e_equipment_1",
        en="Northrop Gamma 2E", zh="诺斯罗普 伽马 2E",
        year=1936, x=34, mfr="northrop_air", prev=None,
        desc_en="The Gamma 2E light attack bomber was licence-assembled in China and used against Japanese columns in 1937.",
        desc_zh="伽马 2E 轻型攻击机曾在中国组装，1937 年用于攻击日军行军纵队。",
    ),
    dict(
        key="hs123", equip="ad_hs_123_equipment_1",
        en="Henschel Hs 123", zh="亨舍尔 Hs 123",
        year=1937, x=34, mfr="henschel_air", prev="gamma2e",
        desc_en="Twelve Hs 123 dive bombers were bought from Germany in 1937 and flew close-support sorties until 1941.",
        desc_zh="1937 年从德国购入的十二架 Hs 123 俯冲轰炸机一直执行近距支援任务到 1941 年。",
    ),
    dict(
        key="a19", equip="ad_vultee_a19_equipment_1",
        en="Vultee A-19", zh="伏尔梯 A-19",
        year=1938, x=34, mfr="vultee_air", prev="hs123",
        desc_en="The A-19 (V-11) attack bomber was China's most modern ground-attack type of the late 1930s, armed with a 20mm cannon.",
        desc_zh="A-19（V-11）攻击机是 1930 年代末中国最先进的对地攻击机，装有 20 毫米机关炮。",
    ),
    dict(
        key="mosquito_fb6", equip="ad_mosquito_hvf_equipment_1",
        en="De Havilland Mosquito FB Mk VI", zh="蚊式 FB Mk VI",
        year=1944, x=34, mfr="de_havilland_air", prev="a19",
        desc_en="Wooden, fast and hard-hitting, the Mosquito fighter-bomber gave Chinese squadrons a precision strike capability.",
        desc_zh="木质结构、高速且火力凶猛的蚊式战斗轰炸机为中国空军带来精确打击能力。",
    ),
    dict(
        key="il10", equip="ad_il_10_equipment_1",
        en="Ilyushin Il-10", zh="伊尔-10",
        year=1945, x=34, mfr="ilyushin_air", prev="mosquito_fb6",
        desc_en="The Il-10 armoured ground-attack aircraft became the standard close-support type of the new Chinese air force.",
        desc_zh="伊尔-10 装甲强击机成为新中国空军标准的近距支援机型。",
    ),
    # ---------------- bombers (x=38) ----------------
    dict(
        key="he111a", equip="ad_he_111_bomber_equipment_1",
        en="Heinkel He 111A", zh="亨克尔 He 111A",
        year=1936, x=38, mfr="heinkel_air", prev=None,
        desc_en="China bought early He 111 bombers in 1936; they flew the first long-range raids on Japanese positions.",
        desc_zh="1936 年中国购入早期型 He 111 轰炸机，执行了对日军目标的首次远程轰炸。",
    ),
    dict(
        key="sb2m", equip="ad_sb_2m_bomber_equipment_1",
        en="Tupolev SB 2M", zh="图波列夫 SB 2M",
        year=1937, x=38, mfr="tupolev_air", prev="he111a",
        desc_en="Soviet SB bombers formed the core of the Chinese bomber force and raided bases in Formosa and Japan-held territory.",
        desc_zh="苏联 SB 轰炸机构成中国轰炸机部队的核心，曾空袭台湾与日占区基地。",
    ),
    dict(
        key="br20", equip="br20_bomber_equipment_1",
        en="Fiat BR.20 Cicogna", zh="菲亚特 BR.20 鹳",
        year=1939, x=38, mfr="fiat_air", prev="sb2m",
        desc_en="A small batch of Italian BR.20 bombers served with the Chinese Air Force in the late 1930s.",
        desc_zh="1930 年代末，少量意大利 BR.20 轰炸机在中国空军服役。",
    ),
    dict(
        key="db3", equip="ad_db_3_bomber_equipment_1",
        en="Ilyushin DB-3", zh="伊尔-4（DB-3）",
        year=1940, x=38, mfr="ilyushin_air", prev="br20",
        desc_en="The long-range DB-3 flew the famous leaflet raids over Japan in 1938 and remained China's heavy bomber.",
        desc_zh="DB-3 远程轰炸机执行了 1938 年著名的对日“纸弹”空袭，并长期担任中国空军唯一的远程轰炸力量。",
    ),
    dict(
        key="b25c", equip="ad_northamerican_b25_equipment_2",
        en="North American B-25C Mitchell", zh="B-25C 米切尔",
        year=1942, x=38, mfr="north_american_air", prev="db3",
        desc_en="Lend-lease Mitchells equipped the Chinese-American Composite Wing's bomber squadrons.",
        desc_zh="租借法案提供的 B-25 米切尔装备了中美混合联队的轰炸机中队。",
    ),
    dict(
        key="tu2", equip="ad_tu_2_bomber_equipment_1",
        en="Tupolev Tu-2", zh="图-2",
        year=1943, x=38, mfr="tupolev_air", prev="b25c",
        desc_en="The Tu-2 fast bomber became the mainstay of the post-war Chinese bomber force.",
        desc_zh="图-2 快速轰炸机成为战后中国轰炸机部队的中坚。",
    ),
    dict(
        key="b24j", equip="ad_consolidated_b24_equipment_2",
        en="Consolidated B-24J Liberator", zh="B-24J 解放者",
        year=1944, x=38, mfr="consolidated_air", prev="tu2",
        desc_en="Four-engine Liberators gave China a genuine strategic bombing capability against Japan's supply lines.",
        desc_zh="四发 B-24 解放者使中国第一次具备打击日军补给线的真正战略轰炸能力。",
    ),
    dict(
        key="g4m2", equip="ad_mitsubishi_g4m2_equipment_1",
        en="Mitsubishi G4M2", zh="一式陆攻二二型",
        year=1945, x=38, mfr="mitsubishi_air", prev="b24j",
        desc_en="Captured G4M2 bombers were used for maritime patrol and transport duties at the end of the war.",
        desc_zh="战争末期缴获的一式陆攻被用于海上巡逻与运输任务。",
    ),
    # ---------------- support (x=42) ----------------
    dict(
        key="ki15", equip="ad_mitsubishi_ki_15_scout_equipment_1",
        en="Mitsubishi Ki-15", zh="九七式司令部侦察机",
        year=1937, x=42, mfr="mitsubishi_air", prev=None,
        desc_en="Fast reconnaissance aircraft bought from Japan before the war provided the Chinese Air Force's eyes.",
        desc_zh="战前从日本购入的高速侦察机，是中国空军重要的空中侦察力量。",
    ),
    dict(
        key="pby5", equip="ad_consolidated_pby_equipment_2",
        en="Consolidated PBY-5 Catalina", zh="PBY-5 卡特琳娜",
        year=1942, x=42, mfr="consolidated_air", prev="ki15",
        desc_en="Catalina flying boats performed maritime patrol, search and rescue along the Yangtze and the southern coast.",
        desc_zh="卡特琳娜水上飞机在长江与华南沿海执行海上巡逻与搜救任务。",
    ),
    dict(
        key="c47", equip="douglas_c47_transport_equipment_1",
        en="Douglas C-47 Skytrain", zh="C-47 空中列车",
        year=1942, x=42, dy=1, mfr="douglas_air", prev="ki15",
        desc_en="The C-47 became the backbone of the Hump airlift, hauling supplies over the Himalayas into China.",
        desc_zh="C-47 是“驼峰航线”的主力运输机，把物资从印度空运至中国。",
    ),
    dict(
        key="f5", equip="ad_lockheed_p38_scout_equipment_2",
        en="Lockheed F-5 Lightning", zh="F-5 闪电侦察机",
        year=1943, x=42, mfr="lockheed_air", prev="pby5",
        desc_en="Photo-reconnaissance Lightning variants mapped Japanese dispositions across the China theatre.",
        desc_zh="F-5 照相侦察机为中国战区绘制了日军部署图。",
    ),
    dict(
        key="mosquito_pr", equip="ad_mosquito_scout_equipment_2",
        en="De Havilland Mosquito PR Mk IX", zh="蚊式 PR Mk IX",
        year=1944, x=42, mfr="de_havilland_air", prev="f5",
        desc_en="High-altitude Mosquito reconnaissance aircraft flew deep missions over occupied China and Japan.",
        desc_zh="高空蚊式侦察机深入日占中国与日本本土执行侦察任务。",
    ),
]

# --------------------------------------------------------------------------
# Engines.  modules: exact equipment-module ids (validated against BIAD)
# --------------------------------------------------------------------------
ENGINES = [
    dict(key="r1820", x=0, year=1935, mfr="curtiss_air",
         en="Wright R-1820 Cyclone", zh="莱特 R-1820 旋风",
         modules=["ad_engine_usa_r1820_1x"], prev=None,
         desc_en="Licence-built Wright Cyclone radials powered the Hawk III and Gamma 2E.",
         desc_zh="授权生产的莱特旋风星型发动机，装备霍克 III 与伽马 2E。"),
    dict(key="v1710", x=0, year=1940, mfr="curtiss_air",
         en="Allison V-1710", zh="艾利森 V-1710",
         modules=["ad_engine_usa_v1710_1x"], prev="r1820",
         desc_en="The V-1710 inline engine was the standard powerplant of the P-40 family.",
         desc_zh="V-1710 液冷发动机是 P-40 系列的标准动力。"),
    dict(key="r2800", x=0, year=1943, mfr="republic_air",
         en="Pratt & Whitney R-2800 Double Wasp", zh="普惠 R-2800 双黄蜂",
         modules=["ad_engine_usa_r2800_1x"], prev="v1710",
         desc_en="The 2,000 hp Double Wasp gave the Thunderbolt its speed and ruggedness.",
         desc_zh="2000 马力的双黄蜂发动机赋予雷电战斗机速度与坚固性。"),
    dict(key="v1650", x=0, year=1944, mfr="north_american_air",
         en="Packard V-1650 Merlin", zh="帕卡德 V-1650 梅林",
         modules=["ad_engine_usa_v1650_1x"], prev="r2800",
         desc_en="Licence-built Rolls-Royce Merlins turned the Mustang into a long-range escort fighter.",
         desc_zh="授权生产的梅林发动机使野马成为远程护航战斗机。"),
    dict(key="r2600", x=2, year=1941, mfr="north_american_air",
         en="Wright R-2600 Twin Cyclone", zh="莱特 R-2600 双旋风",
         modules=["ad_engine_usa_r2600_2x"], prev=None,
         desc_en="Twin Cyclones powered the B-25 Mitchell medium bomber.",
         desc_zh="双旋风发动机是 B-25 米切尔中型轰炸机的动力。"),
    dict(key="r1830", x=2, year=1942, mfr="consolidated_air",
         en="Pratt & Whitney R-1830 Twin Wasp", zh="普惠 R-1830 双黄蜂",
         modules=["ad_engine_usa_r1830_2x", "ad_engine_usa_r1830_4x"], prev="r2600",
         desc_en="Fourteen-cylinder Twin Wasps powered the C-47, the PBY and the B-24.",
         desc_zh="十四缸双黄蜂发动机用于 C-47、PBY 与 B-24。"),
    dict(key="j33", x=2, year=1946, mfr="lockheed_air",
         en="General Electric J33 Turbojet", zh="通用电气 J33 涡喷发动机",
         modules=["ad_engine_usa_j33_1x"], prev="r1830",
         desc_en="The J33 centrifugal-flow turbojet powered the P-80 Shooting Star.",
         desc_zh="J33 离心式涡喷发动机是 P-80 流星的动力。"),
    dict(key="m25", x=4, year=1936, mfr="polikarpov_air",
         en="Shvetsov M-25", zh="什韦佐夫 M-25",
         modules=["ad_engine_sov_m25_1x"], prev=None,
         desc_en="The M-25 radial was the standard engine of the I-15 and early I-16 fighters.",
         desc_zh="M-25 星型发动机是伊-15 与早期伊-16 的标准动力。"),
    dict(key="m62", x=4, year=1938, mfr="polikarpov_air",
         en="Shvetsov M-62", zh="什韦佐夫 M-62",
         modules=["ad_engine_sov_m62_1x"], prev="m25",
         desc_en="The uprated M-62 powered the I-16 Type 24 and the I-153.",
         desc_zh="功率提升的 M-62 用于伊-16 24 型与伊-153。"),
    dict(key="m82", x=4, year=1943, mfr="lavochkin_air",
         en="Shvetsov M-82 / ASh-82", zh="什韦佐夫 M-82 / ASh-82",
         modules=["ad_engine_sov_m82_1x", "ad_engine_sov_m82_2x"], prev="m62",
         desc_en="The M-82 family powered the La-5/La-9 fighters and the Tu-2 bomber.",
         desc_zh="M-82 系列发动机用于拉-5/拉-9 战斗机与图-2 轰炸机。"),
    dict(key="am42", x=4, year=1944, mfr="ilyushin_air",
         en="Mikulin AM-42", zh="米库林 AM-42",
         modules=["ad_engine_sov_am42_1x"], prev="m82",
         desc_en="The AM-42 was developed for the Il-10 armoured attack aircraft.",
         desc_zh="AM-42 是专为伊尔-10 装甲强击机研制的发动机。"),
    dict(key="m103", x=6, year=1937, mfr="tupolev_air",
         en="Klimov M-103", zh="克里莫夫 M-103",
         modules=["ad_engine_sov_m103_2x"], prev=None,
         desc_en="Twin M-103 inlines powered the SB 2M fast bomber.",
         desc_zh="两台 M-103 液冷发动机为 SB 2M 快速轰炸机提供动力。"),
    dict(key="m34", x=6, year=1939, mfr="ilyushin_air",
         en="Mikulin M-34 / AM-34", zh="米库林 M-34 / AM-34",
         modules=["ad_engine_sov_m34_2x"], prev="m103",
         desc_en="The M-34 powered the DB-3 long-range bomber.",
         desc_zh="M-34 发动机用于 DB-3 远程轰炸机。"),
    dict(key="rd20", x=6, year=1946, mfr="mikoyan_gurevich_air",
         en="Mikulin RD-20 Turbojet", zh="米库林 RD-20 涡喷发动机",
         modules=["ad_engine_sov_rd20_2x"], prev="m34",
         desc_en="The RD-20 was a Soviet copy of the Junkers Jumo 004 and powered the MiG-9.",
         desc_zh="RD-20 是容克 Jumo 004 的苏联仿制型，用于米格-9。"),
    dict(key="kotobuki", x=8, year=1937, mfr="nakajima_air",
         en="Nakajima Ha-1 Kotobuki", zh="中岛 Ha-1 寿",
         modules=["ad_engine_kotobuki_1x"], prev=None,
         desc_en="The Kotobuki radial powered the Ki-27 fighter and Ki-15 reconnaissance aircraft.",
         desc_zh="中岛“寿”星型发动机用于九七式战斗机与九七式司侦。"),
    dict(key="sakae", x=8, year=1940, mfr="nakajima_air",
         en="Nakajima Ha-35 Sakae", zh="中岛 Ha-35 荣",
         modules=["ad_engine_sakae_1x"], prev="kotobuki",
         desc_en="The Sakae 14-cylinder radial powered the A6M Zero and the Ki-43 Hayabusa.",
         desc_zh="荣 14 缸星型发动机用于零式战斗机与一式战。"),
    dict(key="homare", x=8, year=1944, mfr="nakajima_air",
         en="Nakajima Ha-45 Homare", zh="中岛 Ha-45 誉",
         modules=["ad_engine_homare_1x"], prev="sakae",
         desc_en="The 1,900 hp Homare powered the Ki-84 Hayate.",
         desc_zh="1900 马力的“誉”发动机用于四式战。"),
    dict(key="kasei", x=8, year=1943, mfr="mitsubishi_air",
         en="Mitsubishi Ha-32 Kasei", zh="三菱 Ha-32 火星",
         modules=["ad_engine_kasei_2x"], prev="sakae",
         desc_en="Twin Kasei radials powered the G4M bomber family.",
         desc_zh="两台火星发动机为一式陆攻提供动力。"),
    dict(key="bmw132", x=12, year=1935, mfr="henschel_air",
         en="BMW 132 Radial", zh="宝马 132 星型发动机",
         modules=["ad_engine_bmw_132_1x"], prev=None,
         desc_en="The BMW 132 powered the Hs 123 dive bomber.",
         desc_zh="宝马 132 发动机用于 Hs 123 俯冲轰炸机。"),
    dict(key="bmw_vi", x=12, year=1936, mfr="heinkel_air",
         en="BMW VI", zh="宝马 VI",
         modules=["ad_engine_bmw_vi_2x"], prev="bmw132",
         desc_en="Twin BMW VI engines powered the early He 111A bombers sold to China.",
         desc_zh="两台宝马 VI 发动机为售华的早期 He 111A 轰炸机提供动力。"),
    dict(key="merlin", x=12, year=1943, mfr="de_havilland_air",
         en="Rolls-Royce Merlin XX", zh="罗尔斯-罗伊斯 梅林 XX",
         modules=["ad_engine_merlin_20_28_38_2x"], prev="bmw_vi",
         desc_en="Twin Merlin XX engines gave the Mosquito its exceptional speed.",
         desc_zh="两台梅林 XX 发动机赋予蚊式卓越的速度。"),
]

# --------------------------------------------------------------------------
# Guns / cannons
# --------------------------------------------------------------------------
GUNS = [
    dict(key="m1919", x=16, year=1935, mfr="curtiss_air",
         en=".30 cal M1919 Browning", zh="7.62 毫米 M1919 勃朗宁机枪",
         modules=["ad_mg_m1919_1x", "ad_mg_m1919_2x", "ad_mg_m1919_3x", "ad_mg_m1919_4x"], prev=None,
         desc_en="The standard American light machine gun arming early Chinese fighters.",
         desc_zh="早期中国战斗机使用的美制 7.62 毫米航空机枪。"),
    dict(key="shkas", x=16, year=1936, mfr="polikarpov_air",
         en="ShKAS 7.62mm", zh="ShKAS 7.62 毫米机枪",
         modules=["ad_mg_shkas_1x", "ad_mg_shkas_2x", "ad_mg_shkas_4x"], prev="m1919",
         desc_en="The high-rate ShKAS armed Polikarpov fighters and Soviet-supplied bombers.",
         desc_zh="高射速的 ShKAS 是波利卡波夫战斗机与苏联援华轰炸机的标准武器。"),
    dict(key="mg17", x=16, year=1936, mfr="henschel_air",
         en="MG 17 7.92mm", zh="MG 17 7.92 毫米机枪",
         modules=["ad_mg17_1x", "ad_mg17_2x", "ad_mg81_1x", "ad_mg81_2x"], prev="m1919",
         desc_en="German 7.92mm machine guns including the flexible MG 81 for turrets.",
         desc_zh="德制 7.92 毫米机枪，含用于炮塔的 MG 81 活动机枪。"),
    dict(key="m2", x=16, year=1937, mfr="curtiss_air",
         en=".50 cal M2 Browning", zh="12.7 毫米 M2 勃朗宁机枪",
         modules=["ad_mg_m2_1x", "ad_mg_m2_2x", "ad_mg_m2_3x", "ad_mg_m2_4x"], prev="shkas",
         desc_en="Heavy .50 calibre Browning guns gave American-supplied fighters real hitting power.",
         desc_zh="12.7 毫米勃朗宁重机枪使美援战斗机具备真正的毁伤能力。"),
    dict(key="type89", x=16, year=1938, mfr="nakajima_air",
         en="Type 89 7.7mm", zh="八九式 7.7 毫米机枪",
         modules=["ad_mg_type89_1x", "ad_mg_type89_2x"], prev="mg17",
         desc_en="Japanese Army 7.7mm guns recovered from captured aircraft.",
         desc_zh="从缴获日机上拆用的日本陆军 7.7 毫米机枪。"),
    dict(key="shvak20", x=16, year=1940, mfr="lavochkin_air",
         en="ShVAK 20mm", zh="ShVAK 20 毫米机关炮",
         modules=["ad_cannon_shvak20_1x", "ad_cannon_shvak20_2x", "ad_cannon_shvak20_3x"], prev="m2",
         desc_en="The ShVAK cannon was the standard Soviet 20mm aircraft weapon.",
         desc_zh="ShVAK 是苏联标准的 20 毫米航空机关炮。"),
    dict(key="ubs", x=16, year=1941, mfr="polikarpov_air",
         en="Berezin UB 12.7mm", zh="别列津 UB 12.7 毫米机枪",
         modules=["ad_mg_ubs_1x", "ad_mg_ubs_2x"], prev="shvak20",
         desc_en="The UBS heavy machine gun replaced ShKAS in late-war Soviet fighters.",
         desc_zh="UBS 重机枪在战争后期取代 ShKAS 装备苏制战斗机。"),
    dict(key="type99", x=16, year=1941, mfr="mitsubishi_air",
         en="Type 99 20mm", zh="九九式 20 毫米机关炮",
         modules=["ad_cannon_type99_2x", "ad_cannon_type99_3x", "ad_cannon_type99_4x",
                  "ad_defense_cannon_type99_1x"], prev="type89",
         desc_en="The Type 99 cannon was the main armament of Zero and Hayabusa fighters.",
         desc_zh="九九式机关炮是零式与一式战的主要武器。"),
    dict(key="hispano", x=16, year=1943, mfr="de_havilland_air",
         en="Hispano 20mm", zh="西斯潘诺 20 毫米机关炮",
         modules=["ad_cannon_hispano_1_1x", "ad_cannon_hispano_1_2x", "ad_cannon_hispano_1_4x"], prev="type99",
         desc_en="British-built Hispano cannon armed the Mosquito night and strike variants.",
         desc_zh="英制西斯潘诺机关炮装备蚊式夜间与攻击型。"),
    dict(key="ho103", x=16, year=1944, mfr="kawasaki_air",
         en="Ho-103 12.7mm", zh="Ho-103 12.7 毫米机枪",
         modules=["ad_mg_ho103_1x", "ad_mg_ho103_2x"], prev="hispano",
         desc_en="The Ho-103 heavy machine gun armed late Japanese Army fighters.",
         desc_zh="Ho-103 重机枪装备日军后期战斗机。"),
    dict(key="ns23", x=16, year=1945, mfr="ilyushin_air",
         en="NS-23 23mm", zh="NS-23 23 毫米机关炮",
         modules=["ad_cannon_ns23_1x", "ad_cannon_ns23_2x", "ad_cannon_ns23_4x"], prev="ho103",
         desc_en="The NS-23 became the standard jet-age Soviet cannon, arming the Il-10 and MiG-9.",
         desc_zh="NS-23 成为喷气时代苏联标准机炮，装备伊尔-10 与米格-9。"),
]

# --------------------------------------------------------------------------
# Bombs / rockets / ordnance
# --------------------------------------------------------------------------
ORDNANCE = [
    dict(key="fab100", x=20, year=1937, mfr="tupolev_air",
         en="FAB-100 Bomb", zh="FAB-100 航空炸弹",
         modules=["ad_bomb_fab100_1x", "ad_baybomb_fab100_2x", "ad_baybomb_fab100_4x"], prev=None,
         desc_en="Soviet 100 kg general-purpose bomb used by SB and DB-3 bombers.",
         desc_zh="苏制 100 公斤通用航空炸弹，供 SB 与 DB-3 使用。"),
    dict(key="ao10", x=20, year=1938, mfr="polikarpov_air",
         en="AO-10 Fragmentation Bomb", zh="AO-10 杀伤炸弹",
         modules=["ad_bomb_ao10_1x", "ad_bomb_ao10_2x", "ad_bomb_ao10_4x"], prev="fab100",
         desc_en="Light fragmentation bombs for anti-personnel attacks by Polikarpov fighters.",
         desc_zh="轻型杀伤炸弹，用于波利卡波夫战斗机的对地攻击。"),
    dict(key="fab250", x=20, year=1938, mfr="ilyushin_air",
         en="FAB-250 Bomb", zh="FAB-250 航空炸弹",
         modules=["ad_baybomb_fab250_2x", "ad_baybomb_fab250_4x"], prev="fab100",
         desc_en="The 250 kg FAB became the standard medium bomb of Chinese bombers.",
         desc_zh="250 公斤 FAB 炸弹成为中国轰炸机的标准中型炸弹。"),
    dict(key="fab500", x=20, year=1941, mfr="ilyushin_air",
         en="FAB-500 Bomb", zh="FAB-500 航空炸弹",
         modules=["ad_baybomb_fab500_1x", "ad_baybomb_fab500_2x"], prev="fab250",
         desc_en="Heavy 500 kg bombs for attacks on ports and railway junctions.",
         desc_zh="500 公斤重型炸弹，用于攻击港口与铁路枢纽。"),
    dict(key="anm30", x=20, year=1942, mfr="north_american_air",
         en="AN-M30 100 lb Bomb", zh="AN-M30 100 磅炸弹",
         modules=["ad_bomb_anm30_1x", "ad_bomb_anm30_2x", "ad_bomb_anm30_4x",
                  "ad_baybomb_anm30_1x", "ad_baybomb_anm30_2x", "ad_baybomb_anm30_4x"], prev="fab500",
         desc_en="American 100 lb general-purpose bombs for lend-lease aircraft.",
         desc_zh="美制 100 磅通用炸弹，供租借法案机型使用。"),
    dict(key="rs82", x=20, year=1943, mfr="polikarpov_air",
         en="RS-82 Rocket", zh="RS-82 火箭弹",
         modules=["ad_rocket_rs82_1x", "ad_rocket_rs82_2x", "ad_rocket_rs82_4x"], prev="anm30",
         desc_en="Soviet 82mm air-to-ground rockets used against columns and shipping.",
         desc_zh="苏制 82 毫米空对地火箭弹，用于打击行军纵队与船只。"),
    dict(key="type92", x=20, year=1942, mfr="mitsubishi_air",
         en="Type 92 250 kg Bomb", zh="九二式 250 公斤炸弹",
         modules=["ad_baybomb_a_type92_250kg", "ad_baybomb_a_type92_250kg_2x",
                  "ad_baybomb_a_type92_250kg_4x"], prev="anm30",
         desc_en="Japanese 250 kg bombs recovered for use on captured bombers.",
         desc_zh="缴获的日本 250 公斤炸弹，用于缴获的轰炸机。"),
    dict(key="anm57", x=20, year=1943, mfr="consolidated_air",
         en="AN-M57 250 lb Bomb", zh="AN-M57 250 磅炸弹",
         modules=["ad_bomb_anm57_1x", "ad_bomb_anm57_2x", "ad_bomb_anm57_4x",
                  "ad_baybomb_anm57_1x", "ad_baybomb_anm57_2x", "ad_baybomb_anm57_4x"], prev="type92",
         desc_en="The 250 lb AN-M57 was the workhorse bomb of the China theatre.",
         desc_zh="250 磅 AN-M57 是中国战场的通用主力炸弹。"),
    dict(key="hvar", x=20, year=1944, mfr="republic_air",
         en="5-inch HVAR Rocket", zh="5 英寸 HVAR 火箭弹",
         modules=["ad_rocket_hvar_2x", "ad_rocket_hvar_4x", "ad_rocket_hvar_6x"], prev="anm57",
         desc_en="High-velocity aircraft rockets gave late-war fighters a powerful anti-ship punch.",
         desc_zh="高速航空火箭弹为战争后期战斗机提供了强大的反舰火力。"),
]
