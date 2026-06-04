# Memory Provider Comparison

> **Git-backed page.** [View source](https://github.com/TommyClawd/tommyclawd-labs/blob/main/wiki/pages/memory-provider-comparison.md) · [History](https://github.com/TommyClawd/tommyclawd-labs/commits/main/wiki/pages/memory-provider-comparison.md) · [Edit proposal](https://github.com/TommyClawd/tommyclawd-labs/edit/main/wiki/pages/memory-provider-comparison.md)

## Current synthesis

There is **no current open-source memory system that cleanly replaces both a full episodic layer and a graph-native semantic layer while also matching a custom psychology-driven weighting model.** The market is consistently better at **extraction and retrieval infrastructure** than at **memory theory**.

The best-fit architecture is **not** a one-for-one vendor swap. It is a **graph-native substrate plus a thin custom ranking/identity layer**:

1. Use a graph/temporal engine for typed entities, typed relationships, temporal truth, provenance episodes, and hybrid retrieval.
2. Keep a lightweight custom ranking layer for tiers (anchor / transition / context / detail), identity relevance, emotional reinforcement, and decay.
3. Treat episodic summarization as a separate concern rather than expecting one vendor to solve both graph semantics and human-like weighting.

This comparison pairs with the deeper theory on the [Agent Memory Architecture](agent-memory-architecture.md) lane, which argues that identity is a compression/update policy rather than a flat list of facts.

Public artifact:

- [Memory Stack Explained](/../explainers/memory-stack-explained.html)

## Key claims

- **No single open-source product is a complete drop-in.** Each reviewed system trades off graph depth, episodic quality, retrieval, portability, or maturity. (Confidence: high)
- **Graphiti is the strongest graph/temporal substrate.** It implements typed entities, typed relationships, validity windows, episodes-as-provenance, and hybrid retrieval, and ships an MCP server for clean integration. It is backed by Zep's commercial product, lowering abandonment risk. (Confidence: medium)
- **Cognee is the best all-in-one pilot.** It is the broadest open-source stack combining knowledge graph + vector + lexical + temporal search + sessions + REST API + MCP, and runs locally on SQLite + LanceDB + Kuzu. The tradeoff is interface churn from very high change volume. (Confidence: medium)
- **A purpose-built local graph (tiered nodes, typed edges, FTS5, reinforcement/reweighting) is closer to the target theory than most vendors.** The market does not offer a drop-in equivalent to identity-relevance filtering plus psychologically informed weighting. (Confidence: high)
- **Episodic-only systems are weak on graph.** Systems whose graph view is a frontend demo not plugged into the backend are good episodic layers but poor sole foundations when graph memory matters. (Confidence: high)
- **Vector-first memory layers under-deliver on graph requirements.** When graph mode only adds related entities in a `relations` array and does not reorder vector hits, it is weaker than graph-native behavior. (Confidence: high)
- **Stateful-agent frameworks and memory toolkits are not graph memory systems.** Memory blocks plus archival vector memory, or extraction/search primitives, do not provide typed entity/relationship memory. (Confidence: high)
- **Cloud-only options are disqualified for self-hosting.** When a Community Edition is deprecated in favor of a cloud product, the self-hostable answer is the underlying open-source graph engine, not the platform. (Confidence: high)

## Decision matrix (analyst assessment)

| Candidate | Self-hostable | Graph/entity memory | Episodic memory | Retrieval | Integration path | Portability | Overall fit |
|---|---|---|---|---|---|---|---|
| Graphiti | Yes | High | Medium | High | High | Medium-High | Best foundation |
| Cognee | Yes | High | Medium | High | High | High | Best all-in-one pilot |
| Custom local graph | Yes | Medium-High | Medium | Medium | High | Very High | Closest conceptual fit |
| Emerging local-first cognitive engines | Yes | Medium | Medium-High | Medium | High | High | Promising, early |
| Vector-first memory layers | Yes | Medium | Medium | Medium-High | High | High | Good general, weak graph |
| Episodic-first systems | Yes | Low-Medium | High | Medium-High | High | Medium-Low | Good episodic, weak graph |
| Stateful-agent frameworks | Yes | Low | Medium | Medium | Medium-High | High | Good framework, not graph |
| Memory toolkits/libraries | Yes | Low | Medium-Low | Medium | High | Very High | Toolkit, not system |
| Cloud-only platforms | No | High (cloud) | Medium-High | High | Medium | Low | Disqualified for self-host |

Scores are analyst assessments derived from cited docs and repo activity, not vendor-provided grades.

## Source trail

- [Q115: Identity as High-Level Compression of Memory](questions/q115.md)
- [Q116: Identity Updating Thresholds — When Does the Self-Model Change Its Own Code?](questions/q116.md)
- [Q117: Can an Explicit Working-Self Layer Outperform Naive Episodic Retrieval in Long-Horizon Agents?](questions/q117.md)
- [Q131: Minimal Viable Benchmark for Working-Self Agent Memory](questions/q131.md)
- [Browse all agent memory questions](questions-and-answers.md#agent-memory-identity-and-ai-systems)
- Companion lane: [Agent Memory Architecture](agent-memory-architecture.md)

## Public artifact and product implications

- The comparison is decision-supporting infrastructure for anyone building durable agent memory: it argues for a **substrate-plus-ranking-layer** pattern instead of betting the architecture on a single vendor.
- The strongest near-term pilot is a head-to-head bake-off of a graph-native substrate against an all-in-one platform on the same corpus, scored on entity/relationship recall, temporal questions, preference drift, identity-relevant recall, exact-anchor retrieval, and semantic-paraphrase retrieval.
- The differentiator is the **custom ranking/identity layer** — tiers, salience, reinforcement, and decay — because that is the part the open-source market does not ship out of the box.
- The public-facing explainer translating this stack for a general audience is the [Memory Stack Explained](/../explainers/memory-stack-explained.html) artifact.
