"""Regression gates for second-pass one-by-one HTML fact and maths checks."""
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_sources import collect


class ChapterByChapterAuditTests(unittest.TestCase):
    def test_every_chapter_has_a_distinct_reproducible_check(self):
        titles = []
        for i in range(1, 29):
            path = ROOT / f"{i:02d}.html"
            html = path.read_text(encoding="utf-8")
            with self.subTest(chapter=i):
                self.assertEqual(html.count('id="audit-case"'), 1)
                self.assertGreaterEqual(html.count('href="#audit-case"'), 2)
                self.assertIn('class="audit-disclaimer"', html)
                self.assertIn('id="concept-bridge"', html)
                self.assertIn('id="references"', html)
                title = html.split('id="audit-case-title">', 1)[1].split('</h2>', 1)[0]
                self.assertGreater(len(title), 12)
                titles.append(title)
                evidence = json.loads((ROOT / "evidence" / f"chapter-{i:02d}.json").read_text(encoding="utf-8"))
                self.assertEqual(sum(c["id"] == "second-pass-worked-case" for c in evidence["claims"]), 1)
        self.assertEqual(len(set(titles)), 28, "Checks must not be duplicated boilerplate.")

    def test_source_ledgers_are_all_structurally_audited(self):
        report = collect()
        self.assertEqual(report["errors"], [])
        self.assertGreater(report["claims"], 140)
        self.assertGreater(report["unique_urls"], 55)
        self.assertEqual(report["mode"], "offline")
        self.assertIn("not HTTP reachability", report["warning"])

    def test_cashflow_and_formula_oracles(self):
        values = {
            "expected_credit_loss": 1_000_000 * .02 * .4,
            "credit_stress_loss": 1_000_000 * .04 * .5,
            "fisher_deflation": (1.02/.98-1)*100,
            "one_year_zero_coupon_yield_5": 100/1.05,
            "one_year_zero_coupon_yield_6": 100/1.06,
            "liquidity_fire_sale_book_value": 2/.8,
            "capital_ratio_rwa_stress": 7/120*100,
            "repo_act365": 10_000_000*.02*7/365,
            "one_year_coupon_bond": 104/1.05,
            "cip_cny_per_usd": 7.20*1.02/1.04,
            "money_multiplier_stress": 1.1/(.1+.1+.1),
            "velocity_after_money_growth": 200/110,
            "new_credit_rate": 1.3+2.6,
            "new_market_spread_rate": -.25+.5,
            "price_index_pce_inflation": (102.5/100-1)*100,
            "deflation_real_debt": 100/.95,
            "deflation_real_rate": (1.01/.97-1)*100,
            "stress_stablecoin_cover": 105*(1-.10)/100*100,
            "cpi_index_in_capstone": (102.5/101-1)*100,
        }
        expected = {
            "expected_credit_loss": 8000,
            "credit_stress_loss": 20000,
            "fisher_deflation": 4.08163265,
            "one_year_zero_coupon_yield_5": 95.238095,
            "one_year_zero_coupon_yield_6": 94.339623,
            "liquidity_fire_sale_book_value": 2.5,
            "capital_ratio_rwa_stress": 5.833333,
            "repo_act365": 3835.616438,
            "one_year_coupon_bond": 99.047619,
            "cip_cny_per_usd": 7.06153846,
            "money_multiplier_stress": 3.66666667,
            "velocity_after_money_growth": 1.81818182,
            "new_credit_rate": 3.9,
            "new_market_spread_rate": .25,
            "price_index_pce_inflation": 2.5,
            "deflation_real_debt": 105.2631579,
            "deflation_real_rate": 4.12371134,
            "stress_stablecoin_cover": 94.5,
            "cpi_index_in_capstone": 1.48514851485,
        }
        for name, actual in values.items():
            with self.subTest(formula=name):
                self.assertAlmostEqual(actual, expected[name], places=5)

    def test_islm_two_equations_both_hold(self):
        Y, rate = 220.0, 1.5
        self.assertAlmostEqual(.2*Y, 59-10*rate)
        self.assertAlmostEqual(.5*Y-20*rate, 80)

    def test_ytm_discount_rate_vs_realized_return_is_explicit(self):
        html = (ROOT/"07.html").read_text(encoding="utf-8")
        self.assertIn("计算 YTM 本身", html)
        self.assertIn("票息再投资", html)
        self.assertIn("94.34 元", html)
        self.assertNotIn("通常隐含按该收益率再投资等假设", html)

    def test_recent_official_rule_dates_and_types(self):
        article = (ROOT/"26.html").read_text(encoding="utf-8")
        self.assertIn("一、二、三类实名钱包", article)
        self.assertIn("2026 年 1 月 1 日", article)
        article = (ROOT/"27.html").read_text(encoding="utf-8")
        self.assertIn("2027 年 1 月 18 日", article)
        article = (ROOT/"13.html").read_text(encoding="utf-8")
        self.assertIn("BPM7", article)
        self.assertIn("9.6 万亿美元", article)
        self.assertIn("9.5 万亿美元", article)


if __name__ == "__main__":
    unittest.main()
