# VibeThinker-3B operator smoke test

This is the original custom 28-case operator smoke test used in the Substack post. It is intentionally **not** a leaderboard benchmark. It is a practical local smoke test for reasoning/code/format-control behavior on a Mac Mini.

## Hardware/runtime

- Host: Mac Mini M2 Pro
- macOS: 26.5
- Model: `WeiboAI/VibeThinker-3B`
- Runtime: PyTorch 2.12, Transformers 5.12.1
- Backend: MPS
- dtype: fp16
- Sampling: temperature 0.6, top_p 0.95
- max_new_tokens: 128–768 depending on case

## Cases

- 10 locally written GSM8K-style arithmetic prompts
- 5 math/reasoning prompts
- 5 Python coding tasks scored by executable unit tests
- 5 strict instruction-following probes
- 3 Wear OS / Android reasoning prompts

## Results

- Overall: 16/28 pass
- Arithmetic: 7/10
- Math reasoning: 4/5
- Python unit-tested code: 4/5
- Strict instruction-following: 0/5
- Wear OS / Android reasoning: 1/3 by crude keyword scorer

## Files

- `run_kitchen_sink.py` — exact harness used
- `kitchen_sink_run.log` — full stdout/stderr from the run; the final aggregate JSON write failed because one expected-answer field was a Python set, but all cases completed and all raw outputs were written
- `kitchen_sink_summary.md` / `kitchen_sink_summary.json` — reconstructed summary from log + raw outputs
- `*.txt` — raw model response per case

## Reproduction sketch

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install torch transformers accelerate sentencepiece safetensors protobuf psutil datasets evaluate word2number
PYTORCH_ENABLE_MPS_FALLBACK=1 python run_kitchen_sink.py
```

Because sampling uses temperature 0.6 and no fixed seed, exact pass/fail may vary. Treat this as a repeatable smoke-test harness, not a deterministic benchmark.
