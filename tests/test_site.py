from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.validate_site import CHAPTERS, validate

class SiteValidationTests(unittest.TestCase):
    def test_repository_validation(self):
        self.assertEqual(validate(),[])
    def test_course_metadata_covers_all_chapters(self):
        data=json.loads((ROOT/"courses.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["chapters"]),28)
        self.assertEqual([x["num"] for x in data["chapters"]],[f"{i:02d}" for i in range(1,29)])
    def test_first_five_are_independent_articles(self):
        for name in CHAPTERS[:5]:
            raw=(ROOT/name).read_text(encoding="utf-8")
            self.assertIn("<article>",raw)
            self.assertIn('id="references"',raw)
            self.assertIn("assets/css/article.css",raw)
    def test_revised_m1_scope_is_explained(self):
        raw=(ROOT/"03.html").read_text(encoding="utf-8")
        self.assertIn("2025 年 1 月",raw)
        self.assertIn("个人活期存款",raw)
        self.assertIn("非银行支付机构客户备付金",raw)
    def test_p2p_case_is_explicitly_hypothetical(self):
        raw=(ROOT/"05.html").read_text(encoding="utf-8")
        self.assertIn("假设案例",raw)
        self.assertNotIn("真实故事",raw)

if __name__=="__main__": unittest.main()
