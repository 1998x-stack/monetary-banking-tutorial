# 28 篇 HTML 逐页事实、机制与计算复核
**检查日期：2026-11-22｜仓库：1998x-stack/monetary-banking-tutorial｜范围：01–28.html**

## 执行边界

这是一轮可重现的**逐页面**编辑审查，不是声称所有参考网页都已逐字人工证明。28 篇已分别检查章节标题与结构、原有案例、公式展示、交互入口、既有证据台账、跨篇链接，并在每篇加入一个独立的假设推演或反例，正文使用 `#audit-case` 锚点、桌面/手机双目录入口。每一篇的 `evidence/chapter-NN.json` 同步增加 `second-pass-worked-case`，并明确是否是教学示例以及已交叉核对的制度来源。

## 逐篇问题与改进结果

| 章节 | 审核重点 | 本轮独立改进／反例 | 核验类型 |
|---|---|---|---|
| [01](../01.html#audit-case) | 货币、银行与支付 | 银行 A/B 的100万元贷款与跨行清算；结算准备金不等于公众存款 | 数学+账簿 |
| [02](../02.html#audit-case) | 货币历史起源 | 交换媒介、熟人债务与公共记账并存；不把思想实验写成普遍历史 | 机制边界 |
| [03](../03.html#audit-case) | M0/M1/M2 | 演示旧口径100和新口径120造成的虚假20%增速；突出2025中国M1修订 | 时效+统计口径 |
| [04](../04.html#audit-case) | 国际货币制度 | 固定汇率、资本流动与独立利率的条件性套利链条 | 制度假设 |
| [05](../05.html#audit-case) | 信用与征信 | PD×LGD×EAD压测 8000→20000元；不是确定损失 | 数学+风险 |
| [06](../06.html#audit-case) | 利息与费雪方程 | 2%名义利率/−2%预期通胀⇒精确实际4.08% | 数学 |
| [07](../07.html#audit-case) | 收益率曲线 | 修正YTM与再投资混写；无票息100元的5%/6%贴现价格 | 技术纠错 |
| [08](../08.html#audit-case) | 银行资产负债 | 10亿元存款流出、准备金8亿元、折价卖券2.5亿元示例 | 账簿+风险 |
| [09](../09.html#audit-case) | 资本与审慎监管 | CET1=7、RWA100→120、资本比率7%→5.83%；缓冲不是违约 | 监管边界 |
| [10](../10.html#audit-case) | 中央银行 | 央行向银行/非银行买50单位证券的准备金与公众存款区别 | 资产负债 |
| [11](../11.html#audit-case) | 货币市场 | 回购1000万元、2%、7日ACT/365利息3835.62元 | 日数公式 |
| [12](../12.html#audit-case) | 资本市场 | 一年期104元合同现金流按5%折现99.05元；一级/二级交易分开 | 数学+法律 |
| [13](../13.html#audit-case) | 外汇市场 | 一美元7.20×1.02=7.344，两路径CIP远期7.0615；保留BIS初/终值、BPM7 | 数学+版本 |
| [14](../14.html#audit-case) | 非银行金融 | 2025年FSB报告描述2024年末256.8万亿美元=广义NBFI而非窄口径影子银行 | 统计定义 |
| [15](../15.html#audit-case) | 现代货币创造 | 现金/超储比变动乘数4.4→3.67；与真实贷款约束区分 | 模型反证 |
| [16](../16.html#audit-case) | 货币需求 | MV=PY的M100→110时V2→1.82，说明恒等式不是单向因果 | 恒等式 |
| [17](../17.html#audit-case) | 政策工具 | 政策基准1.5%→1.3%、风险加点2→2.6导致贷款利率3.5→3.9 | 模型敏感性 |
| [18](../18.html#audit-case) | 政策传导 | 政策利率−0.25pp、风险溢价+0.50pp、企业成本+0.25pp | 因果边界 |
| [19](../19.html#audit-case) | IS–LM | Y220、r1.5逐步联立、双市场反代而非仅检查一个方程 | 公式逐步 |
| [20](../20.html#audit-case) | 通货膨胀 | CPI 100→103与PCE100→102.5；BEA四种指数差异来源 | 统计口径 |
| [21](../21.html#audit-case) | 通货紧缩 | 名义债务100、价格指数1→.95实负担105.26；精确实际利率4.12% | 数学+预期 |
| [22](../22.html#audit-case) | 金融危机 | 资产100、负债80、跌10%时权益损失50%；不等于违约率 | 风险放大 |
| [23](../23.html#audit-case) | 央行报告 | 5名成员点阵3/3/4/4/5中位数4≠委员会投票 | 信息层级 |
| [24](../24.html#audit-case) | 社融与M2 | 存量400＋流量30−其他调整6＝424；流量≠余额变化 | 存量流量 |
| [25](../25.html#audit-case) | 宏观预测 | 三期误差−0.5/−0.5/1对应MAE.67、RMSE.71；防修订泄漏 | 数学+回测 |
| [26](../26.html#audit-case) | 数字人民币 | 同账户100划转40→60+40不重复计数；银行实名钱包计息分类 | 新制度 |
| [27](../27.html#audit-case) | 稳定币与DeFi | 储备105折价10%→94.5不足面值100；GENIUS 2027-01-18生效 | 压力+法律时效 |
| [28](../28.html#audit-case) | 宏观综合项目 | 虚构2026-12社融400→424、M2 300→318与CPI101→102.5逐项复算 | 可复现性 |

## 一手来源交叉验证记录

以下来源经本轮检索对照，分别支持标准定义或制度时效；**教学中的假设数值并非从这些文献取得**。

- **中国2025 M1 修订**：[官方/机构来源](https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html)。数据自2025-01修订；拼接前做可比处理。
- **债券YTM与实现回报**：[官方/机构来源](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/fixed-income-bond-valuation-prices-and-yields)。YTM为未来现金流的内部收益率；票息再投资是实现回报的额外条件。
- **银行间回购ACT/365**：[官方/机构来源](https://www.chinamoney.com.cn/english/rarrmrrudmrl/20161111/2025.html)。年化回购利息应明确起息与到期日/天数基准。
- **BIS巴塞尔资本比率**：[官方/机构来源](https://www.bis.org/committees/bcbs/basel-framework/standard/rbc?allChapters=true)。最低比率、缓冲、风险加权资产与国别实施分开说明。
- **FSB非银行金融监测**：[官方/机构来源](https://www.fsb.org/2025/12/fsb-reports-continued-growth-in-nonbank-financial-intermediation-in-2024-to-256-8-trillion/)。发布年2025，统计观察年2024；广义资产与窄口径风险监测不同。
- **货币乘数实证**：[官方/机构来源](https://www.federalreserve.gov/econres/feds/money-reserves-and-the-transmission-of-monetary-policy-does-the-money-multiplier-exist.htm)。不能将静态准备金乘数等同现实银行信用创造。
- **CPI/PCE差异**：[官方/机构来源](https://www.bea.gov/help/faq/555)。差异来自公式、权重、覆盖范围及其他因素。
- **美联储SEP**：[官方/机构来源](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm)。成员个人预测不等于委员会政策投票或承诺。
- **e-CNY银行运营钱包**：[官方/机构来源](https://www.abchina.com/cn/PublicPlate/szrmb2021/szrmben2021/202111/t20211115_2067431.htm)。2026-01-01起实名一至三类钱包根据活期存款规则计息；其他钱包不能无条件推广。
- **OCC GENIUS规则**：[官方/机构来源](https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-50.html)。相关最终规则生效日期2027-01-18。
- **外汇初步值与更新**：[官方/机构来源](https://www.bis.org/publications/qr-202512/foreword-shifting-currents-fx-and-interest-rate-derivatives-highlights-2025-triennial-survey)。后续值9.5万亿美元/日、增幅27%；初步值另为9.6与28%。
- **BPM7发布和过渡**：[官方/机构来源](https://www.imf.org/en/News/Articles/2025/03/20/pr25072-imf-and-statistical-community-release-new-global-standards-for-macroeconomic-stats)。2025-03发布；各国采用目标主要在2029–2030。
- **OECD领先指标**：[官方/机构来源](https://www.oecd.org/en/data/datasets/oecd-composite-leading-indicators-clis.html)。观察相对趋势转折，不作为GDP增速精确点预测。

## 新增加的可复算数值（独立 Python 测试）

`tests/test_worked_audit.py` 使用 Python 算术独立验证：PD×LGD×EAD、费雪精确式、零息债券价格、NIM与资本分母变化、回购ACT/365、票息债券价格、CIP报价方向、货币乘数参数变化、通胀与M2指数增长、实际债务负担、杠杆权益损失、稳定币折价与宏观预测 MAE/RMSE。同时**反代检验** IS–LM 的两个均衡条件都成立。

`scripts/audit_sources.py` **默认只做离线证据链接结构检查**（28份台账、唯一ID、合法HTTP(S)域名、status和URL字段），提供一个**可选**的 `--live` 模式进行外部HTTP状态检查。该模式将 403/429 归类为可能被反爬或限流，不能当成页面不存在，也不会把 HTTP 200 误称为“该来源已证实所有陈述”。

```bash
python scripts/validate_site.py
python scripts/audit_sources.py --output artifacts/source-audit/offline.json
python -m unittest discover -s tests -v
python scripts/browser_check.py --output artifacts/browser-qa

# 可选：检查前30个唯一外部链接的HTTP状态；会访问网络，不等于核实正文命题
python scripts/audit_sources.py --live --limit 30 --output artifacts/source-audit/live-sample.json
```

## 质量风险与尚未完成的工作

1. 需要逐项复核所有独立外链的原始出处、附件PDF原文与法律条款有效性。静态校验只确认本地链接；在线HTTP状态即使为200也不能保证统计口径正确。
2. 本轮的模拟数值有独立可复算公式，但不替代对28章所有历史理论、经验研究、金融产品法律定义的专家同行评议。
3. 数据版本会修订：2025年 BIS 外汇初值与后续值应并列标版本；BPM7 发布与国别实施时点应分开；数字人民币和稳定币监管应以当前版本为准。
4. 对复现项目第28章，`2026-12`仍是本检查日之后的**虚构数据**，不能误用为已发布统计。
5. CI 成功后才能在本文或PR中填写“浏览器质量门禁通过”；尚未运行或失败时只能写明待验证。

## 维护约束

- 新增重要案例必须给定单位、假设、数值、公式及不可外推边界。
- 更新统计法律内容时，同时更新正文 `#audit-case` 与本章 ledger。对同一原始研究的初值与修订值应保留日期。
- 每个交互示例至少有一个实际浏览器检查，额外的数学验证由独立 Python 断言提供。
- 读者直接打开任意 `NN.html` 仍能自足理解，不应把跨章节导航当作必要的背景。
