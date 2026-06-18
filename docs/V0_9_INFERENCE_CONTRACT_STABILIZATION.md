# V0.9 Inference Contract Stabilization

v0.9 stabilizes the inference path exposed by v0.8R:

1. Parse strict JSON if available.
2. Parse JSON fragments when the model adds surrounding text.
3. Classify from new generated text when the model repeats prompt/case text.
4. Repair forbidden or malformed outputs to FAILCLOSED.
5. Return one normalized result object.

The branch intentionally does not train. It creates a local contract and CLI/API harness that can later wrap model inference.
