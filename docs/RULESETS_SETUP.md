# Suggested GitHub Rulesets

## Branch rule for main and v0.1

- Require pull request before merging: ON
- Required approvals: 1
- Require status checks: ON
- Block force pushes: ON
- Restrict deletions: ON
- Require linear history: OFF

## Tag rules

Protect:

```text
zant-explanation-*-anchor-*
zant-llm-release-*
```

Enable:

- Restrict updates
- Restrict deletions
- Block force pushes
