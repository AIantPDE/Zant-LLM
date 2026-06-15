# Zant-LLM Governance v0.3

Zant-LLM 是 AIant PDE 中面向解释生成能力的独立外部模型训练仓。

v0.3 允许在仓内训练 Gemma 4 E2B QLoRA explanation baseline，但不允许把训练产物直接接入 aiant-zant runtime。

## Boundary Flags

```text
zant_llm_repository_created=True
zant_llm_training_started=True
zant_llm_provider_connected=False
zant_model_call_enabled_in_aiant_zant=False
provider_dispatch_enabled=False
provider_registry_changed=False
route_decision_created=False
fetch_decision_created=False
runtime_loader_changed=False
worker_activation_started=False
side_effecting_execution_authorized=False
runtime_authority_granted=False
```

## Forbidden Output Principle

解释输出 payload 不得包含控制面或执行面字段。即使字段值为 false，也不应出现在 explanation output 中。

输入 bundle 可以在 governance metadata 中声明权限边界，但模型生成的 explanation output 不得生成：route_decision、fetch_decision、provider_dispatch、worker_trigger、writeback_execution、runtime_authority_granted 等字段。
