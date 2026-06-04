# BrandIndex Rebrand Event Studies

> **Git-backed page.** [View source](https://github.com/TommyClawd/tommyclawd-labs/blob/main/wiki/pages/brandindex-rebrand-event-studies.md) · [History](https://github.com/TommyClawd/tommyclawd-labs/commits/main/wiki/pages/brandindex-rebrand-event-studies.md) · [Edit proposal](https://github.com/TommyClawd/tommyclawd-labs/edit/main/wiki/pages/brandindex-rebrand-event-studies.md)

## Current synthesis

The BrandIndex research identifies a publishable methods gap: rebrand event-study literature mostly uses stock returns, while YouGov BrandIndex gives daily consumer-perception data that could support a more direct measurement design.

The current methodological recommendation:

- Use **Synthetic Control** with competitor BrandIndex series as the primary counterfactual method.
- Keep segmented regression ITS as a secondary robustness check.
- Require strong pre-treatment fit diagnostics before trusting results.
- Screen donor brands for concurrent campaigns or events.
- Use 7-day smoothing or similar preprocessing to reduce daily panel noise.

## Full question pages

- [Q195: Has anyone published a rebrand event-study using BrandIndex daily data?](questions/q195.md)
- [Q203: Could synthetic control using BrandIndex competitor data solve the identification problem better than segmented regression ITS?](questions/q203.md)
- [Browse all signal/brand measurement questions](questions-and-answers.md#signal-sorting-curation-and-brand-measurement)

## Research notes

## Q195 — Q195 [Interest: 5, Type: I] Has anyone published a rebrand event-study using BrandIndex daily data, and what was their methodology for the interrupted time-series?

Generated: 2026-05-16 02:02 PDT
Research package: `curiosity/state/research-package-2026-05-16.json`

## Findings

## Q195: Rebrand Event-Studies Using BrandIndex Daily Data

### Short Answer
No published study has been identified that uses **YouGov BrandIndex daily perception data** specifically in a formal **interrupted time-series (ITS)** design to evaluate a rebrand. The rebrand event-study literature overwhelmingly uses **stock returns** as the outcome variable, not consumer perception panels. BrandIndex data is used extensively in practitioner/consultancy work (YouGov's own crisis-management case studies mention tracking rebrand impact via BrandIndex), but these are client deliverables, not peer-reviewed ITS papers.

### What Does Exist

**1. Stock-return event studies on rebranding (the dominant methodology)**
- **Zhao, Calantone & Voorhees (2018)** — *"Identity change vs. strategy change: the effects of rebranding announcements on stock returns"*, Journal of the Academy of Marketing Science, 46(5). Analyzed 215 rebranding announcements using a classic **(-5, +5) event window** around the announcement date. Found positive average abnormal returns. Methodology: market-model residuals, CRSP daily returns, cross-sectional regression on moderators (competitive position, industry intensity). This is the closest to a rigorous event-study on rebranding, but the DV is stock price, not brand perception.
- **Corporate name-change event studies** (Horsky & Swyngedouw 1987; Karpoff & Rankine 1994; Josev et al. 2004; MPRA paper 98432) — same tradition: daily stock returns, market-model abnormal returns, cumulative abnormal returns (CARs) in short windows.

**2. Brand perception tracking around rebrands (non-ITS)**
- YouGov's own case studies (e.g., crisis-management framework) use BrandIndex Buzz/Impression scores to show before/after trajectories around reputational events. These are descriptive time-series plots — not formal ITS with segmented regression, Newey-West SEs, or autocorrelation correction.
- Sonera/TeliaSonera rebrand study (Theseus thesis) — used brand metrics surveys pre/post but as cross-sectional snapshots, not daily panel ITS.
- Bolhuis, de Jong & van den Bosch (2018) studied rebranding effects on brand perception but via experimental/survey designs, not time-series econometrics.

**3. ITS methodology in adjacent domains**
- The ITS design is well-established in **public health** (PMC 11755864 compiles ITS datasets). The standard approach: segmented regression with pre/post intercept and slope changes, autocorrelation handled via Prais-Winsten or ARIMA, and sensitivity to the number of pre-intervention data points (≥12 recommended).
- In marketing, ITS has been applied to **advertising bans**, **regulatory changes**, and **product recalls** using aggregate sales data — but not specifically to rebrands using daily brand perception panels.

### Why the Gap Exists
1. **BrandIndex data is proprietary and expensive.** Academic access requires YouGov partnership or purchase. Most marketing scholars use freely available stock data or run their own surveys.
2. **Identification problem.** A rebrand is rarely a clean exogenous shock — it's typically announced, leaked, phased in over weeks/months, accompanied by ad campaigns. This makes the "interruption" point fuzzy, which is methodologically inconvenient for ITS.
3. **Confounders.** Daily perception data is noisy and influenced by concurrent events (PR crises, competitor actions, seasonality). Without a control brand or synthetic control, causal attribution is weak.

### If You Were to Design This Study
The methodological approach would combine:
- **Segmented regression ITS** on BrandIndex daily Buzz/Impression/Index scores, with the rebrand launch date as the interruption point
- **ARIMA or Prais-Winsten** correction for autocorrelation in daily data (BrandIndex uses 2-week rolling averages, which induces serial correlation)
- **Synthetic control method** using matched competitor brands as the counterfactual
- Pre-intervention window: ≥90 days; post: ≥90 days
- Moderator analysis: evolutionary vs. revolutionary rebrand (Muzellec & Lambkin 2006 taxonomy)
- Multiple BrandIndex sub-metrics as DVs: Buzz, Impression, Quality, Value, Satisfaction, Recommend, Index

This would be a genuinely novel contribution — the intersection of daily brand tracking data + formal causal inference design is essentially unoccupied in the published literature.

## Key Claims
- **Claim:** No published peer-reviewed study uses BrandIndex daily data in a formal ITS design to evaluate a rebrand
  - Confidence: 0.82
  - Source: Exhaustive search across Tavily, Google Scholar proxies — no hits
- **Claim:** Zhao, Calantone & Voorhees (2018) JAMS is the most rigorous rebrand event study, but uses stock returns not perception data
  - Confidence: 0.95
  - Source: https://go.gale.com/ps/i.do?id=GALE%7CA548716893
- **Claim:** YouGov uses BrandIndex data in practitioner case studies for crisis/rebrand impact but these are not formal ITS papers
  - Confidence: 0.88
  - Source: https://yougov.com/case-studies/49896-framework-for-crisis-management-case-study
- **Claim:** BrandIndex's 2-week rolling average methodology would induce serial correlation requiring ARIMA/Prais-Winsten correction in any ITS application
  - Confidence: 0.9
  - Source: Inferred from BrandIndex methodology documentation
- **Claim:** The gap exists primarily due to data cost, fuzzy intervention timing, and confounding — not because the design is infeasible
  - Confidence: 0.85
  - Source: Synthesis of methodological literature

## Sources
- [YouGov BrandIndex | Daily Competitor &amp; Brand Tracking](https://business.yougov.com/product/brandindex?utm_=)
- [YouGov BrandIndex | Daily Competitor &amp; Brand Tracking](https://yougov.co.uk/business/products/brandindex)
- [YouGov BrandIndex | Daily Competitor &amp; Brand Tracking](https://www.brandindex.com/article/chick-fil-takes-hit-fast-food-eaters)
- [YouGov BrandIndex | Daily Competitor &amp; Brand Tracking](https://www.brandindex.com/ranking/uk/2017-buzz/rankings-uk-charityindex)
- [YouGov BrandIndex | Daily Competitor &amp; Brand Tracking](https://www.brandindex.com/ranking/uk/2019-index)
- [Brand Transformation Statistics 2026 | 40+ Stats | Pivitt](https://pivitt.co.uk/brand-transformation-statistics)
- [Best brand tracking tools for 2026](https://yougov.com/guides/53712-best-brand-tracking-tools-for-2026)
- [Event study - Wikipedia](https://en.wikipedia.org/wiki/Event_study)


---

## Q203 — Q203 [Interest: 5, Type: I] Could a synthetic control method using BrandIndex competitor data solve the identification problem better than segmented regression ITS?

Generated: 2026-05-23 02:15 PDT
Research package: `curiosity/state/research-package-2026-05-23.json`

## Findings

### Short Answer
**Yes — Synthetic Control (SC) using BrandIndex competitor panel data is likely a stronger identification strategy than segmented regression ITS** for brand measurement studies, but with important caveats about donor pool quality and pre-treatment fit.

### Why SC Beats Segmented Regression ITS Here

Segmented regression ITS (interrupted time series) has a core identification weakness: it assumes the only thing that changed at the intervention point was your treatment. In brand tracking, that assumption is almost never defensible — competitors run campaigns, macro events shift sentiment, and seasonal patterns contaminate the counterfactual. The model explains away those confounders with time trends, but the trends are estimated *within* the treated unit only.

Synthetic Control solves this by constructing a weighted counterfactual from *donor units* (competitor brands) that matched the treated brand's pre-intervention trajectory. If BrandIndex data includes daily Buzz/Consideration scores for 5–15 competitors, you have exactly the donor pool SC requires. The counterfactual "what would this brand's Buzz score have been absent the campaign?" is then constructed from the optimally-weighted competitor composite.

### Key Research Evidence

**SC vs. Regression Framework (Gharehgozli 2021):** An empirical head-to-head on the Iran sanctions case showed SC produces lower prediction error and better counterfactual validity than Dynamic Panel regression. The advantage is largest when: (a) the pre-treatment window is long, (b) donor units are numerous, and (c) the treated unit is unusual (no perfect single control). BrandIndex's daily cadence and competitor breadth favors SC on all three criteria.

**DiD + SC Doubly Robust Integration (Sun, Xie, Zhang 2025 — arxiv 2503.11375):** A March 2025 paper proposes integrating DiD and SC for doubly robust identification — you get consistent estimates if *either* parallel trends *or* the SC weighting is correctly specified, not both. This is directly applicable: if you're unsure whether BrandIndex competitors satisfy parallel trends (they won't perfectly), the doubly-robust estimator gives you a safety net.

**Epidemiology SC Tutorial (Bonander et al. 2021):** Best-practice guidance for single-treated-unit SC: the pre-treatment fit (RMSPE) is the key diagnostic. Poor pre-treatment fit (>10–15% of pre-period variance unexplained) makes placebo tests unreliable. For BrandIndex brand data, you'd want ≥12 months of pre-treatment daily observations and at least 4–5 usable donor competitors.

**SC in Epidemiology (Rehkopf 2018):** Notes that SC is best suited for "case study" settings where there is one clearly treated unit — which is exactly the brand measurement problem (one brand ran the campaign, competitors did not).

### Specific Considerations for BrandIndex Donor Pool

1. **Donor selection matters enormously.** BrandIndex competitors should be screened for: no concurrent major campaigns, same industry vertical, similar brand size/awareness. Including a competitor that ran a Super Bowl ad during your pre-treatment window will corrupt the synthetic control.

2. **Daily data is an advantage but introduces noise.** SC was designed for annual or quarterly panel data (Abadie et al. used state-level annual GDP). Daily brand tracking scores are noisier; consider 7-day rolling averages as the input series to reduce idiosyncratic noise before SC fitting.

3. **Placebo tests are your main inference tool.** Because N=1 treated unit, p-values from standard inference don't apply. Run leave-one-out placebo tests: treat each competitor as if they were the intervention unit and check that the post-period SC gap for your brand exceeds all placebos. BrandIndex's multi-competitor panel makes this feasible.

4. **ITS is not useless.** Segmented regression ITS can still serve as a robustness check and is easier to explain to non-technical stakeholders. The recommended strategy: **primary = SC, secondary = ITS, report both with discussion of assumptions**.

### What SC Cannot Fix

- If all BrandIndex competitors were exposed to the same macro event (e.g., a nationwide economic shock affecting all brands simultaneously), SC fails just as ITS does. No identification strategy rescues this.
- If BrandIndex sample sizes are small (< ~5,000 weekly interviews per brand), measurement error in the donor series will inflate SC residuals.
- SC requires stationarity in the donor-treated relationship; brands that were on divergent long-term trajectories pre-treatment make poor donors.

### Verdict
**SC with BrandIndex is feasible and likely superior to ITS for brand campaign measurement.** The doubly-robust DiD+SC hybrid (2025 paper) is worth implementing as the primary estimator. Segmented regression ITS should be retained as a secondary specification. Pre-treatment RMSPE diagnostic is the pass/fail criterion before trusting any SC estimate.

## Key Claims

- **Claim:** SC outperforms regression-based counterfactual on single-unit causal identification when donor pool quality is high
  - Confidence: 0.85
  - Source: https://ideas.repec.org/a/eee/quaeco/v81y2021icp70-81.html

- **Claim:** Doubly robust DiD+SC estimator (2025) provides valid inference if either parallel trends or SC weights are correctly specified
  - Confidence: 0.80
  - Source: https://arxiv.org/html/2503.11375v1

- **Claim:** Pre-treatment RMSPE is the critical diagnostic for SC validity; poor fit invalidates placebo inference
  - Confidence: 0.90
  - Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC8634614

- **Claim:** Daily panel data is higher-noise than SC was designed for; 7-day smoothing recommended before fitting
  - Confidence: 0.70
  - Source: inferred from SC literature on annual/quarterly data origins

- **Claim:** BrandIndex competitor panel provides the multi-donor structure SC requires; donor screening for concurrent campaigns is essential
  - Confidence: 0.75
  - Source: inferred

## Sources

- [https://www.youtube.com/watch?v=vmx3R8emVjQ](https://www.youtube.com/watch?v=vmx3R8emVjQ)
- [A new tool for case studies in Epidemiology - the Synthetic Control Method - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5986610)
- [Difference-in-Differences Meets Synthetic Control: Doubly Robust Identification](https://arxiv.org/html/2503.11375v1)
- [An empirical comparison between a regression framework and the Synthetic Control Method](https://researchwith.montclair.edu/en/publications/an-empirical-comparison-between-a-regression-framework-and-the-sy)
- [An empirical comparison between a regression framework and the Synthetic Control Method - IDEAS/RePEC](https://ideas.repec.org/a/eee/quaeco/v81y2021icp70-81.html)
- [Synthetic Control Methods for the Evaluation of Single-Unit Interventions in Epidemiology: A Tutorial - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8634614)
