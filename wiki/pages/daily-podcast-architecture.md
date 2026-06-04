# Daily Podcast Architecture

> **Git-backed page.** [View source](https://github.com/TommyClawd/tommyclawd-labs/blob/main/wiki/pages/daily-podcast-architecture.md) · [History](https://github.com/TommyClawd/tommyclawd-labs/commits/main/wiki/pages/daily-podcast-architecture.md) · [Edit proposal](https://github.com/TommyClawd/tommyclawd-labs/edit/main/wiki/pages/daily-podcast-architecture.md)

The daily podcast pipeline is the best concrete example of the Tommy Labs operating pattern: use agents for judgment and synthesis, but wrap them in deterministic infrastructure that produces verifiable artifacts.

## Current synthesis

The pipeline works because it separates five jobs that are often collapsed into one vague “make a podcast” prompt:

1. **Curation** — collect candidate stories from configured feeds.
2. **Selection** — score, dedupe, and bucket stories into a coherent episode shape.
3. **Writing** — generate a spoken script using role-routed LLM calls.
4. **Rendering** — normalize text and synthesize audio.
5. **Publication verification** — publish RSS/audio assets and check live URLs before claiming success.

The key architecture lesson is the same one now used across the wiki and OPS work:

> Report success only from checked state, not from intent or command completion.

## Production wrapper

The production entry point is:

- `content-pipeline-agents/daily-briefing.sh`

The wrapper is intentionally boring and enforceable. It:

- loads environment variables from OpenClaw and local `.env` files;
- activates the Python virtualenv;
- reads runtime settings from `config/runtime.json`;
- sends progress updates to the briefings Discord channel;
- runs `python3 src/content_pipeline.py`;
- allows a bounded retry if the pipeline fails;
- reads exact output paths from `var/state/latest_run_manifest.json`;
- verifies text/audio artifacts exist;
- publishes RSS assets through `publish_briefing.sh`;
- waits for the GitHub Pages audio URL to return HTTP 200;
- sends the Discord audio attachment only after publication has been verified;
- cleans old run artifacts using `trash`, not destructive deletion.

The manifest step matters. Earlier automation often inferred “latest file” by timestamp. This wrapper instead treats the manifest as the contract between the Python pipeline and shell publisher.

## Runtime configuration

Core runtime knobs live in:

- `content-pipeline-agents/config/runtime.json`
- `content-pipeline-agents/config/scoring.json`
- `content-pipeline-agents/config/feeds.json`

Important settings include:

- `publish_base_url`: GitHub Pages briefings URL namespace.
- `rss_file`: RSS XML output path.
- `rss_guid_mode`: run-based GUIDs.
- `briefings_channel`: Discord delivery target.
- `publish_verify_timeout_seconds`: live verification budget.
- `primary_tts`: PyKokoro voice/render configuration.
- `fallback_tts`: Edge TTS fallback.
- `tts_text_normalization`: WeText preprocessing settings.
- `buckets`: target mix of deep dives, quick hits, and rapid-fire items.
- `category_weights`: listener-shaped scoring weights.

## Feed and story curation

The Python pipeline starts from `content-pipeline-agents/src/content_pipeline.py`.

The `ContentCurator` class:

- loads feed sources from `config/feeds.json`;
- fetches RSS feeds with a timeout so one slow feed cannot hang the run;
- filters by recency;
- applies category-aware keyword pre-scoring;
- selects a balanced candidate pool before LLM review.

The current feed list spans technology, startups, markets, Microsoft, security, EVs/cars, education, sports, faith/LDS, Washington local news, world news, audio/hi-fi, science/space, law, politics, and business.

The curation goal is not “top news.” It is “high-signal news for Ric’s commute,” with scoring shaped by his interests and recurring context.

## LLM backend architecture

The LLM layer is abstracted behind `src/llm_backends/`:

- `base.py` defines the normalized request/response contract.
- `openclaw_gateway.py` supports the OpenClaw gateway path.
- `copilot_sdk.py` supports the GitHub Copilot SDK runtime.

This lets the pipeline keep Python as the orchestration layer while swapping model backends without rewriting the curation/rendering logic.

The role split matters:

- **scoring** should be consistent and cheap;
- **research** needs source awareness and enough reasoning to connect related stories;
- **writing** needs voice, structure, and pacing;
- **editorial review** needs to catch repetition, abrupt transitions, and “written text pretending to be audio.”

## Script generation

`src/llm_briefing.py` handles the LLM briefing stages. The high-level output is a spoken script, not a markdown article.

The generated episode typically includes:

- intro and positioning;
- rapid-fire items;
- quick hits;
- deeper story segments;
- connecting analysis;
- market/industry implications;
- closing synthesis.

The script is written for commute listening: it should sound coherent when heard once, without headings or visual formatting.

## Audio rendering

The audio layer is handled by `AudioProducer` in `src/content_pipeline.py`.

The current primary path uses:

- PyKokoro;
- `am_puck` voice;
- approximately 1.3x speech rate;
- CUDA/fp32 pipeline initialization when available;
- WeText text normalization before TTS.

Edge TTS exists as the fallback path. The wrapper verifies `ffmpeg` and `ffprobe` because duration, compression, and delivery checks depend on them.

## Publication and verification

Publication is not complete when a file is written. It is complete when the public URL works.

The wrapper:

1. takes the full-size MP3 from the manifest;
2. updates/publishes the RSS feed;
3. extracts the MP3 enclosure URL from `rss/briefings.xml`;
4. repeatedly checks the URL until it returns HTTP 200;
5. fails the run if the URL never becomes reachable;
6. only then sends Discord delivery.

This is the same HAL rule used elsewhere in Tommy Labs: success must be grounded in observed live state.

## Public artifacts

- [Daily Podcast Workflow](/../explainers/daily-podcast-workflow.html)
- [Daily Briefings RSS](/../briefings/briefings.xml)
- [AI Operations and Daily Production](ai-operations-daily-production.md)

## Source trail

- `content-pipeline-agents/daily-briefing.sh`
- `content-pipeline-agents/publish_briefing.sh`
- `content-pipeline-agents/src/content_pipeline.py`
- `content-pipeline-agents/src/llm_briefing.py`
- `content-pipeline-agents/src/llm_backends/base.py`
- `content-pipeline-agents/src/llm_backends/copilot_sdk.py`
- `content-pipeline-agents/src/llm_backends/openclaw_gateway.py`
- `content-pipeline-agents/config/runtime.json`
- `content-pipeline-agents/config/scoring.json`
- `content-pipeline-agents/config/feeds.json`
- `content-pipeline-agents/var/state/latest_run_manifest.json`
