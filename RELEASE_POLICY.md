# Release Policy · v1.5R

v1.5R 只允许作为 v1.5 的 post-release 审计修正版存在。

## Entry criteria

- v1.5 已本地验证通过。
- v1.5 已 push 到远端。
- v1.5 successor 指向 v1.5R。

## Exit criteria

- audit checks 全部通过。
- hotfix readiness checks 全部通过。
- regression replay 全部通过。
- smoke pass rate = 1.0。
- blocking issues = 0。
- 运行时硬开关继续保持 False。
