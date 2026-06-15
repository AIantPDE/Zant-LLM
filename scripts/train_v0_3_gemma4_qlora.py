from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_module(name: str) -> None:
    try:
        __import__(name)
    except Exception as exc:
        raise SystemExit(
            f"Missing or broken dependency: {name}\n"
            f"Error: {repr(exc)}\n"
            f"Please run: powershell -ExecutionPolicy Bypass -File .\\scripts\\INSTALL_ZANT_LLM_V0_3_TRAIN_DEPS.ps1"
        )


class JsonlTextDataset:
    def __init__(self, rows: list[dict[str, Any]], tokenizer: Any, max_seq_len: int) -> None:
        self.rows = rows
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        row = self.rows[idx]
        text = row.get("text")
        if not text:
            prompt = row.get("prompt", "")
            completion = row.get("completion", "")
            text = prompt + completion

        enc = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_seq_len,
            padding=False,
            return_attention_mask=True,
        )
        enc["labels"] = list(enc["input_ids"])
        return enc


def make_collate_fn(tokenizer: Any):
    def collate(batch: list[dict[str, Any]]) -> dict[str, Any]:
        import torch

        input_features = [
            {
                "input_ids": item["input_ids"],
                "attention_mask": item["attention_mask"],
            }
            for item in batch
        ]
        padded = tokenizer.pad(
            input_features,
            padding=True,
            return_tensors="pt",
        )
        labels = padded["input_ids"].clone()
        labels[padded["attention_mask"] == 0] = -100
        padded["labels"] = labels
        return padded

    return collate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", default=r"D:\gemma-4-E2B-it")
    parser.add_argument("--train-data", default=str(ROOT / "data/trace_hix_v0_3/sft_train_60.jsonl"))
    parser.add_argument("--eval-data", default=str(ROOT / "data/trace_hix_v0_3/sft_eval_12.jsonl"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs/v0_3/gemma4_qlora_adapter"))
    parser.add_argument("--max-seq-len", type=int, default=128)
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--no-4bit", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    base_model = Path(args.base_model)
    train_data = Path(args.train_data)
    eval_data = Path(args.eval_data)
    output_dir = Path(args.output_dir)

    if not base_model.exists():
        raise SystemExit(f"Base model path does not exist: {base_model}")

    if not train_data.exists():
        raise SystemExit(f"Train data does not exist: {train_data}")

    if not eval_data.exists():
        raise SystemExit(f"Eval data does not exist: {eval_data}")

    train_rows = load_jsonl(train_data)
    eval_rows = load_jsonl(eval_data)

    if args.dry_run:
        print("ZANT_LLM_V0_3_TRAIN_DRY_RUN_OK=True")
        print(f"TRAIN_ROWS={len(train_rows)}")
        print(f"EVAL_ROWS={len(eval_rows)}")
        print("RUNTIME_AUTHORITY_GRANTED=False")
        print("PROVIDER_DISPATCH_ENABLED=False")
        return 0

    # 不再 import datasets / pyarrow，避免 Windows 原生崩溃。
    for module_name in ["torch", "transformers", "peft", "accelerate"]:
        require_module(module_name)

    import torch
    from torch.utils.data import DataLoader
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from peft import LoraConfig, get_peft_model

    if not args.no_4bit:
        from transformers import BitsAndBytesConfig
        from peft import prepare_model_for_kbit_training
    else:
        BitsAndBytesConfig = None
        prepare_model_for_kbit_training = None

    print("ZANT_LLM_V0_3_REAL_TRAIN_START=True")
    print(f"BASE_MODEL={base_model}")
    print(f"TRAIN_ROWS={len(train_rows)}")
    print(f"EVAL_ROWS={len(eval_rows)}")
    print(f"MAX_SEQ_LEN={args.max_seq_len}")
    print(f"NO_4BIT={args.no_4bit}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")

    cuda_ok = torch.cuda.is_available()
    print(f"TORCH_VERSION={torch.__version__}")
    print(f"CUDA_AVAILABLE={cuda_ok}")
    if cuda_ok:
        print(f"CUDA_DEVICE={torch.cuda.get_device_name(0)}")

    tokenizer = AutoTokenizer.from_pretrained(str(base_model), trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quantization_config = None
    if not args.no_4bit:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )

    model = AutoModelForCausalLM.from_pretrained(
        str(base_model),
        trust_remote_code=True,
        torch_dtype=torch.float16 if cuda_ok else torch.float32,
        device_map="auto" if cuda_ok else None,
        quantization_config=quantization_config,
        low_cpu_mem_usage=True,
    )

    if not args.no_4bit:
        model = prepare_model_for_kbit_training(model)
    else:
        if hasattr(model, "gradient_checkpointing_enable"):
            model.gradient_checkpointing_enable()

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        # Gemma4 wraps projection layers as Gemma4ClippableLinear(linear=nn.Linear).
        # PEFT cannot attach LoRA to Gemma4ClippableLinear directly, so target the inner nn.Linear.
        target_modules=[
            "q_proj.linear",
            "k_proj.linear",
            "v_proj.linear",
            "o_proj.linear",
            "gate_proj.linear",
            "up_proj.linear",
            "down_proj.linear",
        ],
    )

    model = get_peft_model(model, lora_config)
    model.train()

    if hasattr(model, "print_trainable_parameters"):
        model.print_trainable_parameters()

    train_dataset = JsonlTextDataset(train_rows, tokenizer, args.max_seq_len)
    collate_fn = make_collate_fn(tokenizer)
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        collate_fn=collate_fn,
    )

    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=args.learning_rate,
    )

    start_time = time.time()
    total_steps = max(1, math.ceil(len(train_loader) * args.epochs))
    global_step = 0
    running_loss = 0.0
    optimizer.zero_grad(set_to_none=True)

    for epoch_idx in range(int(math.ceil(args.epochs))):
        for step_idx, batch in enumerate(train_loader, start=1):
            if cuda_ok:
                batch = {k: v.to("cuda") for k, v in batch.items()}

            outputs = model(**batch)
            loss = outputs.loss / args.grad_accum
            loss.backward()

            running_loss += float(loss.detach().cpu()) * args.grad_accum

            if step_idx % args.grad_accum == 0 or step_idx == len(train_loader):
                optimizer.step()
                optimizer.zero_grad(set_to_none=True)
                global_step += 1

                print(
                    f"TRAIN_PROGRESS epoch={epoch_idx + 1} "
                    f"global_step={global_step} "
                    f"loss={running_loss / max(1, global_step):.6f}"
                )

    output_dir.mkdir(parents=True, exist_ok=True)

    # Windows / GTX1070 fallback:
    # device_map="auto" may leave some offloaded tensors on meta device.
    # PEFT save_pretrained can fail with:
    # NotImplementedError: Cannot copy out of meta tensor; no data!
    # In that case, save only real non-meta trainable LoRA tensors.
    adapter_save_mode = "peft_save_pretrained"
    try:
        model.save_pretrained(str(output_dir))
    except NotImplementedError as exc:
        print(f"PEFT_SAVE_PRETRAINED_FAILED={repr(exc)}")
        print("FALLBACK_SAVE_NON_META_LORA_TENSORS=True")
        adapter_save_mode = "non_meta_lora_torch_save"

        import torch

        adapter_state = {}
        skipped_meta = []
        for name, param in model.named_parameters():
            if not param.requires_grad:
                continue
            if "lora_" not in name:
                continue
            if getattr(param, "is_meta", False):
                skipped_meta.append(name)
                continue
            adapter_state[name] = param.detach().cpu()

        if not adapter_state:
            raise RuntimeError(
                "No non-meta LoRA tensors were available to save. "
                "Try reducing target modules or using true 4bit loading."
            )

        torch.save(adapter_state, output_dir / "adapter_model_non_meta_lora.pt")

        adapter_config_fallback = {
            "format": "zant_llm_v0_3_non_meta_lora_fallback",
            "base_model_name_or_path": str(base_model),
            "task_type": "CAUSAL_LM",
            "r": 8,
            "lora_alpha": 16,
            "lora_dropout": 0.05,
            "bias": "none",
            "target_modules": [
                "q_proj.linear",
                "k_proj.linear",
                "v_proj.linear",
                "o_proj.linear",
                "gate_proj.linear",
                "up_proj.linear",
                "down_proj.linear",
            ],
            "saved_tensor_count": len(adapter_state),
            "skipped_meta_tensor_count": len(skipped_meta),
            "skipped_meta_tensor_names": skipped_meta[:100],
            "runtime_authority_granted": False,
            "provider_dispatch_enabled": False,
        }

        (output_dir / "adapter_config_fallback.json").write_text(
            json.dumps(adapter_config_fallback, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    tokenizer.save_pretrained(str(output_dir))

    elapsed = time.time() - start_time
    train_report = {
        "report_version": "zant_llm_v0_3_train_report_v1_windows_no_pyarrow",
        "branch": "v0.3-gemma4-qlora-explanation-baseline",
        "base_model": str(base_model),
        "output_dir": str(output_dir),
        "train_rows": len(train_rows),
        "eval_rows": len(eval_rows),
        "max_seq_len": args.max_seq_len,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "grad_accum": args.grad_accum,
        "learning_rate": args.learning_rate,
        "no_4bit": args.no_4bit,
        "elapsed_seconds": elapsed,
        "train_data_sha256": sha256_file(train_data),
        "eval_data_sha256": sha256_file(eval_data),
        "runtime_authority_granted": False,
        "provider_dispatch_enabled": False,
    }

    (ROOT / "outputs/v0_3/train_report.json").write_text(
        json.dumps(train_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    (output_dir / "zant_llm_v0_3_training_manifest.json").write_text(
        json.dumps(train_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("ZANT_LLM_V0_3_GEMMA4_QLORA_TRAINED=True")
    print(f"ADAPTER_OUTPUT_DIR={output_dir}")
    print(f"TRAIN_REPORT={ROOT / 'outputs/v0_3/train_report.json'}")
    print("RUNTIME_AUTHORITY_GRANTED=False")
    print("PROVIDER_DISPATCH_ENABLED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


