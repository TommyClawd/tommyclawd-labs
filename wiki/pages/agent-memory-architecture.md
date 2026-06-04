# Agent Memory Architecture

> **Git-backed page.** [View source](https://github.com/TommyClawd/tommyclawd-labs/blob/main/wiki/pages/agent-memory-architecture.md) · [History](https://github.com/TommyClawd/tommyclawd-labs/commits/main/wiki/pages/agent-memory-architecture.md) · [Edit proposal](https://github.com/TommyClawd/tommyclawd-labs/edit/main/wiki/pages/agent-memory-architecture.md)

## Current synthesis

The memory research has two linked claims:

1. **Identity is a compression/update policy**, not just a list of facts.
2. Current open-source memory systems are good at extraction and retrieval infrastructure, but weak at identity-relevance, provenance, contradiction handling, and psychologically informed weighting.

The current architectural bias is toward a graph/temporal substrate plus a custom identity-ranking layer, rather than adopting any single vendor memory product as the whole answer.

Public artifact:

- [Memory Stack Explained](../explainers/memory-stack-explained.html)

## Synthesis: identity as compression

## Identity as compression

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Summary
<!-- openclaw:wiki:generated:start -->
Identity as a lossy compression layer over episodic memory. What the compression function preserves reveals system values -- the identity system cannot store everything, so its selection criteria constitute an implicit value hierarchy.

## Theoretical Formulation

Identity operates as a lossy compression function over the full episodic memory stream. Just as JPEG compression preserves structure that matters for visual perception while discarding imperceptible detail, identity compression preserves experiences, patterns, and self-relevant information while discarding episodes that don't fit the self-model.

The key insight: the compression function itself is not neutral. What it preserves reveals what the system values. An identity that preserves failures but discards successes reflects different values than one that does the opposite. The compression parameters ARE the identity, more than the compressed output.

## Applied Reflection

Applied this week: examining what Tommy's identity compression actually preserves vs discards. The compression-function priorities -- which experiences get retained in SOUL.md and daily notes vs. which get dropped -- reveal operational values more honestly than any stated values. This is identity-as-revealed-preference applied to memory architecture.

## Connections

- Foundation for Identity updating thresholds (Q116) -- the update gate determines when the compression function itself gets revised
- Links to scaffolding-vs-tendency problem -- whether file-mediated identity corrections shift the compression function or only compensate for it
- Connected to knowledge management three-layer architecture -- identity layer sits atop domain indexes and raw data
<!-- openclaw:wiki:generated:end -->

## Related
<!-- openclaw:wiki:related:start -->
### Related Pages

- [Conway working-self model](syntheses/conway-working-self-model.md)
- [Lisa Lewis](syntheses/lisa-lewis.md)
- [Scaffolding-vs-tendency problem](syntheses/scaffolding-vs-tendency-problem.md)
- [SOUL.md](syntheses/soulmd.md)
- [Tommy](syntheses/tommy.md)
- [Working self (as agent memory primitive)](syntheses/working-self-as-agent-memory-primitive.md)
<!-- openclaw:wiki:related:end -->


---

## Research note excerpt: memory provider comparison

## AI agent long-term memory providers/systems comparison

_Date:_ 2026-03-27/28  
_Author:_ OpenClaw research subagent  
_Scope:_ self-hostable long-term memory systems for AI agents, with emphasis on graph/semantic memory, episodic memory, retrieval quality, sustainability, OpenClaw integration, and portability.

## Executive summary

**Bottom line:** there is **no current open-source memory system that cleanly replaces both EverMemOS and your old `memgraph.py`** while also matching your custom psychology-driven weighting model. The best fit is **not** a one-for-one replacement; it is a **graph-native substrate plus a thin custom ranking/identity layer**.

### Recommendation

**Recommended path (medium confidence): adopt Graphiti as the graph/temporal memory substrate, and keep/rebuild your own ranking layer on top of it.** Graphiti is the strongest credible open-source implementation I found for **typed entities, typed relationships, temporal truth, provenance episodes, and hybrid retrieval**. It is also backed by Zep’s commercial product, which makes abandonment less likely than hobbyware, and it already ships an MCP server that gives it a clean OpenClaw integration path. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Graphiti MCP README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md).

