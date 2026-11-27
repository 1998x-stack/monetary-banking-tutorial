# 货币银行学 · 从货币到金融体系

一个以中文为主的静态课程站点，覆盖货币、信用、银行、金融市场、货币政策与宏观金融分析，共 28 个主题章节。无需构建工具或第三方 CDN，页面可在本地浏览器打开，也可部署到 GitHub Pages。

> **内容状态：** 第 01–28 章均已完成第一轮深度重构：独立叙事、证据与统计口径、原创图解、交互练习。第 28 章还包含可离线运行的 Python 计算、虚构样本 CSV 和回归测试。

## 开始学习

- 在线入口（GitHub Pages）：<https://1998x-stack.github.io/monetary-banking-tutorial/>
- [全站知识关联地图](knowledge-map.html)：五条学习路线、九条跨主题因果链，文章中共有 84 个直达相关小节的链接；离线可用
- 本地阅读：下载或克隆仓库，直接打开 `index.html`。首页章节卡片是静态 HTML，不依赖 `fetch()`，因此 `file://` 环境也能使用。
- 章节入口：`01.html` 至 `28.html`。

```bash
git clone https://github.com/1998x-stack/monetary-banking-tutorial.git
cd monetary-banking-tutorial
# macOS
open index.html
# Linux
xdg-open index.html
```

## 学习路线

| 路线 | 章节 | 你将建立的能力 |
|---|---:|---|
| 货币基础 | 01–05 | 解释货币、信用、货币统计与国际货币制度 |
| 利率与金融机构 | 06–14 | 理解利率定价、银行资产负债表和金融市场 |
| 货币供需与政策 | 15–18 | 分析货币创造、货币需求及政策传导 |
| 宏观模型与金融稳定 | 19–23 | 使用宏观模型解释通胀、危机和政策沟通 |
| 数据与新金融 | 24–28 | 读懂金融数据、宏观预测及数字金融议题 |

## 仓库结构

```text
.
├── index.html                 # 静态课程门户（28 章，可搜索）
├── knowledge-map.html         # 五条路线及跨主题因果地图
├── courses.json               # 章节元数据
├── 01.html … 28.html          # 28 篇独立文章
├── theme.css                  # 保留历史兼容样式；新页面不依赖它
├── assets/
│   ├── css/
│   │   ├── home.css           # 首页设计系统
│   ├── knowledge.css      # 知识关联地图样式
│   │   └── article.css        # 第 01–28 章共用文章样式
│   ├── js/
│   │   ├── home.js            # 首页本地搜索
│   │   └── article-demos.js   # 文章中的渐进增强交互
│   └── diagrams/              # 独立、可访问的 SVG 图解
├── knowledge/                 # 28 章 × 3 个关联的可审核关系数据
├── reports/                   # 按日期记录研究来源与事实修复
├── evidence/                  # 第 01–28 章的事实—来源证据台账
├── examples/                  # 第 28 章的虚构数据与可复现计算
├── scripts/
│   ├── validate_site.py       # 静态结构、链接和证据校验
│   └── browser_check.py       # Chromium 多视口验收
├── tests/                     # 自动化回归测试
├── .github/workflows/         # GitHub Actions 质量门禁
└── AGENTS.md                  # 后续内容编辑与验收规范
```

## 内容与事实规范

- 每篇文章都是独立阅读单元：首次出现的概念必须给出定义、必要背景、适用边界和例子，不要求读者先读其他章节。
- 正文按“问题 → 机制 → 图解 → 公式/制度 → 例子 → 局限 → 总结”组织。章节导航只负责引路，不替代正文解释。
- 区分事实、理论解释、教学模型和假设案例；不把虚构故事写成真实事件。
- 对统计口径和制度规则标注地区、发布日期或生效日期。中国 M1 自 2025 年 1 月起采用修订口径，第 03 章按新口径解释。
- 重要事实优先引用央行、统计部门、国际组织、监管机构和原始研究；每篇文章在 `evidence/` 中保留可追溯的证据台账。
- 不复制 Christopher Olah 或 The Annotated Transformer 的文字、图形、代码或品牌，只借鉴渐进式解释、清晰图解和可复现示例的教学方法。

## 第二轮精修：知识关联与事实复核

- 每章保持独立解释，并额外提供 **3 个跨主题、带原因说明的具体小节入口**。关系源文件为 [`knowledge/concept-links.json`](knowledge/concept-links.json)，可通过 [知识地图](knowledge-map.html) 以主题路线浏览。
- 首页和文章的跳转不依赖网络或 JavaScript。响应式关联卡片在 390px/360px 手机宽度下改为单列，长表格和公式支持键盘焦点与横向滚动。
- 第 13 章新增 **CIP 两条套期保值路径图**，修订 BIS 的 2025 年 FX 初步值与后续修订值，并增加 **BPM7 2025 年发布、各国分阶段采用**的说明。
- [本轮证据与工程审计记录](reports/deep-audit-2026-11-22.md) 明确列出已核对的官方来源、修复范围和仍需滚动检查的事项。
- 自动化检查增加 84 个跨章节链接的目标锚点验证、知识地图页面验收、MathML 呈现几何检查、首个 Tab 键可用性，以及新增图解的关键数字断言。

