# VibeThinker-3B Kitchen Sink Benchmark — Mac Mini

Model: `WeiboAI/VibeThinker-3B`
Device: Mac Mini M2 Pro MPS fp16
Settings: temp 0.6, top_p 0.95, max_new_tokens 128-768 (bounded local run)

Overall: 16/28 pass (57.1%); generated 11478 tokens in 1042.7s; avg case tok/s 12.25.

## By benchmark
- gsm8k_manual: 7/10 (70.0%), 3138 tokens, 258.6s, avg 12.92 tok/s
- math_reasoning: 4/5 (80.0%), 2175 tokens, 178.8s, avg 12.68 tok/s
- code_tests: 4/5 (80.0%), 3328 tokens, 343.8s, avg 9.80 tok/s
- instruction_following: 0/5 (0.0%), 789 tokens, 60.8s, avg 14.10 tok/s
- untidy_reasoning: 1/3 (33.3%), 2048 tokens, 200.7s, avg 10.31 tok/s

## Cases
- ✅ gsm8k_manual/gsm8k_01: 384 tok, 27.9s, 13.76 tok/s
- ✅ gsm8k_manual/gsm8k_02: 312 tok, 28.8s, 10.85 tok/s
- ❌ gsm8k_manual/gsm8k_03: 384 tok, 36.1s, 10.65 tok/s
- ❌ gsm8k_manual/gsm8k_04: 384 tok, 35.9s, 10.69 tok/s
- ✅ gsm8k_manual/gsm8k_05: 141 tok, 11.9s, 11.83 tok/s
- ✅ gsm8k_manual/gsm8k_06: 223 tok, 12.9s, 17.33 tok/s
- ✅ gsm8k_manual/gsm8k_07: 251 tok, 14.4s, 17.38 tok/s
- ✅ gsm8k_manual/gsm8k_08: 291 tok, 18.9s, 15.36 tok/s
- ✅ gsm8k_manual/gsm8k_09: 384 tok, 35.9s, 10.70 tok/s
- ❌ gsm8k_manual/gsm8k_10: 384 tok, 35.9s, 10.69 tok/s
- ✅ math_reasoning/contradiction_marbles: 512 tok, 38.8s, 13.21 tok/s
- ❌ math_reasoning/modular: 512 tok, 50.3s, 10.17 tok/s
- ✅ math_reasoning/probability: 383 tok, 22.6s, 16.97 tok/s
- ✅ math_reasoning/quadratic: 384 tok, 30.7s, 12.52 tok/s
- ✅ math_reasoning/geometry: 384 tok, 36.4s, 10.55 tok/s
- ✅ code_tests/first_unique: 512 tok, 50.1s, 10.22 tok/s
- ✅ code_tests/is_palindrome: 512 tok, 48.3s, 10.60 tok/s
- ❌ code_tests/merge_intervals: 768 tok, 85.1s, 9.03 tok/s
- ✅ code_tests/top_k_frequent: 768 tok, 78.4s, 9.79 tok/s
- ✅ code_tests/roman_to_int: 768 tok, 81.9s, 9.38 tok/s
- ❌ instruction_following/json_only: 169 tok, 14.6s, 11.54 tok/s
- ❌ instruction_following/no_think: 108 tok, 9.0s, 12.02 tok/s
- ❌ instruction_following/bullet_count: 256 tok, 22.8s, 11.22 tok/s
- ❌ instruction_following/quote_wrapper: 128 tok, 7.3s, 17.61 tok/s
- ❌ instruction_following/csv: 128 tok, 7.1s, 18.11 tok/s
- ✅ untidy_reasoning/queue_race: 768 tok, 67.3s, 11.42 tok/s
- ❌ untidy_reasoning/compose_deprecation: 512 tok, 49.2s, 10.40 tok/s
- ❌ untidy_reasoning/service_state: 768 tok, 84.2s, 9.12 tok/s
