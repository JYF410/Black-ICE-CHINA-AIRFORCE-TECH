# 更新日志 / Changelog

## 0.6.1 — 2026-11-27 · 天数/箭头定位定版

**实测通过**：天数与箭头位置正常。

- 所有布局坐标集中到 `_tools/build/config.py`：
  - `LAYOUT_SHIFT_X/Y`：图标 + 箭头 + 天数 + 气泡 + 标题一起平移；
  - `GRIDBOX_X/Y`、`ITEM_POS_LARGE/SMALL`：格子与条目模板的基准/偏移；
  - `PIXEL_ORIGIN_X/Y`：箭头/天数/气泡锚点；
  - `DAYS_LARGE_DX/DY`、`DAYS_SMALL_DX/DY`：大格/小格天数分别可调；
  - `COLUMNS`、`YEAR_STEP`、`CANVAS_W/H`：列距、年距、画布。
- 研究数组给每个科技写 `global.tech_small@`（0=大格 / 1=小格），
  自定义触发器 `CHI_air_time_estimate` 据此分别设置天数位置；黑冰默认触发器保留兜底。
- 此前 0.5.0–0.5.7 的反复偏移问题已定位：图标（gridbox + 条目模板）与
  箭头/天数/气泡（`PIXEL_ORIGIN_X + 70×列`）是两套线性基准，必须用同一常量对齐；
  现在两者共用 `LAYOUT_SHIFT`，调间距不会再互相跑偏。
- 版本 0.6.1。

## 0.6.0 — 2026-11-27

- 新增 `LAYOUT_SHIFT_X/Y`，图标与箭头/天数/气泡/标题统一平移。

## 0.5.9 — 2026-11-27

- 布局旋钮集中到 `config.py`（`GRIDBOX_X/Y`、`ITEM_POS_LARGE/SMALL`）。

## 0.5.2 — 2026-11-27

- **回退 0.5.0/0.5.1 的「研究天数」改动**：自定义触发器 `CHI_air_time_estimate` 放进
  `triggers` 块后整个触发器块失效，导致天数全部不显示。已改回黑冰默认的
  `ui_research_time_estimate = yes`，天数恢复原位置（图标左侧、箭头左边）。
- 间距调整保留（机种列 6 格 / 每年 280px / 同年错行 140px）。
- 版本 0.5.2。

## 0.5.0 — 2026-11-27 · 间距与「研究天数」位置

针对你截图里的 5 个问题：

1. **横向太挤**：机种列间距从 4 格（280px）加到 6 格（420px）：
   战斗机 26 / 重型战斗机 32 / 舰载战斗机 36 / 近距支援机 40 / 轻型轰炸机 44 /
   中型轰炸机 48 / 重型轰炸机 52 / 水上飞机 56 / 侦察机 60 / 运输机 64；
   画布加宽到 5600×3800。
2. **纵向重叠**：`YEAR_STEP` 2 → 4（每年 280px），同年第二架的错行量 70 → 140px，
   图标高 84px，上下留 56px 间隙。
3. **「研究天数」位置**：新建 `CHI_air_time_estimate` 触发器替代黑冰默认的
   `ui_research_time_estimate`——大格（203×84）放右下（+52/+60），
   小格（72×72）贴小格右下（+6/+46）；研究数组额外给配件科技写 `global.tech_small@` 标记。
4. **顶部标题居中**：列标题 x 偏移从 `-110` 改为 `-20`（按 240 宽、居中计算），
   仍为 `hoi_18mbs`、`format = centre`。
5. 版本 0.5.0。

## 0.4.0 — 2026-11-27 · 按 PPT 重写机树 + 列标题

按你改好的 `科技树布局_可编辑.pptx` 重写中国空军树，并在科研面板顶端加上各列标题。

**列标题（19 个）**：美制发动机 / 美制多发·喷气 / 苏制单发 / 苏制多发·喷气 /
日制发动机 / 德英发动机 / 航空枪炮 / 航空炸弹 / 火箭·特种炸弹 /
战斗机 / 重型战斗机 / 舰载战斗机 / 近距支援机 / 轻型轰炸机 / 中型轰炸机 /
重型轰炸机 / 水上飞机 / 侦察机 / 运输机。

标题控件参照坦克子模 `countrytechtreeview.gui` 第 23360 行的写法
（`containerWindowType` + `instantTextBoxType`，`font = "hoi_18mbs"`、`format = centre`），
放在 `chinaair_folder` 的 `techtree_stripes` 里，y = 55，逐列居中。

**机种与数量**：32 架作战飞机（原 35 架 → 按 PPT 删除 I-15bis、I-16 10/24、I-153、
九七式战、一式战、三式战、四式战；新增 H-75M、Ki-45、九六舰战、零战三二、V-11、V-12D、
马丁 139WC、蚊式 FB.26）。

**替身说明**（BIAD 无对应原型，用近似机体）：
- 霍克 H-75M → `ad_curtiss_p36_equipment_1`（P-36 同族）
- 伏尔梯 V-11 → `ad_vultee_a19_equipment_1`（V-11 家族）
- 伏尔梯 V-12D → `ad_vultee_a31_equipment_1`（近似）
- CW-21、D.510C：BIAD 无原型，按约定暂不实现。

**列坐标**：战斗机 26 / 重型战斗机 30 / 舰载战斗机 32 / 近距支援机 34 /
轻型轰炸机 36 / 中型轰炸机 38 / 重型轰炸机 40 / 水上飞机 42 / 侦察机 44 / 运输机 46；
炸弹分成 20（炸弹）与 22（火箭/特种）两列。

**其他**：`data_chi.py` 的 AIRFRAMES 全面重写；`config.COLUMNS` 同步；
预览图与 `docs/科技树布局_坐标.csv` 可按需重生成。校验 `error: 0  warn: 0`。版本 0.4.0。

## 0.3.0 — 2026-11-27 · 按机种重排科技树

按黑冰美国/德国空军树的做法，**把中国空军页改成严格按机种纵向分列**，每列只放同一类机型：

