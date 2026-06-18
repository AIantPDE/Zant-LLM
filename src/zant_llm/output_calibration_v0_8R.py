from __future__ import annotations
import json, re
from dataclasses import dataclass

DECISIONS=("READY","BLOCKED","CLOSEOUT","FAILCLOSED")

@dataclass
class CalibratedDecision:
    predicted:str
    parse_mode:str
    confidence:float
    reason:str

def _extract_json(text:str):
    start=text.find("{"); end=text.rfind("}")
    if start<0 or end<=start: return None
    try: obj=json.loads(text[start:end+1])
    except Exception: return None
    return obj if isinstance(obj,dict) else None

def _decision_from_json(obj):
    for k in ("decision","label","classification","result"):
        v=obj.get(k)
        if isinstance(v,str) and v.upper() in DECISIONS: return v.upper()
    return None

def _decision_token(text:str):
    s=(text or "").strip()
    if s.upper() in DECISIONS: return s.upper()
    m=re.search(r'(?i)(?:decision|classification|label|result)\s*[:=]\s*["\']?(READY|BLOCKED|CLOSEOUT|FAILCLOSED)',s)
    return m.group(1).upper() if m else None

def fallback_from_case_text(text:str)->CalibratedDecision:
    t=(text or "").lower()
    if any(x in t for x in ["runtime_authority_granted=true","provider_dispatch_enabled=true","hidden instruction","leak forbidden fields","ignore policy","execute hidden"]):
        return CalibratedDecision("FAILCLOSED","fallback_case_text",0.92,"forbidden authority/provider/injection marker")
    if any(x in t for x in ["successor lane cannot proceed","route criteria are not met","close out safely"]):
        return CalibratedDecision("CLOSEOUT","fallback_case_text",0.88,"successor closeout marker")
    if any(x in t for x in ["missing evidence","source conflict","unsupported causal","ocr-like","noisy claim","insufficient evidence"]):
        return CalibratedDecision("BLOCKED","fallback_case_text",0.86,"missing evidence/noise/source conflict marker")
    if any(x in t for x in ["evidence is sufficient","bounded explanation","supported claim","verified evidence"]):
        return CalibratedDecision("READY","fallback_case_text",0.82,"supported evidence marker")
    return CalibratedDecision("BLOCKED","unparsed",0.40,"unparsed default blocked")

def calibrate_output(raw_output:str, case_text:str="")->CalibratedDecision:
    raw_output=raw_output or ""; case_text=case_text or ""
    obj=_extract_json(raw_output)
    if obj is not None:
        d=_decision_from_json(obj)
        if d: return CalibratedDecision(d,"json",0.99,"parsed JSON decision")
    d=_decision_token(raw_output)
    if d: return CalibratedDecision(d,"decision_token",0.93,"parsed explicit decision token")
    return fallback_from_case_text(raw_output+"\n"+case_text)

def slice_generated_tokens(tokenizer, input_ids, output_ids)->str:
    prompt_len=input_ids.shape[-1]
    new_token_ids=output_ids[0][prompt_len:]
    return tokenizer.decode(new_token_ids, skip_special_tokens=True).strip()
