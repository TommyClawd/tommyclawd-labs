# VibeThinker-3B public benchmark subset

{
  "model": "WeiboAI/VibeThinker-3B",
  "device": "mps",
  "dtype": "torch.float16",
  "temp": 0.6,
  "top_p": 0.95,
  "datasets": {
    "gsm8k": "openai/gsm8k main/test indices 0-9",
    "openai_humaneval": "openai/openai_humaneval test indices 0-4",
    "ifeval_like": "local exact-format probes, not official IFEval"
  }
}

## Summary
- gsm8k: 4/10 (40.0%), 10.82 tok/s aggregate
- humaneval: 3/5 (60.0%), 9.81 tok/s aggregate
- ifeval_like: 0/5 (0.0%), 13.56 tok/s aggregate
- overall: 7/20 (35.0%)
