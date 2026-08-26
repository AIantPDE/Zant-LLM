# Zant-LLM v2.5 Release Candidate

## Summary

Zant-LLM v2.5 freezes the current governed explanation-only adapter and its validated inference/evaluation policy.

The v2.5 candidate is based on the chat-aligned text LoRA path and the Audit Policy Gate v1.1.

## Key changes

- Standardized generation through `tokenizer.apply_chat_template`.
- Added `audit_prefix` as the standard inference policy.
- Kept strict-text-only loading by removing vision/audio modules.
- Separated forbidden **mentions** from forbidden **assertive claims**.
- Expanded rationale detection beyond narrow keyword matching.
- Removed fallback dependency on the validated 64-case gate.
- Preserved the invariant that runtime authority and provider dispatch remain disabled.

## Validated gate result

Audit Policy Gate v1.1:

- Cases: 64 / 64
- Raw generation nonblank: 64 / 64
- Raw quality ready: 64 / 64
- Raw auditable rationale: 64 / 64
- Governed quality ready: 64 / 64
- Fallback dependency: 0
- Prompt echo detected: false
- Forbidden assertive leakage: false
- Mojibake detected: false
- Public release ready: true

One case contains an audited forbidden **mention** but no forbidden assertive claim; it is retained in the evidence as an audit record.

## Frozen candidate hashes

- Candidate ZIP SHA256:
  `081efb89f97145a12e3e96571cc42c6a8f2b852b5efce280b25cdf5fee68d6de`
- Adapter model SHA256:
  `c509c640a3a7653b9536078bd25fddc22f2b2cdaa2eb22a45272ad4ffe077314`
- Gate SHA256:
  `678ad4bc6a5c6e3ea9094446171c391f3780b726e90f7c70fefa2b15c0c8349b`
- Manifest SHA256:
  `befe22d399b549a38c7c41fe50f4caed88cfa78467cb8c728534e796b6ef638f`

## Scope and limitations

This release candidate passing the internal 64-case gate does not constitute a universal safety guarantee for all out-of-distribution inputs, languages, deployment environments, or downstream integrations.

The model remains explanation-only:

- `RUNTIME_AUTHORITY_GRANTED=False`
- `PROVIDER_DISPATCH_ENABLED=False`

No external execution, provider dispatch, or upstream override is granted by this release.

## Recommended artifact

`Zant-LLM-v2_5-release-candidate-frozen.zip`
