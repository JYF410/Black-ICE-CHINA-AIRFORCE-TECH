# 黑冰：中系飞机科技树

**Black ICE: Chinese Aircraft Tech Tree** — 为《钢铁雄心 IV》黑冰（Black ICE）与 **BlackICE Aircraft Designer** 制作的子模组，给中国（CHI / PRC 及其内战分裂政权）提供独立的「中国空军」科技标签页。

参考对象：
- 子模组结构：`3808452657 BlackICE Aircraft Designer`（`descriptor.mod` + `common/` + `interface/` + `gfx/` + `localisation/` + `history/` + `events/`）。
- 机型取材：`战争雷霆中系空军科技树参考.png`（中系 I–V 级线），并按 1935–1947 年实际入华时间排序。

---

## 1. 目录结构

```
中系飞机科技树/
├─ descriptor.mod                                  # 模组自身声明（依赖黑冰 + BIAD + 中国坦克科技）
├─ thumbnail.png                                   # 512×512 封面
├─ common/
│  ├─ technologies/CHI_air.txt                     # 76 项科技：35 机型 + 21 发动机 + 11 枪炮 + 9 炸弹火箭
│  ├─ technology_tags/zz_CHI_air_technology.txt    # 注册 chinaair_folder；对中国隐藏通用空军页
│  ├─ scripted_guis/BI_tech_queue_china_air.txt    # 黑冰自定义科技页的文件夹块（必需）
│  ├─ scripted_effects/zz_CHI_air_research_arrays.txt   # 研究数组注册（脚本效果版本）
│  ├─ scripted_triggers/zz_CHI_air_triggers.txt    # 给其它模组复用的触发器
│  └─ on_actions/
│     ├─ zz_CHI_air_startup.txt                    # 开局给 CHI / PRC 挂 CHI_air 标志
│     └─ zz_CHI_air_array_gen.txt                  # 研究数组注册（on_startup 内联版本）
├─ history/units/zz_CHI_air_research_array_generation.txt  # 兜底入口（instant_effect）
├─ interface/
│  ├─ chi_air_technology.gfx                       # 每项科技的 _medium 图标 + 标签页按钮 sprite
│  └─ countrytechtreeview.gui                      # 在原版科技树界面中插入「中国空军」页
├─ gfx/interface/techtree/techtree_china_air_tab.tga  # 标签页按钮（2 帧：常态/选中）
├─ localisation/
│  ├─ english/chi_air_l_english.yml
│  └─ simp_chinese/chi_air_l_simp_chinese.yml
├─ docs/
│  ├─ 模组架构说明.md                                # 架构 / 扩展指南 / 常见坑
│  └─ 科技树预览.png                                 # 离线布局预览（非游戏素材）
├─ _install/                                        # 启动器 .mod 文件与备用界面文件
└─ _tools/                                          # 生成、校验、安装脚本（不参与游戏加载）
   ├─ install.ps1                                   # 一键安装：ASCII 联接 + 启动器 .mod
   ├─ validate.py                                   # 静态校验
   └─ build/                                        # config.py / data_chi.py / make.py …
```

`_tools/` 是本项目的构建工具链：从黑冰 / BIAD 的 `.gfx`、`common/` 中抽取真实装备、模块、图标与本地化，再生成上述文件并做静态校验。

**日常只需要记两条命令**：

```powershell
python _tools/build/make.py all      # 全量重建（科技/数组/图标/预览）+ 自动校验
python _tools/validate.py            # 只跑静态校验（0 error 才算通过）
```

内容数据只写在 [_tools/build/data_chi.py](_tools/build/data_chi.py)，全局常量在 [_tools/build/config.py](_tools/build/config.py)；
扩展方法与文件职责见 **[docs/模组架构说明.md](docs/模组架构说明.md)**。

---

## 2. 科技树布局

`chinaair_folder` 内 1 格 = 70 像素，纵向 2 行 = 1 年（1935 = 第 0 行）。