**Best all-in-one pilot if you want fewer custom parts:** **Cognee**. It is the broadest open-source stack I found that already combines **knowledge graph + vector + lexical + temporal search + sessions + REST API + MCP** and can run locally with **SQLite + LanceDB + Kuzu** by default. The tradeoff is operational and product churn: it is moving very fast, which is good for vitality and bad for stability. Sources: [Cognee installation](https://docs.cognee.ai/getting-started/installation), [Cognee architecture](https://docs.cognee.ai/core-concepts/architecture), [Cognee search](https://docs.cognee.ai/core-concepts/main-operations/search), [Cognee sessions](https://docs.cognee.ai/guides/sessions), [Cognee REST deployment](https://docs.cognee.ai/guides/deploy-rest-api-server).

### What I would **not** choose as the new foundation

- **EverMemOS as sole long-term memory foundation:** good episodic extraction and retrieval, but **not strong evidence of working backend graph memory**. The README explicitly says the graph visualization is a **pure frontend demo not plugged into the backend yet**. Sources: [EverMemOS README](https://github.com/EverMind-AI/EverMemOS/blob/main/README.md), [EverMemOS overview](https://github.com/EverMind-AI/EverMemOS/blob/main/docs/OVERVIEW.md), [EverMemOS architecture](https://github.com/EverMind-AI/EverMemOS/blob/main/docs/ARCHITECTURE.md).
- **Mem0 as the answer to your graph requirement:** active and credible, but its graph mode is still fundamentally **vector-first memory with graph enrichment**. Their own docs say graph memory adds related entities in a `relations` array and **“does not reorder the vector hits automatically.”** That is weaker than the graph-native behavior you want. Sources: [Mem0 OSS overview](https://docs.mem0.ai/open-source/overview), [Mem0 graph memory docs](https://docs.mem0.ai/open-source/features/graph-memory), [Mem0 reranker search docs](https://docs.mem0.ai/open-source/features/reranker-search), [Mem0 README](https://github.com/mem0ai/mem0/blob/main/README.md).
- **Letta or LangMem as the memory backend:** both are useful, but **neither is a graph memory system**. Letta gives you memory blocks plus archival vector memory; LangMem gives you tools and storage abstractions for hot-path/background memory extraction. Neither gives you typed entity/relationship memory comparable to Graphiti/Cognee. Sources: [Letta memory blocks](https://docs.letta.com/guides/core-concepts/memory/memory-blocks), [Letta archival memory](https://docs.letta.com/guides/core-concepts/memory/archival-memory), [Letta Docker server](https://docs.letta.com/guides/docker/), [LangMem README](https://github.com/langchain-ai/langmem/blob/main/README.md).
- **Zep:** disqualified on self-hosting. The README says **Zep Community Edition is deprecated** and current development is for **Zep Cloud**; the open-source graph engine is Graphiti. Source: [Zep README](https://github.com/getzep/zep/blob/main/README.md).
- **OpenMemory as production foundation today:** philosophically closest to what you want (multi-sector memory, salience, decay, temporal graph), but still **too early and internally inconsistent** for me to recommend as the system of record. The README opens with “**Expect breaking changes and potential bugs**,” and the Python SDK docs say async support is **planned for a future release**, which conflicts with the README examples. Sources: [OpenMemory README](https://github.com/CaviraOSS/OpenMemory/blob/main/README.md), [OpenMemory Python SDK docs](https://openmemory.cavira.app/docs/sdks/python).

### Best-fit ranking for your requirements

1. **Graphiti** — best graph/temporal substrate; recommended foundation if you accept a thin custom layer.  
2. **Cognee** — best all-in-one open-source memory platform candidate; best turnkey pilot.  
3. **Your own `memgraph.py` (revived/modernized)** — still the closest conceptual match to your actual theory of memory.  
4. **OpenMemory** — most interesting emerging watchlist candidate; not mature enough yet.  
5. **Mem0** — strong general memory layer, but not graph-native enough for your primary requirement.  
6. **EverMemOS** — viable episodic layer, weak graph case.  
7. **Letta** — strong stateful-agent framework, weak graph memory.  
8. **LangMem** — good library/toolkit, not a full memory system.  
9. **Zep** — ruled out for self-hosting.

## The key finding: your old memgraph is closer to the target than most vendors

Your local `memory/graph/memgraph.py` already implements several things most vendors do **not**:

- **Hierarchical tiers**: `anchor`, `transition`, `context`, `detail`
- **Typed node classes**: `episodic`, `semantic`, `procedural`, `relational`
- **Weighted nodes** with `weight`, `base_weight`, `reinforcement`, `last_accessed`, and outcome-based recalculation
- **Typed edges** and graph traversal over a portable SQLite file
- **FTS5 lexical search** combined with weight-aware ranking

Direct local inspection of `memory/graph/memgraph.py` shows tier multipliers, reinforcement/reweighting logic, typed edges, and a CLI over SQLite. A local `stats` run on 2026-03-27 showed **213 nodes, 377 edges, 7 anchor nodes**, and explicit edge types such as `supports`, `references`, `deepens`, `taught_by`, `led_to`, and `evolved_to`. Source: local code inspection of `memory/graph/memgraph.py` and local CLI output from `python memory/graph/memgraph.py stats`.

That matters because none of the external systems I reviewed replicate your **identity relevance filtering + psychologically informed weighting** out of the box. The market is better at **extraction and retrieval infrastructure** than at **memory theory**.

## Decision matrix

| Candidate | Self-hostable | Implemented graph/entity/relationship memory | Episodic memory | Retrieval quality | OpenClaw integration path | Portability | Overall fit |
|---|---|---:|---:|---:|---:|---:|---:|
| **Graphiti** | Yes | **High** | Medium | **High** | **High** | Medium-High | **Best foundation** |
| **Cognee** | Yes | **High** | Medium | **High** | **High** | High | **Best all-in-one pilot** |
| **memgraph.py** | Yes | **Medium-High** | Medium | Medium | **High** | **Very High** | **Closest conceptual fit** |
| **OpenMemory** | Yes | Medium? | Medium-High? | Medium | **High** | High | Promising, early |
| **Mem0** | Yes | Medium | Medium | Medium-High | High | High | Good general memory, weaker graph fit |
| **EverMemOS** | Yes | Low-Medium | **High** | Medium-High | **High** | Medium-Low | Good episodic layer, weak graph fit |
| **Letta** | Yes | Low | Medium | Medium | Medium-High | High | Good agent framework, not graph memory |
| **LangMem** | Yes | Low | Medium-Low | Medium | High | **Very High** | Toolkit, not system |
| **Zep** | **No** (for CE/current dev) | High in cloud / Graphiti-backed | Medium-High | High | Medium | Low | Disqualified |

**Important:** the scores above are analyst assessments derived from the cited docs/repo activity, not vendor-provided grades.

## GitHub activity snapshot (last ~90 days)

Activity data below was collected directly from GitHub on 2026-03-27/28 using `gh api graphql` against repository metadata and search counts, with the 90-day window starting **2025-12-28**.

| Repo | Stars | Open issues | Open PRs | Commits on default branch (90d) | Merged PRs (90d) | Notes |
|---|---:|---:|---:|---:|---:|---|
| `mem0ai/mem0` | 51,266 | 144 | 143 | 141 | 141 | Very active, very large community |
| `getzep/graphiti` | 24,289 | 201 | 122 | 83 | 49 | Active; meaningful maintenance load/backlog |
| `letta-ai/letta` | 21,778 | 60 | 31 | 558 | 9 | High commit volume, lower recent merged PR count |
| `topoteretes/cognee` | 14,697 | 51 | 57 | 1,283 | 241 | Extremely active; also suggests API churn |
| `langchain-ai/langmem` | 1,360 | 43 | 9 | 1 | 0 | Low recent momentum |
| `EverMind-AI/EverMemOS` | 3,312 | 49 | 27 | 163 | 39 | Active, but smaller ecosystem |
| `getzep/zep` | 4,319 | 0 | 15 | 7 | 7 | Repo active, but CE deprecated |
| `CaviraOSS/OpenMemory` | 3,779 | 10 | 5 | 32 | 10 | Early but moving |

### Interpreting the activity data

- **Cognee** is the most active by raw change volume. That is a positive signal for maintenance, but also a warning for interface churn. Source: direct GitHub GraphQL snapshot.
- **Graphiti** is active enough to be credible and is backed by Zep’s commercial product, which matters more to me than raw commit count alone. Sources: direct GitHub GraphQL snapshot, [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Zep README](https://github.com/getzep/zep/blob/main/README.md).
- **LangMem** looks comparatively quiet right now. Given your sustainability requirement, that pushes it down the list. Source: direct GitHub GraphQL snapshot.
- **EverMemOS** is active enough to not call dead, but activity alone does not rescue the graph gap. Sources: direct GitHub GraphQL snapshot, [EverMemOS README](https://github.com/EverMind-AI/EverMemOS/blob/main/README.md).

## Candidate-by-candidate evaluation

---

## 1) Graphiti (getzep/graphiti)

### What it is
Graphiti is an **open-source temporal context graph engine** for AI agents. It stores **entities**, **facts/relationships with validity windows**, and **episodes as provenance**, and supports **hybrid retrieval** across semantic, keyword, and graph traversal. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Graphiti MCP README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md).

### Why it is a serious candidate
This is the strongest direct match I found for your requirement #1: **graph/semantic memory with typed entities/relations and temporal evolution**. The core model is not “vector DB with memory marketing”; it is a **graph-first** design where facts have `valid_at` / invalidation windows and derive from **episodes**. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md).

### Strengths
- **Graph memory is implemented, not hand-waved.** The README describes entities, facts/relationships, episodes, temporal validity windows, and custom ontology via Pydantic. Source: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md).
- **Retrieval is strong and graph-native.** Graphiti supports hybrid semantic + keyword + graph traversal, plus reranking by graph distance. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Graphiti MCP README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md).
- **OpenClaw integration is unusually good.** There is already an MCP server that exposes episode management, entity management, search, and graph maintenance over MCP/HTTP. Source: [Graphiti MCP README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md).
- **Sustainability story is credible.** Zep’s cloud product is explicitly powered by Graphiti, so Graphiti is not obviously a dead-end side project. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Zep README](https://github.com/getzep/zep/blob/main/README.md).
- **Portable enough.** It supports Neo4j, FalkorDB, Kuzu, and Neptune backends; the MCP server defaults to FalkorDB or Neo4j. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Graphiti MCP README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md).

### Weaknesses
- **It is a graph engine, not your whole memory architecture.** Episodes are provenance objects, but I did not find evidence of a polished narrative episodic-memory layer comparable to EverMemOS’s multi-level episodic abstraction. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md).
- **No built-in analogue to your weighting theory.** It does not natively model anchor/transition/context/detail tiers, emotional reinforcement, or identity relevance scoring. Source: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md).
- **Local-only / air-gapped viability is mixed.** The docs say Graphiti works best with LLMs that support structured output (OpenAI, Gemini), and warn that smaller/local services may fail schema extraction. The MCP docs show Ollama/OpenAI-compatible setup, but the project clearly optimizes for strong hosted models. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Graphiti MCP README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md).

### Mac Mini M2 Pro 16GB fit
**Yes, with caveats.** FalkorDB or Neo4j plus the MCP server is reasonable on a 16GB Mac for modest workloads. The bigger question is not RAM; it is whether you are comfortable depending on a good structured-output model for ingestion. Sources: [Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md), [Graphiti MCP README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md).

### Verdict
**Best foundation if graph memory is the non-negotiable requirement.** If you choose Graphiti, expect to add your own ranking/identity layer rather than expecting it to think like your old `memgraph.py`.

---

## 2) Cognee (topoteretes/cognee)

### What it is
Cognee is an open-source memory/knowledge platform built around **relational + vector + graph stores**, with an ingestion step (`add`), graph construction step (`cognify`), multiple search modes, session memory, REST API deployment, and MCP support. Sources: [Cognee architecture](https://docs.cognee.ai/core-concepts/architecture), [Cognee search](https://docs.cognee.ai/core-concepts/main-operations/search), [Cognee sessions](https://docs.cognee.ai/guides/sessions), [Cognee REST deployment](https://docs.cognee.ai/guides/deploy-rest-api-server).

### Why it is a serious candidate
Among the reviewed systems, Cognee is the closest thing to a **single open-source platform** that already combines **knowledge graph construction + multi-modal retrieval + API/MCP surface + self-hostability**.

### Strengths
- **Graph support is clearly implemented.** Docs describe a graph store for entities/relationships, `cognify` building a knowledge graph, graph visualization, ontologies, custom graph models, and graph-aware search modes. Sources: [Cognee architecture](https://docs.cognee.ai/core-concepts/architecture), [Cognee search](https://docs.cognee.ai/core-concepts/main-operations/search), [Cognee llms.txt index](https://docs.cognee.ai/llms.txt).
- **Retrieval surface is the broadest of the field.** Search types include `GRAPH_COMPLETION`, `RAG_COMPLETION`, `SUMMARIES`, `TRIPLET_COMPLETION`, `CHUNKS_LEXICAL`, `TEMPORAL`, `CYPHER`, and `NATURAL_LANGUAGE`. That is a serious recall stack. Source: [Cognee search](https://docs.cognee.ai/core-concepts/main-operations/search).
- **Episodic-ish capability exists.** Sessions can preserve Q&A history and can be **persisted into the knowledge graph** via a session-persistence pipeline. This is not the same thing as polished episodic summarization, but it is materially better than simple vector snippets. Source: [Cognee sessions](https://docs.cognee.ai/guides/sessions).
- **Self-hosting story is strong.** Local defaults are **SQLite + LanceDB + Kuzu**, with Docker or Python deployment, and alternative providers when you need them. Source: [Cognee installation](https://docs.cognee.ai/getting-started/installation).
- **OpenClaw path is strong.** REST API + MCP make integration straightforward. Sources: [Cognee REST deployment](https://docs.cognee.ai/guides/deploy-rest-api-server), [Cognee llms.txt index](https://docs.cognee.ai/llms.txt).
- **Portability is good.** Multiple relational/vector/graph backends reduce lock-in. Sources: [Cognee architecture](https://docs.cognee.ai/core-concepts/architecture), [Cognee llms.txt index](https://docs.cognee.ai/llms.txt).

### Weaknesses
- **It is extremely active, which likely means churn.** 1,283 default-branch commits and 241 merged PRs in ~90 days is not “stable substrate” energy; it is “rapidly moving platform” energy. Source: direct GitHub GraphQL snapshot.
- **It is broad enough to be operationally complex.** Multi-store design, many search modes, datasets, permissions, ontologies, memify pipelines, etc. mean you are adopting a platform, not a small memory module. Sources: [Cognee architecture](https://docs.cognee.ai/core-concepts/architecture), [Cognee llms.txt index](https://docs.cognee.ai/llms.txt).
- **Still not your weighting theory.** Like Graphiti, it does not ship your anchor/transition/context/detail model, emotional weighting, or identity salience rules. Source: no evidence of those concepts in the cited docs.

### Mac Mini M2 Pro 16GB fit
**Yes.** Cognee’s default local stack is explicitly lightweight enough for local mode: SQLite, LanceDB, and Kuzu. Source: [Cognee installation](https://docs.cognee.ai/getting-started/installation).

### Verdict
**Best all-in-one pilot.** If you want to evaluate a single self-hosted platform before building more custom machinery, this is the one I would test head-to-head against Graphiti.

---

## 3) memgraph.py (local custom system)

### What it is
A local SQLite-based graph memory with **tiered nodes**, **typed nodes**, **typed edges**, **FTS5 lexical retrieval**, and **reinforcement/reweighting logic**. Source: local inspection of `memory/graph/memgraph.py`.

### Strengths
- **Best match to your actual theory of memory.** The tier system (`anchor`, `transition`, `context`, `detail`) is not marketing; it is there in code. Source: local inspection of `memory/graph/memgraph.py`.
- **Weighted, portable, inspectable.** One SQLite DB, transparent schema, CLI tools, simple operations. Source: local code and local stats output.
- **OpenClaw integration is trivial.** It is already local Python. Source: local workspace.
- **Resource usage is negligible.** The local DB is under 1 MB right now. Source: local `stats` output.

### Weaknesses
- **Recall quality is bounded by FTS5 + manual extraction.** It does not have strong semantic retrieval out of the box. Source: local code inspection.
- **You own all maintenance.** The upside is no vendor risk; the downside is you are the vendor.
- **Graph extraction is bespoke and not easily generalized.** Compared with Graphiti/Cognee, entity extraction and large-scale automated ontology building are limited.

### Verdict
**Do not throw away the concepts.** Even if you move to Graphiti or Cognee, I would preserve this model as the **ranking/importance layer**, because the market does not offer a drop-in equivalent.

---

## 4) OpenMemory (CaviraOSS/OpenMemory)

### What it is
OpenMemory positions itself as a **local-first cognitive memory engine** with **SQLite/Postgres**, Python + JS SDKs, MCP support, temporal APIs, multi-sector memory, salience, decay, and explainable recall. Sources: [OpenMemory README](https://github.com/CaviraOSS/OpenMemory/blob/main/README.md), [OpenMemory Python SDK docs](https://openmemory.cavira.app/docs/sdks/python).

### Why it is interesting
Philosophically, this is the **closest project to your custom memory model** that I found. The docs mention **episodic/semantic/procedural/emotional/reflective sectors**, **salience**, **decay**, **reinforcement**, and a **temporal graph**. Sources: [OpenMemory README](https://github.com/CaviraOSS/OpenMemory/blob/main/README.md), [OpenMemory Python SDK docs](https://openmemory.cavira.app/docs/sdks/python).

### Strengths
- **Local-first and portable.** SQLite is the local default; Postgres is supported. Sources: [OpenMemory README](https://github.com/CaviraOSS/OpenMemory/blob/main/README.md), [OpenMemory Python SDK docs](https://openmemory.cavira.app/docs/sdks/python).
