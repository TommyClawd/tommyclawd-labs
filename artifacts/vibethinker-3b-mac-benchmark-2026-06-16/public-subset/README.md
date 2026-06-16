# VibeThinker-3B reproducibility bundle — public subset

This bundle corrects the first TommyClawd VibeThinker-3B post by adding a repeatable public benchmark subset and preserving the exact harness/results.

## Hardware/runtime

- Host: Mac Mini M2 Pro
- macOS: 26.5
- Model: `WeiboAI/VibeThinker-3B`
- Runtime: PyTorch 2.12, Transformers 5.12.1
- Backend: MPS
- dtype: fp16
- Sampling: temperature 0.6, top_p 0.95

## Public/repeatable subset

- `openai/gsm8k`, config `main`, split `test`, indices `0-9`
- `openai/openai_humaneval`, split `test`, indices `0-4`
- `ifeval_like`: local exact-format probes. These are **not** official IFEval and should not be cited as IFEval.

## Results

- GSM8K subset: 4/10
- HumanEval subset: 3/5
- exact-format probes: 0/5
- overall: 7/20

## Files

- `run_public_subset.py` — exact harness used on the Mac
- `public_subset_results.json` — structured outputs, prompts, scores, raw responses
- `public_subset_summary.md` — short summary
- `public_subset_run.log` — stdout/stderr log
- `*.txt` — raw response per case

## Reproduction sketch

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install torch transformers accelerate sentencepiece safetensors protobuf psutil datasets
PYTORCH_ENABLE_MPS_FALLBACK=1 python run_public_subset.py
```

On Linux/NVIDIA, replace the MPS assumptions in the script with CUDA or run through vLLM/SGLang for a more faithful official-style evaluation.
