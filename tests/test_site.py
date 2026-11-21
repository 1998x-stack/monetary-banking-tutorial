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
    def test_first_thirteen_are_independent_articles(self):
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
        for n in range(6,14):
            name=f"{n:02d}.html"
            ledger=ROOT/"evidence"/f"chapter-{n:02d}.json"
            self.assertTrue(ledger.is_file(),name)
            self.assertIn('data-demo=',(ROOT/name).read_text(encoding="utf-8"))
    def test_cip_formula_and_bop_accounts_are_distinguished(self):
        raw=(ROOT/"13.html").read_text(encoding="utf-8")
        self.assertIn("资本账户",raw)
        self.assertIn("金融账户",raw)
        self.assertIn("CNY/USD",raw)
    def test_yield_curve_warning_is_not_deterministic(self):
        raw=(ROOT/"07.html").read_text(encoding="utf-8")
        self.assertIn("不是衰退日期预报",raw)
        self.assertIn("期限溢价",raw)

if __name__=="__main__": unittest.main()
