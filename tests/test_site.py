from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.validate_site import CHAPTERS, REBUILT, validate

class SiteValidationTests(unittest.TestCase):
    def test_repository_validation(self):
        self.assertEqual(validate(),[])
    def test_homepage_shows_rebuilt_progress_and_all_cards(self):
        raw=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertIn('<strong>28</strong><span>章节已深度重构</span>',raw)
        self.assertEqual(raw.count('class="chapter-card"'),28)
    def test_course_metadata_covers_all_chapters(self):
        data=json.loads((ROOT/"courses.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["chapters"]),28)
        self.assertEqual([item["num"] for item in data["chapters"]],[f"{i:02d}" for i in range(1,29)])
    def test_all_twenty_eight_are_independent_articles(self):
        for name in REBUILT:
            raw=(ROOT/name).read_text(encoding="utf-8")
            self.assertIn("<article>",raw)
            self.assertIn('id="references"',raw)
            self.assertIn("assets/css/article.css",raw)
            self.assertIn('class="article-toc"',raw)
    def test_revised_m1_scope_is_explained(self):
        raw=(ROOT/"03.html").read_text(encoding="utf-8")
        self.assertIn("2025 年 1 月",raw)
        self.assertIn("个人活期存款",raw)
        self.assertIn("非银行支付机构客户备付金",raw)
    def test_p2p_case_is_explicitly_hypothetical(self):
        raw=(ROOT/"05.html").read_text(encoding="utf-8")
        self.assertIn("假设案例",raw)
        self.assertNotIn("真实故事",raw)
    def test_new_chapters_have_evidence_and_interaction(self):
        for n in range(6,29):
            name=f"{n:02d}.html"
            ledger=ROOT/"evidence"/f"chapter-{n:02d}.json"
            self.assertTrue(ledger.is_file(),name)
            self.assertIn('data-demo=',(ROOT/name).read_text(encoding="utf-8"))
    def test_cip_formula_and_bop_accounts_are_distinguished(self):
        raw=(ROOT/"13.html").read_text(encoding="utf-8")
        self.assertIn("资本账户",raw)
        self.assertIn("金融账户",raw)
        self.assertIn("CNY/USD",raw)
    def test_nonbank_finance_distinguishes_nbfis_from_shadow_banking(self):
        raw=(ROOT/"14.html").read_text(encoding="utf-8")
        self.assertIn("不等于影子银行",raw)
        self.assertIn("流动性转换",raw)
        self.assertIn("256.8 万亿美元",raw)
    def test_money_multiplier_is_explicitly_a_simplified_model(self):
        raw=(ROOT/"15.html").read_text(encoding="utf-8")
        self.assertIn("不是银行每拿到 1 元准备金就机械贷出",raw)
        self.assertIn("rr = RR/D",raw)
    def test_money_demand_distinguishes_identity_from_theory(self):
        raw=(ROOT/"16.html").read_text(encoding="utf-8")
        self.assertIn("核算恒等式",raw)
        self.assertIn("交易、预防和投机",raw)
    def test_islm_equilibrium_example_is_consistent(self):
        raw=(ROOT/"19.html").read_text(encoding="utf-8")
        self.assertIn("Y=220、r=1.5",raw)
        self.assertIn("封闭经济",raw)
    def test_inflation_indices_are_not_interchangeable(self):
        raw=(ROOT/"20.html").read_text(encoding="utf-8")
        self.assertIn("PCE 使用 Fisher 理想指数公式",raw)
        self.assertIn("GDP 平减指数",raw)
    def test_transmission_lags_are_not_described_as_fixed(self):
        raw=(ROOT/"18.html").read_text(encoding="utf-8")
        self.assertIn("长、可变且不确定",raw)
        self.assertIn("信贷渠道",raw)
    def test_deflation_is_distinguished_from_disinflation(self):
        raw=(ROOT/"21.html").read_text(encoding="utf-8")
        self.assertIn("通胀放缓（disinflation）",raw)
        self.assertIn("不是一个“央行无论做什么都没用”的定理",raw)
    def test_systemic_risk_distinguishes_micro_and_macro_prudential(self):
        raw=(ROOT/"22.html").read_text(encoding="utf-8")
        self.assertIn("微观审慎监管",raw)
        self.assertIn("宏观审慎政策",raw)
        self.assertIn("信贷／GDP",raw)
    def test_policy_reports_do_not_treat_dots_as_voting(self):
        raw=(ROOT/"23.html").read_text(encoding="utf-8")
        self.assertIn("不是参与者投票",raw)
        self.assertIn("替代解释",raw)
    def test_tsf_and_m2_are_not_equated(self):
        raw=(ROOT/"24.html").read_text(encoding="utf-8")
        self.assertIn("不是一个未经估计就可被解释为",raw)
        self.assertIn("存量",raw)
    def test_taylor_rule_has_assumptions_and_errors(self):
        raw=(ROOT/"25.html").read_text(encoding="utf-8")
        self.assertIn("MAE",raw)
        self.assertIn("r*=2%",raw)
        self.assertIn("未来数据泄漏",raw)
    def test_ecny_new_framework_is_scoped_and_dated(self):
        raw=(ROOT/"26.html").read_text(encoding="utf-8")
        self.assertIn("2026 年 1 月 1 日",raw)
        self.assertIn("商业银行运营",raw)
        self.assertIn("不能继续把所有数字人民币钱包",raw)
    def test_stablecoin_rule_distinguishes_effective_date(self):
        raw=(ROOT/"27.html").read_text(encoding="utf-8")
        self.assertIn("2027 年 1 月 18 日",raw)
        self.assertIn("不能把将于 2027 年生效的规则",raw)
    def test_capstone_uses_fictional_data_and_local_script(self):
        raw=(ROOT/"28.html").read_text(encoding="utf-8")
        self.assertIn("完全假设数据",raw)
        self.assertIn("2026 年 12 月",raw)
        self.assertIn("examples/analyse_macro.py",raw)
        self.assertTrue((ROOT/"examples"/"sample_macro_data.csv").is_file())
    def test_new_articles_have_local_diagrams(self):
        import re
        from scripts.validate_site import Document
        for n in range(22,29):
            text=(ROOT/f"{n:02d}.html").read_text(encoding="utf-8")
            # A diagram may be a self-contained inline SVG or a local <img> asset;
            # either way each article must ship its own offline, accessible figure.
            inline=[m for m in re.findall(r'<svg\b.*?</svg>',text,flags=re.S)
                    if 'viewBox=' in m and ('<title' in m or '<desc' in m)]
            doc=Document()
            doc.feed(text)
            self.assertTrue(inline or doc.images,f"{n:02d}.html has no local diagram")
            self.assertTrue(all(alt for src,alt in doc.images))
    def test_knowledge_graph_has_84_verified_section_links(self):
        from scripts.validate_site import Document
        data=json.loads((ROOT/"knowledge"/"concept-links.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["chapters"]),28)
        self.assertEqual(sum(len(c["related"]) for c in data["chapters"]),84)
        for item in data["chapters"]:
            article=ROOT/f'{item["chapter"]}.html'
            text=article.read_text(encoding="utf-8")
            self.assertIn('id="concept-bridge"',text)
            self.assertEqual(text.count('class="concept-link"'),3)
            for rel in item["related"]:
                self.assertNotEqual(rel["to"],item["chapter"])
                target=(ROOT/f'{rel["to"]}.html').read_text(encoding="utf-8")
                doc=Document();doc.feed(target)
                self.assertIn(rel["anchor"],doc.ids)
                self.assertIn(f'href="{rel["to"]}.html#{rel["anchor"]}"',text)

    def test_knowledge_map_is_static_and_complete(self):
        raw=(ROOT/"knowledge-map.html").read_text(encoding="utf-8")
        self.assertEqual(raw.count('class="knowledge-card"'),28)
        self.assertEqual(raw.count('class="knowledge-edge"'),9)
        self.assertNotIn('fetch(',raw)
        self.assertIn('href="knowledge-map.html"',(ROOT/"index.html").read_text(encoding="utf-8"))

    def test_fx_audit_preserves_preliminary_and_revised_values(self):
        raw=(ROOT/"13.html").read_text(encoding="utf-8")
        self.assertIn("9.6 万亿美元",raw)
        self.assertIn("9.5 万亿美元",raw)
        self.assertIn("增长 27%",raw)
        self.assertIn("BPM7",raw)
        ledger=json.loads((ROOT/"evidence"/"chapter-13.json").read_text(encoding="utf-8"))
        claim_ids={x["id"] for x in ledger["claims"]}
        self.assertTrue({"bis-fx-revised","bpm7-released","bpm7-transition"}.issubset(claim_ids))

    def test_every_article_has_keyboard_scrollable_tables(self):
        for i in range(1,29):
            h=(ROOT/f"{i:02d}.html").read_text(encoding="utf-8")
            self.assertNotIn('class="table-scroll"><table>',h)
            self.assertNotIn('class="math-scroll"><math',h)

    def test_fx_cip_diagram_matches_formula(self):
        h=(ROOT/"13.html").read_text(encoding="utf-8")
        self.assertIn("assets/diagrams/covered-interest-parity.svg",h)
        svg=(ROOT/"assets"/"diagrams"/"covered-interest-parity.svg").read_text(encoding="utf-8")
        self.assertIn("1.04 × 7.0615",svg)
        self.assertIn("7.20 × 1.02",svg)
    def test_yield_curve_warning_is_not_deterministic(self):
        raw=(ROOT/"07.html").read_text(encoding="utf-8")
        self.assertIn("仅凭一次倒挂就预测衰退发生日期",raw)
        self.assertIn("期限溢价",raw)

if __name__=="__main__": unittest.main()