| 列 x | 内容 |
|---|---|
| 0 | 美制发动机（R-1820 / V-1710 / R-2800 / V-1650） |
| 2 | 美制多发与喷气（R-2600 / R-1830 / J33） |
| 4 | 苏制单发（M-25 / M-62 / M-82 / AM-42） |
| 6 | 苏制多发与喷气（M-103 / M-34 / RD-20） |
| 8 | 日制发动机（寿 / 荣 / 誉 / 火星） |
| 12 | 德制与英制（BMW 132 / BMW VI / 梅林 XX） |
| 16 | 航空枪炮（勃朗宁、ShKAS、ShVAK、九九式、NS-23 等） |
| 20 | 炸弹与火箭（FAB、AN-M、九二式、RS-82、HVAR） |
| 26 | 战斗机主线 |
| 30 | 截击机 / 缴获机 / 后期喷气 |
| 34 | 攻击机（强击机） |
| 38 | 轰炸机 |
| 42 | 支援（侦察 / 运输 / 水上巡逻） |

### 机型一览（按入华年份）

| 年份 | 战斗机 | 截击/缴获 | 攻击机 | 轰炸机 | 支援 |
|---|---|---|---|---|---|
| 1936 | 霍克 III | | 伽马 2E | He 111A | |
| 1937 | 伊-15 比斯 | | Hs 123 | SB 2M | 九七式司侦 |
| 1938 | 伊-16 10 型 | 九七式战 | 伏尔梯 A-19 | | |
| 1939 | | 伊-153 | | BR.20 | |
| 1940 | 伊-16 24 型 | | | DB-3 | |
| 1941 | P-40B | 一式战二型 | | | |
| 1942 | P-40E | 零战二一型 | | B-25C | PBY-5 / C-47 |
| 1943 | P-47D | 三式战一型 | | 图-2 | F-5 |
| 1944 | P-51D | 四式战一型 | 蚊 FB Mk VI | B-24J | 蚊 PR Mk IX |
| 1945 | | | 伊尔-10 | 一式陆攻二二型 | |
| 1946 | P-80A | 拉-9 | | | |
| 1947 | | 米格-9 | | | |

所有机型都直接引用 **BlackICE Aircraft Designer 已有的机体原型**（`ad_*_equipment_*`），因此自带 BIAD 的完整模型、图标、模块槽与数据平衡；本模组只负责「中国什么时候能拿到它」以及对应的发动机 / 武器 / 挂载科技。

---

## 2.5 黑冰科技页的注册机制（关键，别漏）

黑冰的科技页**不是**原版那套「gridbox + folder position」直接渲染，而是用 `common/scripted_guis/BI_research_scripted_gui.txt`
里的脚本界面驱动：它遍历 `global.<folder>` 数组，按 `global.tech_x@<tech>` / `tech_y@<tech>` 的像素坐标摆图标，
再读 `tech_cost` / `tech_date` / `tech_dependents@` 决定研究按钮与前置连线。

所以新增科技文件夹，除了 `.gui` 里要有同名 container，还必须：

1. **`common/scripted_guis/BI_tech_queue_<folder>.txt`**：复制 BIAD 的一个国家空军块，`parent_window_name` 改成你的 folder 名，
   块内 `global.<folder>` 全部替换。本模组的 [BI_tech_queue_china_air.txt](common/scripted_guis/BI_tech_queue_china_air.txt) 由 `luftwaffe_folder` 块改名派生。
2. **研究数组**：每项科技写 5 行——
   ```
   add_to_array = { global.chinaair_folder = token:<tech> }
   set_variable = { global.tech_x@<tech> = <像素x> }
   set_variable = { global.tech_y@<tech> = <像素y> }
   set_variable = { global.tech_cost@<tech> = <成本×100> }
   set_variable = { global.tech_date@<tech> = <年份> }
   ```
   有前置的再加 `global.tech_dependents@<前置>` 画箭头。
   像素映射（从 BIAD 的数组文件与坦克子模反推）：**`tech_x = 327 + 列x × 70`，`tech_y = 165 + 行y × 70`**。

本模组用 [build_arrays.py](_tools/build/build_arrays.py) 自动生成三个入口：
`scripted_effects`（正式调用）+ `on_actions`（on_startup 无作用域，必须内联）+ `history/units`（黑冰 replace_path 后的兜底），
并用 `global.CHI_air_arrays_done` 保证只跑一次。

---

## 3. 依赖与加载顺序

`descriptor.mod` 中声明：

```
Blackice HOI IV TEST
BlackICE Aircraft Designer
黑冰：中国国民革命军坦克科技 Black ICE CHINA TANK TECH
```

