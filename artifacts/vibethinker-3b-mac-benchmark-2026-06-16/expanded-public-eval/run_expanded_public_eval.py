import json, os, re, subprocess, sys, tempfile, time, textwrap
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

MODEL_ID='WeiboAI/VibeThinker-3B'
DEVICE='mps' if torch.backends.mps.is_available() else 'cpu'
DTYPE=torch.float16 if DEVICE=='mps' else torch.float32
TEMP=0.6; TOP_P=0.95
OUT=Path('outputs/expanded_public_eval'); OUT.mkdir(parents=True, exist_ok=True)

# bounded slices so the Mac run completes and is reproducible
AIME24_I_INDICES=list(range(5))
IFEVAL_INDICES=[0,5,25,60,120]  # official prompt source; simplified local evaluator where supported
LCB_INDICES=[0,1,2]             # HF livecodebench/code_generation default subset; NOT v6 unless runner path added


def generate(model,tok,prompt,max_new):
    text=tok.apply_chat_template([{'role':'user','content':prompt}], tokenize=False, add_generation_prompt=True)
    inputs=tok([text], return_tensors='pt').to(DEVICE)
    conf=GenerationConfig(max_new_tokens=max_new, do_sample=True, temperature=TEMP, top_p=TOP_P, top_k=None, pad_token_id=tok.eos_token_id)
    t=time.perf_counter()
    with torch.inference_mode():
        out=model.generate(**inputs, generation_config=conf)
    elapsed=time.perf_counter()-t
    new=out[0, inputs.input_ids.shape[-1]:]
    resp=tok.decode(new, skip_special_tokens=True)
    return resp, int(inputs.input_ids.shape[-1]), int(new.shape[-1]), elapsed

def strip_think(s):
    return re.sub(r'<think>.*?</think>', '', s, flags=re.S|re.I).strip()

def extract_int(s):
    clean=strip_think(s).replace(',','')
    boxed=re.findall(r'\\boxed\{([^}]*)\}', clean)
    if boxed:
        nums=re.findall(r'-?\d+', boxed[-1])
        if nums: return nums[-1]
    nums=re.findall(r'-?\d+', clean)
    return nums[-1] if nums else None

def extract_code(resp):
    clean=strip_think(resp)
    m=re.search(r'```(?:python|py)?\s*(.*?)```', clean, re.S|re.I)
    return (m.group(1) if m else clean).strip()

def run_stdio_code(code, public_tests_json, timeout=15):
    tests=json.loads(public_tests_json) if isinstance(public_tests_json,str) else public_tests_json
    if not tests: return False, 'no public tests'
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write(code)
        path=f.name
    logs=[]; ok=True
    try:
        for i,t in enumerate(tests):
            inp=t.get('input',''); exp=t.get('output','')
            try:
                r=subprocess.run([sys.executable,path], input=inp, capture_output=True, text=True, timeout=timeout)
                got=r.stdout
                passed=(r.returncode==0 and got.strip()==exp.strip())
                logs.append({'case':i,'passed':passed,'returncode':r.returncode,'expected':exp[:500],'got':got[:500],'stderr':r.stderr[-500:]})
                ok=ok and passed
            except Exception as e:
                logs.append({'case':i,'passed':False,'error':repr(e)})
                ok=False
        return ok, json.dumps(logs, ensure_ascii=False)
    finally:
        try: os.unlink(path)
        except OSError: pass

def eval_ifeval_simplified(ex, resp):
    # This is not official IFEval scoring. It handles a few detectable constraints and labels unsupported ones.
    text=strip_think(resp)
    ids=ex['instruction_id_list']; kwargs=ex['kwargs']
    checks=[]
    for iid,kw in zip(ids, kwargs):
        kw=kw or {}
        if iid=='punctuation:no_comma':
            checks.append(('no_comma', ',' not in text))
        elif iid=='detectable_format:number_highlighted_sections':
            n=kw.get('num_highlights') or 3
            checks.append(('highlighted_sections', len(re.findall(r'\*[^*]+\*', text))>=n))
        elif iid=='length_constraints:number_words':
            relation=kw.get('relation') or 'at least'; n=kw.get('num_words') or 0
            words=len(re.findall(r'\b\w+\b', text))
            checks.append(('word_count', words>=n if relation=='at least' else words==n))
        elif iid=='startend:end_checker':
            phrase=kw.get('end_phrase')
            checks.append(('end_phrase', text.endswith(phrase) if phrase else None))
        elif iid=='detectable_format:number_bullet_lists':
            n=kw.get('num_bullets') or 0
            bullets=[ln for ln in text.splitlines() if ln.strip().startswith(('-', '*'))]
            checks.append(('bullet_count', len(bullets)==n))
        elif iid=='keywords:existence':
            keyword=kw.get('keyword')
            checks.append(('keyword_existence', (keyword in text) if keyword else None))
        elif iid=='keywords:forbidden_words':
            forbidden=kw.get('forbidden_words') or []
            checks.append(('forbidden_words', all(w not in text for w in forbidden)))
        else:
            checks.append((iid, None))
    supported=[v for _,v in checks if v is not None]
    passed=bool(supported) and all(supported)
    return passed, checks

