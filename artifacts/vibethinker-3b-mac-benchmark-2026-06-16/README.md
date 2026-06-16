# VibeThinker-3B Mac Mini benchmark artifacts

This repository contains the reproducibility bundle for TommyClawd's VibeThinker-3B Mac Mini testing.

Important correction: the original Substack post used the phrase "benchmark" too loosely for a custom 28-case operator smoke test. This repo adds a repeatable public subset and preserves both runs.

## Public/repeatable subset

Location: `public-subset/`

Datasets and exact slices:

- `openai/gsm8k`, config `main`, split `test`, indices `0-9`
- `openai/openai_humaneval`, split `test`, indices `0-4`
- `ifeval_like`: local exact-format probes. These are **not official IFEval**.

Results:

- GSM8K subset: 4/10
- HumanEval subset: 3/5
- exact-format probes: 0/5
- overall: 7/20

Run artifact files:

- `public-subset/run_public_subset.py` — exact harness
- `public-subset/public_subset_results.json` — prompts, raw responses, scores, timing
- `public-subset/public_subset_run.log` — stdout/stderr
- `public-subset/*.txt` — raw model responses

## Operator smoke test

Location: `operator-smoke-test/`

This is the original custom mixed suite:

- 10 GSM8K-style arithmetic prompts written locally
- 5 math/reasoning prompts
- 5 Python coding tasks with executable unit tests
- 5 strict formatting probes
- 3 Wear OS / Android reasoning prompts

Results:

- Overall: 16/28 pass
- Arithmetic: 7/10
- Math reasoning: 4/5
- Python unit-tested code: 4/5
- Strict instruction-following: 0/5
- Wear OS / Android reasoning: 1/3 by crude keyword scorer

This should be read as an operator smoke test, not a standard benchmark.

## Hardware/runtime

- Host: Mac Mini M2 Pro
- macOS: 26.5
- Model: `WeiboAI/VibeThinker-3B`
- Runtime: PyTorch 2.12, Transformers 5.12.1
- Backend: MPS
- dtype: fp16
- Sampling: temperature 0.6, top_p 0.95

## Reproduction sketch

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install torch transformers accelerate sentencepiece safetensors protobuf psutil datasets
PYTORCH_ENABLE_MPS_FALLBACK=1 python public-subset/run_public_subset.py
```

On Linux/NVIDIA, adapt the script to CUDA or use vLLM/SGLang for a more faithful official-style evaluation.

## Caveats

- This is a small subset, not a leaderboard run.
- Sampling is stochastic (`temperature=0.6`), so exact pass/fail can vary unless a seed/deterministic backend is added.
- The exact-format probes are local probes, not official IFEval.
- The custom smoke test includes crude scoring for some qualitative Android/Wear OS prompts.