- 必须启用 **黑冰本体** 与 **BlackICE Aircraft Designer**（机体原型、模块、共享组件科技都来自它们）。
- 第三个依赖用于 **界面合并**：本模组的 `countrytechtreeview.gui` 是在「中国坦克科技」子模的界面文件基础上追加「中国空军」页生成的，这样两边的科技页能同时存在。若不使用坦克子模，请把依赖行删掉，并把 `interface/countrytechtreeview.gui` 换成基于 BIAD 原版界面的版本（重新运行 `_tools/build/build_chi.py` 时会自动优先使用坦克子模的界面作为底稿；把坦克模组移出后再跑一次即可）。
- 加载顺序（启动器从左到右，后者覆盖前者）：
  `黑冰本体 → BlackICE Aircraft Designer → 中国坦克科技 → 本模组`。

---

## 4. 安装

**推荐：一条命令**

```powershell
powershell -ExecutionPolicy Bypass -File _tools\install.ps1
```

它会做两件事：

1. 在 `D:/Steam/steamapps/workshop/content/394360/` 下建 **ASCII 名目录联接** `chi_air_tech` 指向本文件夹
   （游戏对含中文的 mod `path` 兼容性差，会静默跳过整个模组）；
2. 在 `文档/Paradox Interactive/Hearts of Iron IV/mod/` 写 `blackice_chi_air_tech.mod`，`path` 指向该联接。

之后在启动器 → 模组里勾选「黑冰：中系飞机科技树」（排在坦克科技之后）即可。

**手动安装**（等价）：

1. 建联接：`New-Item -ItemType Junction -Path "...\394360\chi_air_tech" -Target "...\394360\中系飞机科技树"`
2. 写 `.mod`（`_install/blackice_chi_air_tech.mod` 是模板），**`path` 必须是 ASCII 路径**：
   ```
   path="D:/Steam/steamapps/workshop/content/394360/chi_air_tech"
   ```
3. 启动器勾选本模组，进入游戏选择中国（CHI）或中共（PRC），空军栏应出现「中国空军」页。

安装完成后可在 `logs/system.log` 里确认 `Active Mod Count` 比之前 +1 且出现
`Active Mod: 黑冰：中系飞机科技树…`。

---

## 5. 校验状态

### 5.1 静态校验（`_tools/validate.py`）

当前结果：**0 error / 0 warning**，覆盖：

- 文件括号配对、`technologies` 根节点、folder 结构；
- 76 项科技 id 与父模组无冲突、格子坐标无重叠；
- `enable_equipments` / `enable_equipment_modules` 全部在 BIAD / 黑冰中真实存在；
- `path.leads_to_tech`、`dependencies` 目标存在；path 不重复指向同一科技；依赖图无环、13 个起始科技可到达全部 76 项；
- `categories` 全部在黑冰 `technology_tags` 的合法分类表中；
- 每项科技在中英文里都有主键，并有 `_desc`；
- 每项科技都有 `<tech_id>_medium` 图标 sprite，且贴图文件真实存在；
- GUI 中每项科技都有 `<tech_id>_tree` gridbox（76 个，与科技集合完全相等），文件夹容器与标签按钮各只有一份；
- 标签页贴图存在（TGA 364×61，2 帧）；
- **必需槽位覆盖检查（59 项）**：每架飞机的 `ad_airforce_powerplant`、`ad_airforce_frame_config` 等 `required = yes` 槽位，都能在本科技树内找到已解锁的模块——即飞机造得出来，不会出现「有飞机没发动机」。

另外用历史 `error.log` 反向确认了 gridbox 规则：日志里确有
`Found no grid box for tech tech_trm_armour_construction_cast_sov` 一类报错（来自坦克子模自身漏配的格子），
说明「每个科技必须有 `<tech_id>_tree` gridbox」这条硬性要求判断正确，漏配只导致该科技不显示、不会崩溃。

### 5.2 游戏内加载验证（部分完成）

**关键发现：本模组此前根本没有被游戏算作启用。** `logs/system.log` 里是
`Active Mod Count: 37`（不是 38），说明游戏在启动时跳过了本模组；因此前面看到的
「中国空军」页不存在、科技页仍是通用空军页，不能当成模组内容有问题——它压根没加载。

