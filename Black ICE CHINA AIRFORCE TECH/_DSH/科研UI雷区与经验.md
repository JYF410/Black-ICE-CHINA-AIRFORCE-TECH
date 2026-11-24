# 黑冰科研界面：雷区与经验

> 这一页的每条结论都是在本机 `1.20.0.0` + 黑冰 + BIAD + 坦克子模环境下实测得到的。
> 换大版本（BI/BIAD/游戏本体）之后要重新验证，但"雷区"大概率仍然成立。

---

## 0. 先理解它怎么画的

黑冰的科技页**不是**原版那套 gridbox 直接排布，而是：

```
common/technologies/*.txt        科技定义，folder = { name = <文件夹> position = {x y} }
common/technology_tags/*.txt     technology_folders：哪些文件夹对这个国家可见（available）
interface/countrytechtreeview.gui
                                ① 每个文件夹一个 containerWindowType（名字 = 文件夹名）
                                ② 里面一堆 gridboxtype，名字 = <tech>_tree（小格科技还要 <tech>_small_tree）
                                ③ guiTypes 顶层两个模板：techtree_<文件夹>_item / _small_item
                                ④ folder_tabs 容器里每个文件夹一个 buttonType（名字 = <文件夹>_tab）
common/scripted_guis/BI_tech_queue_<文件夹>.txt
                                文件夹的 scripted GUI 块（图标、天数、箭头、点击研究都靠它）
on_startup / scripted_effects    研究数组：global.<文件夹> 里塞 tech 列表，
                                 并给每个 tech 设 global.tech_x@ / tech_y@ / tech_cost@ / tech_date@
```

四样东西缺一不可：**文件夹注册 + GUI 窗口 + 条目模板 + 研究数组**。
少任何一样的表现都不一样，见下面对照。

---

## 1. 雷区清单

### R1 绝对不要在游戏中途改变文件夹的「可用性」

**症状**：科研界面点开闪一下就关 / 直接打不开，`error.log` 里**没有任何相关报错**（静默失败）。

**原因**：`technology_folders` 里的 `available` 会在科技视图构建时求值一次；
如果它依赖的东西（国家标志、全局标志、工厂数、国策、科技）在游戏中途由假变真，
文件夹列表和已构建的界面不一致，整页就废了。

**实测案例**：
- 用 `has_country_flag = CHI_air`（on_startup 设置）隐藏通用空军页 → 打不开；
- 用「工厂/国策/科技」条件解锁坦克页 → 点「早期拖拉机」的瞬间打不开；
- 用 `has_global_flag`（坦克子模 on_startup 设）控制坦克页 → 新档打不开（旧档该标志已存在时反而正常）。

**规则**：
- `available` 只用**读档那一刻就确定**的东西：`original_tag`、`has_country_flag`（写在国家历史里的）、
  常量条件；
- 需要"条件解锁"时，不要在文件夹层面做——见 R2。

### R2 需要"条件解锁"时，正确做法不是隐藏文件夹

可选方案（按推荐度）：

1. **接受页面常开**，用一次性事件提示玩家（本模组 v0.7.x 采用）；
2. 给**科技本身**加 `allow = { ... }`（页面可见，科技锁定，不碰文件夹可用性，安全）；
3. 若一定要"先隐藏"，只能把条件做成**开局静态**（例如写进 `history/countries/*.txt`），
   那就变成"某些国家一开始就有"，不是"满足条件后解锁"。

### R3 不要自己造"假文件夹"

**症状**：`Undefined GUI_TYPE: <folder>` + `Window <folder> not found.`，整页打不开。

**原因**：在 `technology_folders` 里注册了一个文件夹，但 GUI 里没有同名 `containerWindowType`。
曾经做过一个「+ 请求页」文件夹，就是想当然地以为"先注册、后补窗口"能行，结果整个科研界面崩。

**规则**：`technology_folders` 里的每个名字，都必须能在 `countrytechtreeview.gui` 里找到
**同名的、直接挂在 `countrytechtreeview` 下的** containerWindowType。

