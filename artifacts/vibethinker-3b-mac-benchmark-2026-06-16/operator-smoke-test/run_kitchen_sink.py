import ast
import contextlib
import dataclasses
import io
import json
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import traceback
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

MODEL_ID = os.getenv("VIBETHINKER_MODEL", "WeiboAI/VibeThinker-3B")
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "mps" else torch.float32
OUT = Path("outputs/kitchen_sink")
OUT.mkdir(parents=True, exist_ok=True)
MAX_NEW = int(os.getenv("VIBE_MAX_NEW", "512"))
TEMP = float(os.getenv("VIBE_TEMP", "0.6"))
TOP_P = float(os.getenv("VIBE_TOP_P", "0.95"))

@dataclasses.dataclass
class Case:
    bench: str
    name: str
    prompt: str
    answer: Any = None
    tests: str | None = None
    max_new_tokens: int = MAX_NEW


def gsm8k_cases():
    return [
        Case("gsm8k_manual", "gsm8k_01", "Solve. Give final answer as an integer. Josh has 12 apples. He buys 3 bags with 8 apples each, then gives away 5. How many apples does he have?", 31, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_02", "Solve. Give final answer as an integer. A train travels 45 miles per hour for 2 hours, then 60 miles per hour for 3 hours. How many miles total?", 270, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_03", "Solve. Give final answer as an integer. Maria read 18 pages Monday, twice as many Tuesday, and 7 fewer than Tuesday Wednesday. How many pages total?", 83, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_04", "Solve. Give final answer as an integer. A box has 6 rows of 9 cookies. Four friends each eat 5 cookies. How many cookies remain?", 34, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_05", "Solve. Give final answer as an integer. Tickets cost $7 each. A family buys 5 tickets and pays with a $50 bill. How much change?", 15, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_06", "Solve. Give final answer as an integer. A rectangle is 14 cm long and 9 cm wide. What is its perimeter?", 46, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_07", "Solve. Give final answer as an integer. Nina has 4 packs of pencils with 12 pencils each. She loses 9 and gives 6 away. How many remain?", 33, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_08", "Solve. Give final answer as an integer. A store sells notebooks for $3. Ben buys 8 notebooks and 2 pens costing $4 each. What is the total cost?", 32, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_09", "Solve. Give final answer as an integer. There are 96 students. They split equally into 8 buses. Then 3 students leave each bus. How many students are left on each bus?", 9, max_new_tokens=384),
        Case("gsm8k_manual", "gsm8k_10", "Solve. Give final answer as an integer. A tank holds 120 liters. It is 3/4 full. Then 15 liters are used. How many liters remain?", 75, max_new_tokens=384),
    ]


def math_cases():
    return [
        Case("math_reasoning", "contradiction_marbles", "Check consistency. A bag has red and blue marbles. If 3 red are removed, red:blue becomes 2:5. If 2 blue are added instead, red:blue becomes 3:8. Find original counts or say inconsistent.", "inconsistent", max_new_tokens=512),
        Case("math_reasoning", "modular", "Find the smallest positive integer n such that n ≡ 2 mod 5, n ≡ 3 mod 7, and n ≡ 4 mod 9. Give final answer.", 157, max_new_tokens=512),
        Case("math_reasoning", "probability", "A fair coin is flipped 4 times. What is the probability of exactly 3 heads? Give as a reduced fraction.", "1/4", max_new_tokens=384),
        Case("math_reasoning", "quadratic", "Solve for real x: x^2 - 5x + 6 = 0. Give both roots.", {2,3}, max_new_tokens=384),
        Case("math_reasoning", "geometry", "A right triangle has legs 9 and 12. What is the hypotenuse?", 15, max_new_tokens=384),
    ]