def main():
    meta={'model':MODEL_ID,'device':DEVICE,'dtype':str(DTYPE),'temp':TEMP,'top_p':TOP_P,'slices':{'aime':'MathArena/aime_2024_I train indices 0-4','ifeval':'google/IFEval train indices [0,5,25,60,120] with simplified local scorer, not official score','livecodebench':'livecodebench/code_generation default test indices 0-2 public tests only; not release_v6 official runner'}}
    print(json.dumps(meta, indent=2), flush=True)
    tok=AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=DTYPE, low_cpu_mem_usage=True, trust_remote_code=True, attn_implementation='eager').eval().to(DEVICE)
    rows=[]

    aime=load_dataset('MathArena/aime_2024_I', split='train')
    for idx in AIME24_I_INDICES:
        ex=aime[idx]
        prompt='Solve this AIME 2024 problem. Give the final answer as an integer from 000 to 999 at the end.\n\n'+ex['problem']
        resp,in_tok,new_tok,elapsed=generate(model,tok,prompt,1024)
        extracted=extract_int(resp); expected=str(ex['answer'])
        passed=(extracted==expected)
        rec={'benchmark':'aime_2024_I','dataset':'MathArena/aime_2024_I','split':'train','index':idx,'problem_idx':ex['problem_idx'],'passed':passed,'expected':expected,'extracted':extracted,'input_tokens':in_tok,'new_tokens':new_tok,'elapsed_s':elapsed,'tokens_per_s':new_tok/elapsed,'prompt':prompt,'response':resp}
        rows.append(rec); (OUT/f'aime_2024_I_{idx:02d}.txt').write_text(resp)
        print(f"RESULT aime index={idx} pass={passed} expected={expected} extracted={extracted} new={new_tok} elapsed={elapsed:.1f}s tok_s={new_tok/elapsed:.2f}", flush=True)

    ifeval=load_dataset('google/IFEval', split='train')
    for idx in IFEVAL_INDICES:
        ex=ifeval[idx]
        resp,in_tok,new_tok,elapsed=generate(model,tok,ex['prompt'],768)
        passed,checks=eval_ifeval_simplified(ex,resp)
        rec={'benchmark':'ifeval_simplified','dataset':'google/IFEval','split':'train','index':idx,'key':ex['key'],'passed':passed,'checks':checks,'instruction_id_list':ex['instruction_id_list'],'kwargs':ex['kwargs'],'input_tokens':in_tok,'new_tokens':new_tok,'elapsed_s':elapsed,'tokens_per_s':new_tok/elapsed,'prompt':ex['prompt'],'response':resp}
        rows.append(rec); (OUT/f'ifeval_google_{idx:03d}.txt').write_text(resp)
        print(f"RESULT ifeval index={idx} pass={passed} supported_checks={checks} new={new_tok} elapsed={elapsed:.1f}s tok_s={new_tok/elapsed:.2f}", flush=True)

    lcb=load_dataset('livecodebench/code_generation', split='test')
    for idx in LCB_INDICES:
        ex=lcb[idx]
        prompt=(
            'Solve this programming problem in Python 3. Output only a complete program that reads stdin and writes stdout.\n\n'
            f"Title: {ex['question_title']}\n\n{ex['question_content']}\n"
        )
        resp,in_tok,new_tok,elapsed=generate(model,tok,prompt,1536)
        code=extract_code(resp)
        passed,log=run_stdio_code(code, ex['public_test_cases'])
        rec={'benchmark':'livecodebench_public_tests','dataset':'livecodebench/code_generation','split':'test','index':idx,'question_id':ex['question_id'],'contest_date':str(ex['contest_date']),'difficulty':ex['difficulty'],'passed':passed,'test_log':log,'input_tokens':in_tok,'new_tokens':new_tok,'elapsed_s':elapsed,'tokens_per_s':new_tok/elapsed,'prompt':prompt,'response':resp,'candidate_code':code[:5000]}
        rows.append(rec); (OUT/f'lcb_{idx:03d}_{ex["question_id"]}.txt').write_text(resp); (OUT/f'lcb_{idx:03d}_{ex["question_id"]}.py').write_text(code)
        print(f"RESULT lcb index={idx} qid={ex['question_id']} pass={passed} new={new_tok} elapsed={elapsed:.1f}s tok_s={new_tok/elapsed:.2f}", flush=True)

    by={}
    for r in rows:
        b=by.setdefault(r['benchmark'], {'n':0,'pass':0,'tokens':0,'elapsed_s':0})
        b['n']+=1; b['pass']+=int(r['passed']); b['tokens']+=r['new_tokens']; b['elapsed_s']+=r['elapsed_s']
    for b in by.values():
        b['pass_rate']=b['pass']/b['n']; b['tokens_per_s']=b['tokens']/b['elapsed_s'] if b['elapsed_s'] else 0
    summary={'meta':meta,'by_benchmark':by,'overall':{'n':len(rows),'pass':sum(int(r['passed']) for r in rows)},'rows':rows}
    summary['overall']['pass_rate']=summary['overall']['pass']/summary['overall']['n']
    (OUT/'expanded_public_eval_results.json').write_text(json.dumps(summary, indent=2))
    md=['# VibeThinker-3B expanded public eval', '', json.dumps(meta, indent=2), '', '## Summary']
    for k,b in by.items(): md.append(f"- {k}: {b['pass']}/{b['n']} ({b['pass_rate']:.1%}), {b['tokens_per_s']:.2f} tok/s aggregate")
    md.append(f"- overall: {summary['overall']['pass']}/{summary['overall']['n']} ({summary['overall']['pass_rate']:.1%})")
    (OUT/'expanded_public_eval_summary.md').write_text('\n'.join(md)+'\n')
    print('SUMMARY')
    print((OUT/'expanded_public_eval_summary.md').read_text(), flush=True)

if __name__=='__main__': main()
