from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.validate_site import CHAPTERS, REBUILT, validate

class SiteValidationTests(unittest.TestCase):
    def test_repository_validation(self):
        self.assertEqual(validate(),[])
    def test_course_metadata_covers_all_chapters(self):
        data=json.loads((ROOT/"courses.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["chapters"]),28)
        self.assertEqual([item["num"] for item in data["chapters"]],[f"{i:02d}" for i in range(1,29)])
    def test_first_twenty_one_are_independent_articles(self):
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
        for n in range(6,22):
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
    def test_deflation_is_distinguished_from_disinflation(self):
        raw=(ROOT/"21.html").read_text(encoding="utf-8")
        self.assertIn("通胀放缓（disinflation）",raw)
        self.assertIn("不是一个“央行无论做什么都没用”的定理",raw)
    def test_yield_curve_warning_is_not_deterministic(self):
        raw=(ROOT/"07.html").read_text(encoding="utf-8")
        self.assertIn("仅凭一次倒挂就预测衰退发生日期",raw)
        self.assertIn("期限溢价",raw)

if __name__=="__main__": unittest.main()
