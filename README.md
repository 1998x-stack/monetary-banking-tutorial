# 货币银行学 · 从货币到金融体系

一个以中文为主的静态课程站点，覆盖货币、信用、银行、金融市场、货币政策与宏观金融分析，共 28 个主题章节。无需构建工具或第三方 CDN，页面可在本地浏览器打开，也可部署到 GitHub Pages。

> **内容状态：** 第 01–21 章已完成第一轮深度重构：独立叙事、图解、公式/案例、来源证据清单和交互练习。第 22–28 章保留既有页面与 URL，后续按相同规范逐批迁移。

## 开始学习

- 在线入口（仓库启用 GitHub Pages 后）：<https://1998x-stack.github.io/monetary-banking-tutorial/>
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
├── courses.json               # 章节元数据
├── 01.html … 21.html          # 已重构的独立文章
├── 22.html … 28.html          # 保留原有 URL 的后续章节
├── theme.css                  # 旧章节使用的兼容样式
├── assets/
│   ├── css/
│   │   ├── home.css           # 首页设计系统
│   │   └── article.css        # 第 01–21 章共用文章样式
│   ├── js/
│   │   ├── home.js            # 首页本地搜索
│   │   └── article-demos.js   # 文章中的渐进增强交互
│   └── diagrams/              # 独立、可访问的 SVG 图解
├── evidence/                  # 每篇文章的事实—来源证据台账
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

## 本地质量检查

Python 3.10+：

```bash
python scripts/validate_site.py
python -m unittest discover -s tests -v
```

浏览器验收需要安装开发依赖：

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python scripts/browser_check.py --output artifacts/browser-qa
```

浏览器检查覆盖首页和第 01–21 章的 1440、768、390、360 像素视口、图片加载、页面溢出、控制台错误、打印模式及每篇文章的交互控件。未运行的检查不得标记为通过；CI 运行结果以 GitHub Actions 为准。

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
