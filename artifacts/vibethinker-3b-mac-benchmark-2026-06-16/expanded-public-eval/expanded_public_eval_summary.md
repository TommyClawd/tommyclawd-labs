# VibeThinker-3B expanded public eval

{
  "model": "WeiboAI/VibeThinker-3B",
  "device": "mps",
  "dtype": "torch.float16",
  "temp": 0.6,
  "top_p": 0.95,
  "slices": {
    "aime": "MathArena/aime_2024_I train indices 0-4",
    "ifeval": "google/IFEval train indices [0,5,25,60,120] with simplified local scorer, not official score",
    "livecodebench": "livecodebench/code_generation default test indices 0-2 public tests only; not release_v6 official runner"
  }
}

## Summary
- aime_2024_I: 2/5 (40.0%), 10.15 tok/s aggregate
- ifeval_simplified: 1/5 (20.0%), 10.39 tok/s aggregate
- livecodebench_public_tests: 0/3 (0.0%), 7.19 tok/s aggregate
- overall: 3/13 (23.1%)
