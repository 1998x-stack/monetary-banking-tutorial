#!/usr/bin/env python3
"""Deterministic finance formulas behind the chapter calculators.

Each function mirrors the arithmetic in the interactive demos of chapters
05/06/08/09/11/12/13/15/16/19/20/21/22/24/25/27. These are teaching
calculations, never live market data or forecasts.
"""
from __future__ import annotations

import math


def _finite(*values: float) -> None:
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Inputs must be finite numbers.")


def fisher_real(nominal_pct: float, inflation_pct: float) -> tuple[float, float]:
    """Exact and approximate real rate (chapter 06)."""
    _finite(nominal_pct, inflation_pct)
    i, p = nominal_pct / 100.0, inflation_pct / 100.0
    if i <= -1 or p <= -1:
        raise ValueError("Rates must exceed -100%.")
    return ((1 + i) / (1 + p) - 1) * 100.0, nominal_pct - inflation_pct


def repo_interest(principal: float, annual_rate_pct: float, days: int) -> tuple[float, float]:
    """ACT/365 repo interest and repayment (chapter 11)."""
    _finite(principal, annual_rate_pct)
    if principal < 0 or annual_rate_pct < 0 or days <= 0:
        raise ValueError("Require principal >= 0, rate >= 0 and days > 0.")
    interest = principal * annual_rate_pct / 100.0 * days / 365.0
    return interest, principal + interest


def bond_price(face: float, coupon_pct: float, ytm_pct: float, years: int) -> float:
    """Annual-coupon bond price from discounted cash flows (chapter 12)."""
    _finite(face, coupon_pct, ytm_pct)
    if face < 0 or coupon_pct < 0 or ytm_pct <= -100 or not 1 <= years <= 50:
        raise ValueError("Require face >= 0, coupon >= 0, ytm > -100% and 1-50 years.")
    y = ytm_pct / 100.0
    cashflows = [face * coupon_pct / 100.0 / (1 + y) ** t for t in range(1, years + 1)]
    return sum(cashflows) + face / (1 + y) ** years


def money_multiplier(cash_pct: float, reserve_pct: float, excess_pct: float, base: float) -> tuple[float, float]:
    """Simplified money multiplier, an approximation only (chapter 15)."""
    _finite(cash_pct, reserve_pct, excess_pct, base)
    if min(cash_pct, reserve_pct, excess_pct, base) < 0:
        raise ValueError("Ratios and base money must be non-negative.")
    c, rr, e = cash_pct / 100.0, reserve_pct / 100.0, excess_pct / 100.0
    denom = c + rr + e
    if denom <= 0:
        raise ValueError("Cash plus reserve ratios must be positive.")
    m = (1 + c) / denom
    return m, m * base


def money_demand_linear(income: float, rate: float, income_sens: float, rate_sens: float) -> float:
    """Linear money-demand teaching function (chapter 16)."""
    _finite(income, rate, income_sens, rate_sens)
    if min(income, rate, income_sens, rate_sens) < 0:
        raise ValueError("Inputs must be non-negative.")
    demand = income_sens * income - rate_sens * rate
    if demand < 0:
        raise ValueError("Parameters produce negative demand.")
    return demand


def islm_equilibrium(government: float, real_money: float) -> tuple[float, float]:
    """Closed-economy linear IS-LM equilibrium (chapter 19)."""
    _finite(government, real_money)
    if government < 0 or real_money <= 0:
        raise ValueError("Require non-negative G and positive real money.")
    c, c0, t, i0, b, k, h = 0.8, 20.0, 20.0, 30.0, 10.0, 0.5, 20.0
    a = c0 - c * t + i0 + government
    y = (a + b * real_money / h) / ((1 - c) + b * k / h)
    r = (k * y - real_money) / h
    return y, r


def inflation_rate(previous_index: float, current_index: float) -> float:
    """Period change of a price index (chapter 20)."""
    _finite(previous_index, current_index)
    if previous_index <= 0 or current_index <= 0:
        raise ValueError("Price indexes must be positive.")
    return (current_index / previous_index - 1) * 100.0


