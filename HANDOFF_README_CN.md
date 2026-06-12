# Zant-LLM v0.1 初始分支文件包说明

这个 ZIP 是给 `https://github.com/AIantPDE/Zant-LLM` 的 `v0.1` 分支准备的初始文件。

它不是训练完成版，也不是 runtime 接入版。

它的作用是：

```text
先建立 v0.1 初始分支
后续所有 Zant-LLM 修改都可以在这个基础上继续
```

## 快速使用

```powershell
Set-Location 解压后的目录
powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_1_LOCAL.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_1_BRANCH_TO_GITHUB.ps1
```

默认推送目标：

```text
https://github.com/AIantPDE/Zant-LLM.git
```

默认分支：

```text
v0.1
```

## 注意

本包明确保持：

```text
provider_dispatch_enabled=False
runtime_authority_granted=False
```

所以它可以作为训练仓初始分支，但不能作为 aiant-zant runtime 接入代码。
