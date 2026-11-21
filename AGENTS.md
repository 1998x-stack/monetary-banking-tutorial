# Repository authoring rules

## Purpose
Maintain a trustworthy, independently readable Chinese monetary-and-banking course. The first five chapters define the editorial and engineering standard for later migrations.

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

## Repository workflow
1. Preserve existing chapter URLs unless an explicit migration plan includes redirects.
2. Update `courses.json` whenever chapter title, topic, group or file path changes.
3. Add/update the corresponding evidence ledger when facts or citations change.
4. Run `python scripts/validate_site.py`, unit tests and Chromium browser checks.
5. Inspect desktop, tablet, 390px and 360px mobile layouts; check print mode and at least one real interaction per interactive article.
6. Never weaken a test simply to make a failing page pass. Record any unverified check honestly.
7. Keep build/test notes in README or CI artifacts, not in the reader-facing article.