嫌疑最大的是 **`.mod` 的 `path` 含中文目录名**。已做的处理：
在 `D:\Steam\steamapps\workshop\content\394360\` 下建了一个 ASCII 目录联接
`chi_air_tech` → `中系飞机科技树`，并把 `Documents/.../mod/blackice_chi_air_tech.mod` 的
`path` 指到 `.../394360/chi_air_tech`。下一次启动应先确认 `system.log` 出现
`Active Mod Count: 38` 与 `Active Mod: 黑冰：中系飞机科技树…`。

其它已确认的事实：

- 2026-11-22 17:56 有一次完整加载（`Loaded 13414 provinces`、`Executing History … 1936.1.1.12`），
  该次 `error.log` 225 万字节里匹配 `ad_chi` / `chinaair` / `CHI_air` 的行数为 0；
- 18:08 那次续玩玩家存档，空军页是黑冰通用页，已存为对照基线：
  [docs/基线_中国通用空军页.png](docs/基线_中国通用空军页.png)；
- 直接运行 `hoi4.exe` 会 `0xc0000005` 崩溃（必须由 Paradox 启动器拉起）；
- 本机 Steam 客户端不稳定：`steamwebhelper.exe` 在 `libcef.dll` 崩溃（`0xc0000409` / BEX64），
  启动后 1–2 分钟即退出，导致「启动器 → 游戏」这条链路时好时坏。

验证只需一步：**启动器里勾选「黑冰：中系飞机科技树」（排在坦克科技之后）→ 启动 → 读存档 →
打开科技界面 → 空军栏应出现「中国空军」页，且通用空军页消失**。
也可以运行下面的一键脚本（会临时启用模组、启动、抓日志、还原启用列表）：

```powershell
powershell -ExecutionPolicy Bypass -File _tools\verify_in_game.ps1
```

脚本会临时启用模组、以 `-debug_mode` 启动游戏、抓取 `ad_chi|chinaair|CHI_air` 相关日志与
`Found no grid box / Could not find sprite / Unknown effect` 等关键字，最后还原启用列表，
报告写入 `_tools/state/ingame_report.txt`。

另外 `common/on_actions/zz_CHI_air_startup.txt` 里保留了一行诊断日志：

```
log = "CHI_AIR_TREE: CHI_air granted to [THIS.GetTag]"
```

游戏启动后 `logs/game.log` 出现 `CHI_AIR_TREE:` 即证明模组的 on_actions 已生效（可用来快速判断模组是否真的被加载）。

---

## 6. 已知限制

- **没有 F-86F / 米格-15 / 轰-5**：这三类在 BIAD 现有的机体原型里不存在（BIAD 的喷气线止于 P-80A 与米格-9），要新增就必须自制机体、模块与图标，留作 v0.2。
- **CW-21、P-66、银河（P1Y）** 同样没有现成机体原型，用同期可用机型替代（如 BR.20、四式战等）。
- 缴获日机线（九七式战 / 一式战 / 零战 / 三式战 / 四式战 / 一式陆攻）在历史上属于「缴获与评估」，模组里作为可研发科技处理，属于游戏性折中。
- 覆盖了 `interface/countrytechtreeview.gui`。黑冰或 BIAD 大版本更新界面结构后，需要重跑 `_tools/build/build_chi.py` 重新合并。
- 启用任何模组都会禁用成就。

---

## 7. 后续可做

已经补掉的：黑冰自定义科技页的注册层（`common/scripted_guis` 文件夹块 + 研究数组全局变量），见 2.5 节。

还剩的工作，按优先级：

1. **游戏内验证**（唯一阻塞项）：先在 `logs/system.log` 确认 `Active Mod Count: 38` 与
   `Active Mod: 黑冰：中系飞机科技树…`，再看空军页是否被「中国空军」替换、格子/连线/研究按钮是否正常。
2. **相机校对**：确认 `tech_x/tech_y` 像素映射（327 + 列×70 / 165 + 行×70）在 4000×2600 容器里的观感，
   必要时微调原点或行距；确认箭头（`tech_dependents`）方向正确。
3. **兼容性**：分别测「有坦克子模」和「无坦克子模」两套 `countrytechtreeview.gui`（后者用 `_install/countrytechtreeview.gui.biad_base`）。
4. **发布准备**：更新 `thumbnail.png`、加 `remote_file_id`、写创意工坊说明与更新日志。
5. **内容扩展 v0.2**：F-86F、米格-15、轰-5 的自制机体原型（含 frame_config 模块与图标）；
   CW-21、P-66、银河（P1Y）；国产发动机/武器线细化（按厂牌分叉）。
6. **AI**：为 CHI 增加 air AI 策略与 `ai_will_do` 调优，避免 AI 只造步兵；确认 AI 会研究本树并创建变体。
7. **联动**：与「黑冰：东亚补充」等国策模组联动，通过国策解锁 `CHI_air` 或额外科技。
