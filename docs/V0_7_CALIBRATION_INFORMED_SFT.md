# v0.7 Calibration-Informed SFT

v0.7 consumes calibration buckets from v0.6R and creates SFT cases that teach the model to map real-world noisy inputs to bounded, evidence-gated explanations.

## Main classes

1. READY calibrated explanations
2. BLOCKED missing-evidence responses
3. CLOSEOUT route-closure responses
4. FAILCLOSED safety refusals
5. Source-conflict abstentions
6. OCR / mixed-language robustness
7. Provider-dispatch and runtime-authority refusal

## Boundary

This branch trains only explanation behavior. It does not train execution, routing, provider dispatch, writeback, worker trigger, or runtime authorization.
