# Repository authoring rules

## Purpose
Maintain a trustworthy, independently readable Chinese monetary-and-banking course. All 28 chapters use the same independently readable, evidence-grounded editorial and engineering standard.

## Non-negotiable article rules
1. Every chapter must stand alone. A reader who opens one URL directly must be able to understand the question, background, terms, mechanism, equations, examples, caveats and conclusion without reading another chapter first.
2. Never write meta descriptions such as “本讲义介绍了……”, “课件提到了……”, “上一章已经讲过……” or “如前文所述” as substitutes for explanation. Reintroduce the minimum context when a concept is needed.
3. Do not invent a “真实故事”, named person, company, quotation, market event or statistic. Hypothetical cases must be labeled “假设案例” or “教学示例”.
4. Distinguish established facts, textbook models, competing theories, interpretations and illustrative calculations. Do not present one contested explanation as the only historical account.
5. Every time-sensitive statistic must include its period, unit, statistical definition and source. Explain breaks in series when statistical scope changes.
6. Use primary sources where possible: PBOC, NBS, State Council, regulators, IMF, BIS, central banks, statutes and original academic research. Put a source link near the claim and record the claim in the chapter's `evidence/chapter-NN.json`.
7. Every substantive formula needs symbol definitions, units, assumptions and a worked example. A simplified formula must be explicitly labeled as an approximation.
8. Keep historical regimes, jurisdictions and dates distinct. Never silently apply current institutional rules to earlier periods.
9. Write original diagrams. SVGs must include `<title>`, `<desc>`, a `viewBox`, legible labels and a meaningful adjacent caption.
10. Use semantic HTML, one H1, ordered heading levels, keyboard-operable native controls, visible focus, responsive layouts and print styles. Do not depend on remote fonts, scripts, stylesheets or CDN math renderers.

## Narrative structure
Prefer: concrete question → baseline intuition → mechanism → stepwise diagram → equation or institutional rule → worked example → limitations / common misreadings → concise synthesis → sources.

Use progressive disclosure: each figure should answer one question. Captions must explain the diagram without requiring hover or animation. Interactivity is an enhancement; static text and diagrams must remain useful without JavaScript.

## Financial and monetary accuracy
- Distinguish central-bank liabilities (cash/reserves), commercial-bank deposit liabilities and non-bank financial claims.
- Do not teach a fixed reserve multiplier as a literal description of modern bank lending. Explain balance-sheet mechanics and constraints.
- Do not equate money supply with total wealth, the fiscal deficit, or “cash printed”.
- M0/M1/M2 are jurisdiction-specific statistical aggregates. State the applicable definition and date.
- Explain that the barter-origin story is a model, not a universally established historical sequence.
- Distinguish financial credit reporting from broader public/social credit-information systems.
- Label expected-loss equations and risk parameters as model estimates, not certain predictions.

## Current-data and reproducibility safeguards
- The 2026-01-01 e-CNY framework treats commercial-bank-operated relevant wallets as deposit liabilities for interest, deposit insurance and reserve-requirement purposes. Do not describe every wallet as cash-only M0 or universally as an unconditional central-bank liability; specify wallet and operator type.
- The U.S. GENIUS Act was enacted in July 2025, and the OCC 2026 final rule has a January 2027 effective date. Distinguish enactment from the effective date before suggesting any rule is in force.
- The e-CNY and stablecoin regime may evolve; check current primary official sources and state the as-of date.
- Treat TSF/AFRE flows, TSF/AFRE stocks and M2 as different statistical objects. The TSF-M2 growth-rate difference is not an accounting identity for credit demand minus monetary supply.
- Historical macro forecasts require release vintage, observation period, forecast horizon, output definition, benchmark and out-of-sample errors. Do not use subsequently revised observations as if they were available in real time.
- In `examples/`, all provided CSV numbers (including future 2026-12 values) are fictional teaching fixtures. Never label them actual or current market information.
- Keep Python examples deterministic, dependency-light, validation-first and covered by unit tests.

## Deep-audit knowledge graph and evidence maintenance
- `knowledge/concept-links.json` contains exactly 28 source chapters with 3 manually curated links each. Every link has a real chapter section fragment, a reader-facing explanation title and a causal reason. Keep all 84 links in sync with article HTML; generated navigation must remain fully usable without JavaScript.
- Each article links to `knowledge-map.html`; the map has five learning routes and selected causal bridges. Never replace explanatory prose with “see chapter X” as a prerequisite.
- Tables and formulas that overflow on mobile must have a keyboard-accessible scroll region with a useful label. Check 360px as well as 390px devices, and check first-tab skip navigation and native MathML geometry.
- For BIS foreign-exchange turnover, distinguish preliminary September 2025 reports (9.6T USD/day, +28%) from later BIS December 2025 analysis (9.5T USD/day, +27%); cite the version and retain both values when teaching the impact of revisions.
- The IMF published BPM7 in March 2025 while countries may still compile using BPM6 as standards are phased in. Specify which standard a country uses and do not assume same-day global implementation.
- Use `reports/deep-audit-2026-11-22.md` for this audit's traceability. Keep future audit reports separate and never replace dated official evidence with unsupported remembered values.

## Third-pass per-HTML verification and evidence integrity
- Every `NN.html` (01–28) now contains a unique `#audit-case`: an independently useful numeric worked example or mechanism counterexample, with assumptions, units, a checkable result, limitations and desktop/mobile TOC anchors. A one-line boilerplate substitution is not acceptable.
- Update `evidence/chapter-NN.json` with `second-pass-worked-case`. Use `illustrative` for a fictional calculation without a source; use `derived` with a real source URL when deriving a sourced institutional/mechanistic claim. Never mark hypothetical numbers themselves as real official observations.
- Run `python scripts/audit_sources.py` to check all 28 ledgers for unique IDs, URL syntax, missing references and evidence status. An HTTP 200 only tests reachability; it does not validate the proposition. HTTP 403/429 and timeouts are inconclusive.
- Run `python -m unittest discover -s tests -v` for independent numeric oracles and the existing site tests, and execute Chromium responsive, keyboard anchor, image, MathML, interaction and print checks.
- Use `reports/html-by-html-audit-2026-11-22.md` as the individual chapter audit trail, with explicit caveats and official sources. Reassess date-scoped facts each time a new update is added.

## Repository workflow
1. Preserve existing chapter URLs unless an explicit migration plan includes redirects. Chapters 01–28 use the shared article design system.
2. Update `courses.json` whenever chapter title, topic, group or file path changes; keep the homepage's 28 static chapter cards in sync.
3. Add/update the corresponding evidence ledger when facts or citations change.
4. Run `python scripts/validate_site.py`, unit tests and Chromium browser checks.
5. Inspect desktop, tablet, 390px and 360px mobile layouts; check print mode and at least one real interaction per interactive article.
6. Never weaken a test simply to make a failing page pass. Record any unverified check honestly.
7. Keep build/test notes in README or CI artifacts, not in the reader-facing article.
