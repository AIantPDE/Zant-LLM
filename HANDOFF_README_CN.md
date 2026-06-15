# Zant-LLM v0.3 交接说明

本包是 `v0.3-gemma4-qlora-explanation-baseline` 分支交付包。

它的作用不是替代 v0.2，而是在 v0.2 的 TRACE-HIX contracts/validators 基础上，增加 Gemma 4 E2B QLoRA 训练基线。

## 推荐执行顺序

```powershell
cd C:\Users\Hilo\Desktop\zant_llm_v0_3_gemma4_qlora_explanation_baseline_branch
powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_3_LOCAL.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V0_3_SFT_DATASET.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1 -Mode contract
```

确认本地环境有 transformers / datasets / peft / accelerate / bitsandbytes 后，再训练：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\TRAIN_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1
```

## 注意

训练生成的 adapter 权重默认在 `outputs/v0_3/gemma4_qlora_adapter`。`.gitignore` 默认忽略权重文件。源码仓只提交 manifest、配置、评估报告与 SHA256，不反复提交模型大文件。


## Windows PowerShell 验证修复说明

fixed 版本中，`VERIFY_ZANT_LLM_V0_3_LOCAL.ps1` 不再强制调用 pytest，而是直接使用 `scripts/run_v0_3_stdlib_tests.py`。这样在未安装 pytest 的 Windows PowerShell 环境中也能完成本地验证。
