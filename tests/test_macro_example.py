from __future__ import annotations
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from examples.analyse_macro import DATA, read_rows, pct_change, compare


class ReproducibleMacroExampleTests(unittest.TestCase):
    def test_example_math(self):
        values = compare(read_rows(DATA), "2025-12", "2026-12")
        self.assertAlmostEqual(values["tsf_stock_growth"], 6.0)
        self.assertAlmostEqual(values["m2_stock_growth"], 6.0)
        self.assertAlmostEqual(values["cpi_index_growth"], (102.5/101-1)*100)
        self.assertAlmostEqual(values["growth_gap_pp"], 0.0)
        self.assertAlmostEqual(values["policy_rate"], 1.6)

    def test_duplicate_dates_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "dupe.csv"
            path.write_text("date,tsf_stock,m2_stock,cpi_index,policy_rate\n2025-12,1,1,1,1\n2025-12,2,2,2,1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "strictly increasing"):
                read_rows(path)

    def test_zero_stock_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "zero.csv"
            path.write_text("date,tsf_stock,m2_stock,cpi_index,policy_rate\n2025-12,0,1,1,1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "positive"):
                read_rows(path)

    def test_non_finite_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "nan.csv"
            path.write_text("date,tsf_stock,m2_stock,cpi_index,policy_rate\n2025-12,NaN,1,1,1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Non-finite"):
                read_rows(path)

    def test_comparison_requires_same_month(self):
        rows = read_rows(DATA)
        with self.assertRaisesRegex(ValueError, "same month"):
            compare(rows, "2025-12", "2026-09")

    def test_pct_change_validates_baseline(self):
        with self.assertRaises(ValueError):
            pct_change(0, 100)


if __name__ == "__main__":
    unittest.main()