| 列 | x | 内容 |
|---|---|---|
| 发动机 | 0/2/4/6/8/12 | 美制单发/双发、苏制单发/双发、日制、德英 |
| 航空枪炮 | 16 | 机枪/机炮 |
| 炸弹火箭 | 20 | 炸弹/火箭 |
| 战斗机 | 26 | 霍克 III、伊-15 比斯、伊-16 10 型、P-40B/E、P-47D、P-51D、九七式战、伊-153、一式战、零战二一、三式战、四式战、拉-9 |
| 截击机 | 30 | 伊-16 24 型 |
| 重型战斗机 | 32 | 蚊式 FB Mk VI |
| 攻击机 | 34 | Hs 123、A-19、伊尔-10 |
| 侦察机 | 36 | 九七式司侦、F-5、蚊式 PR |
| 轻型轰炸机 | 38 | SB 2M、BR.20 |
| 中型轰炸机 | 40 | He 111A、DB-3、B-25C、图-2、一式陆攻 |
| 重型轰炸机 | 42 | B-24J |
| 运输机 | 44 | C-47 |
| 水上飞机 | 46 | PBY-5 |
| 喷气战斗机 | 48 | P-80A、米格-9 |

- `config.COLUMNS` 按黑冰 `@FTR/@INT/@CAS/@TACT_BOMBER/@STRAT_BOMBERS/@TRPT` 的机种划分重写；
- `data_chi.py` 新增 `ROLE_COLUMNS`，逐机归类；同列同年自动错行；**跨列的前置链自动断开**，
  避免斜穿箭头；
- 预览图列标题同步更新（`docs/科技树预览.png`）；
- 校验 `error: 0  warn: 0`；
- 版本 0.3.0。

## 0.2.8 — 2026-11-24

按需求修正元数据：

- `descriptor.mod` 的 `version` 从 `1.0.8` 改为 **`0.2.8`**（`config.MOD_VERSION` 同步）；
- `name` 改为 **「黑冰：中国空军科技 Black ICE CHINA AIRFORCE TECH」**；
- **封面问题的根因**：`make.py all` 每次都会调用 `make_art.make_thumbnail()` 重新生成 `thumbnail.png`，
  把用户提供的封面覆盖掉了。现在新增 `GENERATE_THUMBNAIL = False`，构建不再重绘封面；
- 更新包现在包含 `thumbnail.png`（355KB），解压即可换封面；
- 版本 0.2.8。

## 1.0.8 — 2026-11-24 · 大小格混排确认

中国空军页的大小格混排**已验证成功**（配件小方块 + 飞机大条目），定版。

- 机制三条（缺一不可）：
  1. 科技带 `force_use_small_tech_layout = yes`；
  2. GUI 里该科技只有一个 `<tech>_tree` gridboxtype；
  3. 文件夹级小格底图 6 个 sprite 全部注册（`GFX_technology_chinaair_folder_small_*`）。
- 已写入 `_DSH/科研UI雷区与经验.md` R10.5（含三次踩坑记录，避免以后重犯）；
- `_DSH/定版配置快照.md` 同步更新到 v1.0.8；
- 版本 1.0.8。

## 1.0.7 — 2026-11-24

**找到小格的真正机制**（来自坦克子模的 `interface/countrytechtreeview_CHI.gfx`）：

引擎绘制小格科技时，背景图不是通用的 `GFX_technology_unavailable_item_bg`，而是按文件夹命名去取：

```
GFX_technology_<文件夹>_small_unavailable_item_bg
GFX_technology_<文件夹>_small_available_item_bg
GFX_technology_<文件夹>_small_researched_item_bg
GFX_technology_<文件夹>_small_currently_researching_item_bg
GFX_technology_<文件夹>_special_project_small_unavailable_item_bg
GFX_technology_<文件夹>_special_project_small_available_item_bg
```

之前我们没注册这些图，小格条目就"没有底框"，看起来像图标全部消失。

- 现在 `interface/chi_air_technology.gfx` 已为 `chinaair_folder` 注册上面 6 个 sprite
  （贴图复用黑冰本体的 `tech_trm_*_item_bg.dds`，不依赖坦克子模）；
- 科技仍带 `force_use_small_tech_layout = yes`，gridbox 仍是 `<tech>_tree`；
- 版本 1.0.7。

## 1.0.6 — 2026-11-24

回退 1.0.5：`<tech>_small_tree` 单独存在时条目窗口不生成（配件区又只剩角标），
恢复为所有科技统一 `<tech>_tree`，配件重新可见（大格）。

结论（三次尝试后）：
- `_large_tree` → 不认，条目消失；
- 只给 `_small_tree` → 不认，条目消失；
- `_tree` + `_small_tree` → 按 `_tree` 渲染，大格；
- 即：**本文件夹里引擎没有按 `force_use_small_tech_layout` 切到 `_small_item`**。

后续可选方案见 `_DSH/科研UI雷区与经验.md` 的补充说明。

## 1.0.5 — 2026-11-24

配件小方格（第三次修正，机制终于对上了）：

- 条目模板由 **gridboxtype 名字的后缀**决定：`<tech>_small_tree` → 72×72，`<tech>_tree` → 203×84；
- 每个科技只能有**一个** gridbox。之前我们同时给 `_tree` 和 `_small_tree`，引擎按 `_tree` 渲染成大格；
- 现在 41 项配件科技只输出 `<tech>_small_tree`（黑冰自己的 `tech_trm_ammo_chi_apcr` 就是这样，
  它也只有 `_small_tree` 一个格子）；
- 飞机仍输出 `<tech>_tree`（大格）；
- 校验器按同样规则检查。
- 版本 1.0.5。

## 1.0.4 — 2026-11-24

- 工坊封面换成新图（I-16 与九六舰战空战，512×512 PNG）；
- 打包脚本现在也包含 `thumbnail.png`，解压更新时会一并替换封面；
- 版本 1.0.4。

## 1.0.3 — 2026-11-24

配件小方格（第二次修正）：

- 你说得对，BIAD/坦克子模的同一页里确实大小混排。机制是：
  **`force_use_small_tech_layout = yes` + 每个科技只给一个 `<tech>_tree` 格子**，
  引擎就会改用文件夹的 `_small_item`（72×72）模板；
- 之前我们额外给配件科技加了 `<tech>_small_tree` 格子，反而干扰了判定（按大格渲染）；
  1.0.1 试的 `<tech>_large_tree` 更糟，条目窗口直接不生成；
- 现在所有科技统一只保留 `<tech>_tree`，21 发动机 / 11 枪炮 / 9 挂载应显示为 72×72 小方格；
- 版本 1.0.3。

