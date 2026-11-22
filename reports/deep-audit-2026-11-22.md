# 货币银行学 28 章第二轮深度审计（2026-11-22）

> **审计范围**：GitHub `1998x-stack/monetary-banking-tutorial`，全 28 篇 HTML 的可读性、跨章机制链接、样式与自动化质量门禁；同时针对有版本风险的统计口径、历史制度和近期数字金融规则抽样交叉核验。本报告是有日期的审计记录，不是对 28 章所有外部参考资料逐页验真的保证。

## 一、核心结论与修复

| 优先级 | 位置 | 审计发现 | 本轮处理 | 证据 |
|---|---|---|---|---|
| P0 | 13 外汇市场 | 2025-09 BIS 初步值 9.6 万亿美元/日（+28%），后续 BIS 2025-12 分析为 9.5 万亿美元/日（+27%）。一个统计对象有不同版本，若只引用初报会产生过时印象 | 正文并列解释初值和后续值，保留发布日期、计算对象与两个版本的来源；证据 ledger 补 1 条修订条目 | [BIS 初报](https://www.bis.org/media-releases/20250930-global-fx-trading-hits-96-trillion-day-april-2025-and-otc-interest-rate-derivatives-surge-79)；[BIS 后续分析](https://www.bis.org/publications/qr-202512/foreword-shifting-currents-fx-and-interest-rate-derivatives-highlights-2025-triennial-survey) |
| P0 | 13 国际收支 | 仅讲 BPM6 不能反映 2025 年已发布的 BPM7，但发布新标准也不意味着各国统计已经全面切换 | 加入 BPM7 2025-03 发布、各经济体过渡和版本可比性说明；ledger 增 2 条来源；保留 BPM6 的既有定义 | [IMF 发布](https://www.imf.org/en/News/Articles/2025/03/20/pr25072-imf-and-statistical-community-release-new-global-standards-for-macroeconomic-stats)；[2026 实施规划](https://www.imf.org/en/publications/tnm/issues/2026/07/02/sna-bpm-implementation-planning-playbook-575192) |
| P1 | 13 有担保利率平价 | 文字公式与数值正确，但缺乏两条等价现金流的直观说明；容易把远期价格误认为即期价格的无偏预测 | 绘制两条一年期套期保值现金流路径，标注 1 USD、7.2 CNY/USD、2%/4%、7.344 CNY 与远期 F≈7.0615 CNY/USD；新增图文与静态回归断言 | 第 13 章图解与 `assets/diagrams/covered-interest-parity.svg` |
| P1 | 全站 28 章 | 原本只有上一页/下一页的线性导航，无法回答“这个机制与其他哪些模型互相约束” | 每篇新增三个有原因解释、直达目标小节的关系卡；`knowledge/concept-links.json` 收录 28×3=84 关系；独立知识地图补充 9 条因果示例 | `knowledge-map.html` / `knowledge/concept-links.json` |
| P1 | 移动端与键盘 | 原有长表格在手机上可滚动，但键盘用户难以进入滚动容器；关联卡片需要更大触控区域 | 长表格和公式容器加 focus/role/aria-label；新增文章链接卡的单列适配、focus-visible 和减弱动画样式；首页加入跳过导航链接 | `assets/css/article.css`、`assets/css/home.css`、本地 HTML |
| P1 | 自动化质量门禁 | 原先以链接是否存在、页面是否溢出及一次交互为主，跨篇锚点准确性和 MathML 呈现未建立专门门禁 | 对全部关系图与 84 个目标锚点建立静态校验、知识地图单独验收、4 组视口下 MathML 非零尺寸及命名空间验证、首页首 Tab 焦点检查 | `scripts/validate_site.py`、`scripts/browser_check.py`、`tests/test_site.py` |

## 二、已抽样交叉核对的一手来源与关键边界

本轮从法律/统计时效风险最高、最容易被旧教材忽略的概念切入，不在缺乏证据时制造最新利率或实际回报数据。

| 章节群 | 被核查的事实与边界 | 一手来源与结果 |
|---|---|---|
| 03 / 15 | 中国 M1 自 2025-01 起含 M0、单位活期、个人活期及非银行支付机构客户备付金；现代银行贷款与存款在同一记账过程形成，非机械准备金乘数 | [人民银行 M1 统计口径文告](https://www.pbc.gov.cn/chubanwu/fileDir/resource/cms/2025/06/2025062416082199683.pdf)；[BoE 2014 货币创造研究](https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy) |
| 03 / 24 | 2025 年末中国 M2=340.3、M1=115.5、M0=14.1 万亿元；M1 改制应与增长率的口径可比性一起说明 | [国家统计局 2025 年统计公报](https://www.stats.gov.cn/sj/zxfb/202602/t20260228_1962662.html) |
| 09 / 22 | Basel CET1 最低资本要求 4.5%，资本留存缓冲 2.5% 等属标准框架；信贷/GDP 缺口是预警指标而非单月危机倒计时 | [BIS Basel 标准](https://www.bis.org/committees/bcbs/basel-framework/standard/rbc/20/inforce/2019-12-15/published/2019-12-15)；[BIS 信贷缺口](https://data.bis.org/topics/CREDIT_GAPS) |
| 13 | BIS 2025 FX 调查初报与后续更新不同；BPM7 已发布但实施按国别逐步推进 | [BIS 2025-09](https://www.bis.org/media-releases/20250930-global-fx-trading-hits-96-trillion-day-april-2025-and-otc-interest-rate-derivatives-surge-79)；[BIS 2025-12](https://www.bis.org/publications/qr-202512/foreword-shifting-currents-fx-and-interest-rate-derivatives-highlights-2025-triennial-survey)；[IMF BPM7 2025](https://www.imf.org/en/News/Articles/2025/03/20/pr25072-imf-and-statistical-community-release-new-global-standards-for-macroeconomic-stats) |
| 22 | 宏观审慎与逆周期资本缓冲不能仅凭单一统计信号机械决定；需要判断国别与金融结构 | [Basel CCyB 指导](https://www.bis.org/committees/bcbs/basel-consolidated-guidelines/module/cad/20) |
| 24 / 25 / 28 | 历史宏观回测须使用当时可得的数据版本，不得把事后修订当作原始信息 | [FRED/ALFRED 实时数据版本](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html) |
| 26 | 2026-01-01 中国数字人民币新框架涉及商业银行运营钱包的存款负债、计息与存款保险；应明确钱包类型；欧洲数字欧元 2029 年可能发行仍依赖立法 | [中国政府网 2025-12](https://english.www.gov.cn/news/202512/29/content_WS69526d4ec6d00ca5f9a08511.html)；[ECB 数字欧元 FAQ](https://www.ecb.europa.eu/euro/digital_euro/faqs/html/ecb.faq_digital_euro.en.html) |
| 27 | GENIUS Act 已在 2025 年成为法律，但美国 OCC 的有关最终规则生效日为 2027-01-18（本报告时点为 2026-11-22），不能说当前全部实施 | [OCC Bulletin 2026-50](https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-50.html) |

## 三、28 章逐页结构检查与主题清单

> `结构`、`关系`、`可视化`、`交互` 是网站内的自动化或静态可验证项目。`事实抽核` 只针对上表明确列出的优先概念，其他声明保留逐章 `evidence/` 台账，不冒充“已穷尽复核”。

| 章节 | 主题群 | 此次二轮处理 |
|---|---|---|
| 01–05 | 货币、起源、统计、制度、信用 | 每篇增 3 条跳转，检查独立语义与引用；03 M1 时效抽核 |
| 06–09 | 利率、收益率、银行和监管 | 3 条跳转/篇、键盘滚动与公式展示；09 资本框架抽核 |
| 10–13 | 央行、货币市场、资本市场、外汇 | 3 条跳转/篇；13 完成统计版本、BPM7、CIP 图解纠正 |
| 14–18 | 非银行中介、货币创造与政策传导 | 3 条跳转/篇；15 银行货币创造理论和 17–18 政策边界抽核 |
| 19–23 | 宏观模型、物价、通缩、危机、央行报告 | 3 条跳转/篇；图解和现有 MathML、宏观审慎监测抽核 |
| 24–28 | 数据、预测、CBDC、稳定币、综合项目 | 3 条跳转/篇；历史数据版本、数字人民币与 GENIUS Act 日期抽核 |

## 四、验收方法和未完成的事情

本轮将在 GitHub Actions 上执行以下质量门禁；**只有实际产生 success 结论后，才能标为通过**。

```bash
python scripts/validate_site.py
python -m unittest discover -s tests -v
python scripts/browser_check.py --output artifacts/browser-qa
```

增加检查：知识地图 28 张链接卡及 9 条跨概念关联、28 篇各 3 条的锚点完整性、桌面 1440/平板 768/手机 390 与 360 像素、键盘首 Tab、MathML 命名空间和非零几何尺寸、图片与溢出、打印视图以及每篇一个真实交互。

本轮 **不声称完成** 下列事项：
- 对 `evidence/chapter-01.json` 至 `chapter-28.json` 每条外链进行了实时无死链批量抓取；目前主要采取内部链接静态解析和高优先级官方事实抽核。
- 对所有带 MathML 的公式完成数学专家逐项证明，或复现所有历史研究与宏观实证结果；新增的 CIP 例子使用明确现金流路径进行检查。
- 对未来央行措施、全球数字货币立法、某日期市场报价给出无条件预言。变动快的政策段落应按季度定期对照官方来源。

## 五、后续建议

保留发布日期清晰的更新审计记录；优先按季度核对货币统计与 CBDC/稳定币政策。自动化可以验证链接和演示计算，不能取代对原始公告、法律条款与统计发布版本的专家判断。对于跨国国际收支，要在国家统计局或央行确认 BPM6/BPM7 实际编制口径。
