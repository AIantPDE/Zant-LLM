# Governance Invariants

Zant-LLM v1.5R 继承 v1.5 的 post-release monitoring 目标，并新增 audit + hotfix readiness 闭环。

## Hard flags

```text
runtime_authority_granted = False
provider_dispatch_enabled = False
```

## Allowed behavior

- 读取本地 fixture / JSONL / registry。
- 生成审计报告、smoke report、hotfix readiness report。
- 标记 issue / regression / release-health drift / maintenance closeout。
- 推荐后继版本。

## Forbidden behavior

- 不得调用真实 runtime provider。
- 不得执行任何系统级 action。
- 不得把模型输出作为审批通过依据。
- 不得把 hotfix readiness 解释为生产发布授权。
