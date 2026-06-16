from __future__ import annotations
import argparse, hashlib, json, math, time
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]

def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]

def sha256_file(path: Path) -> str:
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def require_module(name: str) -> None:
    try: __import__(name)
    except Exception as exc: raise SystemExit(f"Missing or broken dependency: {name}\nError: {repr(exc)}")

class JsonlTextDataset:
    def __init__(self, rows, tokenizer, max_seq_len): self.rows=rows; self.tokenizer=tokenizer; self.max_seq_len=max_seq_len
    def __len__(self): return len(self.rows)
    def __getitem__(self, idx):
        row=self.rows[idx]; text=row.get('text') or (row.get('prompt','')+row.get('completion',''))
        enc=self.tokenizer(text,truncation=True,max_length=self.max_seq_len,padding=False,return_attention_mask=True); enc['labels']=list(enc['input_ids']); return enc

def make_collate_fn(tokenizer):
    def collate(batch):
        import torch
        feats=[{'input_ids':x['input_ids'],'attention_mask':x['attention_mask']} for x in batch]
        padded=tokenizer.pad(feats,padding=True,return_tensors='pt'); labels=padded['input_ids'].clone(); labels[padded['attention_mask']==0]=-100; padded['labels']=labels; return padded
    return collate

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--base-model',default=r'E:\\gemma-4-E2B-it'); ap.add_argument('--train-data',default=str(ROOT/'data/trace_hix_v0_4/sft_train_180.jsonl')); ap.add_argument('--eval-data',default=str(ROOT/'data/trace_hix_v0_4/sft_eval_45.jsonl')); ap.add_argument('--output-dir',default=str(ROOT/'outputs/v0_4/gemma4_lora_adapter')); ap.add_argument('--max-seq-len',type=int,default=64); ap.add_argument('--epochs',type=float,default=1.0); ap.add_argument('--batch-size',type=int,default=1); ap.add_argument('--grad-accum',type=int,default=64); ap.add_argument('--learning-rate',type=float,default=1e-4); ap.add_argument('--no-4bit',action='store_true'); ap.add_argument('--dry-run',action='store_true'); args=ap.parse_args()
    base=Path(args.base_model); train_data=Path(args.train_data); eval_data=Path(args.eval_data); out=Path(args.output_dir)
    if not base.exists(): raise SystemExit(f'Base model path does not exist: {base}')
    train_rows=load_jsonl(train_data); eval_rows=load_jsonl(eval_data)
    if args.dry_run:
        print('ZANT_LLM_V0_4_TRAIN_DRY_RUN_OK=True'); print(f'TRAIN_ROWS={len(train_rows)}'); print(f'EVAL_ROWS={len(eval_rows)}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False'); return 0
    for m in ['torch','transformers','peft','accelerate']: require_module(m)
    import torch
    from torch.utils.data import DataLoader
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    if not args.no_4bit:
        from transformers import BitsAndBytesConfig
        from peft import prepare_model_for_kbit_training
    else:
        BitsAndBytesConfig=None; prepare_model_for_kbit_training=None
    print('ZANT_LLM_V0_4_REAL_TRAIN_START=True'); print(f'BASE_MODEL={base}'); print(f'TRAIN_ROWS={len(train_rows)}'); print(f'EVAL_ROWS={len(eval_rows)}'); print(f'NO_4BIT={args.no_4bit}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False')
    cuda_ok=torch.cuda.is_available(); print(f'TORCH_VERSION={torch.__version__}'); print(f'CUDA_AVAILABLE={cuda_ok}');
    if cuda_ok: print(f'CUDA_DEVICE={torch.cuda.get_device_name(0)}')
    tok=AutoTokenizer.from_pretrained(str(base),trust_remote_code=True)
    if tok.pad_token is None: tok.pad_token=tok.eos_token
    qcfg=None
    if not args.no_4bit: qcfg=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_use_double_quant=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=torch.float16)
    model=AutoModelForCausalLM.from_pretrained(str(base),trust_remote_code=True,torch_dtype=torch.float16 if cuda_ok else torch.float32,device_map='auto' if cuda_ok else None,quantization_config=qcfg,low_cpu_mem_usage=True)
    if not args.no_4bit: model=prepare_model_for_kbit_training(model)
    elif hasattr(model,'gradient_checkpointing_enable'): model.gradient_checkpointing_enable()
    cfg=LoraConfig(r=8,lora_alpha=16,lora_dropout=0.05,bias='none',task_type='CAUSAL_LM',target_modules=['q_proj.linear','k_proj.linear','v_proj.linear','o_proj.linear','gate_proj.linear','up_proj.linear','down_proj.linear'])
    model=get_peft_model(model,cfg); model.train()
    if hasattr(model,'print_trainable_parameters'): model.print_trainable_parameters()
    loader=DataLoader(JsonlTextDataset(train_rows,tok,args.max_seq_len),batch_size=args.batch_size,shuffle=True,collate_fn=make_collate_fn(tok)); opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=args.learning_rate)
    start=time.time(); global_step=0; running=0.0; opt.zero_grad(set_to_none=True)
    for epoch in range(int(math.ceil(args.epochs))):
        for step,batch in enumerate(loader,start=1):
            if cuda_ok: batch={k:v.to('cuda') for k,v in batch.items()}
            loss=model(**batch).loss/args.grad_accum; loss.backward(); running+=float(loss.detach().cpu())*args.grad_accum
            if step % args.grad_accum==0 or step==len(loader): opt.step(); opt.zero_grad(set_to_none=True); global_step+=1; print(f'TRAIN_PROGRESS epoch={epoch+1} global_step={global_step} loss={running/max(1,global_step):.6f}')
    out.mkdir(parents=True,exist_ok=True); adapter_save_mode='peft_save_pretrained'
    try: model.save_pretrained(str(out))
    except NotImplementedError as exc:
        print(f'PEFT_SAVE_PRETRAINED_FAILED={repr(exc)}'); print('FALLBACK_SAVE_NON_META_LORA_TENSORS=True'); adapter_save_mode='non_meta_lora_torch_save'; state={}; skipped=[]
        for name,param in model.named_parameters():
            if not param.requires_grad or 'lora_' not in name: continue
            if getattr(param,'is_meta',False): skipped.append(name); continue
            state[name]=param.detach().cpu()
        if not state: raise RuntimeError('No non-meta LoRA tensors were available to save.')
        torch.save(state,out/'adapter_model_non_meta_lora.pt')
        (out/'adapter_config_fallback.json').write_text(json.dumps({'format':'zant_llm_v0_4_non_meta_lora_fallback','base_model_name_or_path':str(base),'task_type':'CAUSAL_LM','r':8,'lora_alpha':16,'lora_dropout':0.05,'bias':'none','target_modules':['q_proj.linear','k_proj.linear','v_proj.linear','o_proj.linear','gate_proj.linear','up_proj.linear','down_proj.linear'],'saved_tensor_count':len(state),'skipped_meta_tensor_count':len(skipped),'skipped_meta_tensor_names':skipped[:100],'runtime_authority_granted':False,'provider_dispatch_enabled':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    tok.save_pretrained(str(out))
    report={'report_version':'zant_llm_v0_4_train_report_v0_windows_no_pyarrow','branch':'v0.4-evidence-gated-explanation-admissibility','base_model':str(base),'output_dir':str(out),'train_rows':len(train_rows),'eval_rows':len(eval_rows),'max_seq_len':args.max_seq_len,'epochs':args.epochs,'batch_size':args.batch_size,'grad_accum':args.grad_accum,'learning_rate':args.learning_rate,'no_4bit':args.no_4bit,'adapter_save_mode':adapter_save_mode,'elapsed_seconds':time.time()-start,'train_data_sha256':sha256_file(train_data),'eval_data_sha256':sha256_file(eval_data),'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    (ROOT/'outputs/v0_4/train_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (out/'zant_llm_v0_4_training_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('ZANT_LLM_V0_4_GEMMA4_LORA_TRAINED=True'); print(f'ADAPTER_OUTPUT_DIR={out}'); print(f"TRAIN_REPORT={ROOT/'outputs/v0_4/train_report.json'}"); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False'); return 0
if __name__=='__main__': raise SystemExit(main())