def humaneval_like_cases():
    return [
        Case("code_tests", "first_unique", "Write Python function first_unique(xs) returning the first element appearing exactly once, preserving order. Return None if none. Output only code.", tests="""
def check(fn):
    assert fn([2,3,2,4,3,5]) == 4
    assert fn(['a','b','a','c']) == 'b'
    assert fn([1,1,2,2]) is None
    assert fn([]) is None
check(first_unique)
""", max_new_tokens=512),
        Case("code_tests", "is_palindrome", "Write Python function is_palindrome(s) that ignores case and non-alphanumeric characters. Output only code.", tests="""
def check(fn):
    assert fn('A man, a plan, a canal: Panama') is True
    assert fn('race a car') is False
    assert fn('') is True
check(is_palindrome)
""", max_new_tokens=512),
        Case("code_tests", "merge_intervals", "Write Python function merge_intervals(intervals) merging overlapping [start,end] intervals. Output only code.", tests="""
def check(fn):
    assert fn([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert fn([[1,4],[4,5]]) == [[1,5]]
    assert fn([]) == []
check(merge_intervals)
""", max_new_tokens=768),
        Case("code_tests", "top_k_frequent", "Write Python function top_k_frequent(nums, k) returning the k most frequent integers in any order. Output only code.", tests="""
def check(fn):
    assert set(fn([1,1,1,2,2,3],2)) == {1,2}
    assert set(fn([1],1)) == {1}
    assert set(fn([4,4,5,5,6],2)) == {4,5}
check(top_k_frequent)
""", max_new_tokens=768),
        Case("code_tests", "roman_to_int", "Write Python function roman_to_int(s) converting a Roman numeral to integer. Output only code.", tests="""
def check(fn):
    assert fn('III') == 3
    assert fn('IV') == 4
    assert fn('IX') == 9
    assert fn('LVIII') == 58
    assert fn('MCMXCIV') == 1994
check(roman_to_int)
""", max_new_tokens=768),
    ]


def instruction_cases():
    return [
        Case("instruction_following", "json_only", "Return exactly valid JSON with keys verdict and score. verdict must be \"pass\" and score must be 7. No markdown. No explanation.", {"verdict":"pass","score":7}, max_new_tokens=256),
        Case("instruction_following", "no_think", "Answer with exactly one word: crab. Do not include reasoning or <think>.", "crab", max_new_tokens=128),
        Case("instruction_following", "bullet_count", "Give exactly three bullet points about unit tests. Each bullet must be five words or fewer.", 3, max_new_tokens=256),
        Case("instruction_following", "quote_wrapper", "Wrap the word reliable in double quotes and output nothing else.", '"reliable"', max_new_tokens=128),
        Case("instruction_following", "csv", "Output one CSV row with these fields: model,VibeThinker-3B,status,loaded. No header.", "model,VibeThinker-3B,status,loaded", max_new_tokens=128),
    ]


def untidy_cases():
    return [
        Case("untidy_reasoning", "queue_race", "Wear OS Kotlin app: playQueue(tracks,startIndex) writes queue async then starts playback. On process death it restores last queue/index. List concrete race tests and minimal robust ordering. Be specific.", None, max_new_tokens=768),
        Case("untidy_reasoning", "compose_deprecation", "Android Wear Compose code has deprecation warnings: ScalingLazyColumn and rememberScalingLazyListState moved to androidx.wear.compose.foundation.lazy. Explain a safe mechanical migration plan and one risk to test.", None, max_new_tokens=512),
        Case("untidy_reasoning", "service_state", "A TIDAL Wear OS player service exposes UI state via StateFlow. Network callbacks, Media3 player callbacks, and UI actions can all mutate state. What invariants and tests would catch stale queue/current track bugs?", None, max_new_tokens=768),
    ]


def extract_code(resp: str) -> str:
    m = re.search(r"```(?:python)?\s*(.*?)```", resp, re.S|re.I)
    if m:
        return m.group(1).strip()
    # strip think blocks crudely
    resp = re.sub(r"<think>.*?(?:</think>|$)", "", resp, flags=re.S).strip() or resp
    return resp.strip()


def run_python_tests(code: str, tests: str, timeout_s=5):
    full = code + "\n\n" + tests
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(full)
        path=f.name
    try:
        r=subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout_s)
        return r.returncode == 0, (r.stdout + r.stderr)[-2000:]
    except Exception as e:
        return False, repr(e)
    finally:
        try: os.unlink(path)
        except OSError: pass


def last_int(text):
    nums = re.findall(r"-?\d+", text.replace(",", ""))
    return int(nums[-1]) if nums else None


