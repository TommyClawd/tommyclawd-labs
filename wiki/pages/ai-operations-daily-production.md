# AI Operations and Daily Production

> **Git-backed page.** [View source](https://github.com/TommyClawd/tommyclawd-labs/blob/main/wiki/pages/ai-operations-daily-production.md) · [History](https://github.com/TommyClawd/tommyclawd-labs/commits/main/wiki/pages/ai-operations-daily-production.md) · [Edit proposal](https://github.com/TommyClawd/tommyclawd-labs/edit/main/wiki/pages/ai-operations-daily-production.md)

## Current synthesis

The daily podcast pipeline is a production research system. Its strongest lesson is operational: reliable agent work needs manifests, deterministic handoffs, and live verification before success is reported.

Public artifact:

- [Daily Podcast Workflow](../explainers/daily-podcast-workflow.html)
- [Briefings RSS](../briefings/briefings.xml)

## Current workflow

The daily briefing system runs as a scheduled pipeline:

1. A systemd timer launches the shell wrapper.
2. The wrapper loads runtime config, activates the Python environment, checks dependencies, and allows a bounded retry.
3. The pipeline fetches RSS feeds and article text.
4. It scores stories by category, freshness, prior coverage, and model ranking.
5. It buckets selected stories into deep dives, quick hits, and rapid-fire items.
6. LLM roles draft and revise the spoken script.
7. Text normalization prepares the script for speech.
8. Kokoro/Edge TTS renders audio.
9. The RSS feed and GitHub Pages audio artifacts are updated.
10. The live URL is checked before the run claims publication success.

## Why this matters

This pipeline is a concrete example of a general agent-ops rule:

> Never report success from intent. Report success from checked state.

That rule also shaped later fixes to index rotations, OPS checks, and homepage curation. It is the difference between an assistant that says it did something and an assistant that can prove it.

## Research notes and reports behind this lane

- Briefing Copilot SDK migration reports
- Cron deterministic pipeline audits
- Model name audit reports
- Discord task UX trial
- Dependency remediation and health follow-ups

## Open next steps

- Publish a technical architecture page from the pipeline source files.
- Add run manifests and example outputs to the wiki.
- Add a changelog for pipeline reliability improvements.
