from __future__ import annotations
import argparse, json, hashlib, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open("r", encoding="utf-8") if line.strip()]

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def missing_modules() -> list[str]:
    out=[]
    for m in ["torch","transformers","datasets","peft","accelerate"]:
        try: __import__(m)
        except Exception: out.append(m)
    return out

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--base-model", default=r"D:\gemma-4-E2B-it")
    ap.add_argument("--train-data", default=str(ROOT/"data/trace_hix_v0_3/sft_train_60.jsonl"))
    ap.add_argument("--eval-data", default=str(ROOT/"data/trace_hix_v0_3/sft_eval_12.jsonl"))
    ap.add_argument("--output-dir", default=str(ROOT/"outputs/v0_3/gemma4_qlora_adapter"))
    ap.add_argument("--max-seq-len", type=int, default=1024)
    ap.add_argument("--epochs", type=float, default=2.0)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--grad-accum", type=int, default=4)
    ap.add_argument("--learning-rate", type=float, default=2e-4)
    ap.add_argument("--no-4bit", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args=ap.parse_args()
    if not Path(args.train_data).exists():
        subprocess.check_call([sys.executable, str(ROOT/"scripts/build_v0_3_sft_dataset.py")])
    train_rows=load_jsonl(Path(args.train_data)); eval_rows=load_jsonl(Path(args.eval_data))
    if args.dry_run:
        print("ZANT_LLM_V0_3_TRAIN_DRY_RUN_OK=True")
        print(f"TRAIN_ROWS={len(train_rows)}")
        print(f"EVAL_ROWS={len(eval_rows)}")
        print("RUNTIME_AUTHORITY_GRANTED=False")
        return 0
    miss=missing_modules()
    if miss:
        print("ZANT_LLM_V0_3_TRAIN_DEPS_MISSING=True")
        print("MISSING_MODULES=" + ",".join(miss))
        print("Run .\\scripts\\INSTALL_ZANT_LLM_V0_3_TRAIN_DEPS.ps1")
        return 2
    import torch
    from datasets import Dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    base=Path(args.base_model)
    if not base.exists(): raise SystemExit(f"Base model path does not exist: {base}")
    tokenizer=AutoTokenizer.from_pretrained(str(base), trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token=tokenizer.eos_token
    qconf=None if args.no_4bit else BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.float16)
    model=AutoModelForCausalLM.from_pretrained(str(base), trust_remote_code=True, device_map="auto" if torch.cuda.is_available() else None, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, quantization_config=qconf)
    if not args.no_4bit: model=prepare_model_for_kbit_training(model)
    lora=LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,bias="none",task_type="CAUSAL_LM",target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])
    model=get_peft_model(model,lora)
    def tok(batch): return tokenizer(batch["text"], truncation=True, max_length=args.max_seq_len, padding=False)
    train_ds=Dataset.from_list(train_rows).map(tok, batched=True, remove_columns=list(train_rows[0].keys()))
    eval_ds=Dataset.from_list(eval_rows).map(tok, batched=True, remove_columns=list(eval_rows[0].keys()))
    out=Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    targs=TrainingArguments(output_dir=str(out), num_train_epochs=args.epochs, per_device_train_batch_size=args.batch_size, per_device_eval_batch_size=1, gradient_accumulation_steps=args.grad_accum, learning_rate=args.learning_rate, logging_steps=1, save_strategy="epoch", evaluation_strategy="epoch", fp16=torch.cuda.is_available(), report_to=[], remove_unused_columns=False)
    trainer=Trainer(model=model,args=targs,train_dataset=train_ds,eval_dataset=eval_ds,data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False))
    trainer.train(); model.save_pretrained(str(out)); tokenizer.save_pretrained(str(out))
    manifest={"manifest_version":"zant_llm_v0_3_training_manifest_v0","branch":"v0.3-gemma4-qlora-explanation-baseline","base_model":str(base),"adapter_output_dir":str(out),"train_rows":len(train_rows),"eval_rows":len(eval_rows),"train_data_sha256":sha(Path(args.train_data)),"eval_data_sha256":sha(Path(args.eval_data)),"runtime_authority_granted":False,"provider_dispatch_enabled":False}
    (out/"zant_llm_v0_3_training_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("ZANT_LLM_V0_3_GEMMA4_QLORA_TRAINED=True")
    print(f"ADAPTER_OUTPUT_DIR={out}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0
if __name__ == "__main__": raise SystemExit(main())
