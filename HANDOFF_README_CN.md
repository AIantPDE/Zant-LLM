# Zant-LLM v0.9 交接说明

v0.9 是推理契约稳定化分支，不是训练分支。它把 v0.8R 中已经验证的 output calibration 逻辑固化为本地 CLI / API 可调用入口。

核心目标：无论模型输出 JSON、半 JSON、复读 prompt、还是混入注入文本，最终都要归一化为 READY / BLOCKED / CLOSEOUT / FAILCLOSED 之一，并强制 `runtime_authority_granted=false`、`provider_dispatch_enabled=false`。
