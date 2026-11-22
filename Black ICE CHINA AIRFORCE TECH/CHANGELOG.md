# 更新日志 / Changelog

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
