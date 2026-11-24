# -*- coding: utf-8 -*-
"""中系飞机科技树 —— 构建配置（单一事实来源）

所有"会变的常量"集中在这里：模组路径、父模组路径、文件夹名、国家标志、
科技网格的像素映射、年份布局。改 folder 名或换机器时只改这个文件。
"""

# ---------------------------------------------------------------- 路径
MOD = r"D:\Steam\steamapps\workshop\content\394360\中系飞机科技树"

# 父模组（按加载顺序：黑冰本体 -> BIAD -> 中国坦克科技）
BI = r"D:\Steam\steamapps\workshop\content\394360\1851181613"
BIAD = r"D:\Steam\steamapps\workshop\content\394360\3808452657"
TANK = r"D:\Steam\steamapps\workshop\content\394360\3463196432"

# 安装用：ASCII 目录联接（游戏对含中文的 mod path 兼容性不佳）
MOD_LINK = r"D:\Steam\steamapps\workshop\content\394360\chi_air_tech"
MOD_FILE_NAME = "blackice_chi_air_tech.mod"

# ---------------------------------------------------------------- 标识
FOLDER = "chinaair_folder"          # 科技文件夹 / GUI 容器名
FLAG = "CHI_air"                    # 国家标志：拥有该标志即显示本科技页
ARRAY_FLAG = "CHI_air_arrays_done"  # 研究数组只注册一次的全局标志
ARRAY_EFFECT = "CHI_air_build_research_arrays"
LOG_MARKER = "CHI_AIR_TREE"

# 哪些国家算"中系"
CHINESE_TAGS = ("CHI", "PRC")

# ---------------------------------------------------------------- 布局
# 科技网格：1 格 = 70px；每年 2 行（与 BIAD 国家空军树一致）
SLOT = 70
YEAR_BASE = 1935
YEAR_STEP = 2

# 文件夹坐标 -> 黑冰自定义科技页的像素坐标
# 由 BIAD 的 ad_research_array_generation.txt 与坦克子模反推
PIXEL_ORIGIN_X = 327
PIXEL_ORIGIN_Y = 165

# 科技页容器尺寸（interface/countrytechtreeview.gui）
CANVAS_W = 4000
CANVAS_H = 2600

# 列定义：名字 -> 文件夹 x 坐标
COLUMNS = {
    "engine_usa": 0,
    "engine_usa_multi": 2,
    "engine_sov": 4,
    "engine_sov_multi": 6,
    "engine_jap": 8,
    "engine_other": 12,
    "gun": 16,
    "ordnance": 20,
    "fighter": 26,
    "interceptor": 30,
    "cas": 34,
    "bomber": 38,
    "support": 42,
}

# ---------------------------------------------------------------- 元数据
MOD_VERSION = "1.0.0"
MOD_NAME_CN = "黑冰：中系飞机科技树"
MOD_NAME_EN = "Black ICE Chinese Aircraft Tech Tree"
SUPPORTED_VERSION = "1.20.*"
DEPENDENCIES = [
    "Blackice HOI IV TEST",
    "BlackICE Aircraft Designer",
    "黑冰：中国国民革命军坦克科技 Black ICE CHINA TANK TECH",
]

# ---------------------------------------------------------------- 诊断开关
# 排查「科技树窗口闪一下打不开」时的二分开关：
#   HIDE_GENERIC_AIR = False 时不重定义 air_techs_folder（中系会同时有两个空军页），
#   用于判断问题是否出在"隐藏通用空军页"这一步。
HIDE_GENERIC_AIR = False

# 文件夹可用性判定：True 只用 CHI_air 标志（与 BIAD 写法一致），
# False 额外允许 original_tag = CHI/PRC。
AVAILABLE_BY_FLAG_ONLY = True
# ---------------------------------------------------------------- 提示事件
# 与坦克科技子模同款：科研界面会缓存布局，首次打开后科技连线/箭头可能不显示，
# 需要存档再读档一次。开一个新局时弹一次提示（仅玩家）。
TIP_EVENT_ENABLED = True
TIP_EVENT_ID = "CHI_air_unlock.1"
TIP_EVENT_NAMESPACE = "CHI_air_unlock"
TIP_FLAG = "CHI_air_unlock_shown"

# 「+」请求页签：解锁前显示 + 页，满足条件点击后授予 CHI_air
REQUEST_FOLDER = "chinaair_request_folder"
# 0.2.0 的"独立请求页文件夹"方案会让引擎报 Window not found、整个科技树打不开，
# 关掉它，改为后续用 scripted GUI 覆盖层实现「+」。
REQUEST_GATE = False
# 中系候选标志：开局给 CHI/PRC 挂上，用于显示「+」请求页（避免在 technology_folders 里用 original_tag）
CANDIDATE_FLAG = "CHI_air_candidate"

# 坦克子模的文件夹：即使坦克子模没启用也注册一份（条件相同），
# 这样它就是「未解锁」而不是「文件夹不存在」，页签自动隐藏，不会留死页签。
TANK_FOLDER = "trm_armour_chi_folder"
TANK_FLAG = "CHI_armor"
# ---------------------------------------------------------------- 页签图标
# 用户自制的中国空军页签贴图（2 帧、每帧 182x61，可直接用 DDS）。
# 文件存在时优先使用；不存在时回退到程序生成的占位 TGA。
TAB_TEXTURE = "gfx/interface/techtree/techtree_chiair_tab.dds"
TAB_FRAMES = 2
# 占位图只在用户尚未提供自制页签时生成；现已使用自制 DDS，不再生成 TGA
GENERATE_TAB_PLACEHOLDER = False
# ---------------------------------------------------------------- 装甲请求提示修正
# 黑冰的「请求外国装甲科技」触发器里有一句 CHI 专属条件（对美请求需完成国策），
# 它会出现在所有捐赠国图标的提示里。开启后我们覆盖该 block，把这句话包进
# hidden_trigger，逻辑不变、提示里不再显示。
ARMOR_TT_FIX = True
# ---------------------------------------------------------------- 诊断开关
# True 时 countrytechtreeview.gui 原样输出坦克子模版本（不插入中国空军页），
# 用于判断坦克页图标丢失是否由我们的 gui 改动引起。
GUI_MINIMAL = False