## 第三轮逐页核验（2026-11-22）

本轮不是增加新章节，而是逐篇检查和完善现有的 28 篇独立 HTML 教程。每篇新增一段**可复算的具体情景与反例**（正文目录「推演核验」），并同步登记到相应 `evidence/chapter-NN.json`：

- [28 篇逐章检查矩阵、核算结果和官方出处](reports/html-by-html-audit-2026-11-22.md)：说明每个页面核查了什么、修改了什么、尚未验证什么。
- 债券 YTM 与实际持有回报的再投资条件已在第 07 章重新区分；其他重要改进包括回购 ACT/365、CET1 分母变动、IS–LM 双方程反代、CPI/PCE 口径及数字人民币钱包制度时间。
- 全部证据台账支持离线结构审核：`python scripts/audit_sources.py`。可选 `--live` 只检查 HTTP 状态，403/429/超时不当成确定死链，也不把 HTTP 200 当作事实证明。
- `tests/test_worked_audit.py` 独立验算关键数字，浏览器额外检查手机目录能跳转到各章的「推演核验」。

## 计算器公式与可复算校验

- 第 11、22、27 章的交互计算器与其余数值型章节一致，现在把所用公式以原生 MathML 展示（符号、单位、假设与适用边界写在公式下方），窄屏下公式区域可键盘聚焦并横向滚动。
- 新增 `examples/money_math.py`：用纯标准库复现各章计算器的确定性公式，覆盖费雪实际利率、回购 ACT/365 利息、债券折现价、货币乘数、线性货币需求、IS–LM 均衡、价格指数变化、通缩债务负担、杠杆权益损失、同比增速、泰勒规则、预期损失、稳定币储备覆盖率与抛补利率平价远期。
- `tests/test_money_math.py` 既做数值断言，也逐页校验模块结果与页面静态默认值一致，降低“可运行示例与正文自相矛盾”的风险。

## 移动端图解可读性修复（2026-11-25）

窄屏下图解内的 SVG 标注会随容器缩到约 5–6px 而不可读。本轮让每个图解在手机上可横向平移，并保留可读的 12–13px 最小宽度；每个图解都是可聚焦的滚动区域，图注在平移时保持可见。修复范围与核验证据见 [移动端图解可读性修复记录](reports/mobile-diagram-legibility-2026-11-25.md)。

## 本地质量检查

Python 3.10+：

```bash
python scripts/validate_site.py
python scripts/audit_sources.py --output artifacts/source-audit/offline.json
python -m unittest discover -s tests -v
```

浏览器验收需要安装开发依赖：

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python scripts/browser_check.py --output artifacts/browser-qa
```

浏览器检查覆盖首页、知识地图和第 01–28 章，包含逐篇计算核验板块的 1440、768、390、360 像素视口、图片加载、页面溢出、控制台错误、打印模式及每篇文章的交互控件。未运行的检查不得标记为通过；CI 运行结果以 GitHub Actions 为准。

## 可复现综合项目

第 28 章以完全虚构数据演示宏观政策报告的可复核数据流程，附带源数据词典、Python 标准库分析脚本与自动化测试：

```bash
python examples/analyse_macro.py
python -m unittest discover -s tests -v
```

- [完整第 28 章](28.html)：问题 → 数据审计 → 金融传导机制 → 政策情景 → 复盘
- [数据、代码和输入校验](examples/README.md)：拒绝重复月份、非正存量和不合法的同比月份
- 所有示例数据（含 2026-12）均为**虚构教学样本**，不是已经发布的真实经济数据，不得作为投资或政策预测依据

## GitHub Pages

仓库页面以根目录 `index.html` 为入口。若尚未启用 Pages，请在 GitHub 仓库 **Settings → Pages → Build and deployment** 中选择 **Deploy from a branch**，分支选择 `main`、目录选择 `/(root)`，保存后等待部署完成。只有 Pages 部署成功并能实际访问时，才可称网站已上线。

## 主要参考资料

- [中国国家统计局：什么是货币供应量](https://www.stats.gov.cn/zs/tjws/zytjzbqs/hbgyl/202409/t20240910_1956348.html)
- [中国国家统计局：2025 年国民经济和社会发展统计公报](https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html)
- [中国人民银行征信中心：机构概况](https://www.pbccrc.org.cn/en/gywm/zxgk/index.html)
- [Bank of England: Money creation in the modern economy](https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy)
- [Federal Reserve History: Creation of the Bretton Woods System](https://www.federalreservehistory.org/essays/bretton-woods-created)
- [IMF: The IMF and the Silent Revolution](https://www.imf.org/external/pubs/ft/silent/index.htm)

## 许可与贡献

新增文字、示意图和代码为本项目独立编写。引用外部资料时保留来源链接；使用第三方资产前必须核对许可证并记录署名要求。发现事实错误、失效链接或可复现问题，欢迎提交 Issue 或 Pull Request。