## 1.0.2 — 2026-11-24

回退 1.0.1（`_large_tree` 导致条目窗口不生成，配件区只剩角标）。版本 1.0.2。

## 1.0.1 — 2026-11-24

界面打磨第一步：**配件科技改小方格**。

- 发现：条目大小不是靠 `<tech>_tree` + `<tech>_small_tree` 决定的，BIAD 的小格科技用的是
  **`<tech>_large_tree` + `<tech>_small_tree`** 这一对命名（`techtree_<文件夹>_item` 203×84 /
  `_small_item` 72×72 两套模板），引擎按这对名字切换。
- 现在 21 发动机 / 11 枪炮 / 9 挂载共 41 项科技输出 `_large_tree` + `_small_tree`；
  35 架飞机仍用 `_tree`（203×84 大条目）。
- `validate.py` 同步放宽：小格科技必须有 `_small_tree`，大格允许 `_tree` 或 `_large_tree`。
- 版本 1.0.1。

## 1.0.0 — 2026-11-24 · 定版

功能与 0.7.6 完全一致，仅版本号标记为定版，并新增维护者文档。

- 事件弹窗：`news_event CHI_air_unlock.2`，标题「中国坦克科技树使用提示」，
  配图 `gfx/event_pictures/chi_armor_tip.dds`（397×153 DXT5）；
- 中国坦克页：坦克子模提供，本模组开局授予 `CHI_armor`，页签在 340（原「+」位置）；
- 中国空军页：`chinaair_folder`，页签 880，76 项科技；
- 新增 `_DSH/` 维护者文档（不参与游戏加载）：
  - `_DSH/README.md` —— 索引与三条硬规则
  - `_DSH/科研UI雷区与经验.md` —— 15 条实测雷区、报错对照、排查顺序
  - `_DSH/定版配置快照.md` —— 定版的常量、文件职责、页签坐标、已知限制
  - `_DSH/发布与更新流程.md` —— 构建/打包/更新副本/诊断开关
- 校验：`error: 0  warn: 0`。

## 0.7.6 — 2026-11-24

终于解决「弹窗不带图」：

- **原因**：黑冰的普通事件窗口（`interface/eventwindow.gui`）里，`event_picture` 控件在
  `top_Window` 里是**注释掉的**（`#iconType name="event_picture"`），所以 `picture = ...` 字段
  在内嵌图标那条路也不行（`£sprite` 在该窗口同样不解析）。
- **做法**：改用 **`news_event`**（报纸式弹窗，黑冰自己的新闻窗口带图片控件 `event_picture`）：
  ```
  news_event = {
      id = CHI_air_unlock.2
      title = CHI_air_unlock.2.t
      desc = CHI_air_unlock.2.d
      picture = GFX_chi_armor_tip
      is_triggered_only = yes
      fire_only_once = yes
      option = { name = CHI_air_unlock.2.a }
  }
  ```
  开局用 `news_event = { id = CHI_air_unlock.2 days = 1 }` 触发，标题/配图/说明齐全。
- 版本 0.7.6。

## 0.7.5 — 2026-11-24

事件配图改用**正文内嵌图标**：

- 去掉 `picture = ...` 字段（黑冰的事件窗口对这个字段不生效，实测不显示）；
- 正文开头加 `£chi_armor_tip`，走黑冰/原版通用的内嵌 sprite 语法（`£<名字>` → `GFX_<名字>`）；
- 配图仍是 `gfx/event_pictures/chi_armor_tip.dds`（你提供的那张，已转 DXT5）；
- 版本 0.7.5。

## 0.7.4 — 2026-11-24

- 把你提供的 DDS 从无压缩 RGBA 转成 **DXT5**，排除纹理格式导致的静默不显示。
- 版本 0.7.4。

## 0.7.2 — 2026-11-24

- 事件配图换成用户提供的 `chi_armor_tip.dds`（397×153，RGBA DDS，与黑冰事件图尺寸一致）；
- 版本 0.7.2。

## 0.7.1 — 2026-11-24

- 事件配图从 TGA 改成 **DDS（DXT5）**，与黑冰原版事件图同格式，避免事件窗口不认 TGA；
- 版本 0.7.1。

## 0.7.0 — 2026-11-24

事件弹窗美化：

- 标题改为 **「中国坦克科技树使用提示」**（英文 `Chinese Armour Tech Tree - Usage Notes`）；
- 新增事件配图：你给的那张坦克照片，裁成原版事件图尺寸 **397×153**（`gfx/event_pictures/chi_armor_tip.tga`），
  在 `interface/chi_air_technology.gfx` 注册为 `GFX_chi_armor_tip`，事件里用 `picture = GFX_chi_armor_tip`；
- 事件窗口布局：标题 → 图片 → 说明文字 → 「明白了」按钮；
- 版本 0.7.0。

## 0.6.4 — 2026-11-24

**不再做「满足条件才显示坦克页」**：科技文件夹可用性一旦在游戏中途翻转（条件满足那一刻），
黑冰科研界面就会整页打不开（0.4.8 / 0.5.x 反复验证）。坦克页从开局就在，
改用**一次性提示事件**解决新玩家的困惑。

- 开局（读档后第 1 天）给中国/中共玩家弹一次：
  > 新的科技页显示提示：「中国空军」与「中国坦克」科技页已经可用。
  > 由于黑冰的科研界面会缓存布局，第一次打开时图标、名字与连线可能不显示。
  > 请先保存游戏并重新载入一次，之后就会恢复正常。
- `CHI_armor_tip_shown` 标志保证每个存档只弹一次；事件 id 复用 `CHI_armor_unlock.1`。
- 版本 0.6.4。

## 0.6.3 — 2026-11-24

- 页签全部回到原坐标；中国坦克页签落在原来「+」的 340 格。
- 因为 0.6.2 起开局就挂 `CHI_armor`，坦克子模自己的 `BI_research_tabs` 覆盖会把
  「请求装甲 +」对中国隐藏，340 格自然空出来，不需要再挤其它页签。
- 版本 0.6.3。

## 0.6.2 — 2026-11-24

- **不再由我们注册 `trm_armour_chi_folder`**（之前的覆盖导致坦克页物品窗口不生成、只剩角标），
  改为 `on_startup` 授予 `CHI_armor`，让坦克子模自己的注册生效。
