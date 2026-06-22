# Zant-LLM v1.3 交接说明

v1.3 是 release candidate packaging 分支，基于 `v1.2-runtime-deployment-readiness`。本分支不训练模型，目标是把运行时部署就绪产物整理成 RC 交付包。

运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_3_ALL_LOCAL.ps1
```

成功标志：`ZANT_LLM_V1_3_ALL_LOCAL_OK=True`。
