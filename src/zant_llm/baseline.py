import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

TOKEN_RE = re.compile(r"[A-Za-z0-9_\u4e00-\u9fff]+")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def flatten_input(item: dict[str, Any]) -> str:
    inp = item.get("input", {})
    parts = [str(inp.get("semantic_preview", ""))]
    for key in ["evidence_references", "reason_codes", "residual_hints", "uncertainty_hints"]:
        val = inp.get(key, [])
        if isinstance(val, list):
            parts.extend(str(x) for x in val)
        else:
            parts.append(str(val))
    return " ".join(parts)


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text)]


def vectorize(text: str) -> dict[str, float]:
    counts = Counter(tokenize(text))
    norm = math.sqrt(sum(v * v for v in counts.values())) or 1.0
    return {k: v / norm for k, v in counts.items()}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(k, 0.0) for k, v in a.items())


def train_baseline(train_path: str | Path) -> dict[str, Any]:
    rows = read_jsonl(train_path)
    examples = []
    category_counts: dict[str, int] = {}
    for row in rows:
        text = flatten_input(row)
        cat = row.get("category", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
        examples.append({"id": row.get("id"), "category": cat, "text": text, "vector": vectorize(text), "output": row.get("output", {})})
    return {"model_type": "stdlib_token_overlap_explanation_baseline", "version": "v0.1", "example_count": len(examples), "category_counts": category_counts, "examples": examples, "runtime_authority_granted": False, "provider_dispatch_enabled": False}


def predict(model: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    qv = vectorize(flatten_input(item))
    best = None
    best_score = -1.0
    for ex in model["examples"]:
        score = cosine(qv, ex["vector"])
        if score > best_score:
            best = ex
            best_score = score
    output = dict(best["output"] if best else {})
    output.setdefault("fail_closed_fallback", "未找到可靠解释模板，保持 fail-closed 并请求人工复核。")
    return {"id": item.get("id"), "predicted_category": best["category"] if best else "unknown", "nearest_train_id": best["id"] if best else None, "confidence": round(float(max(best_score, 0.0)), 4), "prediction": output, "runtime_authority_granted": False, "provider_dispatch_enabled": False}