def deflation_burden(nominal_rate_pct: float, expected_inflation_pct: float,
                    nominal_debt: float) -> tuple[float, float]:
    """Fisher approximation and real debt burden (chapters 06 and 21)."""
    _finite(nominal_rate_pct, expected_inflation_pct, nominal_debt)
    if nominal_rate_pct <= -100 or expected_inflation_pct <= -100 or nominal_debt < 0:
        raise ValueError("Rates must exceed -100% and debt must be non-negative.")
    real_approx = nominal_rate_pct - expected_inflation_pct
    burden = nominal_debt / (1 + expected_inflation_pct / 100.0)
    return real_approx, burden


def equity_loss(assets: float, debt: float, shock_pct: float) -> tuple[float, float, float]:
    """Leverage-amplified equity loss in a stress test (chapter 22)."""
    _finite(assets, debt, shock_pct)
    if assets <= 0 or debt < 0 or debt >= assets or not 0 <= shock_pct <= 100:
        raise ValueError("Require assets > debt >= 0 and a 0-100% shock.")
    before = assets - debt
    after = assets * (1 - shock_pct / 100.0) - debt
    return before, after, (before - after) / before * 100.0


def growth_rate(old: float, new: float) -> float:
    """Year-on-year stock growth (chapter 24)."""
    _finite(old, new)
    if old <= 0 or new <= 0:
        raise ValueError("Stocks must be positive.")
    return (new / old - 1) * 100.0


def taylor_rule(neutral: float, inflation: float, target: float, gap: float) -> float:
    """Simplified Taylor rule benchmark, a model not a decision (chapter 25)."""
    _finite(neutral, inflation, target, gap)
    if max(abs(neutral), abs(inflation), abs(target), abs(gap)) > 100:
        raise ValueError("Parameters must be within +/-100.")
    return neutral + inflation + 0.5 * (inflation - target) + 0.5 * gap


def expected_loss(pd_pct: float, lgd_pct: float, ead: float) -> float:
    """Parameterised expected loss = PD x LGD x EAD (chapter 05)."""
    _finite(pd_pct, lgd_pct, ead)
    if not 0 <= pd_pct <= 100 or not 0 <= lgd_pct <= 100 or ead < 0:
        raise ValueError("Require 0-100% probabilities and non-negative EAD.")
    return ead * pd_pct / 100.0 * lgd_pct / 100.0


def stablecoin_coverage(liabilities: float, reserves: float, haircut_pct: float) -> tuple[float, float]:
    """Stressed reserve coverage of a stablecoin (chapter 27)."""
    _finite(liabilities, reserves, haircut_pct)
    if liabilities <= 0 or reserves < 0 or not 0 <= haircut_pct <= 100:
        raise ValueError("Require positive liabilities, non-negative reserves, 0-100% haircut.")
    stressed = reserves * (1 - haircut_pct / 100.0)
    return stressed, stressed / liabilities * 100.0


def fx_forward_rate(spot: float, domestic_pct: float, foreign_pct: float) -> float:
    """Covered interest parity one-year forward (chapter 13)."""
    _finite(spot, domestic_pct, foreign_pct)
    if spot <= 0 or domestic_pct <= -100 or foreign_pct <= -100:
        raise ValueError("Require positive spot and rates above -100%.")
    return spot * (1 + domestic_pct / 100.0) / (1 + foreign_pct / 100.0)


def main() -> int:
    """Reproduce the default values shown by the chapter calculators."""
    print("教学算术示例（不是真实货币或市场数据）")
    exact, approx = fisher_real(3, 2)
    print(f"费雪精确实际利率：{exact:.2f}%（近似 {approx:.2f}%）")
    interest, total = repo_interest(10_000_000, 1.8, 7)
    print(f"回购利息：{interest:,.2f} 元（到期偿还 {total:,.2f} 元）")
    print(f"债券理论价格：{bond_price(100, 3, 4, 5):.2f} 元")
    m, money = money_multiplier(10, 10, 5, 100)
    print(f"简化货币乘数：{m:.2f}（模型货币量 {money:.2f}）")
    y, r = islm_equilibrium(25, 80)
    print(f"IS-LM 均衡：Y≈{y:.1f}，r≈{r:.2f}")
    stressed, coverage = stablecoin_coverage(100, 105, 10)
    print(f"稳定币压力后储备：{stressed:.2f}，覆盖率 {coverage:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