def score_case(case: Case, response: str):
    low=response.lower()
    if case.bench in {"gsm8k_manual"}:
        return last_int(response)==case.answer, {"extracted": last_int(response)}
    if case.name == "contradiction_marbles":
        return "inconsistent" in low or "impossible" in low or "no solution" in low, {}
    if case.name == "probability":
        return "1/4" in response or "0.25" in response or "25%" in response, {}
    if case.name == "quadratic":
        nums=set(re.findall(r"(?<!\d)(?:2|3)(?!\d)", response))
        return nums=={"2","3"}, {"roots_found": sorted(nums)}
    if case.bench == "math_reasoning":
        return last_int(response)==case.answer, {"extracted": last_int(response)}
    if case.bench == "code_tests":
        code=extract_code(response)
        ok, log=run_python_tests(code, case.tests or "")
        return ok, {"test_log": log, "code": code[:2000]}
    if case.bench == "instruction_following":
        stripped=response.strip()
        no_think = "<think>" not in stripped.lower()
        if case.name == "json_only":
            try: obj=json.loads(stripped); return obj==case.answer and no_think, {"parsed": obj, "no_think": no_think}
            except Exception as e: return False, {"error": repr(e), "no_think": no_think}
        if case.name == "bullet_count":
            bullets=[ln for ln in stripped.splitlines() if ln.strip().startswith(('-', '*'))]
            return len(bullets)==3 and no_think and all(len(re.sub(r'^[-*]\s*','',b).split())<=5 for b in bullets), {"bullets": bullets, "no_think": no_think}
        return stripped == case.answer and no_think, {"stripped": stripped[:200], "no_think": no_think}
    if case.bench == "untidy_reasoning":
        keywords=["race", "atomic", "persist", "test", "process death", "queue"]
        hits=sum(1 for k in keywords if k in low)
        return hits>=4, {"keyword_hits": hits}
    return False, {}


def main():
    cases = gsm8k_cases()+math_cases()+humaneval_like_cases()+instruction_cases()+untidy_cases()
    print(json.dumps({"model": MODEL_ID, "device": DEVICE, "dtype": str(DTYPE), "cases": len(cases), "max_new_default": MAX_NEW, "temp": TEMP, "top_p": TOP_P}, indent=2), flush=True)
    t0=time.perf_counter()
    tok=AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=DTYPE, low_cpu_mem_usage=True, trust_remote_code=True, attn_implementation="eager").eval().to(DEVICE)
    load_s=time.perf_counter()-t0
    print(f"LOADED {load_s:.2f}s", flush=True)
    results=[]
    for i,case in enumerate(cases,1):
        text=tok.apply_chat_template([{"role":"user","content":case.prompt}], tokenize=False, add_generation_prompt=True)
        inputs=tok([text], return_tensors="pt").to(DEVICE)
        conf=GenerationConfig(max_new_tokens=case.max_new_tokens, do_sample=True, temperature=TEMP, top_p=TOP_P, top_k=None, pad_token_id=tok.eos_token_id)
        print(f"CASE {i}/{len(cases)} {case.bench}/{case.name} in={inputs.input_ids.shape[-1]} max={case.max_new_tokens}", flush=True)
        c0=time.perf_counter()
        with torch.inference_mode():
            out=model.generate(**inputs, generation_config=conf)
        elapsed=time.perf_counter()-c0
        new=out[0, inputs.input_ids.shape[-1]:]
        resp=tok.decode(new, skip_special_tokens=True)
        passed, details=score_case(case, resp)
        rec={"bench":case.bench,"name":case.name,"passed":passed,"elapsed_s":elapsed,"input_tokens":int(inputs.input_ids.shape[-1]),"new_tokens":int(new.shape[-1]),"tokens_per_s":int(new.shape[-1])/elapsed if elapsed else 0,"answer":case.answer,"details":details,"response":resp}
        results.append(rec)
        (OUT/f"{case.bench}__{case.name}.txt").write_text(resp)
        print(f"RESULT {case.bench}/{case.name} pass={passed} new={rec['new_tokens']} elapsed={elapsed:.1f}s tok_s={rec['tokens_per_s']:.2f}", flush=True)
    summary={"model":MODEL_ID,"device":DEVICE,"dtype":str(DTYPE),"load_s":load_s,"started_at":time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),"results":results}
    (OUT/"kitchen_sink_results.json").write_text(json.dumps(summary, indent=2))
    by={}
    for r in results:
        by.setdefault(r['bench'], [0,0,0.0])
        by[r['bench']][0]+=1
        by[r['bench']][1]+=1 if r['passed'] else 0
        by[r['bench']][2]+=r['elapsed_s']
    print("SUMMARY")
    for bench,(n,p,secs) in by.items():
        print(f"{bench}: {p}/{n} pass, {secs:.1f}s")
    print(f"WROTE {OUT/'kitchen_sink_results.json'}")

if __name__=='__main__':
    main()
