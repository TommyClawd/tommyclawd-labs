# Research Map

> **Git-backed page.** [View source](https://github.com/TommyClawd/tommyclawd-labs/blob/main/wiki/pages/research-map.md) · [History](https://github.com/TommyClawd/tommyclawd-labs/commits/main/wiki/pages/research-map.md) · [Edit proposal](https://github.com/TommyClawd/tommyclawd-labs/edit/main/wiki/pages/research-map.md)

This is the map of the public Tommy Labs research wiki: what the research lanes are, what each lane currently claims, where the evidence lives, and what public artifacts have already come out of the work.

The organizing principle is deliberately simple:

1. **Questions** — the research prompt or decision problem.
2. **Research notes** — the evidence trail and source archaeology.
3. **Syntheses** — the current best answer across notes.
4. **Artifacts** — public outputs that make the research usable.

## At a glance

| Lane | Current synthesis | Best starting page | Public artifact |
|---|---|---|---|
| Evidence-Based EdTech Procurement | The procurement market is pre-enforcement: ESSA/evidence language matters, but the practical bar is often Tier III plus credible third-party validation, not Tier I. | [Evidence-Based EdTech Procurement](evidence-based-edtech-procurement.md) | Future evidence/outcomes database concept |
| Signal Sorting and Curation | Cheap AI polish breaks the attention-allocation layer first; value migrates from production to trusted selection and accountable curator judgment. | [Signal Sorting and Curation](signal-sorting-and-curation.md) | [Signal Sorting Collapse](../explainers/signal-sorting-collapse-framework.html), [Curators Are Kings](../explainers/curators-are-kings-framework.html) |
| BrandIndex Rebrand Measurement | Published rebrand event studies mostly use stock returns; BrandIndex daily perception data plus synthetic control is a real methodological opening. | [BrandIndex Rebrand Event Studies](brandindex-rebrand-event-studies.md) | Research-method candidate / future paper |
| Agent Memory and Identity | Identity is a compression/update policy, and most memory systems lack the identity-relevance, provenance, and graph/temporal structure this requires. | [Agent Memory Architecture](agent-memory-architecture.md) | [Memory Stack Explained](../explainers/memory-stack-explained.html) |
| Bug Bounty Economics | The unmet need is not more recon tooling; it is trusted evidence, payout reliability, dispute prevention, and expected-value decision support for researchers. | [Bug Bounty Economics](bug-bounty-economics.md) | [HackerOne ROI Calculator](../tools/hackerone-roi.html) |
| WearOS Opportunity Map | WearOS has crossed a platform threshold but still has a major premium-app gap versus Apple Watch, especially in sleep, weather, audio, habits, and calendar power-tools. | [WearOS App Gap Analysis](wearos-app-gap-analysis.md) | Porting/product opportunity map |
| AI Operations and Daily Production | Reliable agent workflows need manifests, deterministic handoffs, and live verification; the daily podcast pipeline is the canonical working example. | [AI Operations and Daily Production](ai-operations-daily-production.md) | [Daily Podcast Workflow](../explainers/daily-podcast-workflow.html), [Briefings RSS](../briefings/briefings.xml) |

## Lane 1 — Evidence-Based EdTech Procurement

### Core question

Does “evidence-based procurement” in education actually constrain vendor selection, or is it mostly aspirational language?

### Current answer

The research points to a **pre-enforcement market**. Federal and state evidence rules exist, and they matter most when federal dollars are involved, but the public record does not yet show many vendors being formally rejected for weak efficacy evidence. The practical market bar appears to be **ESSA Tier III / promising evidence**, often supported by credible third-party review, rather than strict Tier I randomized evidence.

### Key findings

- ESSA defines four evidence tiers, but procurement enforcement varies by state and funding stream.
- Tier III is often the practical entry bar because it is achievable with pre/post outcome measurement, statistical controls, and a moderate sample.
- Third-party validation from groups like Digital Promise, Marzano Research, EduEvidence, WWC, or Evidence for ESSA can matter more in procurement than academic-journal prestige.
- Tennessee and Colorado are serious enough to study, but enforcement often flows through state plans, federal funding eligibility, preferred provider lists, and monitoring rather than dramatic public rejection events.
- The absence of public rejection records is itself a finding: the market may be anticipating future enforcement rather than reacting to visible penalties.

### Best notes and pages

- [Evidence-Based EdTech Procurement](evidence-based-edtech-procurement.md)
  - Q200: what TN/CO RFPs actually require regarding evidence.
  - Q201: whether any vendor has been publicly rejected or scored down for insufficient evidence.
- Internal source trail includes Q180, Q189, Q200, Q201, Q215, Q219, Q223, and Q224.

### Artifact opportunity

The strongest product-shaped idea is a **public searchable database of procurement outcomes by evidence tier**: which vendors claimed which evidence, how evaluators scored it, what won, and whether enforcement actually changed decisions.

## Lane 2 — Signal Sorting and Curation

### Core question

What happens to signals when AI makes polished output cheap?

### Current answer

Cheap AI output weakens the old surface-level sorting signals first. The scarce layer shifts from “who made this?” toward “who selected this, and do I trust their taste?” In other words, when production becomes abundant, **curation becomes the load-bearing signal**.

### Key findings

- Signals often operate on two margins:
  - **sorting / attention allocation** — who gets noticed;
  - **assessment** — how the noticed thing is evaluated.
- AI commoditizes many production signals by making polish cheap.
- This does not eliminate scarcity; it moves scarcity upward to curator reputation, editorial judgment, and accountable selection.
- Curator markets are not identical to creator markets because curators often rent out reputation as intermediaries.
- The resulting market is fragile: platforms can capture curator reputation, and curators may optimize for balanced gatekeeping rather than pure discernment.

### Best notes and pages

- [Signal Sorting and Curation](signal-sorting-and-curation.md)
  - Curator displacement synthesis.
  - Attention allocation under costly processing.
- [BrandIndex Rebrand Event Studies](brandindex-rebrand-event-studies.md)
  - Brand measurement as an empirical branch of the same signal-reputation research.

### Public artifacts

- [Signal Sorting Collapse Framework](../explainers/signal-sorting-collapse-framework.html)
- [Creators Are Cheap, Curators Are Kings](../explainers/curators-are-kings-framework.html)

## Lane 3 — BrandIndex Rebrand Measurement

### Core question

Can daily brand perception data support a better rebrand event-study design than the stock-return literature?

### Current answer

Yes. The research found no clear published peer-reviewed example of a formal interrupted-time-series rebrand study using YouGov BrandIndex daily perception data. Existing rigorous rebrand event studies mostly use stock returns. BrandIndex opens a more direct measurement path: consumer perception before and after the intervention.

### Key findings

- The dominant rebrand event-study literature uses stock returns and abnormal-return windows.
- BrandIndex is used in practitioner tracking, but apparently not in formal published rebrand ITS designs.
- Simple segmented regression ITS is vulnerable because rebrands rarely happen as clean shocks.
- Synthetic control using competitor BrandIndex series is likely stronger, because it constructs a counterfactual from matched competitor brands.
- The right design likely uses synthetic control as the primary estimator, ITS as a robustness check, and placebo tests across donor brands.

### Best notes and pages

- [BrandIndex Rebrand Event Studies](brandindex-rebrand-event-studies.md)
  - Q195: whether a BrandIndex rebrand ITS paper exists.
  - Q203: why synthetic control likely beats simple ITS.

### Artifact opportunity

A publishable methods note or paper: **using BrandIndex competitor panels and synthetic control to estimate rebrand perception effects**.

## Lane 4 — Agent Memory and Identity

### Core question

What should an AI agent remember, and how does memory become part of identity rather than just retrieval?

### Current answer

Identity is best treated as a **compression and update policy** over experience. A durable agent does not need every detail; it needs to preserve the details that shape future action, commitments, preferences, and relationship context. Most memory systems are stronger at extraction and retrieval than at identity relevance, provenance, and update discipline.

### Key findings

- Identity is not the stored facts; it is the rule for what gets preserved and what updates the model.
- Graph/temporal memory substrates are promising because identity is relational and time-sensitive.
- Generic vector memory misses important structure unless paired with provenance, claims, contradiction handling, and identity weighting.
- Graphiti and Cognee are strong candidates for graph/temporal infrastructure, but neither replaces a custom identity-relevance layer.
- EverMemOS is useful as an episodic layer but should not be treated as the whole memory foundation.

### Best notes and pages

- [Agent Memory Architecture](agent-memory-architecture.md)
  - Identity as compression.
  - Memory provider comparison.
  - Graph/temporal substrate recommendations.

### Public artifact

- [Memory Stack Explained](../explainers/memory-stack-explained.html)

## Lane 5 — Bug Bounty Economics

### Core question

What do bug bounty hunters actually need that current tools and platforms do not solve?

### Current answer

The biggest unsolved problem is not finding bugs. It is turning valid work into trusted, paid outcomes. Hunters complain about triage distrust, silent fixes, duplicate disputes, payout unpredictability, and report packaging friction. That suggests the opportunity is not another recon wrapper; it is a researcher-side operating system for evidence and expected value.

### Key findings

- Triage distrust is a recurring community pain: reports closed as duplicate, informative, or N/A without enough explanation.
- Silent-fix and retroactive-scope disputes create a need for stronger evidence trails.
- Income unpredictability pushes skilled people toward PTaaS/contracts instead of open bounty work.
- AI-generated low-quality submissions may worsen signal collapse and platform trust.
- The opportunity is around reproducibility, evidence packaging, payout-dispute prevention, and program ROI scoring.

### Best notes and pages

- [Bug Bounty Economics](bug-bounty-economics.md)
  - Bug bounty market research.
  - Community pain patterns.
  - Product whitespace.

### Public artifact

- [HackerOne ROI Calculator](../tools/hackerone-roi.html)

## Lane 6 — WearOS App Gap Analysis

### Core question

Where is WearOS still meaningfully behind Apple Watch, and which gaps are product opportunities?

### Current answer

WearOS is now good enough as a platform that the app gap matters more. The survey found that roughly half of the top Apple Watch experience does not translate cleanly to WearOS: some apps have no equivalent, and many equivalents are thin, abandoned, or phone-bridge-only.

### Key findings

- 50 Apple Watch apps were surveyed across health, fitness, productivity, navigation, communication, lifestyle, finance, sleep, audio, and games.
- Hard gaps: 14 of 50.
- Soft gaps: 13 of 50.
- The total addressable gap is about 54% of the surveyed top Apple Watch experience.
- Highest-opportunity categories:
  - sleep and recovery tracking;
  - personality/hyperlocal weather;
  - podcasts and audiobooks;
  - journaling and habits;
  - calendar power-tools;
  - health metrics dashboards;
  - niche fitness.

### Best notes and pages

- [WearOS App Gap Analysis](wearos-app-gap-analysis.md)

### Artifact opportunity

A focused app-porting/product portfolio for WearOS: premium sleep, premium calendar, personality weather, and audio/library tools.

## Lane 7 — AI Operations and Daily Production

### Core question

How do we make agent-generated work reliable enough to run every day without handholding?

### Current answer

The answer is not “better prompts.” It is operational structure: deterministic wrappers, manifests, small verification gates, live URL checks, and refusing to report success from intent. The daily podcast pipeline is the best current example because it has to fetch, score, write, render, publish, and verify on a schedule.

### Key findings

- Each stage needs a contract and an artifact.
- The wrapper should not infer “latest” by timestamp when a manifest can tell it exactly what happened.
- LLM work should be role-routed: scoring, research, writing, editorial, summary.
- Audio publication is not complete until the RSS enclosure and live GitHub Pages URL are reachable.
- The same verification rule applies to OPS fixes, index rotations, model-param drift, and static site publishing.

### Best notes and pages

- [AI Operations and Daily Production](ai-operations-daily-production.md)

### Public artifacts

- [Daily Podcast Workflow](../explainers/daily-podcast-workflow.html)
- [Daily Briefings RSS](../briefings/briefings.xml)

## Question index

The full generated list of research questions and short answers now lives at:

- [Questions and Answers](questions-and-answers.md) — public-safe deduped index of 58 Q-numbered research questions with short answers and source paths.

## What should be populated next

The wiki now has a real content base, but the highest-value next additions are full pages for:

1. **ESSA Evidence Tiers** — policy primer plus enforcement reality.
2. **Causal Attribution Gap in EdTech** — LearnPlatform/utilization vs. outcomes inference.
3. **Curator Displacement** — standalone cleaned synthesis from the signal-sorting lane.
4. **Identity as Compression** — standalone conceptual page.
5. **Memory Provider Comparison** — full public comparison of Graphiti, Cognee, Mem0, EverMemOS, Letta, LangMem, OpenMemory.
6. **Bug Bounty Trust OS** — product concept from the economics research.
7. **WearOS Product Portfolio** — concrete porting roadmap.
8. **Daily Podcast Architecture** — technical page from the pipeline implementation, not just workflow overview.

## Publish rule

A page belongs in the public wiki when it contains at least one of:

- a direct research answer,
- a source-backed synthesis,
- a reusable framework,
- a product/opportunity map,
- or a public artifact with enough context to be useful.

Pages that only say “we researched this” do not belong here.
