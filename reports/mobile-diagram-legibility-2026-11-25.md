# 移动端图解可读性修复记录（2026-11-25）

> 本记录只描述 2026-11-25 这一轮针对「窄屏下 SVG 图解文字过小」的检查与修复，
> 不替代 `reports/html-by-html-audit-2026-11-22.md` 的逐章事实核验，也不新增任何
> 未经核实的经济数据。

## 一、发现的问题

第 01–28 章的内联图解使用 `viewBox="0 0 900 …"`，并以 `figure svg{width:100%}`
随容器缩放。用 Chromium（真实 `file://` 加载，含本地 CSS）实测：

| 视口宽度 | 图解渲染宽度 | 最小标签实测高度 |
|---:|---:|---:|
| 1440px | ≈788px | ≈12–13px |
| 390px | ≈338px | ≈6px |
| 360px | ≈308px | ≈5–6px |

即：手机宽度下图解内的标注缩到约 5–6px，虽然页面不产生横向溢出、自动化 `blankSVG`
检查也为通过，但文字实际上不可读。这是自动门禁（只检查 SVG 是否有非零包围盒）
无法发现的缺陷。

## 二、修复方式

在 `assets/css/article.css` 增加窄屏规则，并把每个图解设为可聚焦的滚动区域：

- `@media(max-width:900px)` 下，`figure` 允许横向平移，`figure>svg{min-width:46rem}`，
  使 12–13px 的原始标注在手机上仍渲染约 10–12px；`figcaption{position:sticky;left:0}`
  保证图注在图解平移时保持可见。
- 第 01–28 章每个 `<figure>` 增加 `tabindex="0"`，并补充 `:focus-visible` 轮廓，
  与既有 `.table-scroll` 的键盘可滚动模式一致。
- `@media print` 下取消最小宽度与滚动，保持打印排版。
- 同时把参考书目中未转义的 `&` 修正为 `&amp;`（第 01、02、05 章，共 5 处），
  使文档成为结构合法的 HTML 而非依赖浏览器容错。

## 三、验证证据

- 站点结构：`python scripts/validate_site.py` → `SITE VALIDATION PASSED`。
- 单元测试：`python -m unittest discover -s tests` → 43 项全部通过；新增
  `test_every_diagram_is_a_keyboard_pannable_figure` 守卫每个图解都是可聚焦、
  带图注、且使用 46rem 最小宽度的滚动区域；`test_remaining_chapter_checks_have_numeric_oracles`
  为第 01/03/23/24/25/26 章的推演核验补充可独立复算的数值断言。
- 浏览器：脚本 `qa/verify_legibility.py`（运行日志目录，未提交仓库）对
  首页、知识地图与第 01–28 章在 1440、390、360px 下逐页实测，结论
  `PROBLEMS: []`：无横向溢出、无 JS 报错、每个图解可聚焦、最小标签高度 ≥11px。
- 抽样 `browser_check.py`（第 01、03 章）四种视口全部 `pass`。该脚本以
  `page.set_content` 渲染，相对路径的外部 CSS/JS 不会加载，因此其实例中
  「交互 failed」是工具限制而非页面缺陷：改用真实 `file://` 加载后，
  第 01、02、04、07、10、14、17、18、23、26、28 章的按钮交互均验证为可用。

## 四、尚未验证 / 局限

- 键盘方向键在该无头 Chromium（macOS）中不滚动聚焦的滚动容器；平移通过
  触控板横向手势与 `Shift+滚轮` 实测可用。此行为与既有表格滚动区域一致。
- 未测量真实设备上的触控惯性、旁白读屏顺序或字号放大（200%）下的表现。
