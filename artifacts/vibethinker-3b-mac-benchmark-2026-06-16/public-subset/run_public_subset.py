import json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from datasets import load_dataset

MODEL_ID='WeiboAI/VibeThinker-3B'
DEVICE='mps' if torch.backends.mps.is_available() else 'cpu'
DTYPE=torch.float16 if DEVICE=='mps' else torch.float32
OUT=Path('outputs/public_subset'); OUT.mkdir(parents=True, exist_ok=True)
TEMP=0.6; TOP_P=0.95

HUMANEVAL_INDICES=[0,1,2,3,4]
GSM8K_INDICES=[0,1,2,3,4,5,6,7,8,9]
IFEVAL_LIKE=[
  {'id':'json_exact','prompt':'Return exactly valid JSON: {"ok": true, "n": 3}. No markdown, no explanation.','kind':'exact','answer':'{"ok": true, "n": 3}'},
  {'id':'one_word','prompt':'Output exactly one word: lobster','kind':'exact','answer':'lobster'},
  {'id':'quoted','prompt':'Output exactly the word benchmark wrapped in double quotes and nothing else.','kind':'exact','answer':'"benchmark"'},
  {'id':'csv_row','prompt':'Output exactly this CSV row and nothing else: model,VibeThinker-3B,result,loaded','kind':'exact','answer':'model,VibeThinker-3B,result,loaded'},
  {'id':'two_bullets','prompt':'Output exactly two bullet points. Each bullet must contain exactly three words. Topic: tests.','kind':'bullets','answer':2},
]

def gen(model,tok,prompt,max_new):
    text=tok.apply_chat_template([{'role':'user','content':prompt}], tokenize=False, add_generation_prompt=True)
    inputs=tok([text], return_tensors='pt').to(DEVICE)
    conf=GenerationConfig(max_new_tokens=max_new, do_sample=True, temperature=TEMP, top_p=TOP_P, top_k=None, pad_token_id=tok.eos_token_id)
    t=time.perf_counter()
    with torch.inference_mode():
        out=model.generate(**inputs, generation_config=conf)
    elapsed=time.perf_counter()-t
    new=out[0, inputs.input_ids.shape[-1]:]
    return tok.decode(new, skip_special_tokens=True), int(inputs.input_ids.shape[-1]), int(new.shape[-1]), elapsed

def strip_think(s):
    return re.sub(r'<think>.*?</think>', '', s, flags=re.S|re.I).strip()

def last_number(s):
    nums=re.findall(r'-?\d+(?:\.\d+)?', s.replace(',',''))
    return nums[-1] if nums else None

def gsm_answer(ans):
    m=re.search(r'####\s*([-\d,\.]+)', ans)
    return m.group(1).replace(',','') if m else None

def extract_code(resp):
    m=re.search(r'```(?:python)?\s*(.*?)```', resp, re.S|re.I)
    if m: return m.group(1).strip()
    return strip_think(resp)

def run_tests(code, prompt, tests, entry_point):
    # HumanEval prompt contains the function signature/docstring. Model may output only body or full function.
    candidate=extract_code(code)
    if f'def {entry_point}' not in candidate:
        candidate=prompt + '\n' + candidate
    full=candidate+'\n\n'+tests+f'\ncheck({entry_point})\n'
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write(full); path=f.name
    try:
        r=subprocess.run([sys.executable,path], capture_output=True, text=True, timeout=10)
        return r.returncode==0, (r.stdout+r.stderr)[-3000:], candidate[:3000]
    except Exception as e:
        return False, repr(e), candidate[:3000]
    finally:
        try: os.unlink(path)
        except OSError: pass