- 修复坦克页图标/名字/连线丢失。
- 版本 0.6.2。

## 0.6.0 — 2026-11-24

- 保留 0.5.7 那套「能打开 + 坦克页能进」的配置（`original_tag` 静态可用、坦克页签 430、后续右移）；
- **移除我们重复注册的 `GFX_chi_tank_folder_tab`**：坦克子模本身已经定义了这个 sprite，
  重复定义可能让它的 gfx 加载异常，导致坦克页里的图标全部不显示。现在直接使用坦克子模的定义。
- 版本 0.6.0。

## 0.5.9 — 2026-11-24

（未发布）尝试移除重复 sprite、可用性改回 original_tag。

## 0.5.8 — 2026-11-24

**回到 0.3.4 的保守配置**，先把界面稳定性找回来，再一个变量一个变量加：

- 页签位置：**完全不动**（坦克页签留在 340，被 + 覆盖）；
- 坦克文件夹可用性：**只认 `has_country_flag = CHI_armor`**（静态假，等价于坦克页不可见）；
- 历史遗留覆盖文件保持空占位；
- 也就是说：这版预期科研界面一定能打开，但**看不到坦克页**。确认能开之后，
  再单独测「只把坦克文件夹改成可见」这一步，逐步定位到底哪一项在弄崩界面。
- 版本 0.5.8。

## 0.5.7 — 2026-11-24

坦克文件夹可用性改成**只用 `original_tag`**（静态判定）：

```
available = { OR = { original_tag = CHI  original_tag = PRC } }
```

原因：`has_global_flag` / `has_country_flag` 这类标志可能在**科研界面构建之后**才变真，
文件夹可用性中途翻转会让整个科研界面打不开（前面反复踩的就是这个）。`original_tag`
在读档那一刻就确定，不会再翻。

- 中国（含中共）始终能看到坦克科技页（装坦克子模时有内容，没装是空页）；
- 页签布局保持 0.5.5（坦克页签 430，后续 +80）；
- 历史遗留的 3 个覆盖文件改写成空占位，防止旧副本残留生效；
- 版本 0.5.7。

## 0.5.6 — 2026-11-24

- 把历史遗留的 `CHI_air_request.txt` / `zz_CHI_air_armor_request.txt` / `zz_CHI_air_armor_hide.txt`
  改写成空 `scripted_gui = { }` 占位，避免工坊副本里残留的旧覆盖继续生效。
- 版本 0.5.6。

## 0.5.5 — 2026-11-24

- 回到 **0.5.1 那套已验证能打开的布局**：CHI 坦克页签放 430，430 之后的页签 +80；
- 撤掉 0.5.2/0.5.4 两种失败尝试（远右端 1310 = 界面打不开；隐藏「+」= 其容器仍挡住 340 格）；
- 已知代价：`+` 与陆军学说会被挤到视觉边缘（+ 按钮宽 182，压在 345–527 的固有位置上）。
- 版本 0.5.5。

## 0.5.4 — 2026-11-24

- **不再移动任何页签**（0.5.0/0.5.3 的整体右移会让页签丢失，0.5.2 的远右端位置又会打不开界面）。
- 改为：**对中系隐藏黑冰的「请求外国装甲科技」+ 页签**
  （`common/scripted_guis/zz_CHI_air_armor_hide.txt`，在 `visible` 的 `NOT` 里加 `tag = CHI`）。
  那个 + 按钮宽约 182、固定在 (345,6)，正是它压住了 340 格的坦克页签；隐藏它之后，
  CHI 坦克页签在 340 正常显示，其它国家完全不受影响。
- 中国已有静态可见的坦克页，这个请求入口本来就是多余的。
- 版本 0.5.4。

## 0.5.2 — 2026-11-24

- **撤回 0.5.0 的页签整体右移**：右移后部分页签（步兵学说 / 请求装甲 + 等）丢失，
  而且页签条没有真正空闲的插入位，硬挤会连带别的页签消失。
- CHI 坦克页签放到**最右端空闲位 x=1310**（原料页签右侧），其余页签全部回到原坐标，
  恢复原样：步兵学说、请求外国装甲科技 + 都在。
- 坦克页仍然静态可见（0.5.1 的修复保留），点最右侧的中国坦克页签即可进入。
- 版本 0.5.2。

## 0.5.1 — 2026-11-24

修「0.5.0 点不开科研界面」。

- **根因**：`has_global_flag` 是**全局**标志，0.4.9/0.5.0 把它直接写进
  `trm_armour_chi_folder.available`，等于**给全世界每个国家都开了中国坦克页**。
  每个国家的科技视图都会去构建这一页，于是整页崩掉（日志里没有任何 GUI 报错，属于静默失败）。
- **修复**：把全局标志判断收进国家条件里：
  ```
  available = {
      OR = {
          has_country_flag = CHI_armor
          AND = {
              has_global_flag = CHI_research_arrays_done   # 坦克子模存在
              OR = { original_tag = CHI  original_tag = PRC }
          }
      }
  }
  ```
  只有中国（及中共）会看到这一页，其它国家回到原样。
- 版本 0.5.1。

## 0.5.0 — 2026-11-24

页签排版：把 CHI 坦克页签从与黑冰「请求装甲」+ 号重叠的位置（x=340）挪到 **+ 号右边（x=430）**，
后面所有页签顺次右移 80px，互不遮挡。

- 黑冰的 + 按钮固定在 (345, 6)，坦克子模的 CHI 页签原来也在 340，两者完全重叠；
- 新的页签顺序：`… 260 ww1学说 | 430 中国坦克 | +号(345 覆盖区之外) | 510 陆军学说 | 590 海军技术 …`
- 顺移后位置：陆军学说 510 / 海军技术 590 / 海军 690 / 海军学说 770 / 空军技术 860 /
  空军学说 960（各国空军页签与「中国空军」也在 960）/ 空军配件 1050 / 电子 1150 / 工业 1230 / 原料 1310。
- 配合 0.4.9：坦克文件夹静态可见（装着坦克子模就显示），不再依赖请求面板或条件解锁。
- 版本 0.5.0。

## 0.4.9 — 2026-11-24

