from zant_llm.governance import forbidden_fields_in_output

def validate_forbidden_output(explanation: dict) -> dict:
    found = forbidden_fields_in_output(explanation)
    return {"validator":"ForbiddenOutputScannerV0", "passed": not found, "forbidden_fields": found}
