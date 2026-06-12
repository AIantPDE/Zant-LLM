# Release Policy v0.1

A Zant-LLM release candidate must include:

- source branch;
- source commit;
- training config reference;
- data manifest reference;
- model card;
- evaluation report;
- checkpoint artifact reference;
- checkpoint SHA256;
- explicit runtime-authority status.

## Protected tag patterns

```text
zant-explanation-*-anchor-*
zant-llm-release-*
```

## Weight policy

Do not repeatedly commit heavy model files to this source repository.

Ignored by default:

```text
*.safetensors
*.gguf
*.bin
*.pt
*.pth
*.ckpt
*.onnx
```

Record model artifacts through manifest fields instead.