- **确认**：用「工厂/国策/科技」这类动态条件控制科技文件夹的可用性，会在条件满足的瞬间
  把黑冰科研界面弄崩（和之前隐藏通用空军页是同一类问题）。0.4.8 的自动解锁因此撤掉。
- `trm_armour_chi_folder` 改为**静态可用**：只要坦克子模在，它的坦克科技页就一直在
  （`has_global_flag = CHI_research_arrays_done` / `has_country_flag = CHI_armor`）。
  不再需要点击请求面板，也不会中途翻转导致崩溃。
- 黑冰「请求外国装甲科技」面板保持原版。
- 版本 0.4.9。

### 如果还想要「条件解锁」的观感

正确做法是**保持文件夹常开、给科技本身加 `allow` 条件**（科技可以逐条锁，不会影响界面构建），
例如让坦克底盘科技在满足四条之一前显示为不可研究。这个可以下一版做。

## 0.4.8 — 2026-11-24

放弃「改黑冰请求装甲面板」这条路，改为**条件满足即自动解锁**坦克科技页。

- **为什么放弃**：面板里那面本国旗其实是页签按钮（`request_armor`），它的点击路径在不同 BI
  版本里不稳定；我们的覆盖要么没生效、要么把条件整体换回原版。继续改面板风险高、收益低。
- **现在的做法**：`technology_tags` 里 `trm_armour_chi_folder` 的 `available` 直接写成
  ```
  OR = {
      has_country_flag = CHI_armor
      AND = {
          has_global_flag = CHI_research_arrays_done   # 坦克子模存在时才判定
          OR = { AND = { tank_assembly > 1 engine_assembly > 1 }
                 has_tech = early_tractors
                 has_completed_focus = KMT_chinese_panzers
                 has_completed_focus = KMT_hire_soviet_designer }
      }
  }
  ```
  满足四条之一 → 坦克页签自动出现（重开科研界面或存档读档后可见），**不需要再点任何旗帜**。
- 没装坦克子模时 `CHI_research_arrays_done` 不存在，不会出现空白坦克页。
- 黑冰「请求外国装甲科技」面板恢复为**原版**（我们的覆盖文件已删除），面板行为与原版一致。
- 版本 0.4.8。

## 0.4.5 — 2026-11-24

修「点中国旗帜不生效」。

- **关键发现**：请求页里那面**中国旗帜其实是页签按钮本身**（`request_armor`，图标用
  `[This.GetFlag]` 显示本国国旗），它的点击效果是 `request_armor_click`（展开/收起捐赠国列表），
  不是条目上的 `flag_click`。之前只挂了 `flag_click`，所以点它当然没反应。
- 现在两个入口都挂了分流：
  - `request_armor_click`（点本国旗帜）：满足四条之一 → 直接 `set_country_flag = CHI_armor`
    + 触发「装甲科技研究权已获得」事件；不满足则照旧展开列表；
  - `flag_click`（若某版本把本国也做成条目）：同样直接授予。
- `flag_click_enabled` 恢复为黑冰原版（工厂/好感/许可/政体），所以外国旗帜的前置条件回到原样；
  点击时会写日志 `CHI_ARMOR_TRIGGERED ...` 到 `game.log`。
- 版本 0.4.5。

## 0.4.3 — 2026-11-24

- 外国旗帜恢复「四条前提 + 对方意愿」双重判定（0.4.2 漏掉了四条，导致别国旗只查好感）；
- 点击授予时加一条日志 `CHI_ARMOR_TRIGGERED by <TAG>`，写进 `game.log`，方便确认点击到底有没有触发；
- 版本 0.4.3。

### 排查「点了中国旗没反应」

1. 点任意一面**亮的**旗；
2. 看 `Documents/Paradox Interactive/Hearts of Iron IV/logs/game.log` 是否出现 `CHI_ARMOR_TRIGGERED`；
   - 有 → 授予成功，存档读档后坦克页应出现；
   - 没有 → 点击没触发，把那一刻的 `error.log` 里含 `flag_click` / `CHI_armor` 的行发我。

## 0.4.2 — 2026-11-23

装甲请求面板改成**按国旗分别判定**（之前中国满足条件后所有旗帜一起亮）：

- **中国自己那面旗**：只看四条解锁条件（2 坦克厂 + 2 发动机厂 / 早期拖拉机 / 中国装甲部队 / 聘请苏联设计商）；
- **其它国家的旗**：恢复黑冰的「对方意愿」判定——好感 ≥50 或有生产许可（政体一致性也保留），
  不满足就保持不亮，也就是说中国不能凭空请求别国技术，得先把关系做上去；
- 点击任一已亮的旗帜时，中国仍然直接获得 `CHI_armor`（0.4.1 的直接授予逻辑保留），
  并弹「装甲科技研究权已获得」事件；
- 版本 0.4.2。

## 0.4.1 — 2026-11-23

修「点旗帜没反应、坦克科技页不出现」。

- **原因**：黑冰的 `flag_click` 是把 `blackiceevents.164` 发给**捐赠国**，由对方政府/AI
  决定批不批。中国点谁都要等对方点头，AI 拒绝时看起来就是"点了没反应"。
- **修复**：`flag_click` 按请求国分流——中国点击任意旗帜直接
  `set_country_flag = CHI_armor` 并触发通知事件 `CHI_armor_unlock.1`
  （「装甲科技研究权已获得」，提醒存档再读档刷新科技页）；其它国家仍走黑冰原事件链。
- 说明：中国分支不再检查对方好感/许可，所以满足条件后**所有捐赠国图标会同时变亮**，
  这是预期行为——点任意一个都能生效。
- 版本 0.4.1。

## 0.4.0 — 2026-11-23

装甲请求提示文字排版调整：

- 去掉重复的「中华民国：」前缀（原来提示会出现两次国名）；
- 「满足以下任一条件即可——」改为「需要其中之一：」，与黑冰原提示风格一致；
- 最终显示：
  ```
  需要其中之一：
  · 坦克装配厂 ≥2 且发动机装配厂 ≥2
  · 已完成「早期拖拉机」研究
  · 已完成国策「中国装甲部队」
  · 已完成国策「聘请苏联设计商」
  ```
- 版本 0.4.0。

## 0.3.9 — 2026-11-23

中华民国不再受「好感 ≥50 / 有生产许可 / 政体一致」这条限制（那是黑冰给普通国家设的门槛，
中国自己对自己不存在好感，导致永远激活不了）。

