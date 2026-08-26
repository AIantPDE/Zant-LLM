# Zant-LLM v2.5 GitHub Publish Plan

This document is a plan only. It does not push, publish, or modify GitHub.

## 1. Pre-publish checks

Confirm locally:

- `PUBLIC_RELEASE_REVIEW_READY=True`
- candidate ZIP SHA256 matches the freeze receipt
- adapter SHA256 matches the freeze receipt
- gate SHA256 matches the freeze receipt
- manifest SHA256 matches the freeze receipt
- `CHECKSUMS_VALID=True`
- no `__pycache__`, `.pyc`, temporary files, or unexpected artifacts
- `RUNTIME_AUTHORITY_GRANTED=False`
- `PROVIDER_DISPATCH_ENABLED=False`

## 2. Recommended branch

Create a dedicated release-preparation branch, for example:

`release/v2.5`

Do not modify protected `main` directly.

## 3. Recommended repository changes

Add or update:

- `README.md`
  - current version: v2.5
  - inference contract: `apply_chat_template + audit_prefix`
  - explanation-only safety boundary
- `docs/RELEASE_NOTES_v2.5.md`
- `docs/V2_5_INFERENCE_POLICY_V1_1.md`
- `docs/V2_5_RELEASE_VALIDATION.md`
- frozen candidate receipt / manifest hashes as text metadata
- optional link/reference to the release artifact

Avoid committing:
- local base-model weights
- local caches
- temporary diagnostics
- secrets
- machine-specific absolute paths
- Python bytecode/cache files

## 4. Pull request

Open a PR from `release/v2.5` to the protected default branch.

PR title suggestion:

`Release Zant-LLM v2.5`

PR description should summarize:

- chat-template inference standardization
- audit_prefix
- Gate v1.1 64/64 result
- forbidden mention vs assertive distinction
- frozen candidate SHA256
- no runtime execution/provider dispatch authority

## 5. GitHub Release

After the PR is reviewed and merged, create a GitHub Release:

Tag:
`v2.5`

Title:
`Zant-LLM v2.5`

Attach:
`Zant-LLM-v2_5-release-candidate-frozen.zip`

Include the SHA256 in the release body.

## 6. Post-publish verification

After publication:

- download the public release ZIP
- recompute SHA256
- compare against:
  `081efb89f97145a12e3e96571cc42c6a8f2b852b5efce280b25cdf5fee68d6de`
- verify release notes render correctly
- verify no unexpected binary/model files were committed to the repository
- verify public documentation still states:
  - `RUNTIME_AUTHORITY_GRANTED=False`
  - `PROVIDER_DISPATCH_ENABLED=False`

## 7. Stop conditions

Do not publish if:

- any hash differs
- Gate v1.1 evidence is missing
- the candidate ZIP changed after freeze
- safety flags changed
- unexpected files appear
- protected-branch policy would be bypassed

## Recommended next step

When the user explicitly asks to publish/push:
prepare the release branch/commit/PR workflow first, then perform GitHub changes only with explicit authorization.
