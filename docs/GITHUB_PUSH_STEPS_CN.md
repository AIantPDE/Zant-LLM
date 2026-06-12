# Zant-LLM v0.1 本地推送步骤

假设你已经解压本 ZIP 到：

```powershell
C:\aiant\Zant-LLM-v0.1
```

进入目录：

```powershell
Set-Location C:\aiant\Zant-LLM-v0.1
```

本地验证：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_1_LOCAL.ps1
```

推送到 GitHub 的 `v0.1` 分支：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_1_BRANCH_TO_GITHUB.ps1
```

默认仓库：

```text
https://github.com/AIantPDE/Zant-LLM.git
```

默认分支：

```text
v0.1
```

如果你想用 SSH：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_1_BRANCH_TO_GITHUB.ps1 `
  -Repository "git@github.com:AIantPDE/Zant-LLM.git" `
  -Branch "v0.1"
```

推送后，建议从 `v0.1` 再开训练 Lane：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\CREATE_LANE_FROM_V0_1.ps1
```
