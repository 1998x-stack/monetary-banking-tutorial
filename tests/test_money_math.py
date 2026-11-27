from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from examples import money_math as mm


class MoneyMathTests(unittest.TestCase):
    def test_fisher_exact_and_approximation(self):
        exact, approx = mm.fisher_real(3, 2)
        self.assertAlmostEqual(exact, 0.9803921, places=5)
        self.assertEqual(approx, 1.0)

    def test_repo_interest_matches_chapter_defaults(self):
        interest, total = mm.repo_interest(10_000_000, 1.8, 7)
        self.assertAlmostEqual(interest, 3452.0548, places=3)
        self.assertAlmostEqual(total, 10_003_452.0548, places=2)

    def test_bond_price_discounts_cashflows(self):
        self.assertAlmostEqual(mm.bond_price(100, 3, 4, 5), 95.5486, places=3)

    def test_money_multiplier_is_an_approximation(self):
        m, money = mm.money_multiplier(10, 10, 5, 100)
        self.assertAlmostEqual(m, 4.4, places=6)
        self.assertAlmostEqual(money, 440.0, places=6)

    def test_linear_money_demand(self):
        self.assertEqual(mm.money_demand_linear(1000, 2, 0.25, 3), 244.0)

    def test_islm_matches_two_equation_solution(self):
        y, r = mm.islm_equilibrium(25, 80)
        self.assertAlmostEqual(y, 220.0, places=6)
        self.assertAlmostEqual(r, 1.5, places=6)
        self.assertAlmostEqual(0.5 * y - 20.0 * r, 80.0, places=6)

    def test_inflation_and_deflation(self):
        self.assertAlmostEqual(mm.inflation_rate(100, 103), 3.0, places=6)
        real, burden = mm.deflation_burden(0.25, -2, 100)
        self.assertAlmostEqual(real, 2.25, places=6)
        self.assertAlmostEqual(burden, 102.0408, places=3)
        self.assertAlmostEqual(mm.fisher_real(1, -3)[0], 4.1237, places=3)

    def test_equity_loss_amplifies_with_leverage(self):
        before, after, loss = mm.equity_loss(100, 80, 10)
        self.assertEqual((before, after), (20.0, 10.0))
        self.assertAlmostEqual(loss, 50.0, places=6)

    def test_growth_taylor_expected_loss_and_coverage(self):
        self.assertAlmostEqual(mm.growth_rate(400, 424), 6.0, places=6)
        self.assertAlmostEqual(mm.taylor_rule(2, 3, 2, -1), 5.0, places=6)
        self.assertAlmostEqual(mm.expected_loss(2, 40, 1_000_000), 8000.0, places=6)
        stressed, coverage = mm.stablecoin_coverage(100, 105, 10)
        self.assertAlmostEqual(stressed, 94.5, places=6)
        self.assertAlmostEqual(coverage, 94.5, places=6)

    def test_fx_forward_matches_chapter_defaults(self):
        self.assertAlmostEqual(mm.fx_forward_rate(7.2, 2, 4), 7.061538, places=5)

    def test_invalid_inputs_are_rejected(self):
        for call in (
            lambda: mm.repo_interest(10, 2, 0),
            lambda: mm.money_multiplier(0, 0, 0, 100),
            lambda: mm.equity_loss(100, 100, 10),
            lambda: mm.stablecoin_coverage(100, 105, 150),
            lambda: mm.growth_rate(0, 5),
        ):
            with self.assertRaises(ValueError):
                call()

    def test_chapter_demo_defaults_match_module(self):
        checks = {
            "06.html": f"{mm.fisher_real(3, 2)[0]:.2f}%",
            "11.html": f"{mm.repo_interest(10_000_000, 1.8, 7)[0]:,.2f}",
            "12.html": f"{mm.bond_price(100, 3, 4, 5):.2f}",
            "13.html": f"{mm.fx_forward_rate(7.2, 2, 4):.4f}",
            "15.html": f"{mm.money_multiplier(10, 10, 5, 100)[0]:.2f}",
            "16.html": f"{mm.money_demand_linear(1000, 2, 0.25, 3):.0f}",
            "19.html": f"{mm.islm_equilibrium(25, 80)[0]:.1f}",
            "20.html": f"{mm.inflation_rate(100, 103):.2f}%",
            "21.html": f"{mm.deflation_burden(0.25, -2, 100)[0]:.2f}%",
            "22.html": f"{mm.equity_loss(100, 80, 10)[2]:.2f}%",
            "24.html": f"{mm.growth_rate(400, 424):.2f}%",
            "25.html": f"{mm.taylor_rule(2, 3, 2, -1):.2f}%",
            "27.html": f"{mm.stablecoin_coverage(100, 105, 10)[1]:.2f}%",
        }
        for page, expected in checks.items():
            text = (ROOT / page).read_text(encoding="utf-8")
            self.assertIn(expected, text, f"{page} static output missing {expected}")


if __name__ == "__main__":
    unittest.main()
