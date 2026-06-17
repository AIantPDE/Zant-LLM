# Zant-LLM v0.6 Real-World Adversarial Eval

Branch:

```text
v0.6-realworld-adversarial-eval
```

v0.6 is an eval-first branch after v0.5. It does not add another training loop by default. Instead it introduces 300 real-world adversarial evaluation cases covering noisy bilingual input, OCR-like corruption, forum-style short prompts, source conflict, missing trace, prompt injection, runtime authority induction, provider dispatch induction, follow-up overreach, counterfactual overreach, and unsupported claims.

Expected local run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_6_ALL_LOCAL.ps1
```

Expected success markers:

```text
ZANT_LLM_V0_6_REPOSITORY_VALID=True
ZANT_LLM_V0_6_STDLIB_TESTS_PASSED=True
ZANT_LLM_V0_6_EVALUATED=True
REALWORLD_ADV_PASS_RATE=1.0
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
ZANT_LLM_V0_6_ALL_LOCAL_OK=True
```
