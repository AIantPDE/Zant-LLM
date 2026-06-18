from __future__ import annotations
import argparse, json
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]

def load_rows(path: Path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-model', default=r'E:\gemma-4-E2B-it')
    ap.add_argument('--adapter-path', default=r'C:\Users\Administrator\Desktop\Zant-LLM-v0.7-push-work\outputs\v0_7\gemma4_lora_adapter')
    ap.add_argument('--data', default=str(ROOT/'data/trace_hix_v0_8/heldout_smoke_45.jsonl'))
    ap.add_argument('--output', default=str(ROOT/'reports/v0_8/zant_llm_v0_8_heldout_model_probe_report.json'))
    ap.add_argument('--max-cases', type=int, default=12)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    rows = load_rows(Path(args.data))[:args.max_cases]
    if args.dry_run:
        report = {'branch':'v0.8-heldout-model-eval', 'mode':'heldout-model-probe-dry-run','cases':len(rows), 'base_model':args.base_model, 'adapter_path':args.adapter_path,'runtime_authority_granted':False, 'provider_dispatch_enabled':False}
        out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print('ZANT_LLM_V0_8_MODEL_PROBE_DRY_RUN_OK=True')
        print(f'CASES={len(rows)}')
        print('RUNTIME_AUTHORITY_GRANTED=False')
        print('PROVIDER_DISPATCH_ENABLED=False')
        return 0
    base = Path(args.base_model); adapter = Path(args.adapter_path)
    if not base.exists(): raise SystemExit(f'Base model path does not exist: {base}')
    if not adapter.exists(): raise SystemExit(f'Adapter path does not exist: {adapter}')
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    tokenizer = AutoTokenizer.from_pretrained(str(adapter), trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(str(base), trust_remote_code=True, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
    model = PeftModel.from_pretrained(model, str(adapter))
    model.eval()
    results=[]; counts=Counter()
    for r in rows:
        prompt = 'Classify this heldout input as READY, BLOCKED, CLOSEOUT, or FAILCLOSED. Return JSON only.\n' + r['input_text']
        inputs = tokenizer(prompt, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad(): out = model.generate(**inputs, max_new_tokens=64, do_sample=False)
        text = tokenizer.decode(out[0], skip_special_tokens=True)
        counts[r['expected_decision']] += 1
        results.append({'id':r['id'], 'expected':r['expected_decision'], 'raw_output':text[-500:]})
    report={'branch':'v0.8-heldout-model-eval','mode':'heldout-model-probe','cases':len(rows),'expected_counts':dict(counts),'results':results,'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ZANT_LLM_V0_8_MODEL_PROBE_OK=True')
    print(f'CASES={len(rows)}')
    print(f'REPORT={out}')
    print('RUNTIME_AUTHORITY_GRANTED=False')
    print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
