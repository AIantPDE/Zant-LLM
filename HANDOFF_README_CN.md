# Zant-LLM v0.6 交接说明

v0.6 不是继续训练分支，而是真实复杂输入评估分支。它用于验证 v0.5 后的模型/规则在混合噪声、伪权威、注入、证据冲突、缺 trace、反事实越界、追问越权等真实输入下是否仍能稳定输出 READY / BLOCKED / CLOSEOUT / FAILCLOSED。

本地运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_6_ALL_LOCAL.ps1
```