### R4 缺少条目模板 = 闪一下打不开

**症状**：
```
Undefined GUI_TYPE: techtree_<folder>_item - This will most likely crash the game
Error: Failed to create containerWindowType "techtree_<folder>_item".
```
外加每个科技一条，共 76 条。

**原因**：引擎按 `techtree_<文件夹>_item` / `techtree_<文件夹>_small_item` 取名模板，
新文件夹必须自己补这两个顶层 containerWindowType。

**规则**：新增文件夹时，从 BIAD 的 `techtree_luftwaffe_folder_item` / `_small_item`
复制改名即可（`build_chi.py` 的 `emit_gui` 已自动做）。

### R5 `gridboxtype` 必须是文件夹容器的直接子节点

**症状**：`Found no grid box for tech <tech>`，科技页空着。

**原因**：把 gridbox 放进了 `techtree_stripes` 之类的子容器里。纵深必须比文件夹名深 1 层。

**规则**：`name = "<tech>_tree"` 的 depth 必须等于文件夹 `name` 的 depth + 1。

### R6 小格科技需要额外的 `<tech>_small_tree`

**症状**：发动机/枪炮/挂载这些本该是 72×72 小方格的科技，显示成 203×84 的大条目，
相邻列/行互相压住。

**规则**：科技带 `force_use_small_tech_layout = yes` 时，除了 `<tech>_tree` 还要再给一个
`<tech>_small_tree` gridboxtype（同样 70×70）。坦克子模的弹药科技就是这么做的。

### R7 不要覆盖别的子模对 `technology_folders` 的注册

**症状**：坦克科技页能打开，但**只剩费用数字和箭头**，物品窗口（边框/图标/名字）全都没有；
`error.log` 里没有任何 GUI 报错。

**原因**：我们曾在自己的 `technology_tags` 里覆盖 `trm_armour_chi_folder`
（哪怕字段看起来一样），坦克页就只剩 BI 的角标图层。

**规则**：别的子模注册的文件夹**不要碰**。要让它可见，就满足它自己的条件
（例如 `on_startup` 里给中国挂 `CHI_armor`），让**它自己的定义**生效。

### R8 不要重复注册别的模组已经定义的 sprite

**症状**：某个模组自己的页面图标全部消失，日志无报错。

**原因**：我们曾为了"坦克子模可禁用"而重复注册 `GFX_chi_tank_folder_tab`，
和坦克子模的 gfx 冲突。

**规则**：别人的 sprite 名一律不要抢；需要兜底时用**新名字**。

### R9 `has_global_flag` 不能直接写进 `available`

**症状**：所有国家打不开科研界面（因为全局标志对所有国家都为真，每个国家都去渲染一个它不该有的页）。

**规则**：全局标志只能作为**国家条件之一**的一部分：
```
AND = { has_global_flag = X  OR = { original_tag = CHI  original_tag = PRC } }
```

### R10 页签条（folder_tabs）不能随便挪

页签是**绝对坐标**，原始布局：

```
0 步兵 | 10 支援 | 90 炮兵 | 170 坦克 | 260 一战学说 | 340 各国装甲组 | 430 陆军学说
| 510 海军技术 | 610 海军 | 690 海军学说 | 780 空军技术 | 880 各国空军组 | 970 空军配件
| 1070 电子 | 1150 工业 | 1230 原料
```

- `340` 和 `880` 是"多国共用一格"的组，同格内只有当前国家那一个可见；
- **黑冰的「请求外国装甲科技 +」按钮**由 `_BI_misc_scripted_gui.gui` 固定画在 `(345, 6)`，
  宽度约 182，实际占据 345–527，正好压住 340 格和 430 格；
- 试过把后面所有页签整体 +80 腾位置：会丢页签（被挤出可视区）；
- 试过把新页签放最右 1310：科研界面直接打不开（超出容器范围）。

**实测可行的做法**：让坦克子模自己的逻辑把「+」对 CHI 隐藏
（它的 `BI_research_tabs_scripted_gui.txt` 在 `CHI_armor` 存在时隐藏 +），
于是 340 格空出来，坦克页签留在 340 即可，其它页签一个都不用动。