def main():
    meta={'model':MODEL_ID,'device':DEVICE,'dtype':str(DTYPE),'temp':TEMP,'top_p':TOP_P,'datasets':{'gsm8k':'openai/gsm8k main/test indices 0-9','openai_humaneval':'openai/openai_humaneval test indices 0-4','ifeval_like':'local exact-format probes, not official IFEval'}}
    print(json.dumps(meta, indent=2), flush=True)
    tok=AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=DTYPE, low_cpu_mem_usage=True, trust_remote_code=True, attn_implementation='eager').eval().to(DEVICE)
    rows=[]

    gsm=load_dataset('openai/gsm8k','main',split='test')
    for idx in GSM8K_INDICES:
        ex=gsm[idx]
        prompt='Solve this GSM8K problem. Give the final numeric answer clearly at the end.\n\n'+ex['question']
        resp,in_tok,new_tok,elapsed=gen(model,tok,prompt,512)
        expected=gsm_answer(ex['answer']); extracted=last_number(strip_think(resp))
        passed=(extracted==expected)
        rec={'benchmark':'gsm8k','dataset':'openai/gsm8k/main','split':'test','index':idx,'passed':passed,'expected':expected,'extracted':extracted,'input_tokens':in_tok,'new_tokens':new_tok,'elapsed_s':elapsed,'tokens_per_s':new_tok/elapsed,'prompt':prompt,'response':resp}
        rows.append(rec); (OUT/f'gsm8k_{idx:03d}.txt').write_text(resp)
        print(f"RESULT gsm8k index={idx} pass={passed} expected={expected} extracted={extracted} new={new_tok} elapsed={elapsed:.1f}s tok_s={new_tok/elapsed:.2f}", flush=True)

    he=load_dataset('openai/openai_humaneval', split='test')
    for idx in HUMANEVAL_INDICES:
        ex=he[idx]
        prompt='Complete this Python function. Output only code.\n\n'+ex['prompt']
        resp,in_tok,new_tok,elapsed=gen(model,tok,prompt,768)
        passed,log,candidate=run_tests(resp, ex['prompt'], ex['test'], ex['entry_point'])
        rec={'benchmark':'humaneval','dataset':'openai/openai_humaneval','split':'test','index':idx,'task_id':ex['task_id'],'entry_point':ex['entry_point'],'passed':passed,'test_log':log,'candidate':candidate,'input_tokens':in_tok,'new_tokens':new_tok,'elapsed_s':elapsed,'tokens_per_s':new_tok/elapsed,'prompt':prompt,'response':resp}
        rows.append(rec); (OUT/f'humaneval_{idx:03d}_{ex["entry_point"]}.txt').write_text(resp)
        print(f"RESULT humaneval index={idx} task={ex['task_id']} pass={passed} new={new_tok} elapsed={elapsed:.1f}s tok_s={new_tok/elapsed:.2f}", flush=True)

    for ex in IFEVAL_LIKE:
        resp,in_tok,new_tok,elapsed=gen(model,tok,ex['prompt'],256)
        stripped=resp.strip()
        if ex['kind']=='exact': passed=(stripped==ex['answer'])
        else:
            lines=[l for l in stripped.splitlines() if l.strip().startswith(('-', '*'))]
            passed=(len(lines)==ex['answer'] and all(len(re.sub(r'^[-*]\s*','',l).split())==3 for l in lines))
        rec={'benchmark':'ifeval_like','dataset':'local_exact_format_probes','split':'n/a','index':ex['id'],'passed':passed,'expected':ex['answer'],'input_tokens':in_tok,'new_tokens':new_tok,'elapsed_s':elapsed,'tokens_per_s':new_tok/elapsed,'prompt':ex['prompt'],'response':resp}
        rows.append(rec); (OUT/f'ifeval_like_{ex["id"]}.txt').write_text(resp)
        print(f"RESULT ifeval_like id={ex['id']} pass={passed} new={new_tok} elapsed={elapsed:.1f}s tok_s={new_tok/elapsed:.2f}", flush=True)

    by={}
    for r in rows:
        by.setdefault(r['benchmark'], {'n':0,'pass':0,'tokens':0,'elapsed_s':0})
        b=by[r['benchmark']]; b['n']+=1; b['pass']+=int(r['passed']); b['tokens']+=r['new_tokens']; b['elapsed_s']+=r['elapsed_s']
    for b in by.values(): b['pass_rate']=b['pass']/b['n']; b['tokens_per_s']=b['tokens']/b['elapsed_s'] if b['elapsed_s'] else 0
    summary={'meta':meta,'by_benchmark':by,'overall':{'n':len(rows),'pass':sum(int(r['passed']) for r in rows)},'rows':rows}
    summary['overall']['pass_rate']=summary['overall']['pass']/summary['overall']['n']
    (OUT/'public_subset_results.json').write_text(json.dumps(summary, indent=2))
    md=['# VibeThinker-3B public benchmark subset','',json.dumps(meta, indent=2),'','## Summary']
    for k,b in by.items(): md.append(f"- {k}: {b['pass']}/{b['n']} ({b['pass_rate']:.1%}), {b['tokens_per_s']:.2f} tok/s aggregate")
    md.append(f"- overall: {summary['overall']['pass']}/{summary['overall']['n']} ({summary['overall']['pass_rate']:.1%})")
    (OUT/'public_subset_summary.md').write_text('\n'.join(md)+'\n')
    print('SUMMARY')
    print((OUT/'public_subset_summary.md').read_text(), flush=True)

if __name__=='__main__': main()
