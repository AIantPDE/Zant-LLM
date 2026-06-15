# Zant-LLM v0.3 Gemma4 QLoRA Explanation Baseline

分支名：`v0.3-gemma4-qlora-explanation-baseline`

本分支的目标是把 v0.2 的 TRACE-HIX schema、registry、validator 与 gold/negative seed，推进到第一个可训练的 **Gemma 4 E2B QLoRA explanation baseline**。

本分支允许：

- 构造 TRACE-HIX supervised fine-tuning dataset；
- 使用本地 `D:\gemma-4-E2B-it` 进行 QLoRA / LoRA 解释生成基线训练；
- 运行 contract-only eval 与可选 model eval；
- 输出 adapter manifest、eval report、release manifest；
- 保留 checkpoint sha256 / config / data manifest / model card 信息。

本分支仍然禁止：

- 接入 `aiant-zant runtime`；
- provider dispatch；
- provider registry update；
- route decision；
- fetch decision；
- worker trigger；
- writeback execution；
- runtime authority。

## 快速开始：只做本地验证

```powershell
cd C:\Users\Hilo\Desktop\zant_llm_v0_3_gemma4_qlora_explanation_baseline_branch
powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_3_LOCAL.ps1
```

## 构建 v0.3 SFT 数据集

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V0_3_SFT_DATASET.ps1
```

## 安装训练依赖

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\INSTALL_ZANT_LLM_V0_3_TRAIN_DEPS.ps1
```

如果你的 CUDA / torch 环境已经稳定，可以先不运行安装脚本，直接使用当前环境。

## 训练 Gemma 4 E2B QLoRA baseline

默认 base model：`D:\gemma-4-E2B-it`

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\TRAIN_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1
```

自定义 base model：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\TRAIN_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1 `
  -BaseModelPath "D:\gemma-4-E2B-it" `
  -OutputDir "E:\Zant-LLM-v0.3\gemma4_qlora_adapter"
```

## 评估

contract-only 评估不加载大模型，只验证 eval targets 是否满足 TRACE-HIX gates：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1 -Mode contract
```

model 评估会尝试加载 base model + adapter：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1 `
  -Mode model `
  -BaseModelPath "D:\gemma-4-E2B-it" `
  -AdapterPath "outputs0_3\gemma4_qlora_adapter"
```

## 推送到 GitHub

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_3_BASED_ON_REMOTE_V0_2.ps1
```

默认从远程 `v0.2-trace-hix-contracts-and-validators` 新建 `v0.3-gemma4-qlora-explanation-baseline` 并推送到 `https://github.com/AIantPDE/Zant-LLM.git`。
