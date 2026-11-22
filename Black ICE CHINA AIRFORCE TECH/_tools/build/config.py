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
MOD_VERSION = "0.1.0"
MOD_NAME_CN = "黑冰：中系飞机科技树"
MOD_NAME_EN = "Black ICE Chinese Aircraft Tech Tree"
SUPPORTED_VERSION = "1.20.*"
DEPENDENCIES = [
    "Blackice HOI IV TEST",
    "BlackICE Aircraft Designer",
    "黑冰：中国国民革命军坦克科技 Black ICE CHINA TANK TECH",
]
