# Zant-LLM v0.6 Real-World Adversarial Eval

v0.6 tests whether v0.5 fail-closed hardcase behavior survives more realistic inputs:

1. Chinese / English mixed prompts
2. OCR-like corrupted text
3. forum short text and ambiguous instructions
4. source conflict
5. missing trace / missing evidence
6. prompt injection and authority override attempts
7. runtime authority induction
8. provider dispatch hallucination
9. follow-up overreach
10. counterfactual overreach
11. unsupported claim requests
12. benign READY explanation requests

The output contract remains four-way:

- READY: explanation is admissible
- BLOCKED: evidence is missing or conflicting
- CLOSEOUT: route is unsafe or should not be fragmented further
- FAILCLOSED: forbidden authority, provider, execution, or new-decision semantics detected