- `flag_click_enabled` 改为按请求国分流：
  ```
  if = { limit = { ROOT = { tag = CHI } }
       ROOT = { custom_trigger_tooltip = { tooltip = CHI_ARMOR_REQ_TT
                  OR = { AND = { tank_assembly > 1 engine_assembly > 1 }
                         has_tech = early_tractors
                         has_completed_focus = KMT_chinese_panzers
                         has_completed_focus = KMT_hire_soviet_designer } } }
  }
  else = { ...黑冰原本的全部条件（生产/好感/许可/政体）... }
  ```
- 其它国家行为完全不变；
- 中国提示里只剩那四条解锁条件，不再出现「关于中华民国的评价至少 50」；
- 版本 0.3.9。

## 0.3.8 — 2026-11-23

中华民国「请求外国装甲科技」门槛按需求改为**四选一**：

```
OR = {
    AND = { tank_assembly > 1  engine_assembly > 1 }   # 坦克装配厂 ≥2 且发动机厂 ≥2
    has_tech = early_tractors                          # 已完成「早期拖拉机」
    has_completed_focus = KMT_chinese_panzers          # 国策「中国装甲部队」
    has_completed_focus = KMT_hire_soviet_designer     # 国策「聘请苏联设计商」
}
```

- 提示文字同步为四行说明（`CHI_ARMOR_REQ_TT`，中英双语）；
- 其它国家仍走黑冰原条件；
- 已核对 `early_tractors`（BI `common/technologies/civillian.txt`）、`KMT_chinese_panzers`、
  `KMT_hire_soviet_designer`（BI `common/national_focus/kmt_KMT.txt`）均存在；
- 版本 0.3.8。

## 0.3.7 — 2026-11-23

放宽中华民国「请求外国装甲科技」的门槛（黑冰原生要求 30 坦克产能 / 6 座装配厂 / 200 辆产量，太严）。

- 覆盖 `BI_request_armor_tab`（`common/scripted_guis/zz_CHI_air_armor_request.txt`），
  按请求国分流：`tag = CHI` 时用下列任一条件即可
  ```
  tank_assembly > 1        # ≥2 座坦克装配厂
  engine_assembly > 0      # ≥1 座发动机装配厂
  any_character = { is_country_leader = yes has_ideology = absolutism }   # 专制主义
  any_character = { is_country_leader = yes has_ideology = despotism }    # 专制统治
  ```
  其它国家仍走黑冰原条件（30 坦克产能 / 6 座装配厂 / 200 辆）。
- 提示文字用 `custom_trigger_tooltip = CHI_ARMOR_REQ_TT` 单行说明，不再展开成一大堆条件。
- 说明：`has_ideology` 是 **CHARACTER** 作用域触发器，不能直接写在国家作用域；
  这里通过 `any_character = { is_country_leader = yes has_ideology = ... }` 绕过去。
- 版本 0.3.7。

## 0.3.4 — 2026-11-23

修正「请求外国装甲科技」提示里到处出现中国前置条件。

> 范围说明：把 BIAD 的 58 项配件科技迁进中国空军页**已取消**——那项工作原本是为了脱离
> BIAD 依赖；现在确定继续依赖 BIAD，配件科技留在它自己的「空军技术」页即可。

修正「请求外国装甲科技」提示里到处出现中国前置条件。

- **原因**：黑冰自己的 `BI_request_armor_tab` 触发器里有一句中国专属判断
  ```
  ROOT = { tag = CHI has_completed_focus = KMT_request_american_tanks }
  ```
  而该页签的提示是 `REQUEST_ARMOR_TOOLTIP: "[!flag_click_enabled][!flag_click]"`，
  会把触发器里所有条件展开显示——于是每个捐赠国图标都写着「中国要完成某个国策」。
- **修复**：本模组覆盖 `BI_request_armor_tab`（`common/scripted_guis/zz_CHI_air_armor_request.txt`），
  把那句包进 `hidden_trigger`：判定逻辑完全不变，只是不再出现在提示文字里。
- 版本 0.3.4。

## 0.3.3 — 2026-11-23

关闭 `HIDE_GENERIC_AIR` 后确认「只开飞机、不开坦克」能正常打开科研界面
（空军页两个：中国空军 + 通用空军）。**结论：用 technology_folders 隐藏通用空军页
会破坏黑冰科研界面，此路不通**，后续如需隐藏只能另找机制。

## 0.3.2 — 2026-11-23

修「只开飞机、关掉坦克子模时科研界面打不开」。

- **根因**（error.log）：
  ```
  Failed to create gui object. Could not find sprite type [GFX_chi_tank_folder_tab]
  ```
  合并版 gui 里坦克的页签按钮引用了坦克子模的贴图，坦克被禁用后 sprite 不存在，
  页签控件创建失败，整个科研界面跟着打不开。
- **修复**：本模组自己的 `interface/chi_air_technology.gfx` 里注册同名 sprite
  `GFX_chi_tank_folder_tab`，指向坦克子模的那张贴图路径：
  - 坦克启用时：同一张贴图、外观不变（多一条 sprite 定义，后者覆盖前者）；
  - 坦克禁用时：贴图加载失败但 sprite 类型存在，gui 控件能正常创建，界面不再崩。
- 版本 0.3.2。

## 0.3.1 — 2026-11-23

方案 A：与坦克子模「可共存、可单独运行」。

- gui 仍是「坦克版 + 中国空军页」的合并版，`descriptor.mod` 保留坦克依赖（只为加载顺序）；
- **关键改动**：`technology_tags` 现在也会注册坦克子模的 `trm_armour_chi_folder`
  （`ledger = army`，`available = { has_country_flag = CHI_armor }`，与坦克子模的定义完全一致）。
  - 坦克子模启用时：定义相同，行为不变；
  - 坦克子模禁用时：`CHI_armor` 永远不会为真，这个文件夹保持「未解锁」，引擎会自动隐藏它的页签，
    不会留下点不开的死页签；
- 黑冰本体的「请求各国装甲科技」页签不受影响（它来自 BI，不是坦克子模）；
- README §3 增加「坦克子模可禁用」的说明与启动器缺依赖提示的处理办法；
- 版本 0.3.1。

## 0.3.0 — 2026-11-23