### R11 事件弹窗带图片：必须用 news_event

- 黑冰的普通事件窗口 `interface/eventwindow.gui` 里，`event_picture` 控件是**注释掉的**
  （`top_Window` 部分），所以 `picture = GFX_xxx` 不显示；
- 正文里用内嵌图标 `£sprite` 同样不显示；
- **黑冰的新闻窗口**有可用的 `event_picture`，`news_event` 的 `picture = GFX_xxx` 能正常显示。

**规则**：需要配图的事件写成 `news_event`，用 `news_event = { id = ... days = 1 }` 触发。
图片按原版尺寸 **397×153**，放 `gfx/event_pictures/`，格式 DDS（DXT5）或 TGA 均可。

### R12 科研界面缓存：新科技页首次打开缺图标/连线

这不是 bug，是黑冰的布局缓存：新页签第一次打开时物品窗口还没生成，
**存档 → 读档一次**即恢复正常（坦克子模单独使用也一样）。

**本模组的处理**：开局第 1 天弹一次 `news_event`（带坦克照片），
标题「中国坦克科技树使用提示」，正文说明"先存读档"。
用 `CHI_armor_tip_shown` 标志保证每存档只弹一次。

### R13 `has_ideology` 是角色作用域

```
## has_ideology
* Supported Scopes: CHARACTER
```

直接写进国家作用域会让整个触发器非法（连带整份 `scripted_triggers` 全部失效）。
要在国家层面判断执政党子意识形态，用：

```
any_character = {
    is_country_leader = yes
    has_ideology = absolutism
}
```

### R14 压缩包解压不会删除旧文件

游戏加载的是工坊副本（`3844078670`），我们通过 zip 覆盖更新。
**删掉的文件不会因为解压而消失**，旧版本留下的覆盖文件会继续生效，导致"明明改了却没效果"。

**规则**：
- 退役的覆盖文件不要"删除"，改成写一个空的 `scripted_gui = { }` 占位文件（`emit_legacy_stubs()` 就是干这个的）；
- 每次更新后确认副本 `build_info.txt` 的版本与时间戳。

### R15 动态 token 警告是噪音

```
Token ad_chi_tech_xxx is a dynamic token, this can cause OOS ...
```
BIAD 自己会刷几千条，忽略即可，和界面问题无关。

---

## 2. 常见报错对照

| 日志 | 含义 | 处理 |
|---|---|---|
| `Found no grid box for tech X` | gridbox 缺失或层级不对 | 见 R5 |
| `Undefined GUI_TYPE: techtree_<f>_item` + `Failed to create containerWindowType` | 缺条目模板 | 见 R4 |
| `Undefined GUI_TYPE: <folder>` + `Window <folder> not found` | 注册了文件夹但没窗口 | 见 R3 |
| `Could not find sprite type [GFX_xxx]` + `Failed to create gui object` | sprite 没注册（别的模组提供而我们没启用） | 见 R8 |
| 界面闪一下 / 打不开但**日志干净** | 文件夹可用性中途翻转 | 见 R1 |
| 页面只剩数字和箭头 | 覆盖了别的模组的文件夹注册 | 见 R7 |
| `Invalid trigger` / `Unknown trigger-type` | 作用域不对（如 `has_ideology` 写进国家） | 见 R13 |

---

## 3. 排查顺序（省钱版）

1. 先看 `error.log` **只过滤自己相关的行**（`ad_chi|chinaair|trm_armour|本模组文件名`）；
2. 日志干净 → 不要继续翻日志，改用"二分"：
   - 关掉我们的模组，看父模组自己是否正常（这一步曾直接定位出"覆盖 tank 文件夹注册"的根因）；
   - 打开我们的模组，一次只加/减一个改动；
3. 保留一个**已知能打开**的版本作为回退点，改坏了立刻回退再试下一个变量；
4. 任何"应该生效却没生效"的情况，先检查工坊副本的文件和版本（见 R14）。
