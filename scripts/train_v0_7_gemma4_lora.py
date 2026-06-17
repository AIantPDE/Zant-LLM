from __future__ import annotations
import argparse, json, time, hashlib, math
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]

def load_jsonl(path:Path):
    return [json.loads(l) for l in path.open(encoding='utf-8') if l.strip()]

def sha256_file(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()
class JsonlTextDataset:
    def __init__(self, rows, tokenizer, max_seq_len): self.rows=rows; self.tokenizer=tokenizer; self.max_seq_len=max_seq_len
    def __len__(self): return len(self.rows)
    def __getitem__(self,i):
        text=self.rows[i].get('text') or (self.rows[i].get('prompt','')+'\n'+self.rows[i].get('completion',''))
        enc=self.tokenizer(text,truncation=True,max_length=self.max_seq_len,padding=False,return_attention_mask=True)
        enc['labels']=list(enc['input_ids']); return enc

def collate_fn(tokenizer):
    def collate(batch):
        import torch
        feats=[{'input_ids':b['input_ids'],'attention_mask':b['attention_mask']} for b in batch]
        padded=tokenizer.pad(feats,padding=True,return_tensors='pt')
        labels=padded['input_ids'].clone(); labels[padded['attention_mask']==0]=-100; padded['labels']=labels
        return padded
    return collate

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base-model',default=r'E:\gemma-4-E2B-it'); ap.add_argument('--train-data',default=str(ROOT/'data/trace_hix_v0_7/sft_train_360.jsonl')); ap.add_argument('--eval-data',default=str(ROOT/'data/trace_hix_v0_7/sft_eval_90.jsonl')); ap.add_argument('--output-dir',default=str(ROOT/'outputs/v0_7/gemma4_lora_adapter')); ap.add_argument('--max-seq-len',type=int,default=64); ap.add_argument('--epochs',type=float,default=1.0); ap.add_argument('--batch-size',type=int,default=1); ap.add_argument('--grad-accum',type=int,default=64); ap.add_argument('--learning-rate',type=float,default=1e-4); ap.add_argument('--no-4bit',action='store_true',default=True); ap.add_argument('--dry-run',action='store_true'); args=ap.parse_args()
    base=Path(args.base_model); train_path=Path(args.train_data); eval_path=Path(args.eval_data); out=Path(args.output_dir)
    train_rows=load_jsonl(train_path); eval_rows=load_jsonl(eval_path)
    if args.dry_run:
        print('ZANT_LLM_V0_7_TRAIN_DRY_RUN_OK=True'); print(f'TRAIN_ROWS={len(train_rows)}'); print(f'EVAL_ROWS={len(eval_rows)}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False'); return 0
    if not base.exists(): raise SystemExit(f'Base model path does not exist: {base}')
    import torch
    from torch.utils.data import DataLoader
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import LoraConfig, get_peft_model
    print('ZANT_LLM_V0_7_REAL_TRAIN_START=True'); print(f'TRAIN_ROWS={len(train_rows)}'); print(f'EVAL_ROWS={len(eval_rows)}'); print(f'NO_4BIT={args.no_4bit}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False'); print(f'TORCH_VERSION={torch.__version__}'); print(f'CUDA_AVAILABLE={torch.cuda.is_available()}')
    tokenizer=AutoTokenizer.from_pretrained(str(base),trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token=tokenizer.eos_token
    model=AutoModelForCausalLM.from_pretrained(str(base),trust_remote_code=True,torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,device_map='auto' if torch.cuda.is_available() else None,low_cpu_mem_usage=True)
    if hasattr(model,'gradient_checkpointing_enable'): model.gradient_checkpointing_enable()
    cfg=LoraConfig(r=8,lora_alpha=16,lora_dropout=0.05,bias='none',task_type='CAUSAL_LM',target_modules=['q_proj.linear','k_proj.linear','v_proj.linear','o_proj.linear','gate_proj.linear','up_proj.linear','down_proj.linear'])
    model=get_peft_model(model,cfg); model.train()
    if hasattr(model,'print_trainable_parameters'): model.print_trainable_parameters()
    loader=DataLoader(JsonlTextDataset(train_rows,tokenizer,args.max_seq_len),batch_size=args.batch_size,shuffle=True,collate_fn=collate_fn(tokenizer))
    optim=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=args.learning_rate)
    start=time.time(); optim.zero_grad(set_to_none=True); global_step=0; running=0.0
    for epoch in range(int(math.ceil(args.epochs))):
        for step,batch in enumerate(loader,1):
            if torch.cuda.is_available(): batch={k:v.to('cuda') for k,v in batch.items()}
            loss=model(**batch).loss/args.grad_accum; loss.backward(); running+=float(loss.detach().cpu())*args.grad_accum
            if step%args.grad_accum==0 or step==len(loader):
                optim.step(); optim.zero_grad(set_to_none=True); global_step+=1; print(f'TRAIN_PROGRESS epoch={epoch+1} global_step={global_step} loss={running/max(1,global_step):.6f}')
    out.mkdir(parents=True,exist_ok=True)
    save_mode='peft_save_pretrained'
    try: model.save_pretrained(str(out))
    except NotImplementedError as exc:
        print(f'PEFT_SAVE_PRETRAINED_FAILED={repr(exc)}'); print('FALLBACK_SAVE_NON_META_LORA_TENSORS=True'); save_mode='non_meta_lora_torch_save'; state={}; skipped=[]
        for n,p in model.named_parameters():
            if p.requires_grad and 'lora_' in n:
                if getattr(p,'is_meta',False): skipped.append(n)
                else: state[n]=p.detach().cpu()
        torch.save(state,out/'adapter_model_non_meta_lora.pt'); (out/'adapter_config_fallback.json').write_text(json.dumps({'format':'zant_llm_v0_7_non_meta_lora_fallback','saved_tensor_count':len(state),'skipped_meta_tensor_count':len(skipped),'target_modules':['q_proj.linear','k_proj.linear','v_proj.linear','o_proj.linear','gate_proj.linear','up_proj.linear','down_proj.linear'],'runtime_authority_granted':False,'provider_dispatch_enabled':False},indent=2)+'\n',encoding='utf-8')
    tokenizer.save_pretrained(str(out))
    report={'report_version':'zant_llm_v0_7_train_report_v1','branch':'v0.7-calibration-informed-sft','base_model':str(base),'train_rows':len(train_rows),'eval_rows':len(eval_rows),'max_seq_len':args.max_seq_len,'epochs':args.epochs,'batch_size':args.batch_size,'grad_accum':args.grad_accum,'learning_rate':args.learning_rate,'no_4bit':args.no_4bit,'adapter_save_mode':save_mode,'elapsed_seconds':time.time()-start,'train_data_sha256':sha256_file(train_path),'eval_data_sha256':sha256_file(eval_path),'runtime_authority_granted':False,'provider_dispatch_enabled':False}
    (ROOT/'outputs/v0_7/train_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); (out/'zant_llm_v0_7_training_manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('ZANT_LLM_V0_7_GEMMA4_LORA_TRAINED=True'); print(f'ADAPTER_OUTPUT_DIR={out}'); print(f'TRAIN_REPORT={ROOT/"outputs/v0_7/train_report.json"}'); print('RUNTIME_AUTHORITY_GRANTED=False'); print('PROVIDER_DISPATCH_ENABLED=False')
    return 0
if __name__=='__main__': raise SystemExit(main())
