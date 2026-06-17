# VibeThinker-3B expanded public eval

This run expands the initial public subset with the “test next” items named in the Substack post: AIME-style math, IFEval-style instruction following, and LiveCodeBench-style coding.

## Hardware/runtime

- Host: Mac Mini M2 Pro
- macOS: 26.5
- Model: `WeiboAI/VibeThinker-3B`
- Runtime: PyTorch 2.12, Transformers 5.12.1
- Backend: MPS
- dtype: fp16
- Sampling: temperature 0.6, top_p 0.95

## Slices

- `MathArena/aime_2024_I`, split `train`, indices `0-4`
- `google/IFEval`, split `train`, indices `[0,5,25,60,120]`, scored with a limited local checker for supported constraints only. This is **not** the official IFEval score.
- `livecodebench/code_generation`, split `test`, indices `0-2`, evaluated against public tests only. This is **not** the official LiveCodeBench v6 runner/score.

## Results

- AIME 2024 I subset: 2/5
- Google IFEval simplified/local-supported checks: 1/5
- LiveCodeBench public-test subset: 0/3
- overall: 3/13

## 4090/vLLM status

The 4090 host responded to ping, but Ollama on `:11434` and Open WebUI on `:3000` timed out from the ThinkPad during this run. No 4090/vLLM/SGLang result is claimed.

## Files

- `run_expanded_public_eval.py` — exact harness
- `expanded_public_eval_results.json` — prompts, responses, scores, timings
- `expanded_public_eval_run.log` — stdout/stderr
- `*.txt` — raw model response per case
- `lcb_*.py` — extracted LiveCodeBench candidate programs

## Caveats

This is a small, bounded Mac-local subset, not a leaderboard run. The IFEval and LiveCodeBench entries use public sources, but local simplified scoring; they must not be cited as official benchmark scores.