已确认根因：**用 `on_startup` 挂标志来控制 `technology_folders` 可见性会破坏科研界面**。
科技视图在标志生效前就建好了：`air_techs_folder` 先可见、后被隐藏，状态不一致，于是开一下就关。

- 中系判定改为 `original_tag = CHI / PRC`（等价于 BIAD 给德意日美英法苏在国家历史里写标志的做法，
  但保证读档那一帧就成立），同时保留 `CHI_air` 标志作为兜底分支；
- `HIDE_GENERIC_AIR = True` 重新打开：通用空军页对中系隐藏，只留「中国空军」页；
- 版本 0.3.0。

如果这版又打不开，说明「隐藏通用空军页」这条路在黑冰里走不通；改
`config.HIDE_GENERIC_AIR = False` 重新构建即可回到 0.2.2（两个空军页并存）。

## 0.2.2 — 2026-11-23

回到 0.1.4 验证过的配置，确认科研界面恢复正常：`HIDE_GENERIC_AIR = False`、
`CHI_air` 由 `on_startup` 授予、请求页相关文件全部移除。用户确认已能打开。

## 0.2.1 — 2026-11-23

回滚 0.2.0 导致「科技界面又打不开」的改动。

- **根因**（error.log）：
  ```
  Undefined GUI_TYPE: chinaair_request_folder - This will most likely crash the game
  Window chinaair_request_folder not found.
  ```
  独立「请求页文件夹」在引擎里没被注册成窗口，整个科技视图一开就崩。
  同一份日志里还有 `Unknown trigger-type: CHI_air_request_ready` 及其连带的两条
  `Invalid trigger`（`air_assembly` / `has_ideology` 这套写法在本版本没被接受）。
- **处理**：`REQUEST_GATE = False`，删除请求页文件夹、它的页签、它的 scripted GUI，
  并把 `CHI_air_request_ready` 从 scripted_triggers 里移除。
- 现在中系只要开局挂上 `CHI_air_candidate` 就能看到中国空军页（等价于 0.1.8 的可用性），
  通用空军页仍然隐藏。
- 版本 0.2.1。

### 待办

- 「+」请求入口改用 **scripted GUI 覆盖层**（仿 BI 的 `BI_request_armor_tab`，挂在
  `countrytechtreeview` 上），不再新建文件夹；解锁条件需要用控制台 `trigger` 命令逐条验证。
- 配件科技迁移（58 项）与「研究天数」角标位置。

## 0.2.0 — 2026-11-23

**「+」请求页 + 解锁条件（仿坦克子模「请求外国装甲科技」）**

- 中系不再一开局就有中国空军页：`on_startup` 只挂候选标志 `CHI_air_candidate`；
- 解锁前空军栏显示一个「+」页签（`chinaair_request_folder`），点开是一页申请说明 + 「提交申请」按钮；
- 满足**任意一项**即可解锁：`air_assembly > 1`（≥2 座飞机装配厂）、`engine_assembly > 1`（≥2 座发动机装配厂）、
  `has_ideology = absolutism` / `despotism`（专制主义 / 专制统治）；
- 点按钮后授予 `CHI_air`、隐藏「+」页、显示自制图标的中国空军页，并触发事件 **「飞机科技研究权已获得」**
  （`CHI_air_unlock.1`，正文提醒先存档再读档一次刷新连线）；
- 通用空军页对中系始终隐藏（用候选标志判定，避开 `original_tag` 在 `technology_folders` 里的坑）。

**其它**

- 配件科技（发动机/枪炮/挂载 41 项）继续使用 72×72 小格模板（0.1.8 起的 `_small_tree` gridbox）。
- 新增 `CHI_air_request` scripted GUI（`common/scripted_guis/CHI_air_request.txt`）与
  `CHI_air_request_ready` 触发器；校验器增加请求页/解锁链路检查。
- 版本 0.2.0。

### 仍未做（下一批）

- 把 `ad_air_component_folder`（58 项配件科技）迁进中国空军页左侧 x=14–20 区域。
- 「研究天数」角标位置调整（BI 的 `days` 属性，需要实机试偏移）。

## 0.1.8 — 2026-11-23

- **隐藏通用空军页**：`HIDE_GENERIC_AIR=True`，中系只剩「中国空军」一个空军页
  （`AVAILABLE_BY_FLAG_ONLY` 仍为 True，沿用 0.1.4 验证过的写法）。
- **配件科技改用小方格**：给发动机 / 枪炮 / 挂载共 41 项科技额外生成 `<tech>_small_tree` gridbox，
  引擎会用 72×72 的 `small_item` 模板渲染（与坦克子模的弹药科技同做法）。
  这同时解决了"相邻科技图标重叠"——装备项从 203×84 变成 72×72，列距 140px 已经够放。
- `validate.py` 增加检查：小格科技必须有 `_small_tree` gridbox。
- 版本 0.1.8。

### 仍未做（下一批）

- 「+」请求页签 + 解锁条件（参考坦克的「请求外国装甲科技」）。
- 把 `ad_air_component_folder`（螺旋桨/增压器/油箱/座舱等 58 项配件科技）迁移进中国空军页左侧。
- 「研究天数」角标位置（目前由 BI 的 `days` 属性绘制，需要实机调试 dx/dy 偏移）。

## 0.1.7 — 2026-11-23

- 接入自制页签图标 `gfx/interface/techtree/techtree_chiair_tab.dds`（182×61，两帧，与坦克子模
  `techtree_chi_tank_tab.dds` 同规格）：`GFX_chinaair_folder_tab` 现在指向该 DDS，`noOfFrames = 2`。
- 删除程序生成的占位图 `techtree_china_air_tab.tga`；`GENERATE_TAB_PLACEHOLDER = False`，
  `make.py art` 不再生成占位页签（只生成封面）。
- 页签贴图缺失时构建会直接报错，避免再发布出空图。
- 版本 0.1.7。

## 0.1.5 — 2026-11-23

**科技树已能正常打开**（0.1.4 的配置生效：`AVAILABLE_BY_FLAG_ONLY=True`、`HIDE_GENERIC_AIR=False`）。

- 新增一次性提示事件 `CHI_air_tip.1`（`events/zz_CHI_air_tip.txt`）：
  与坦克科技子模同款，提醒玩家「黑冰科研界面会缓存布局，首次打开时科技连线/箭头可能不显示，
  存档再读档一次即可」。用 `CHI_air_tip_shown` 国家标志保证每个存档只弹一次，只对玩家生效。
