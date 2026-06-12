# AIant PDE Context

Zant-LLM is a governed external model-training lane for explanation-generation work.

It is parallel to the current `aiant-zant` host/runtime work and must not be treated as a runtime component.

Current relation:

```text
aiant-zant  -> explanation-preview consumer / safe host seam
Zant-LLM    -> independent explanation model training lane
```

The two lines are intentionally not connected in v0.1.
