#!/usr/bin/env python3
"""Deterministic analysis of clearly fictional macroeconomic observations.

The CSV is a teaching fixture, never live or real-world macroeconomic data.
"""
from __future__ import annotations

import argparse
import csv
import math
from datetime import datetime
from pathlib import Path

DATA = Path(__file__).with_name("sample_macro_data.csv")
COLUMNS = ("tsf_stock", "m2_stock", "cpi_index", "policy_rate")


def read_rows(path: Path) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    previous: str | None = None
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or not set(("date", *COLUMNS)).issubset(reader.fieldnames):
            raise ValueError("Missing required columns in CSV.")
        for row in reader:
            date = row["date"].strip()
            try:
                parsed = datetime.strptime(date, "%Y-%m")
                if parsed.strftime("%Y-%m") != date:
                    raise ValueError("Invalid date format")
                values = {key: float(row[key]) for key in COLUMNS}
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid row at {date!r}: {error}") from error
            if previous is not None and date <= previous:
                raise ValueError(f"Dates must be strictly increasing and unique: {date}")
            if not all(math.isfinite(value) for value in values.values()):
                raise ValueError(f"Non-finite value at {date}")
            if any(values[key] <= 0 for key in ("tsf_stock", "m2_stock", "cpi_index")):
                raise ValueError(f"Stock values and price index must be positive: {date}")
            rows[date] = values
            previous = date
    if not rows:
        raise ValueError("CSV contains no observations.")
    return rows


def pct_change(old: float, new: float) -> float:
    if old <= 0 or not math.isfinite(old) or not math.isfinite(new):
        raise ValueError("Percent changes require finite values and a positive baseline.")
    return (new / old - 1.0) * 100.0


def compare(rows: dict[str, dict[str, float]], baseline: str, current: str) -> dict[str, float]:
    if baseline not in rows or current not in rows:
        raise ValueError("Baseline and current months must both exist in the CSV.")
    b, c = datetime.strptime(baseline, "%Y-%m"), datetime.strptime(current, "%Y-%m")
    if c.year - b.year != 1 or c.month != b.month:
        raise ValueError("Year-on-year comparison requires the same month one year apart.")
    result = {key + "_growth": pct_change(rows[baseline][key], rows[current][key])
              for key in ("tsf_stock", "m2_stock", "cpi_index")}
    result["growth_gap_pp"] = result["tsf_stock_growth"] - result["m2_stock_growth"]
    result["policy_rate"] = rows[current]["policy_rate"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DATA)
    parser.add_argument("--baseline", default="2025-12")
    parser.add_argument("--current", default="2026-12")
    args = parser.parse_args()
    results = compare(read_rows(args.csv), args.baseline, args.current)
    print("教学虚构数据（不是实际经济统计）")
    print(f"对比月份：{args.baseline} → {args.current}")
    print(f"社融存量同比：{results['tsf_stock_growth']:.2f}%")
    print(f"M2 存量同比：{results['m2_stock_growth']:.2f}%")
    print(f"CPI 指数同期变化：{results['cpi_index_growth']:.2f}%")
    print(f"增速差（社融－M2）：{results['growth_gap_pp']:.2f} 个百分点")
    print(f"假设政策利率：{results['policy_rate']:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