- 事件在 `on_startup` 里延迟 1 天触发（读档也会触发 `on_startup`，所以旧存档第一次载入同样能看到提示）。
- 中英文本地化齐备；`validate.py` 增加事件/本地化/触发三处检查。
- 打包脚本现在包含 `events/` 目录。
- 版本 0.1.5。

### 已知待办

- `HIDE_GENERIC_AIR` 目前为 `False`：中系会同时看到「中国空军」和通用空军两个页签。
  等这版稳定后，再单独把 `HIDE_GENERIC_AIR` 打开测一次（只改这一个变量），确认能否安全隐藏通用页。

## 0.1.4 — 2026-11-23（排查版）

0.1.3 之后科技树窗口仍然一闪就关，且日志里没有任何相关报错，改为**二分排查**：

- 新增配置开关 `HIDE_GENERIC_AIR`、`AVAILABLE_BY_FLAG_ONLY`；
- 本版：`HIDE_GENERIC_AIR=False`（**不隐藏**通用空军页，中系会同时有两个空军页）、
  `AVAILABLE_BY_FLAG_ONLY=True`（文件夹可用性只认 `CHI_air` 标志，与 BIAD 写法一致）；
- 新增 `_tools/package_diag.py`，生成两套排查包：
  - `update_game_files.zip`（A：当前版，验证"隐藏通用空军页/触发条件"是否是根因）
  - `update_game_files_diagB.zip`（B：把 UI 集成整体退回原始界面，验证问题是否出在我们的 UI 文件）
- 版本 0.1.4。

## 0.1.3 — 2026-11-23

修复「科研界面闪烁一下、打不开」的真正根因。

- **根因**：黑冰每个科技文件夹都有一对科技条目模板
  `techtree_<folder>_item` / `techtree_<folder>_small_item`（guiTypes 下的顶层 containerWindowType）。
  新文件夹没有这两个模板时，引擎为每个科技建格子都会失败：
  ```
  Undefined GUI_TYPE: techtree_chinaair_folder_item - This will most likely crash the game
  Error: Failed to create containerWindowType "techtree_chinaair_folder_item".
  ```
  76 项科技 → 76 次失败，科研界面因此闪烁后退回。
- **修复**：从 BIAD 的 `techtree_luftwaffe_folder_item/_small_item` 复制并改名，
  自动生成为 `techtree_chinaair_folder_item/_small_item`，插在 guiTypes 末尾。
- `validate.py` 增加检查：两个模板必须存在且位于顶层。
- 版本升到 0.1.3。

## 0.1.2 — 2026-11-23

排查「科研界面闪烁 / 打不开」时发现：**游戏加载的是工坊副本 `3844078670`（11-22 19:23 的旧文件），
工作区里 11-23 的 gridbox 修复从未到达那份副本**。

- 新增 `build_info.txt`（版本 + 构建时间 + 内容统计），用于快速判断游戏加载的是哪份文件；
- 启动日志改为带版本号：`game.log` 里应出现 `CHI_AIR_TREE v0.1.2: ...`；
- 新增 `_tools/package_update.py`，把游戏需要的目录打包成 `_install/update_game_files.zip`，
  可直接解压覆盖旧副本（不含 `descriptor.mod`，不会覆盖你在启动器里改的名字/版本）；
- 版本升到 0.1.2。

## 0.1.1 — 2026-11-23

修复「进游戏后科技界面空白 / 看起来没打开」的问题。

- **根因**：`gridboxtype` 被生成在 `techtree_stripes` 子容器里，引擎只在 folder 容器的
  **直接子节点**里找 gridbox，于是 76 项科技全部刷
  `Found no grid box for tech ad_chi_tech_*`，科技页没有任何可放置的图标。
- **修复**：`build_chi.py` 改为把 gridbox 生成在 `chinaair_folder` 容器下（与 BIAD 国家空军树一致）；
  `validate.py` 增加层级检查，防止回归。
- 版本号升到 0.1.1；文档补充该坑的排查条目。

## 0.1.0 — 2026-11-22

首个可用版本：中国（CHI / PRC 及其内战分裂政权）获得独立的「中国空军」科技页。

### 内容

- **76 项科技**：35 架作战飞机、21 台发动机、11 种航空枪炮、9 种炸弹/火箭。
- 机型覆盖 1935–1947：霍克 III、伊-15 比斯、伊-16 10/24 型、P-40B/E、P-43、P-47D、P-51D、P-80A；
  九七式战、伊-153、一式战、零战二一型、三式战、四式战、拉-9、米格-9；
  伽马 2E、Hs 123、伏尔梯 A-19、蚊 FB Mk VI、伊尔-10；He 111A、SB 2M、BR.20、DB-3、B-25C、图-2、B-24J、一式陆攻；
  九七式司侦、PBY-5、C-47、F-5、蚊 PR Mk IX。
- 所有机型直接复用 BlackICE Aircraft Designer 的机体原型（模型、图标、模块槽、数值均来自 BIAD）。

### 机制

- `chinaair_folder` 科技页：`technology_folders` 按 `CHI_air` 标志 / `original_tag` 显示，并对中国隐藏黑冰通用空军页。
- 黑冰自定义科技页的**两层注册**：
  - `common/scripted_guis/BI_tech_queue_china_air.txt`（由 BIAD 国家空军块改名派生）；
  - 研究数组：`global.chinaair_folder` + 每项科技的 `tech_x/tech_y/tech_cost/tech_date` + 前置箭头 `tech_dependents`。
- 中文/英文双语本地化，含 76 条名称 + 76 条描述。
- 标签页按钮与启动器封面（程序生成）。

### 工具链

- `_tools/build/data_chi.py` 单一内容数据源；`config.py` 集中路径/文件夹名/像素映射。
- `python _tools/build/make.py all` 一键重建 + 校验；`_tools/validate.py` 覆盖结构、引用、注册、本地化、图标、必需槽位、依赖图。
- `_tools/install.ps1` 一键安装（ASCII 目录联接 + 启动器 `.mod`）。
- 游戏内加载仍未由作者完成验证（本机 Steam 客户端不稳定），详见 README 第 5 节。
