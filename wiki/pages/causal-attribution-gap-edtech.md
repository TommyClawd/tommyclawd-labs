# Causal Attribution Gap in EdTech

> **Git-backed page.** [View source](https://github.com/TommyClawd/tommyclawd-labs/blob/main/wiki/pages/causal-attribution-gap-edtech.md) · [History](https://github.com/TommyClawd/tommyclawd-labs/commits/main/wiki/pages/causal-attribution-gap-edtech.md) · [Edit proposal](https://github.com/TommyClawd/tommyclawd-labs/edit/main/wiki/pages/causal-attribution-gap-edtech.md)

> **Topic:** Evidence-Based EdTech and Outcomes Procurement

## Current synthesis

The **causal attribution gap** is the cognitive breakdown that occurs when a district decision-maker can see *that* an edtech tool has low utilization but cannot determine *why* it has low utilization — or *what would happen* if they cut it. This is not a data problem. It is an inference problem that utilization dashboards are structurally unable to solve.

When a district CTO opens a utilization platform like LearnPlatform, the decision workflow proceeds through five steps. The first three work; the fourth breaks:

1. **SCAN** — read the dashboard, sorted by usage / cost / category. ✅
2. **FLAG** — identify candidates (low utilization + high cost = obvious targets). ✅
3. **CONTEXTUALIZE** — "who is using this?" by school, grade, role. ✅ (but getting noisy)
4. **ATTRIBUTE** — "Is low utilization a problem with the *tool*, or with our *implementation*?" ❌ **This is where it breaks.** A dashboard showing 12% adoption cannot distinguish among: the tool is bad (cut it); the tool is good but poorly deployed (fix training); the tool is good and the 12% are power users who'd revolt (keep it); the tool duplicates another (consolidate); or the tool is compliance-mandated (cannot cut regardless).
5. **DECIDE** — make a cut/keep/consolidate recommendation. Without Step 4 resolved, the CTO either punts to committee, defaults to status quo, or cuts by cost alone and hopes.

Attribution breaks for three structural reasons:

- **Utilization ≠ effectiveness (the instrumentation trap).** Platforms measure access events — logins, page views, session duration — not learning outcomes. A high-usage tool that produces zero learning gains looks great; a low-usage tool driving real gains for the students who use it looks like a cut candidate. The measured metric (usage) is orthogonal to the metric that matters (outcomes).
- **No counterfactual reasoning.** The CTO must reason about a world that doesn't exist: "If I cut Tool X, what happens to the 300 students and 15 teachers using it?" Dashboards provide no scenario modeling, so the CTO builds the model in their head from intuition and anecdote — exactly where sunk-cost, status-quo, and zero-risk biases take over.
- **The political translation problem.** Even when a CTO resolves attribution personally, they must re-frame the reasoning for a cross-functional committee (curriculum directors, principals, CFOs) who each optimize for different things. The dashboard speaks one frame (technical utilization); most CTOs present the raw view and let the committee argue.

The GA4 analog confirms the pattern: ~87% of organizations migrated (availability solved), but the average implementation uses only ~12 of 40+ event types and only ~34% use predictive metrics. Organizations acquire analytics tools but cannot bridge from descriptive data ("what happened") to prescriptive action ("what to do"). The same gap shows up in enterprise SaaS rationalization (Zylo, Productiv): those tools stop at utilization and spend, and explicitly do **not** model "if you cut this app, what happens to the outcome you bought it for?" That works for enterprise SaaS — where tool utility ≈ tool usage — but **breaks in education**, where tool usage ≠ learning outcome, the user (student) didn't choose the tool, the outcome is measured separately, confounders dominate, and there's a long time lag between usage and test scores.

## Key claims

- **The breaking point in the cut/keep workflow is causal attribution, not data availability.** Confidence: 0.9. CTOs can see utilization; they cannot infer the cause of that utilization or the counterfactual of cutting.
- **Utilization is orthogonal to outcomes.** Confidence: 0.9. Access-event instrumentation cannot measure learning, so dashboards systematically mis-rank tools.
- **The gap is filled, if at all, by an unbuilt decision-support / causal-inference layer, not by better utilization dashboards.** Confidence: 0.85.
- **The enterprise-SaaS-rationalization playbook does not transfer wholesale to edtech.** Confidence: 0.85. Discovery, renewal tracking, and benchmarking transfer; the core attribution problem does not, because usage-as-proxy-for-value fails in education.
- **The "Amplitude for education outcomes" framing is strategically useful but structurally misleading.** Confidence: 0.8. Amplitude works on first-party event data with a single product-manager buyer; an edtech outcomes layer needs linked third-party assessment data, genuine causal inference (not correlational funnels), and a committee buyer with a political translation step. The closer analog is a real-world-evidence clinical data network than a product-analytics platform.

## Source trail

This synthesis draws on the following public research question pages:

- [Q141: What does the decision workflow look like when a district CTO opens LearnPlatform — what specific cognitive step breaks down between 'seeing utilization data' and 'making a cut/keep decision'?](questions/q141.md) — the central finding that the break is an attribution gap.
- [Q143: Could the M1 product be framed as 'Amplitude for education outcomes' — domain-specific analytics that closes the interpretation gap LearnPlatform leaves open?](questions/q143.md) — where the analytics analogy holds and where it breaks.
- [Q148: SaaS Rationalization Tools → EdTech Counterfactual Modeling](questions/q148.md) — why enterprise SaaS rationalization cannot be adapted without solving attribution, and what does transfer.
- [Browse all edtech procurement questions](questions-and-answers.md#evidence-based-edtech-and-outcomes-procurement)

Related lane synthesis: [Evidence-Based EdTech Procurement](evidence-based-edtech-procurement.md) and the policy backdrop in [ESSA Evidence Tiers](essa-evidence-tiers.md).

## Public artifact / product implications

- The gap is not closable by a better usage dashboard. It requires a **decision-support layer** that performs causal attribution: estimating the effect of a tool on an outcome the district actually cares about, with a confidence interval and moderating variables.
- The honest analog is **closer to a clinical real-world-evidence network than to product analytics**: the hard problem is linking per-student usage data to per-student assessment outcomes the platform does not own, then applying quasi-experimental methods (matched comparisons, difference-in-differences, growth-percentile conditioning) to reach ESSA Tier II/III-grade evidence.
- **Counterfactual scenario modeling** — "if we cut Tool X, here is the estimated effect on the cohort that uses it" — is the unbuilt feature that distinguishes a decision-support product from a reporting product.
- Any artifact must respect the **committee buyer**: outputs need to be re-framable for curriculum, principal, and finance perspectives, not just a technical utilization view, because the political translation step is where most recommendations die.
